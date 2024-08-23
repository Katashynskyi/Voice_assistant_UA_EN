"""Text-To-Speech Interface with Pygame Audio Playback

This module provides a function (`tts`) to convert text to speech using Edge TTS
and play the generated audio using Pygame. It supports English (`en`) and Ukrainian
(`uk`, `ua`) languages (for now).
"""

from os import environ
import asyncio
import edge_tts

environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"  # must be before import pygame
import pygame


async def transcribe_and_speak(text="Nice brackets, John!", lang="en") -> pygame.mixer.music:
    """
    Converts text to speech using Edge TTS and plays the generated audio.

    Args:
        text (str, optional): The text to be spoken. Defaults to "Nice brackets, John!".
        lang (str, optional): The language for the TTS voice. Defaults to "en" (English).
            - Supported languages: "en" (English), "uk" (Ukrainian), "ua" (Ukrainian)

    Raises:
        ValueError: If the provided language is not supported.
    """
    if lang in ["en"]:
        voice = "en-GB-SoniaNeural"
    elif lang in ["uk", "ua"]:
        voice = "uk-UA-PolinaNeural"
    else:
        raise ValueError(f"Unsupported language: {lang}")
    output_file = "./data/wav/transcribed_piece.mp3"
    # Generate TTS audio
    communicate = edge_tts.Communicate(text=text, voice=voice, rate="+30%")
    await communicate.save(output_file)

    # Play the audio file
    pygame.mixer.init()
    pygame.mixer.music.load(output_file)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(1)


if __name__ == "__main__":
    PROMPT = "I'd be happy to try singing for you."
    asyncio.run(transcribe_and_speak(text=PROMPT, lang="en"))
    PROMPT = "Я б залюбки для тебе заспівала"
    asyncio.run(transcribe_and_speak(text=PROMPT, lang="ua"))
