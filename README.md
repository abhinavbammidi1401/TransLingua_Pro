# TransLingua_Pro

A Streamlit application designed for real-time language translation. The app supports multiple input methods including text input, file uploads, and voice input. Users can translate text between various languages and listen to the translated text through audio feedback. The interface is interactive and features a customizable background.

## Features

- **Real-Time Language Translation**: Enter text and get instant translations between selected languages.
- **File Upload and Translation**: Upload text or Word files for translation.
- **Voice Input Translation**: Record your voice, transcribe it, and translate it to the selected language.
- **Audio Feedback**: Option to listen to the translated text in audio format.
- **Customizable Background**: Set a background image for the app interface.

![Alt text](trans.png)

## Installation

1. Clone this repository:
    ```bash
    git clone https://github.com/yourusername/your-repo-name.git
    ```

2. Navigate to the project directory:
    ```bash
    cd your-repo-name
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Set up your environment variables by creating a `.env` file in the project root with the following content:
    ```
    GROQ_API_KEY=your_groq_api_key
    ```

2. Run the Streamlit app:
    ```bash
    streamlit run app.py
    ```

3. Open the app in your web browser at `http://localhost:8501`.

## Dependencies

- `streamlit`
- `langchain_openai`
- `langchain_core`
- `langchain_groq`
- `gtts`
- `speech_recognition`
- `docx`
- `python-dotenv`

## Contributing

Feel free to open issues or submit pull requests if you have suggestions or improvements.
