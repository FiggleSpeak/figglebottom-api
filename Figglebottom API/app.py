from flask import Flask, request
import base64
import random
import os
import platform

import torch
import torchaudio

from transformers import AutoProcessor, AutoModelForCTC

from dotenv import load_dotenv

load_dotenv(".env")


HF_TOKEN = os.getenv("HF_TOKEN", "")

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, world!'


@app.route('/evaluate_user', methods=['POST'])
def score_user():
    served_text = request.form.get('served_text')
    user_audio = request.form.get('user_audio')
    if platform.system().lower() == "windows":
        from phonemizer.backend.espeak.wrapper import EspeakWrapper
        EspeakWrapper.set_library('C:\\Program Files\\eSpeak NG\\libespeak-ng.dll')

    var = random.randint(0, 100000)
    
    decoded = base64.b64decode(user_audio)
    
    with open("user_audio_" + str(var) + ".wav", "wb") as fo:
        fo.write(decoded)
        fo.close()

        
    print("sss")
    
    # tokenize
    processor = AutoProcessor.from_pretrained("facebook/wav2vec2-lv-60-espeak-cv-ft", token=HF_TOKEN)
    model = AutoModelForCTC.from_pretrained("facebook/wav2vec2-lv-60-espeak-cv-ft", token=HF_TOKEN)
    input_values = processor(torchaudio.load("user_audio_" + str(var) + ".wav")[0].squeeze(), return_tensors="pt", sampling_rate=16000).input_values


    # retrieve logits
    with torch.no_grad():
        logits = model(input_values).logits

    # take argmax and decode
    predicted_ids = torch.argmax(logits, dim=-1)
    transcription = processor.batch_decode(predicted_ids)
    print(transcription)

    return('92racks')