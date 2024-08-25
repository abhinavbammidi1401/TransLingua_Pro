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
import speech_recognition as sr
import docx

load_dotenv()

# Function to set a background image
@st.cache_data
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_png_as_page_bg(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = '''
    <style>
    body {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    
    st.markdown(page_bg_img, unsafe_allow_html=True)

# Set the background image
set_png_as_page_bg('img.jpg')

# Environment Variables
os.environ['GROQ_API_KEY'] = os.getenv("GROQ_API_KEY")

# Sidebar for navigation
st.sidebar.image("logo1.png", use_column_width=True)
st.sidebar.title("Navigation")
menu_options = ["Real-Time Language Translation", "File Upload and Translation", "Voice Input Translation"]
menu_selection = st.sidebar.radio("Pick and Choose", menu_options)

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

# Shared language selection components on the main screen
st.title("Choose your Languages")
languages = list(language_codes.keys())
source_language = st.selectbox("Select Source Language", languages)
target_language = st.selectbox("Select Target Language", languages)

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

        st.write(f"Translation ({source_language} to {target_language}):")
        st.markdown(f"**{translation}**")

        # Ask if the user wants to hear the audio
        if st.button("Do you want to hear the audio?"):
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
        if uploaded_file.name.endswith(".txt"):
            content = uploaded_file.read().decode("utf-8")
        elif uploaded_file.name.endswith(".docx"):
            doc = docx.Document(uploaded_file)
            content = "\n".join([para.text for para in doc.paragraphs])

        st.write("File content:")
        st.text(content)

        if content:
            groqApi = ChatGroq(model="gemma-7b-It", temperature=0)
            outputparser = StrOutputParser()
            chainSec = prompt | groqApi | outputparser

            translation = chainSec.invoke({
                'source_language': source_language,
                'target_language': target_language,
                'text': content
            })

            st.write(f"Translated content ({source_language} to {target_language}):")
            st.markdown(f"**{translation}**")

            if st.button("Do you want to hear the audio?"):
                tts = gTTS(text=translation, lang=language_codes[target_language], slow=False)
                audio_buffer = BytesIO()
                tts.write_to_fp(audio_buffer)
                audio_buffer.seek(0)

                audio_bytes = audio_buffer.read()
                audio_b64 = base64.b64encode(audio_bytes).decode()

                audio_html = f'<audio controls><source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3"></audio>'
                st.markdown(audio_html, unsafe_allow_html=True)

# Option 3: Voice Input Translation
elif menu_selection == "Voice Input Translation":
    st.title("Voice Input Translation")

    recognizer = sr.Recognizer()

    if 'recording' not in st.session_state:
        st.session_state['recording'] = False

    if not st.session_state['recording']:
        start_recording = st.button("Start Recording")
        if start_recording:
            st.session_state['recording'] = True
            with sr.Microphone() as source:
                st.write("Recording... Please start speaking.")
                audio = recognizer.listen(source)
            st.session_state['audio'] = audio
            st.session_state['recording'] = False
    else:
        stop_recording = st.button("Stop Recording")
        if stop_recording:
            st.session_state['recording'] = False

    if 'audio' in st.session_state:
        try:
            inputText = recognizer.recognize_google(st.session_state['audio'])
            st.write("You said:", inputText)

            groqApi = ChatGroq(model="gemma-7b-It", temperature=0)
            outputparser = StrOutputParser()
            chainSec = prompt | groqApi | outputparser

            translation = chainSec.invoke({
                'source_language': source_language,
                'target_language': target_language,
                'text': inputText
            })

            st.write(f"Translation ({source_language} to {target_language}):")
            st.markdown(f"**{translation}**")

            if st.button("Do you want to hear the audio?"):
                tts = gTTS(text=translation, lang=language_codes[target_language], slow=False)
                audio_buffer = BytesIO()
                tts.write_to_fp(audio_buffer)
                audio_buffer.seek(0)

                audio_bytes = audio_buffer.read()
                audio_b64 = base64.b64encode(audio_bytes).decode()

                audio_html = f'<audio controls><source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3"></audio>'
                st.markdown(audio_html, unsafe_allow_html=True)

        except sr.UnknownValueError:
            st.write("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            st.write(f"Could not request results; {e}")