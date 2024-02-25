from flask import Flask, request
from flask_cors import CORS
import string
import uuid
import os


import torchaudio
import torch

from io import BytesIO


from phonemizer.backend.espeak.wrapper import EspeakWrapper

from transformers import AutoProcessor, AutoModelForCTC

app = Flask(__name__)
CORS(app)


processor = AutoProcessor.from_pretrained("facebook/wav2vec2-xlsr-53-espeak-cv-ft", token="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")
model = AutoModelForCTC.from_pretrained("facebook/wav2vec2-xlsr-53-espeak-cv-ft", token="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")


# thanks to: https://github.com/chdzq/ARPAbetAndIPAConvertor/

class Phoneme:

    def __init__(self, arpabet, american, english, ipa, is_vowel):
        '''
        :param arpabet: ARPAbet
        :param american: 美音
        :param english: 英音
        :param ipa: 国际音标
        :param is_vowel: 是否是元音
        '''
        self._arpabet = arpabet
        self._american = american
        self._english = english
        self._is_vowel = is_vowel
        self._ipa = ipa

    @property
    def ipa(self):
        return self._ipa

    @property
    def english(self):
        return self._english

    @property
    def american(self):
        return self._american

    @property
    def arpabet(self):
        return self._arpabet

    @property
    def is_vowel(self):
        return self._is_vowel

