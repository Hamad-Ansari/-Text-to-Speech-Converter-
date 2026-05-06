import streamlit as st
from openai import OpenAI
import tempfile
import os
from pydub import AudioSegment

# -------------------------------
# 🔊 Text to Speech Function
# -------------------------------
def text_to_speech(api_key, text, model, voice):
    client = OpenAI(api_key=api_key)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmpfile:
        path = tmpfile.name

    response = client.audio.speech.create(
        model=model,
        voice=voice,
        input=text
    )

    response.stream_to_file(path)
    return path


# -------------------------------
# 🔄 Convert Audio Format
# -------------------------------
def convert_audio_format(input_path, output_format):
    audio = AudioSegment.from_file(input_path, format="mp3")

    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{output_format}") as tmpfile:
        output_path = tmpfile.name

    audio.export(output_path, format=output_format)
    return output_path


# -------------------------------
# 🎨 UI Setup
# -------------------------------
st.set_page_config(page_title="TTS Converter", layout="centered")

st.title("🔊 Text to Speech Converter 📝")
st.markdown("Convert your text into high-quality speech using OpenAI models.")

# -------------------------------
# 📌 Sidebar Controls
# -------------------------------
st.sidebar.title("⚙️ Settings")

api_key = st.sidebar.text_input("Enter OpenAI API Key", type="password")

model = st.sidebar.selectbox("Model", ["tts-1", "tts-1-hd"])

voice = st.sidebar.selectbox(
    "Voice",
    ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
)

audio_format = st.sidebar.selectbox(
    "Output Format",
    ["mp3", "wav", "aac", "flac", "opus"]
)

# -------------------------------
# 📝 User Input
# -------------------------------
text_input = st.text_area(
    "Enter text",
    "Hello Hammad! Welcome to your AI Text to Speech App 🚀"
)

# -------------------------------
# ▶️ Convert Button
# -------------------------------
if st.button("Convert to Speech"):
    if not api_key:
        st.error("⚠️ Please enter your API key")
    else:
        try:
            with st.spinner("Generating speech..."):
                mp3_path = text_to_speech(api_key, text_input, model, voice)

                # Convert if needed
                if audio_format != "mp3":
                    final_path = convert_audio_format(mp3_path, audio_format)
                    os.remove(mp3_path)
                else:
                    final_path = mp3_path

                # Play Audio
                with open(final_path, "rb") as f:
                    audio_bytes = f.read()
                    st.audio(audio_bytes, format=f"audio/{audio_format}")

                    # Download Button (Correct Way)
                    st.download_button(
                        label=f"⬇️ Download {audio_format.upper()}",
                        data=audio_bytes,
                        file_name=f"speech.{audio_format}",
                        mime=f"audio/{audio_format}"
                    )

                # Cleanup
                os.remove(final_path)

        except Exception as e:
            st.error(f"❌ Error: {e}")


# -------------------------------
# 👤 Sidebar Profile (YOUR INFO)
# -------------------------------
st.sidebar.markdown("---")
st.sidebar.markdown("### 👤 About Developer")

st.sidebar.markdown("""
**Hammad Zahid** 🚀  
AI Engineer | Data Scientist | Python Developer  

🔗 Connect with me:
- 🌐 GitHub: https://github.com/Hamad-Ansari
- 💼 LinkedIn: www.linkedin.com/in/hammad-zahid-xyz
- 🐦 Twitter/X: https://www.kaggle.com/hammadansari7
- 📊 Kaggle: https://www.kaggle.com/hammadansari7
""")

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

# Hide default Streamlit UI
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)