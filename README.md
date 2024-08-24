# 🚀 UA-EN Voice Assistant  
## 🔐 No API-Keys | 🖥️ Local | 🧠 LLaMA 3.1 (12K Tokens Prompt-Menu ~20 Pages in Single Request)  

![🛠️ GitHub Last Commit](https://img.shields.io/github/last-commit/Katashynskyi/Voice_assistant_UA_EN)  
![🎬 Demo GIF](https://github.com/user-attachments/assets/d83255df-411f-4300-b04f-092f61dd5aae)  

🎥 **Demo Versions:**  
[![🖥️ GUI Version](data/media/GUI_V.png)](https://youtu.be/iw9P4Y7KXI4)  
[![💻 Console Version](data/media/CONSOLE_V.png)](https://youtu.be/c-8Z4qzOcII)  

---  

## 💡 Idea  
This project is a **proof-of-concept** for an **MVP**, inspired by OMNI's capabilities (ChatGPT).  
✅ **Main advantage** — **fully local deployment with no restrictions**.  
🛠️ Use it for:  
- 🌍 Language translation  
- 📚 Learning enhancement (reading, writing, audio skills)  
- 🎛️ Customization for specific needs  

---  

## ⚙️ Features & Tech Stack  

🗣️ **Language Classification**: Auto-detects UA/EN using **Lang-id-voxlingua107-ecapa** (supports 100+ languages).  
🎙️ **Google Legacy Recognizer**: Fast and free speech recognition.  
🔊 **Wav2Vec2-Bert**: **Best** Ukrainian speech-to-text model (so far).  
🗣️ **Edge-TTS**: **High-quality** natural voices for free.  
🤖 **Ollama-python**: Download and run LLMs offline.  
🖥️ **Streamlit**: GUI support.  
📜 **Dialogue saved in JSON**: **HISTORY.json** (for `main.py`), **short-term memory** for `app.py`.  
📝 **Config.py**: Customize **prompt** for the best user experience.  

---  

## 🚀 Getting Started  

### ✅ Tested on:  
🖥️ **WSL 22.04.3**  
🎮 **GeForce GTX 1050Ti (4GB, Mobile)**  
🧠 **RAM 32GB**  

### 📌 Requirements:  
🐍 **Python 3.9+**  
💾 **Conda 3.9+** (virtual environment)  
⚡ **CUDA (optional)**  

### 🔧 Installation  

```bash
# 1️⃣ Clone the repository
git clone https://github.com/Katashynskyi/Voice_assistant_UA_EN.git
cd Voice_assistant_UA_EN

# 2️⃣ Create and activate a virtual environment
conda activate ./.conda

# 3️⃣ Install dependencies
pip install uv
uv pip install -r requirements.txt
```

---  

## ▶️ Usage  

🔹 **Console Mode:**  
```bash
python3 main.py
```  
🔹 **Graphical Interface (GUI):**  
```bash
streamlit run app.py
```  

🚀 **Done! Enjoy your powerful voice assistant!** (suggesting to change LLM to phi4 at least) 🔥

