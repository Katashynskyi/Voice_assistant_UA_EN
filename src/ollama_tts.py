"Run terminal, write to it and get text&audio response"

import sys

import asyncio
from ollama import chat

sys.path.append("./")
from src.transcribe_speak import transcribe_and_speak
from config import SYS_MSG

HISTORY = [{"role": "system", "content": SYS_MSG}]


def ollama_prompt(prompt: str = None, model="llama3.1", history: list = None) -> list:
    """
    Sends a prompt to the Ollama LLM and interacts with the user in a continuous loop.

    Args:
        prompt (str, optional): User's input prompt. Defaults to None.
        model (str, optional): The Ollama model to use. Defaults to "llama3.1".
        history (list, optional): A list of dictionaries representing the conversation history.\
            Defaults to None.

    Returns:
        None
    """
    history.append({"role": "user", "content": prompt})
    stream = chat(model=model, messages=history, stream=True)

    sentence_chunks, response_text = "", ""
    print("Assistant: ", end="")

    try:
        # Process each chunk in the LLM's response stream
        for part in stream:  # not bug but feature
            print(part["message"]["content"], end="", flush=True)
            content = part["message"]["content"]
            sentence_chunks += content
            response_text += content

            # Check for sentence ending and perform language detection and text-to-speech
            if sentence_chunks.endswith(("**:", ".", "!", "?", '?"', '!"', ":", ")")):
                if any("\u0400" <= char <= "\u04FF" for char in sentence_chunks):
                    lang = "ua"
                else:
                    lang = "en"
                asyncio.run(transcribe_and_speak(text=sentence_chunks, lang=lang))
                sentence_chunks = ""

        # Add the final response and updated history to conversation history
        history.append({"role": "assistant", "content": response_text})

    except KeyboardInterrupt:
        history.append({"role": "assistant", "content": response_text})
    return print("")


if __name__ == "__main__":
    try:
        TALKING = True
        while TALKING:
            print("User:", end="")
            ollama_prompt(prompt=input(), model="llama3.1", history=HISTORY)
            print()
    except KeyboardInterrupt:
        TALKING = False
        print()
        print("HISTORY:", HISTORY)
