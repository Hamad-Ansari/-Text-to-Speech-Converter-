import streamlit as st
from openai import OpenAI
import tempfile
import os

# -------------------------------
# 🔊 Text to Speech Function
# -------------------------------
def text_to_speech(api_key, text, model, voice, audio_format):
    client = OpenAI(api_key=api_key)

    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{audio_format}") as tmpfile:
        path = tmpfile.name

    response = client.audio.speech.create(
        model=model,
        voice=voice,
        input=text,
        format=audio_format   # ✅ direct format support
    )

    response.stream_to_file(path)
    return path


# -------------------------------
# 🎨 UI Setup
# -------------------------------
st.set_page_config(page_title="TTS Converter", layout="centered")

st.title("🔊 Text to Speech Converter 📝")
st.markdown("Convert your text into high-quality speech using OpenAI models.")
# -------------------------------
# 🎨 Background Styling
# -------------------------------
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://images.pexels.com/photos/5475756/pexels-photo-5475756.jpeg");
        background-size: cover;
    }
    </style>
    """,
    unsafe_allow_html=True
)
# Sidebar
st.sidebar.title("⚙️ Settings")

api_key = st.sidebar.text_input("Enter OpenAI API Key", type="password")

model = st.sidebar.selectbox("Model", ["tts-1", "tts-1-hd"])

voice = st.sidebar.selectbox(
    "Voice",
    ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
)

audio_format = st.sidebar.selectbox(
    "Output Format",
    ["mp3", "wav"]   # ⚠️ keep only stable formats
)

# Text input
text_input = st.text_area(
    "Enter text",
    "Hello Hammad! Welcome to your AI Text to Speech App 🚀"
)

# Convert
if st.button("Convert to Speech"):
    if not api_key:
        st.error("⚠️ Please enter your API key")
    else:
        try:
            with st.spinner("Generating speech..."):
                path = text_to_speech(api_key, text_input, model, voice, audio_format)

                with open(path, "rb") as f:
                    audio_bytes = f.read()

                    st.audio(audio_bytes, format=f"audio/{audio_format}")

                    st.download_button(
                        label=f"⬇️ Download {audio_format.upper()}",
                        data=audio_bytes,
                        file_name=f"speech.{audio_format}",
                        mime=f"audio/{audio_format}"
                    )

                os.remove(path)

        except Exception as e:
            st.error(f"❌ Error: {e}")


# Sidebar Profile
st.sidebar.markdown("---")
st.sidebar.markdown("""
### 👤 Hammad Zahid 🚀  
AI Engineer | Data Scientist  

🔗 GitHub: https://github.com/Hamad-Ansari  
🔗 LinkedIn: https://www.linkedin.com/in/hammad-zahid-xyz  
🔗 Kaggle: https://www.kaggle.com/hammadansari7  
""")
