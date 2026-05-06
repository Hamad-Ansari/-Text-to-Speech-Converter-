import streamlit as st
from openai import OpenAI
import tempfile
import os
from PyPDF2 import PdfReader
from langdetect import detect

# -------------------------------
# 🔊 TTS FUNCTION (NO PYDUB)
# -------------------------------
def text_to_speech(api_key, text, model, voice, fmt):
    client = OpenAI(api_key=api_key)

    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{fmt}") as tmpfile:
        path = tmpfile.name

    response = client.audio.speech.create(
        model=model,
        voice=voice,
        input=text,
        format=fmt  # ✅ direct format support
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
        content = page.extract_text()
        if content:
            text += content + "\n"
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
# 🎨 PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="AI TTS Studio", layout="centered")

# -------------------------------
# 🌈 CUSTOM STYLING
# -------------------------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #1e3c72, #2a5298);
    color: white;
}
textarea, input {
    border-radius: 10px !important;
}
.stButton>button {
    background: linear-gradient(90deg, #ff6a00, #ee0979);
    color: white;
    border-radius: 12px;
    padding: 10px 20px;
    font-size: 16px;
    border: none;
}
.stButton>button:hover {
    transform: scale(1.05);
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# 🧠 TITLE
# -------------------------------
st.title("🧠 AI Text-to-Speech Studio")
st.markdown("### 🚀 PDF → Speech | Multi-language | Smart Voice")

# -------------------------------
# ⚙️ SIDEBAR
# -------------------------------
st.sidebar.header("⚙️ Settings")

api_key = st.sidebar.text_input("🔑 OpenAI API Key", type="password")

model = st.sidebar.selectbox("Model", ["tts-1", "tts-1-hd"])

voice = st.sidebar.selectbox(
    "Voice",
    ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
)

audio_format = st.sidebar.selectbox("Format", ["mp3", "wav"])

# -------------------------------
# INPUT TYPE
# -------------------------------
input_type = st.radio("Choose Input Type:", ["Text", "Upload PDF"])

text_input = ""

if input_type == "Text":
    text_input = st.text_area(
        "✍️ Enter your text",
        "Hello Hammad! Your AI SaaS is now powerful 🚀"
    )
else:
    uploaded_file = st.file_uploader("📄 Upload PDF", type=["pdf"])

    if uploaded_file:
        text_input = extract_text_from_pdf(uploaded_file)
        st.success("✅ PDF text extracted!")

        with st.expander("🔍 Preview Text"):
            st.write(text_input[:1000])

# -------------------------------
# ▶️ GENERATE
# -------------------------------
if st.button("🎧 Generate Speech"):
    if not api_key:
        st.error("⚠️ API key required")
    elif not text_input.strip():
        st.error("⚠️ No text found")
    else:
        try:
            with st.spinner("🧠 Processing..."):

                # Language detection
                lang = detect_language(text_input)
                st.info(f"🌍 Detected Language: {lang}")

                # Generate speech
                path = text_to_speech(api_key, text_input, model, voice, audio_format)

                # Play audio
                with open(path, "rb") as f:
                    audio_bytes = f.read()

                    st.audio(audio_bytes, format=f"audio/{audio_format}")

                    st.download_button(
                        label="⬇️ Download Audio",
                        data=audio_bytes,
                        file_name=f"speech.{audio_format}",
                        mime=f"audio/{audio_format}"
                    )

                os.remove(path)

        except Exception as e:
            st.error(f"❌ Error: {e}")

# -------------------------------
# 👤 PROFILE
# -------------------------------
st.sidebar.markdown("---")
st.sidebar.markdown("""
### 👤 Hammad Zahid 🚀  
AI Engineer | Data Scientist  

🔗 GitHub: https://github.com/Hamad-Ansari  
🔗 LinkedIn: https://www.linkedin.com/in/hammad-zahid-xyz  
🔗 Kaggle: https://www.kaggle.com/hammadansari7  
""")