phonemes = [Phoneme(arpabet='AA', american='a',  english='ɑ:', ipa='ɑ',  is_vowel=True),
            Phoneme(arpabet='AE', american='æ',  english='æ',  ipa='æ',  is_vowel=True),
            Phoneme(arpabet='AH', american='ʌ',  english='ʌ',  ipa='ɐ',  is_vowel=True),
            Phoneme(arpabet='AO', american='ɔ',  english='ɔ:', ipa='ɔ',  is_vowel=True),
            Phoneme(arpabet='AW', american='aʊ', english='aʊ', ipa='aʊ', is_vowel=True),
            Phoneme(arpabet='AX', american='ə',  english='ə',  ipa='ə',  is_vowel=True),
            Phoneme(arpabet='ER', american='ɚ',  english='ər', ipa='ər', is_vowel=True),
            Phoneme(arpabet='AY', american='aɪ', english='aɪ', ipa='aɪ', is_vowel=True),
            Phoneme(arpabet='EH', american='ɛ',  english='e',  ipa='e',  is_vowel=True),
            Phoneme(arpabet='ER', american='ɝ',  english='ɜ:', ipa='ɜ', is_vowel=True),
            Phoneme(arpabet='EY', american='e',  english='eɪ', ipa='eɪ', is_vowel=True),
            Phoneme(arpabet='IH', american='ɪ',  english='ɪ',  ipa='ɪ',  is_vowel=True),
            Phoneme(arpabet='IX', american='ɨ',  english='ɨ',  ipa='ɨ',  is_vowel=True),
            Phoneme(arpabet='IY', american='i',  english='i:', ipa='i:', is_vowel=True),
            Phoneme(arpabet='OW', american='o',  english='əʊ', ipa='oʊ', is_vowel=True),
            Phoneme(arpabet='OY', american='ɔɪ', english='ɔɪ', ipa='ɔɪ', is_vowel=True),
            Phoneme(arpabet='UH', american='ʊ',  english='ʊ',  ipa='ʊ',  is_vowel=True),
            Phoneme(arpabet='UW', american='u',  english='u:', ipa='u',  is_vowel=True),
            Phoneme(arpabet='UX', american='ʉ',  english='ʉ',  ipa='ʉ',  is_vowel=True),
            Phoneme(arpabet='B',  american='b',  english='b',  ipa='b',  is_vowel=False),
            Phoneme(arpabet='CH', american='tʃ', english='tʃ', ipa='tʃ', is_vowel=False),
            Phoneme(arpabet='D',  american='d',  english='d',  ipa='d',  is_vowel=False),
            Phoneme(arpabet='DH', american='ð',  english='ð',  ipa='ð',  is_vowel=False),
            Phoneme(arpabet='DX', american='ɾ',  english='ɾ',  ipa='ɾ',  is_vowel=False),
            Phoneme(arpabet='F',  american='f',  english='f',  ipa='f',  is_vowel=False),
            Phoneme(arpabet='G',  american='g',  english='g',  ipa='ɡ',  is_vowel=False),
            Phoneme(arpabet='HH', american='h',  english='h',  ipa='h',  is_vowel=False),
            Phoneme(arpabet='JH', american='dʒ', english='dʒ', ipa='dʒ', is_vowel=False),
            Phoneme(arpabet='K',  american='k',  english='k',  ipa='k',  is_vowel=False),
            Phoneme(arpabet='L',  american='l',  english='l',  ipa='l',  is_vowel=False),
            Phoneme(arpabet='M',  american='m',  english='m',  ipa='m',  is_vowel=False),
            Phoneme(arpabet='N',  american='n',  english='n',  ipa='n',  is_vowel=False),
            Phoneme(arpabet='NG', american='ŋ',  english='ŋ',  ipa='ŋ',  is_vowel=False),
            Phoneme(arpabet='P',  american='p',  english='p',  ipa='p',  is_vowel=False),
            Phoneme(arpabet='Q',  american='ʔ',  english='ʔ',  ipa='ʔ',  is_vowel=False),
            Phoneme(arpabet='R',  american='',  english='r',  ipa='ɹ',  is_vowel=False),
            Phoneme(arpabet='S',  american='s',  english='s',  ipa='s',  is_vowel=False),
            Phoneme(arpabet='SH', american='ʃ',  english='ʃ',  ipa='ʃ',  is_vowel=False),
            Phoneme(arpabet='T',  american='t',  english='t',  ipa='t',  is_vowel=False),
            Phoneme(arpabet='TH', american='θ',  english='θ',  ipa='θ',  is_vowel=False),
            Phoneme(arpabet='V',  american='v',  english='v',  ipa='v',  is_vowel=False),
            Phoneme(arpabet='W',  american='w',  english='w',  ipa='w',  is_vowel=False),
            Phoneme(arpabet='WH', american='ʍ',  english='ʍ',  ipa='ʍ',  is_vowel=False),
            Phoneme(arpabet='Y',  american='j',  english='j',  ipa='j',  is_vowel=False),
            Phoneme(arpabet='Z',  american='z',  english='z',  ipa='z',  is_vowel=False),
            Phoneme(arpabet='ZH', american='ʒ',  english='ʒ',  ipa='ʒ',  is_vowel=False)]

IPAs = [p.ipa for p in phonemes] + [" "]
ARPAs = [p.arpabet for p in phonemes] + [" "]

ARPAtoIPAdict = dict(zip(ARPAs, IPAs))
IPAtoARPAdict = dict(zip(IPAs, ARPAs))
for p in phonemes:
    IPAtoARPAdict[p.english] = p.arpabet
    IPAtoARPAdict[p.american] = p.arpabet


def ARPAtoIPA(phoneme_arr):
    return [ARPAtoIPAdict[arpa] for arpa in phoneme_arr]

def ARPAtoIPAchar(char):
    return ARPAtoIPAdict[char]

def IPAtoARPA(phoneme_arr):
    # if string like transcription, convert into arr
    if len(phoneme_arr) == 1:
        phoneme_arr = phoneme_arr[0].split(" ")
    
    res = []
    for ipa in phoneme_arr:
        ipa_fixed = ipa.replace('ː',":")
        if ipa_fixed in IPAtoARPAdict:
            res.append(IPAtoARPAdict[ipa_fixed])
        else:
            res.append(IPAtoARPAdict.get(ipa_fixed.replace(':', ''), ''))
    return res

