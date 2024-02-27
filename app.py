from flask import Flask, request
from flask_cors import CORS

import string
import uuid
import os

from minineedle.needle import NeedlemanWunsch
from minineedle.core import Gap, AlignmentFormat

from g2p import make_g2p

from dotenv import load_dotenv
load_dotenv(".env")

from phoneme import IPAtoARPAchar, IPAtoARPA, get_correction, ARPA
from transcribe import transcribe, convert_to_wav


app = Flask(__name__)
CORS(app)

transducer = make_g2p('eng', 'eng-ipa')


@app.route('/')
def hello_world():
    return 'Hello, world!'


@app.route('/evaluate_user', methods=['POST'])
def score_user():
    audio_file = request.files['audio']
    sentence = request.form['sentence']

    
    
    #### PART 1: TRANSCRIBE THE AUDIO
    audio_path = 'uploads/' + str(uuid.uuid4())
    audio_file.save(audio_path)
    wav_path = convert_to_wav(audio_path)
    transcribed_phonemes = transcribe(wav_path)
    
    #### PART 2: CONVERT INPUT SENTENCE TO PHONEMES
    t = transducer(sentence)


    #### PART 3: MATCHING PHONEMES AND GETTING INCORRECT GRAPHEMES
    curr_phoneme = "XX"

    phoneme_to_grapheme: list[tuple[ARPA, str]] = [(IPAtoARPAchar(b),a) for (a,b) in t.pretty_edges()]
    new_p2g: list[tuple[ARPA, str]] = []
    old_p2g: list[tuple[ARPA, str]] = []


    for i in range(len(t.pretty_edges())):
        if curr_phoneme != phoneme_to_grapheme[i][0]:
            curr_phoneme = phoneme_to_grapheme[i][0]
            if phoneme_to_grapheme[i][1] != phoneme_to_grapheme[i-1][1]:
                new_p2g.append(list(phoneme_to_grapheme[i]))
                old_p2g.append(list(phoneme_to_grapheme[i]))

    s = ""
    og_text_idx = 0
    
    while t.input_string[og_text_idx] != new_p2g[0][1][-1]:
        s += t.input_string[og_text_idx]
        og_text_idx += 1
        if og_text_idx >= len(t.input_string):
            break

    new_p2g[0][1] = s + new_p2g[0][1]

    og_text_idx += 1

    for i in range(len(new_p2g)):
        # if new_p2g[i][1] == ' ':
        #     continue
        if t.input_string[og_text_idx] != new_p2g[i][1][0]:
            while i+1 < len(new_p2g) and t.input_string[og_text_idx] != new_p2g[i+1][1][0]:
                new_p2g[i][1] += t.input_string[og_text_idx]
                og_text_idx += 1
            new_p2g[i][1] = new_p2g[i][1][1:]
        else:
            og_text_idx += 1
        if og_text_idx >= len(t.input_string):
            break

    input_phonemes = [a[0] for a in new_p2g]

    alignment: NeedlemanWunsch[list] = NeedlemanWunsch(input_phonemes, IPAtoARPA(transcribed_phonemes))
    alignment.align()

    correct_seq, actual_seq = alignment.get_aligned_sequences(AlignmentFormat.list)
    print(correct_seq)
    print(actual_seq)

    words = [[]]
    pronunciation_tips = [[]]
    j = 0

    for i in range(len(correct_seq)):
        if type(correct_seq[i]) == Gap or correct_seq[i] == "":
            continue
        if new_p2g[j][1] == ' ':
            if len(pronunciation_tips[-1]) == 0:
                pronunciation_tips[-1].append('Sorry, we don\'t have tips for this word yet!')
            words.append([])
            pronunciation_tips.append([])
        elif correct_seq[i] == actual_seq[i]:
            words[-1].extend([1]*len(new_p2g[j][1]))
        else:
            words[-1].extend([0]*len(new_p2g[j][1]))
            tip = get_correction(correct_seq[i])
            if tip is not None:
                pronunciation_tips[-1].append(tip)

        j+=1
    
    os.remove(wav_path)

    if len(words) < len(sentence.split(' ')):
        for i in range(len(words), len(sentence.split(' '))):
            words.append([0]*len(sentence.split(' ')[i]))
            pronunciation_tips.append([])  # hm

    for i, word in enumerate(sentence.split(' ')):
        diff = len(word) - len(words[i])
        if diff > 0:
            words[i].extend([0]*diff)
        for j, c in enumerate(word):
            # punctuation is always correct
            if c not in string.ascii_letters:
                words[i][j] = 1

    print(words, pronunciation_tips)
    return [words, pronunciation_tips]


    
if __name__ == '__main__':
    app.run(port=4000)

