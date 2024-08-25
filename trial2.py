import streamlit as st
from langchain_groq import ChatGroq
from gtts import gTTS
import base64
from io import BytesIO
import os
import docx
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
os.environ['GROQ_API_KEY'] = os.getenv("GROQ_API_KEY")

# Custom CSS for the top menu
st.markdown("""
    <style>
    .menu {
        display: flex;
        justify-content: center;
        margin-top: 20px;
    }
    .menu-item {
        margin: 0 20px;
        padding: 10px 20px;
        border-bottom: 2px solid transparent;
        cursor: pointer;
    }
    .menu-item.active {
        color: #FF4B4B;
        border-bottom: 2px solid #FF4B4B;
    }
    </style>
""", unsafe_allow_html=True)

# Menu creation using HTML
menu_items = ["Real-Time Language Translation", "File Upload and Translation"]
selected_menu = st.sidebar.radio("Menu", menu_items)

# Language codes dictionary
language_codes = {
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Chinese": "zh",
    "Japanese": "ja",
    "Korean": "ko",
    "Italian": "it",
    "Portuguese": "pt",
    "Russian": "ru",
    "Arabic": "ar",
    "Hindi": "hi",
    "Dutch": "nl",
    "Greek": "el",
    "Swedish": "sv",
    "Turkish": "tr",
    "Vietnamese": "vi"
}

languages = list(language_codes.keys())

# Shared UI components for language selection
source_language = st.selectbox("Select Source Language", languages)
target_language = st.selectbox("Select Target Language", languages)

if selected_menu == "Real-Time Language Translation":
    st.title("Real-Time Language Translation with Voice Assistant")

    inputText = st.text_input("Enter text to translate")

    if inputText:
        groqApi = ChatGroq(model="gemma-7b-It", temperature=0)

        # Constructing the message dictionary
        message = {
            "role": "user",
            "content": f"Translate the following text from {source_language} to {target_language}: {inputText}"
        }

        # Passing the message dictionary as a list
        translation = groqApi([message]).result()

        st.write(f"Translation ({source_language} to {target_language}):")
        st.markdown(f"**{translation}**")

        # Generate TTS
        tts = gTTS(text=translation, lang=language_codes[target_language], slow=False)
        audio_buffer = BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)

        audio_bytes = audio_buffer.read()
        audio_b64 = base64.b64encode(audio_bytes).decode()

        # Audio element in Streamlit
        audio_html = f'<audio controls><source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3"></audio>'
        st.markdown(audio_html, unsafe_allow_html=True)

elif selected_menu == "File Upload and Translation":
    st.title("File Upload and Translation")

    uploaded_file = st.file_uploader("Upload a text or Word file", type=["txt", "docx"])

    if uploaded_file:
        # Reading the file content
        if uploaded_file.name.endswith(".txt"):
            content = uploaded_file.read().decode("utf-8")
        elif uploaded_file.name.endswith(".docx"):
            doc = docx.Document(uploaded_file)
            content = "\n".join([para.text for para in doc.paragraphs])
        
        st.write("File content:")
        st.text(content)

        # Translate file content
        if content:
            groqApi = ChatGroq(model="gemma-7b-It", temperature=0)

            # Constructing the message dictionary
            message = {
                "role": "user",
                "content": f"Translate the following text from {source_language} to {target_language}: {content}"
            }

            # Passing the message dictionary as a list
            translation = groqApi([message]).result()

            st.write(f"Translated content ({source_language} to {target_language}):")
            st.markdown(f"**{translation}**")

            # Generate TTS
            tts = gTTS(text=translation, lang=language_codes[target_language], slow=False)
            audio_buffer = BytesIO()
            tts.write_to_fp(audio_buffer)
            audio_buffer.seek(0)

            audio_bytes = audio_buffer.read()
            audio_b64 = base64.b64encode(audio_bytes).decode()

            # Audio element in Streamlit
            audio_html = f'<audio controls><source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3"></audio>'
            st.markdown(audio_html, unsafe_allow_html=True)
