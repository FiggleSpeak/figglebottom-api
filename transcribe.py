from transformers import AutoProcessor, AutoModelForCTC
import os

import torch
import torchaudio

from typing import Optional

from dotenv import load_dotenv
load_dotenv(".env")

HF_TOKEN = os.getenv("HF_TOKEN", "")

processor = AutoProcessor.from_pretrained("facebook/wav2vec2-xlsr-53-espeak-cv-ft", token=HF_TOKEN)
model = AutoModelForCTC.from_pretrained("facebook/wav2vec2-xlsr-53-espeak-cv-ft", token=HF_TOKEN)


def convert_to_wav(audio_path: str, wav_path: Optional[str] = None, delete: bool = True) -> str:
    """Converts a normal audio file (typically MPEG or WebM) into a .wav file using FFMPEG.

    Args:
        audio_path (str): Path to original (mp3) file
        wav_path (str, optional): Path to save wav file. Defaults to "{audio_path}.wav".
        delete (bool, optional): Whether to delete the original file or not. Defaults to True.

    Returns:
        str: The new wav file path. It will be the same as wav_path if provided.
    """
    if wav_path is None:
        wav_path = audio_path + ".wav"
        
    os.popen(f'ffmpeg -i {audio_path} -c:a pcm_f32le -ar 16000 {wav_path}').read()
    
    if delete:
        os.remove(audio_path)
    
    return wav_path
    
    
def _load_audio(wav_path: str) -> torch.Tensor:
    """Loads audio waveform from wav file and returns as PyTorch Tensor.
    Note: sampling rate is NOT returned

    Args:
        wav_path (str): Path to wav file

    Returns:
        torch.Tensor: Tensor containing audio in wav file
    """
    waveform, _sr = torchaudio.load(wav_path)
    return waveform.squeeze()


def transcribe(wav_path: str):
    audio = _load_audio(wav_path)
    
    input_values = processor(audio, return_tensors="pt", sampling_rate=16000).input_values
    
    # retrieve logits
    with torch.no_grad():
        logits = model(input_values).logits
    
    # take argmax and decode
    predicted_ids = torch.argmax(logits, dim=-1)
    transcribed_phonemes = processor.batch_decode(predicted_ids)
    
    return transcribed_phonemes    