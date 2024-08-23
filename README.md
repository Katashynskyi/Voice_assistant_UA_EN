# UA-EN Voice Assistant 
## No api-keys | local | llama3.1 (12k tokens prompt-menu ~20 pages in single request)

![GitHub last commit](https://img.shields.io/github/last-commit/Katashynskyi/Voice_assistant_UA_EN)
![gif](https://github.com/user-attachments/assets/d83255df-411f-4300-b04f-092f61dd5aae)


[![GUI version](data/media/GUI_V.png)](https://youtu.be/iw9P4Y7KXI4)
[![Console version](data/media/CONSOLE_V.png)](https://youtu.be/c-8Z4qzOcII)

## The Idea
This project serves as a proof-of-concept for a minimum viable product (MVP) inspired by the capabilities of the OMNI model from ChatGPT. However, it offers a significant advantage: local deployment without restrictions. This empowers users to leverage its functionalities for various purposes, including:
- Translation across languages
- Learning Enhancement by practicing writing, reading, and audio skills
- Customization for tailored use cases

## Features & Tech stack

- **Language Classification**: classify if it's UA or EN for authomatic mode."Lang-id-voxlingua107-ecapa" by speechbrain (supports 100+ lang's).
- **Google legacy recognizer**: it uses a generic key that works out of the box. It's fast and works well.
- **Wav2Vec2-Bert**: best (for now) Ukrainian Speech-to-text converter.
- **Edge-TTS**: best (not generated) voices I can get for free.
- **Ollama-python**: lib to download and use most popular LLM's.
- **Streamlit**: for GUI.
- **dialogue saved in json**: HISTORY.json (only for main.py. For app.py it's only short-term context-window memory).
- **Config.py**: prompt for best user experience (modify it for your own purposes).


## Getting Started
### Tested on
- WSL 22.04.3
- Geforce (mobile) GTX 1050Ti (4GB)
- RAM (32GB)
### Prerequisites
- Python 3.9+
- Virtual environment (Conda 3.9+)
- CUDA (optional)
### Installation

- Clone the repository
- Create conda venv (Conda 3.9)
- sudo apt install portaudio19-dev
- Install the required packages: pip install -r requirements.txt

## Usage

After installation of required libs run main.py for console experience or app.py for GUI lovers.

