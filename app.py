import bcrypt
from flask import Flask, render_template, request, send_from_directory, redirect, url_for, session
from gtts import gTTS
import pdfplumber
import os
import time
import mysql.connector

app = Flask(__name__)

AUDIO_DIR = 'audio_files'
os.makedirs(AUDIO_DIR, exist_ok=True)

app.secret_key = '<your_secret_key>'

DB_CONFIG = {
    'host': '',
    'user': '',
    'password': '',
    'database': 'name of database'
}

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

@app.route('/')
def home():
    return render_template('home.html', audio_files=[], pdf_audio_file=None)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute('SELECT * FROM users1 WHERE email = %s', (email,))
            user = cursor.fetchone()

            if user:
                stored_hashed_password = user['password']
                if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password.encode('utf-8')):
                    return redirect(url_for('index'))
                    session['user_id'] = user['id']
                else:
                    return render_template('login.html', error='Invalid password')
            else:
                return render_template('login.html', error='Email not found')

        except mysql.connector.Error as err:
            return render_template('login.html', error="Database error: " + str(err))

        finally:
            cursor.close()
            conn.close()

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        hashed_password = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users1 (name, email, password) VALUES (%s, %s, %s)', (name, email, hashed_password))
        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/index')
def index():
    return render_template('index.html', audio_files=[], pdf_audio_file=None)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/pdf-to-audio')
def pdf_to_audio():
    return render_template('pdf_to_audio.html')

'''def get_voice_engine(voice_type='female'):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    if voice_type == 'male':
        engine.setProperty('voice', voices[0].id)  # Usually, the first voice is male
    else:
        engine.setProperty('voice', voices[1].id)  # Usually, the second voice is female
    return engine'''


import pyttsx3
@app.route("/generate_text", methods=["POST"])
def generate_audio():
    text = request.form["text"]
    voice_volume = float(request.form["voice_volume"])
    voice_speed = float(request.form["voice_speed"])
    voice_type = request.form["voice_type"]

    engine = pyttsx3.init()

    voices = engine.getProperty("voices")
    if voice_type == "male":
        engine.setProperty("voice", voices[0].id)
    else:
        engine.setProperty("voice", voices[1].id)

    engine.setProperty("rate", 200 + voice_speed)
    engine.setProperty("volume", max(0.0, min(1.0, (voice_volume + 20) / 40)))

    filename = f"text_audio_{int(time.time())}.mp3"
    filepath = os.path.join(AUDIO_DIR, filename)

    engine.save_to_file(text, filepath)
    engine.runAndWait()

    engine.stop()

    return render_template("index.html", audio_files=[filename])

@app.route('/generate_pdf', methods=['POST'])
def generate_audio_from_pdf():
    pdf_file = request.files['pdf_file']
    page_range = request.form['page_range']
    if pdf_file and pdf_file.filename.endswith('.pdf'):
        text = ''

        try:
            start_page, end_page = map(int, page_range.split('-'))
            if start_page < 1 or end_page < start_page:
                raise ValueError("Invalid page range")

            with pdfplumber.open(pdf_file) as pdf:
                num_pages = len(pdf.pages)
                if end_page > num_pages:
                    raise ValueError("End page exceeds total number of pages")

                for page_num in range(start_page - 1, end_page):
                    text += pdf.pages[page_num].extract_text() + '\n'

        except Exception as e:
            return render_template('index.html', error=str(e)), 400

        if text:
            audio_files = os.listdir(AUDIO_DIR)
            for file in audio_files:
                os.remove(os.path.join(AUDIO_DIR, file))

            timestamp = int(time.time())
            audio_file_name = f'pdf_audio_{timestamp}.mp3'
            audio_file_path = os.path.join(AUDIO_DIR, audio_file_name)

            tts = gTTS(text=text, lang='en')
            tts.save(audio_file_path)

            return render_template('index.html', audio_files=os.listdir(AUDIO_DIR), pdf_audio_file=audio_file_name)

    return render_template('index.html', error="No valid PDF file provided"), 400

@app.route('/audio/<filename>')
def audio(filename):
    return send_from_directory(AUDIO_DIR, filename)

if __name__ == '__main__':
    app.run(debug=True)
