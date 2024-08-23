"Python"
import warnings
from speechbrain.inference.classifiers import EncoderClassifier
from torch.cuda import is_available

# Suppress warnings
warnings.filterwarnings("ignore")


def identify_language(wav_filename="./data/wav/UA_test.wav") -> list:
    """
    Identifies the language of an audio file using a pre-trained language identification model.

    Args:
        wav_filename (str, optional): Path to the audio file. Defaults to "UA_test.wav".

    Returns:
        list: Predicted language ID.
    """
    # Load the pre-trained language identification model
    language_id = EncoderClassifier.from_hparams(
        source="speechbrain/lang-id-voxlingua107-ecapa",
        savedir="./data/model_data/",
        run_opts="cuda" if is_available() else None,
    )
    # Load the audio file
    signal = language_id.load_audio(wav_filename, savedir="./data/")
    # Classify the audio file
    prediction = language_id.classify_batch(signal)
    # Return the predicted language ID
    return prediction[3]


if __name__ == "__main__":
    print(identify_language())
