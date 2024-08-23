"""Module providing speech recognition"""

import speech_recognition as sr


def en_transcribe(wav_filename="./data/wav/EN_test.wav"):
    """Function transcribe/recognize english wav."""
    recognizer = sr.Recognizer()

    # Open the audio file and recognize it
    with sr.AudioFile(wav_filename) as source:
        audio_data = recognizer.record(source)
        try:
            return recognizer.recognize_google(audio_data)
        except sr.UnknownValueError:
            return "Didn't recognize that."
        except sr.RequestError as e:
            return f"Could not request results; {e}"


# Example usage
if __name__ == "__main__":
    SAMPLE = "./data/wav/EN_test.wav"
    response = en_transcribe(SAMPLE)
    print()
    print("Response: ", response)
