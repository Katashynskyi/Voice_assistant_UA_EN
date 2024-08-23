"""Main.py provide entry point to terminal based voice agent with memory and speech abilities \
in UA and EN voices. With this configuration it can be used for studying english or ukrainian, \
both writing and listening skills"""

import json
import sounddevice  # fixing ALSA errors
import speech_recognition as sr
from src.english_stt import en_transcribe
from src.identify_lang import identify_language
from src.ollama_tts import ollama_prompt
from src.ukrainian_stt import ua_transcribe
from config import SYS_MSG


def main(memory=False):
    """
    The main entry point for the application.

    Args:
        memory (bool, optional): Whether to load and save conversation history. Defaults to False.

    Returns:
        None

    Automatically detect your language, transcribe it and pronounce & write the answer in UA & EN.
    Optionally save conversation history to a JSON file
    """
    if memory is True:
        try:
            with open("data/HISTORY.json", "r", encoding="UTF-8") as f:
                history = json.load(f)
        except FileNotFoundError:
            print(
                "No previous history is available, creating new one.",
                "\t",
                "Попередньої розмови не знайдено, створюю розмову.",
            )
            history = [{"role": "system", "content": SYS_MSG}]
    try:
        listening = True
        while listening:
            with sr.Microphone() as source:
                recognizer = sr.Recognizer()
                recognizer.pause_threshold = 0.8
                recognizer.energy_threshold = 500
                recognizer.adjust_for_ambient_noise(source)  # , duration=1)
                # recognizer.dynamic_energy_threshold = 3000

                def_lang = "???"
                try:
                    print("Listening...\t\t Слухаю...")
                    audio = recognizer.listen(source, timeout=5.0)
                    print("Working on it...\t Обробка...")
                    # Save the audio data to a WAV file
                    wav_data = audio.get_wav_data(convert_rate=16000)
                    # Write the WAV data to a file
                    wav_file = "./data/wav/chunk.wav"
                    with open(wav_file, "wb") as file:
                        file.write(wav_data)
                except sr.UnknownValueError:
                    print(
                        "Could you repeat please?.It's not recognized",
                        "\t\t",
                        "Повторіть будь ласка, не розчула",
                    )
                def_lang = identify_language(wav_file)
                if def_lang in [
                    ["uk: Ukrainian"],
                    ["pl: Polish"],
                    ["ru: Russian"],
                    ["be: Belarusian"],
                ]:
                    print("Запит Солов'їною, обробка...")
                    prmpt = ua_transcribe(wav_file)
                    print("Користувач:", prmpt)
                    print("Дай подумати...")
                    ollama_prompt(prompt="ua: " + prmpt, history=history)
                else:
                    print("Detected as english, working on it...")
                    prmpt = en_transcribe(wav_file)
                    if prmpt == "Didn't recognize that.":
                        print("Didn't recognize that.\t\t Не зрозуміла.")
                    else:
                        print("User:", prmpt)
                        print("Wait for LLM to answer... Зараз відповім...")
                        ollama_prompt(prompt="en: " + prmpt, history=history)
                    print("\n", "\n")

    except KeyboardInterrupt:
        listening = False
        print("\n", "Stopped listening.\t Перервано.")
        print("\n", "\n")
        print("HISTORY:", history)
        # Also we can save history to reuse it later
        # Specify the file path and name
        history_path = "./data/HISTORY.json"

        # Serialize the list to JSON
        json_data = json.dumps(history)

        # Write the JSON data to the file
        with open(history_path, "w", encoding="utf-8") as file:
            file.write(json_data)


if __name__ == "__main__":
    main(memory=True)
