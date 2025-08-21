document.addEventListener("DOMContentLoaded", function () {
    // Function to update slider values dynamically
    function updateSliderValue(sliderId, displayId, unit) {
        const slider = document.getElementById(sliderId);
        const display = document.getElementById(displayId);

        slider.addEventListener("input", function () {
            display.innerText = slider.value + unit;
        });
    }

    // Apply the function to sliders
    updateSliderValue("voice_volume", "volume_value", "dB");
    updateSliderValue("voice_speed", "speed_value", "%");
    updateSliderValue("voice_pitch", "pitch_value", "%");

    // Ensure form submits slider values correctly
    document.getElementById("audioForm").addEventListener("submit", function (event) {
        console.log("Submitting form with values:");
        console.log("Volume:", document.getElementById("voice_volume").value);
        console.log("Speed:", document.getElementById("voice_speed").value);
        console.log("Pitch:", document.getElementById("voice_pitch").value);
    });
});
