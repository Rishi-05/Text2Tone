# Text2Tone

Convert text (including PDFs) into speech using a simple Flask web app.

##  Overview

Text2Tone is a lightweight and user-friendly Flask application that transforms written text into spoken audio. Using `pdfplumber` for PDF text extraction and `gTTS` (Google Text-to-Speech) for speech synthesis, it allows users to upload or input text and immediately hear it spoken back—and download it if needed.

##  Features

- Extracts text from PDF files using `pdfplumber`
- Converts text into speech using offline TTS (via `pyttsx`)
- Built with Flask for web accessibility
- Supports both text input and PDF uploads
- Ideal for creating audio versions of documents

##  Installation

1. **Clone the repository**  
   ```bash
   git clone https://github.com/Rishi-05/Text2Tone.git
   cd Text2Tone
   ```

2. **Create a Python virtual environment (recommended)**  
   ```bash
   python -m venv venv
   source venv/bin/activate     # macOS/Linux
   venv\Scripts\activate        # Windows
   ```

3. **Install the required dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

   Required packages include:
   - `Flask`
   - `pdfplumber`
   - `pyttsx` (or `pyttsx3`)

