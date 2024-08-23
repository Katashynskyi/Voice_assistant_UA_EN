"""Python script for a voice assistant using Streamlit and Ollama

This script creates a user interface using Streamlit to interact with a large language model\
    (LLM) from Ollama for voice-based and text-based communication.

Features:
  - Audio recording using Streamlit's `audio_recorder` component.
  - Speech recognition for Ukrainian (UA) and English (EN) using custom functions.
  - Automatic language detection based on transcribed text.
  - Text input for user prompts.
  - Streamlit chat interface for displaying conversation history.
  - Interaction with Ollama's LLM for generating responses.
  - Text-to-speech functionality (not implemented in this code).
"""

import warnings
import asyncio
import ollama
import streamlit as st
from audio_recorder_streamlit import audio_recorder
from src.ukrainian_stt import ua_transcribe
from src.english_stt import en_transcribe
from src.transcribe_speak import transcribe_and_speak
from src.utils import convert_audio_to_wav, check_language
from src.identify_lang import identify_language
from config import SYS_MSG

# Suppress warnings
warnings.filterwarnings("ignore")

# File paths
RECORDED_WAV_FILE = "./data/wav/microphone_stereo.wav"
CONV_WAV_FILE = "./data/wav/converted_mono.wav"
WAV_FILE = "./data/wav/chunk.wav"

# Initial conversation history
HISTORY = [{"role": "system", "content": SYS_MSG}]

# Streamlit page configuration
st.set_page_config(
    page_title="Voice assistant UA-EN",
    page_icon=":trident:",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items=None,
)


def ollama_prompt(model="llama3.1", messages=None):
    """
    Sends a prompt to the Ollama LLM and returns a stream of responses.

    Args:
        model (str, optional): The Ollama model to use. Defaults to "llama3.1".
        messages (list, optional): A list of dictionaries representing the conversation history.
                                  Defaults to None.

    Returns:
        stream: An asynchronous stream of dictionaries containing the LLM's responses.
    """
    stream = ollama.chat(model=model, messages=messages, stream=True)
    return stream


def stream_parser(stream):
    """
    Parses the stream of responses from the LLM and displays them in the Streamlit chat interface.

    Args:
        stream: An asynchronous stream of dictionaries containing the LLM's responses.

    Yields:
        str: Each chunk of the LLM's response.
    """
    sentence_chunks, response_text = "", ""
    st.session_state.messages.append({"role": "assistant", "content": response_text})
    print("Assistant: ", end="")
    for chunk in stream:
        print(chunk["message"]["content"], end="", flush=True)
        content = chunk["message"]["content"]
        sentence_chunks += content
        response_text += content
        st.session_state.messages[-1]["content"] += content
        if sentence_chunks.endswith(
            ('."', "\n\n", "**:", ".", "!", "?", '?"', '!"', ":")
        ):
            if any("\u0400" <= char <= "\u04FF" for char in sentence_chunks):
                lang = "ua"
            else:
                lang = "en"
            asyncio.run(transcribe_and_speak(text=sentence_chunks, lang=lang))
            sentence_chunks = ""
        yield chunk["message"]["content"]


def stop_running():
    """The Dummy.Currently does nothing."""
    with my_slot1.chat_message("user"):
        st.markdown("Stop!")

# Setup order of elements
my_slot0 = st.empty()  # most buttons
my_slot1 = st.empty()  # chat_message("user")
my_slot2 = st.empty()  # chat_message(message["role"] & chat_message("assistant")


# Streamlit custom microphone
col1, col2 = my_slot0.columns([1, 8.5], vertical_alignment="bottom")
with col1:
    audio_bytes = audio_recorder(
        text="", energy_threshold=0.01, icon_size="5x"
    )  # if energy_threshold negative - never stops
if audio_bytes is not None and len(audio_bytes) != 44:
    st.audio(audio_bytes, format="audio/wav")
    with open(file=RECORDED_WAV_FILE, mode="wb") as f:
        f.write(audio_bytes)
        f.close()
    convert_audio_to_wav(audio_file=RECORDED_WAV_FILE, output_file=CONV_WAV_FILE)
# Choose language buttons
with col2:
    PRMPT = None
    button0, button1, button2, button3 = st.columns(4)
    with button0:
        if st.button("Stop", use_container_width=True, type="primary"):
            stop_running()
    with button1:
        if st.button("Говорю (UA)", use_container_width=True):
            PRMPT = "ua:" + ua_transcribe(CONV_WAV_FILE)
            print(PRMPT)
    with button2:
        if st.button("Talking (EN)", use_container_width=True):
            PRMPT = "en:" + en_transcribe(CONV_WAV_FILE)
            print(PRMPT)
    with button3:
        if st.button("Automatic", use_container_width=True):
            DEF_LANG = "???"
            DEF_LANG = identify_language(CONV_WAV_FILE)
            if DEF_LANG in [
                ["uk: Ukrainian"],
                ["pl: Polish"],
                ["ru: Russian"],
                ["be: Belarusian"],
            ]:
                PRMPT = "ua:" + ua_transcribe(CONV_WAV_FILE)
                print(PRMPT)
            else:
                PRMPT = "en:" + en_transcribe(CONV_WAV_FILE)
                if PRMPT == "Didn't recognize that.":
                    print(PRMPT)
                    PRMPT = None
                else:
                    print(PRMPT)
    user_prompt = st.chat_input(placeholder="Краще напишу/I'll write instead")
    if user_prompt is not None:
        user_prompt = check_language(user_prompt=user_prompt)
# Checks for existing messages in session state
if "messages" not in st.session_state:
    st.session_state.messages = HISTORY

# Display chat messages from session state
for message in st.session_state.messages:
    with my_slot2.chat_message(message["role"]):
        st.markdown(message["content"])

if user_prompt is not None or PRMPT is not None:
    # Display user prompt in chat message widget
    with my_slot1.chat_message("user"):
        print()
        print("User:", end="")
        print(user_prompt or PRMPT)
        st.markdown(user_prompt or PRMPT)

    # adds user's prompt to session state
    st.session_state.messages.append({"role": "user", "content": user_prompt or PRMPT})

    # retrieves response from model
    LLM_STREAM = ollama_prompt(
        messages=st.session_state.messages,
    )
    with my_slot2.chat_message("assistant"):
        try:
            st.write(stream_parser(LLM_STREAM))
        except stop_running():
            pass
