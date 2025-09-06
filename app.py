import streamlit as st
from groq import Groq
from audio_recorder_streamlit import audio_recorder
import tempfile

# 🔑 Test API Key
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

st.title("🎙️ Groq Whisper Transcriber")
st.write("Record or upload audio to get a transcription.")

audio_bytes = audio_recorder(
    text="Click to record",
    recording_color="#e63946",
    neutral_color="#f1faee",
    icon_name="microphone",
    icon_size="3x",
)

uploaded_file = st.file_uploader("Or upload a .wav/.mp3/.m4a file", type=["wav", "mp3", "m4a"])

# Choose final audio
final_audio = None
if uploaded_file is not None:
    final_audio = uploaded_file.read()
elif audio_bytes:
    final_audio = audio_bytes

if final_audio:
    if len(final_audio) < 500:  # Roughly ~0.01 seconds
        st.error("⚠️ Audio too short! Please record at least 1 second.")
    else:
        st.audio(final_audio, format="audio/wav")
        st.info("Processing transcription...")

        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
            temp_file.write(final_audio)
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