def IPAtoARPAchar(c):
    ipa_fixed = c.replace('ː',":")
    if ipa_fixed in IPAtoARPAdict:
        return IPAtoARPAdict.get(ipa_fixed)
    else:
        return IPAtoARPAdict.get(ipa_fixed.replace(':', ''), '')

@app.route('/')
def hello_world():
    return 'Hello, world!'


@app.route('/evaluate_user', methods=['POST'])
def score_user():

    audio_file = request.files['audio']
    sentence = request.form['sentence']

    audio_path = 'uploads/' + str(uuid.uuid4())

    audio_file.save(audio_path)
        
    wav_path = audio_path + '.wav'
    os.popen(f'ffmpeg -i {audio_path} -c:a pcm_f32le -ar 16000 {wav_path}').read()
    os.remove(audio_path)

    print("sss")
 # tokenize
    input_values = processor(torchaudio.load(wav_path)[0].squeeze(), return_tensors="pt", sampling_rate=16000).input_values

    # retrieve logits
    with torch.no_grad():
        logits = model(input_values).logits

    # take argmax and decode
    predicted_ids = torch.argmax(logits, dim=-1)
    transcribed_phonemes = processor.batch_decode(predicted_ids)
    
    
    from g2p import make_g2p
    transducer = make_g2p('eng', 'eng-ipa')
    t = transducer(sentence) # here is where we put the given text


    ############################## PART 3: MATCHING PHONEMES AND GETTING INCORRECT GRAPHEMES
    from minineedle import needle, core

    curr_phoneme = "XX"

    phoneme_to_grapheme = [(IPAtoARPAchar(b),a) for (a,b) in t.pretty_edges()]
    new_p2g = []
    old_p2g = []

    for i in range(len(t.pretty_edges())):
        if curr_phoneme != phoneme_to_grapheme[i][0]:
            curr_phoneme = phoneme_to_grapheme[i][0]
            if phoneme_to_grapheme[i][1] == phoneme_to_grapheme[i-1][1]:
                continue
            else:
                new_p2g.append(list(phoneme_to_grapheme[i]))
                old_p2g.append(list(phoneme_to_grapheme[i]))
        # else:
        #     new_p2g[-1][1] += phoneme_to_grapheme[i][1]

    s= ""
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
            while t.input_string[og_text_idx] != new_p2g[i+1][1][0]:
                new_p2g[i][1] += t.input_string[og_text_idx]
                og_text_idx += 1
            new_p2g[i][1] = new_p2g[i][1][1:]
        else:
            og_text_idx += 1
        if og_text_idx >= len(t.input_string):
            break


    alignment: needle.NeedlemanWunsch[list] = needle.NeedlemanWunsch([a[0] for a in new_p2g], IPAtoARPA(transcribed_phonemes))
    alignment.align()

    # print(alignment)

    # al1, al2 = alignment.get_aligned_sequences(core.AlignmentFormat.list) # or "list"

    # al1.replace
    # print(" ".join(al1))
    # print(" ".join(al2))

    correct_seq, actual_seq = alignment.get_aligned_sequences(core.AlignmentFormat.list)
    print(correct_seq)
    print(actual_seq)

    words = [[]]
    j = 0

    for i in range(len(correct_seq)):
        if type(correct_seq[i]) == core.Gap:
            continue
        if new_p2g[j][1] == ' ':
            words.append([])
        elif correct_seq[i] == actual_seq[i]:
            words[-1].append(1)
        else:
            words[-1].append(0)
        j=j+1
    

    os.remove(wav_path)

    if len(words) < len(sentence.split(' ')):
        for i in range(len(words), len(sentence.split(' '))):
            words.append([0]*len(sentence.split(' ')[i]))

    for i, word in enumerate(sentence.split(' ')):
        diff = len(word) - len(words[i])
        if diff > 0:
            words[i].extend([0]*diff)
        for j, c in enumerate(word):
            # punctuation is always correct
            if c not in string.ascii_letters:
                words[i][j] = 1

    print(words)
    return words


    
if __name__ == '__main__':
    app.run(port=4000)

