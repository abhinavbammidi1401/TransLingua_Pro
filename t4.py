import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from gtts import gTTS
import base64
from io import BytesIO
import os
from dotenv import load_dotenv
import docx

load_dotenv()

# Environment Variables
os.environ['GROQ_API_KEY'] = os.getenv("GROQ_API_KEY")

# Defining Translation Prompt Template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a language translator. Translate the following text from {source_language} to {target_language}."),
        ("user", "Text: {text}")
    ]
)

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

# Sidebar content
st.sidebar.image("logo1.png", use_column_width=True)  # Add your image here
menu_options = ["Real-Time Language Translation", "File Upload and Translation"]
menu_selection = st.sidebar.radio("Select an option", menu_options)

# Shared language selection components
languages = list(language_codes.keys())
source_language = st.sidebar.selectbox("Select Source Language", languages)
target_language = st.sidebar.selectbox("Select Target Language", languages)

# Option 1: Real-Time Language Translation
if menu_selection == "Real-Time Language Translation":
    st.title("Real-Time Language Translation with Voice Assistant")

    inputText = st.text_input("Enter text to translate")

    if inputText:
        groqApi = ChatGroq(model="gemma-7b-It", temperature=0)
        outputparser = StrOutputParser()
        chainSec = prompt | groqApi | outputparser

        translation = chainSec.invoke({
            'source_language': source_language,
            'target_language': target_language,
            'text': inputText
        })

        # Display the translation result
        st.write(f"Translation ({source_language} to {target_language}):")
        st.markdown(f"**{translation}**")
        
        # Option to generate audio
        if st.checkbox("Generate Audio"):
            tts = gTTS(text=translation, lang=language_codes[target_language], slow=False)
            audio_buffer = BytesIO()
            tts.write_to_fp(audio_buffer)
            audio_buffer.seek(0)
            
            audio_bytes = audio_buffer.read()
            audio_b64 = base64.b64encode(audio_bytes).decode()

            # Create an audio element in Streamlit
            audio_html = f'<audio controls><source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3"></audio>'
            st.markdown(audio_html, unsafe_allow_html=True)

# Option 2: File Upload and Translation
elif menu_selection == "File Upload and Translation":
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
            outputparser = StrOutputParser()
            chainSec = prompt | groqApi | outputparser

            translation = chainSec.invoke({
                'source_language': source_language,
                'target_language': target_language,
                'text': content
            })

            # Display the translation result
            st.write(f"Translated content ({source_language} to {target_language}):")
            st.markdown(f"**{translation}**")

            # Option to generate audio
            if st.checkbox("Generate Audio"):
                tts = gTTS(text=translation, lang=language_codes[target_language], slow=False)
                audio_buffer = BytesIO()
                tts.write_to_fp(audio_buffer)
                audio_buffer.seek(0)

                audio_bytes = audio_buffer.read()
                audio_b64 = base64.b64encode(audio_bytes).decode()

                # Create an audio element in Streamlit
                audio_html = f'<audio controls><source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3"></audio>'
                st.markdown(audio_html, unsafe_allow_html=True)
