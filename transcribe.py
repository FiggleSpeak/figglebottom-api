from transformers import AutoProcessor, AutoModelForCTC
import os

import torch
import torchaudio

from dotenv import load_dotenv
load_dotenv(".env")

HF_TOKEN = os.getenv("HF_TOKEN", "")

processor = AutoProcessor.from_pretrained("facebook/wav2vec2-xlsr-53-espeak-cv-ft", token=HF_TOKEN)
model = AutoModelForCTC.from_pretrained("facebook/wav2vec2-xlsr-53-espeak-cv-ft", token=HF_TOKEN)


def convert_to_wav(audio_path, wav_path = None, delete = True) -> str:
    if wav_path is None:
        wav_path = audio_path + ".wav"
        
    os.popen(f'ffmpeg -i {audio_path} -c:a pcm_f32le -ar 16000 {wav_path}').read()
    
    if delete:
        os.remove(audio_path)
    
    return wav_path
    
    

def load_audio(wav_path: str) -> torch.Tensor:
    waveform, _sr = torchaudio.load(wav_path)
    return waveform.squeeze()

def transcribe(wav_path: str):
    audio = load_audio(wav_path)
    
    input_values = processor(audio, return_tensors="pt", sampling_rate=16000).input_values
    
    # retrieve logits
    with torch.no_grad():
        logits = model(input_values).logits
    
    # take argmax and decode
    predicted_ids = torch.argmax(logits, dim=-1)
    transcribed_phonemes = processor.batch_decode(predicted_ids)
    
    return transcribed_phonemes    