"""Converts audio from stereo to mono"""

import re
import speech_recognition as sr


def convert_audio_to_wav(audio_file, output_file) -> sr.AudioFile:
    """Converts audio file to a 16000 Hz WAV file.

    Args:
      audio_file: Path to the input audio file.
      output_file: Path to the output WAV file.
    """

    recognizer = sr.Recognizer()
    recognizer.pause_threshold = 0.8

    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)

    wav_data = audio.get_wav_data(convert_rate=16000)

    with open(output_file, "wb") as file:
        file.write(wav_data)


def check_language(user_prompt):
    """Checks if the user prompt contains EN characters and assigns a language prefix accordingly.
    Args:
        user_prompt (str): The user-provided prompt.
    Returns:
        str: The user prompt with a language prefix ("en:" or "ua:") based on the presence\
          of English characters.
    """
    english_pattern = re.compile(r"[a-zA-Z]")
    # cyrillic_pattern = re.compile(r"[\u0400-\u04FF]")
    if english_pattern.search(user_prompt):
        return "en: " + user_prompt
    else:
        return "ua: " + user_prompt

if __name__=="__main__":
    # Example usage:
    SAMPLE = "Краще напишу/I'll write instead"
    RESULT = check_language(SAMPLE)
    print(RESULT)  # Output: ua: Краще напишу/I'll write instead
