import streamlit as st
from openai import OpenAI
import tempfile
import os
from pydub import AudioSegment
from PyPDF2 import PdfReader
from langdetect import detect

# -------------------------------
# 🔊 TTS FUNCTION
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
# 📄 PDF → TEXT
# -------------------------------
def extract_text_from_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = ""

    for page in reader.pages:
        text += page.extract_text() + "\n"

    return text


# -------------------------------
# 🌍 LANGUAGE DETECTION
# -------------------------------
def detect_language(text):
    try:
        return detect(text)
    except:
        return "unknown"


# -------------------------------
# 🔄 AUDIO CONVERSION
# -------------------------------
def convert_audio(input_path, format):
    audio = AudioSegment.from_file(input_path)

    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{format}") as tmpfile:
        output_path = tmpfile.name

    audio.export(output_path, format=format)
    return output_path


# -------------------------------
# 🎨 UI
# -------------------------------
st.set_page_config(page_title="Advanced TTS AI", layout="centered")

st.title("🧠 Advanced AI Text-to-Speech System")
st.markdown("PDF → Speech | Multi-language | AI Voice")

# Sidebar
st.sidebar.title("⚙️ Settings")

api_key = st.sidebar.text_input("OpenAI API Key", type="password")

model = st.sidebar.selectbox("Model", ["tts-1", "tts-1-hd"])

voice = st.sidebar.selectbox(
    "Voice Style",
    ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
)

output_format = st.sidebar.selectbox(
    "Output Format",
    ["mp3", "wav", "aac", "flac"]
)

# -------------------------------
# INPUT TYPE
# -------------------------------
input_type = st.radio("Choose Input Type:", ["Text", "Upload PDF"])

text_input = ""

if input_type == "Text":
    text_input = st.text_area(
        "Enter text",
        "Hello Hammad! This is your AI system 🚀"
    )

else:
    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

    if uploaded_file:
        text_input = extract_text_from_pdf(uploaded_file)
        st.success("✅ PDF text extracted!")

        with st.expander("Preview Extracted Text"):
            st.write(text_input[:1000])


# -------------------------------
# ▶️ GENERATE
# -------------------------------
if st.button("Generate Speech"):
    if not api_key:
        st.error("API key required")
    elif not text_input.strip():
        st.error("No text available")
    else:
        try:
            with st.spinner("Processing..."):

                # 🌍 Detect language
                lang = detect_language(text_input)
                st.info(f"Detected Language: {lang}")

                # 🔊 Generate speech
                mp3_path = text_to_speech(api_key, text_input, model, voice)

                # Convert format
                if output_format != "mp3":
                    final_path = convert_audio(mp3_path, output_format)
                    os.remove(mp3_path)
                else:
                    final_path = mp3_path

                # Play
                with open(final_path, "rb") as f:
                    audio_bytes = f.read()

                    st.audio(audio_bytes)

                    st.download_button(
                        "⬇️ Download",
                        data=audio_bytes,
                        file_name=f"speech.{output_format}"
                    )

                os.remove(final_path)

        except Exception as e:
            st.error(f"Error: {e}")


# -------------------------------
# 👤 YOUR PROFILE
# -------------------------------
st.sidebar.markdown("---")
st.sidebar.markdown("""
### 👤 Hammad Zahid

AI Engineer | Data Scientist  

🔗 GitHub: https://github.com/Hamad-Ansari 
🔗 LinkedIn: www.linkedin.com/in/hammad-zahid-xyz 
🔗 Kaggle: https://www.kaggle.com/hammadansari7  
""")