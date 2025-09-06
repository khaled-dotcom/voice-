
#GROQ_API_KEY = "gsk_your_real_key_here"
GROQ_API_KEY = "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"
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

import streamlit as st
from groq import Groq
from audio_recorder_streamlit import audio_recorder

# 🔐 Load API Key securely
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
client = Groq(api_key=GROQ_API_KEY)

st.title("🎙️ Groq Whisper Live Recorder")
st.write("Click the mic to record and get transcription.")

audio_bytes = audio_recorder(
    text="Click to record",
    recording_color="#e63946",
    neutral_color="#f1faee",
    icon_name="microphone",
    icon_size="3x",
)

if audio_bytes:
    st.audio(audio_bytes, format="audio/wav")
    st.info("Processing transcription...")

    try:
        transcription = client.audio.transcriptions.create(
            file=("audio.wav", audio_bytes),
            model="whisper-large-v3-turbo",
            response_format="verbose_json",
        )
        st.success("✅ Transcription Complete")
        st.text_area("Transcription", transcription.text, height=300)

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
