"Ukrainian Speech-to-text converter based on Wav2Vec2-Bert architecture"
import soundfile as sf
import torch
from transformers import AutoModelForCTC, Wav2Vec2BertProcessor
from transformers.utils.logging import set_verbosity_error

set_verbosity_error()


def ua_transcribe(
    file_paths="./data/wav/UA_test_2.wav",
    model_name="Yehor/w2v-bert-2.0-uk",
    device="cuda:0",
    sampling_rate=16000,
) -> str:
    """Transcribes Ukrainian audio using Wav2Vec2-Bert.

    Args:
        file_paths: Audio file path(s). Defaults to "./data/wav/UA_test.wav".
        model_name: Pre-trained model name. Defaults to "Yehor/w2v-bert-2.0-uk".
        device: Device for computation. Defaults to "cuda:0" if available.
        sampling_rate: Audio sampling rate. Defaults to 16000.

    Returns:
        Transcribed text.

    Raises:
        Exception: On errors.
    """

    # Load the Wav2Vec2-Bert model and processor
    asr_model = AutoModelForCTC.from_pretrained(model_name).to(device)
    processor = Wav2Vec2BertProcessor.from_pretrained(model_name)

    # Extract audio data from the provided file paths
    audio_inputs = []
    file_paths = [file_paths]  # Ensure file_paths is a list
    for path in file_paths:
        audio_input, _ = sf.read(path)
        audio_inputs.append(audio_input)

    # Preprocess the audio for model input
    inputs = processor(audio_inputs, sampling_rate=sampling_rate).input_features
    features = torch.tensor(inputs).to(device)

    # Perform audio transcription with no gradient calculation
    with torch.no_grad():
        logits = asr_model(features).logits

    # Decode the predicted token IDs to text
    predicted_ids = torch.argmax(logits, dim=-1)
    prdct = processor.batch_decode(predicted_ids)[0]
    return prdct


if __name__ == "__main__":
    print(ua_transcribe())
