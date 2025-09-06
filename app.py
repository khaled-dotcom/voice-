import os
import streamlit as st
from groq import Groq
from audio_recorder_streamlit import audio_recorder

# Load API Key
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "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")
client = Groq(api_key=GROQ_API_KEY)

st.title("🎙️ Groq Whisper Live Recorder")
st.write("Click the mic to record your voice, then get transcription using `whisper-large-v3-turbo`.")

# Record audio
audio_bytes = audio_recorder(
    text="Click to record",
    recording_color="#e63946",
    neutral_color="#f1faee",
    icon_name="microphone",
    icon_size="3x",
)

if audio_bytes:
    # Save recorded file
    with open("temp_audio.wav", "wb") as f:
        f.write(audio_bytes)

    st.audio("temp_audio.wav")
    st.info("Processing transcription...")

    # Send to Groq API
    with open("temp_audio.wav", "rb") as file:
        transcription = client.audio.transcriptions.create(
            file=("temp_audio.wav", file.read()),
            model="whisper-large-v3-turbo",
            response_format="verbose_json",
        )

    st.success("✅ Transcription Complete")
    st.text_area("Transcription", transcription.text, height=300)
