import streamlit as st
from groq import Groq
from st_audiorec import st_audiorec
import tempfile

# 🔑 Test API key (replace with your own)
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

st.title("🎙️ Groq Whisper Recorder")
st.write("Record your voice and get a transcription!")

# Record Audio
wav_audio = st_audiorec()

if wav_audio is not None:
    st.audio(wav_audio, format="audio/wav")
    st.info("Processing transcription...")

    # Save to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
        temp_file.write(wav_audio)
        temp_filename = temp_file.name

    try:
        with open(temp_filename, "rb") as f:
            transcription = client.audio.transcriptions.create(
                file=("audio.wav", f.read()),
                model="whisper-large-v3-turbo",
                response_format="verbose_json",
            )

        st.success("✅ Transcription Complete")
        st.text_area("Transcription", transcription.text, height=300)

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
