from flask import Flask
import base64
import random
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, world!'



@app.route('/evaluate_user', methods=['POST'])
def score_user():
    served_text = request.form.get('served_text')
    user_audio = request.form.get('user_audio') 
    var = random.randint()
    
    decoded = base64.decode(user_audio)
    
    with open("user_audio_" + var + ".wav", "w") as fo:
        fo.write("decoded")
        fo.close()
    
    
