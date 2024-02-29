"""
Credit goes to https://github.com/chdzq/ARPAbetAndIPAConvertor/
"""

from pydantic import BaseModel


ARPA = str



class Phoneme(BaseModel):
    arpabet: ARPA # ARPAbet
    american: str # American accent
    english: str # English accent
    ipa: str # International Phonetic Alphabet (IPA)
    is_vowel: bool # Is a vowel

_phonemes = [
    Phoneme(arpabet='AA', american='a',  english='ɑ:', ipa='ɑ',  is_vowel=True),
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
    Phoneme(arpabet='ZH', american='ʒ',  english='ʒ',  ipa='ʒ',  is_vowel=False)
]


_ARPAtoIPAdict = {" " : " "}
_IPAtoARPAdict = {" " : " "}

for p in _phonemes:
    _ARPAtoIPAdict[p.arpabet] = p.ipa
    _IPAtoARPAdict[p.ipa] = p.arpabet
    _IPAtoARPAdict[p.english] = p.arpabet
    _IPAtoARPAdict[p.american] = p.arpabet


def ARPAtoIPAchar(char: str) -> str:
    return _ARPAtoIPAdict[char]


def ARPAtoIPA(phoneme_arr: list[str]) -> list[str]:
    return [ARPAtoIPAchar(arpa) for arpa in phoneme_arr]


def IPAtoARPAchar(char: str) -> str:
    ipa_fixed = char.replace('ː',":")
    res = _IPAtoARPAdict.get(ipa_fixed)
    if res is None:
        return _IPAtoARPAdict.get(ipa_fixed.replace(':', ''), '')
    else: return res
        


def IPAtoARPA(phoneme_arr: list[str]) -> list[str]:
    # if string like transcription, convert into arr
    if len(phoneme_arr) == 1:
        phoneme_arr = phoneme_arr[0].split(" ")
    
    return [IPAtoARPAchar(ipa) for ipa in phoneme_arr]


corrections = {
    '/i/': '/i/ as in "beat" or "feet". The /i/ vowel is a high-front sound. Your tongue should be positioned high in your mouth, and shifted toward the front. Your lips should be tensed, and the corners of your mouth slightly stretched apart.',
    '/ɪ/': '/ɪ/ as in "bit" or "gym". The /ɪ/ vowel is a high-front sound. Your tongue should be positioned high in your mouth, and shifted toward the front. Your lips should be relaxed, and only slightly open.',
    '/e/': '/e/ as in "bait" or "late". This vowel is a mid front vowel. Position your tongue at middle height in your mouth, and shift it toward the front. The muscles of your lips and mouth should be fairly tense. Vibrate your vocal cords with your mouth in this position.',
    '/ɛ/': '/ɛ/ as in "bet". This vowel is a mid-front vowel. Position your tongue at mid-height in your mouth, and shift it toward the front. The muscles of your lips and mouth should be relaxed. Vibrate your vocal cords with your mouth in this position.',
    '/æ/': '/æ/ as in "bat". This vowel is a low vowel. Position your tongue low in your mouth, and shift it toward the front. The muscles of your lips and mouth should be relaxed. Vibrate your vocal cords with your mouth in this position.',
    '/ɑ/': '/ɑ/ as in "father". The /ɑ/ vowel is a low-back sound. Your tongue should be positioned low in your mouth, and shifted toward the back. Your mouth should be open wide. Vibrate your vocal cords and push air from your mouth.',
    '/ʌ/': '/ʌ/ as in "but". The /ʌ/ vowel is a mid-central sound. This means it is made with the tongue mostly relaxed, and at the center of the mouth. Your tongue should be at mid-height in the mouth, and your lips should be partially open.',
    '/ɔ/': '/ɔ/ as in "caught". To make this sound, position your tongue at mid height in your mouth, and shifted toward the back. Vibrate your vocal cords, and round your lips into an “o” shape as you do so.',
    '/ʊ/': '/ʊ/ as in "foot". /ʊ/ is a high, back, lax vowel. To make it, your tongue should be lifted high in the mouth, and shifted toward the back. Keep your lips relaxed and slightly open. Then, vibrate your vocal cords as you push air out of your mouth.',
    '/u/': '/u/ as in "boot". /u/ is a high, back, rounded vowel. To make it, your tongue should be lifted high in the mouth, and shifted toward the back. Place your lips into a circle “o” shape. You should feel some tension in your mouth muscles.',
    '/ə/': '/ə/ as in "about". The mouth position for /ə/ is neutral – the lips are relaxed, not rounded, the jaw is roughly half way open, and the tongue is flat, not forward or back',
    '/p/': '/p/ as in "pin". You should close your mouth at the start of the sound, and produce a burst of air.',
    '/b/': '/b/ as in "bin". You should close your mouth at the start of the sound, but do not produce a burst of air.',
    '/t/': '/t/ as in "tin". You should touch the top of your mouth using your tongue in making this sound.',
    '/d/': '/d/ as in "donkey". Place the tip of your tongue on the ridge behind your upper teeth, but not touching the teeth. As you push air out of your mouth, briefly stop it behind your tongue before releasing it.',
    '/k/': '/k/ as in "kin". Lift the back of your tongue and press it against the soft palate, above your throat. Push air out of your throat, stopping it briefly behind your tongue before releasing it.',
    '/ɡ/': '/ɡ/ as in "go". Lift the back of your tongue and press it against the soft palate, above your throat. Push air out of your throat, stopping it briefly behind your tongue before releasing it.',
    '/f/': '/f/ as in "final". Place the bottom edges of your upper teeth against the inside of your lower lip. Push air out of your mouth, forcing it between your teeth and lower lip.',
    '/v/': '/v/ as in "Venus". Place the bottom edges of your upper teeth against the inside of your lower lip. Vibrate your vocal cords, and push air out of your mouth, forcing it between your teeth and lower lip.',
    '/θ/': '/θ/ as in "thin". Place the tip of your tongue between your upper and lower teeth. Push air out of your mouth between your tongue and your teeth.',
    '/ð/': '/ð/ as in "this". Place the tip of your tongue between your upper and lower teeth. Push air out of your mouth between your tongue and your teeth. Y',
    '/s/': '/s/ as in "sin". Place the tip of your tongue lightly against the ridge behind your upper teeth, but not touching the teeth. As you push air out of your mouth, squeeze the air between the tip of your tongue and the top of your mouth.',
    '/z/': '/z/ as in "zoo". Place the blade of your tongue very close to the roof of your mouth, behind your teeth. Now, vibrate your vocal cords and push the air between your tongue and the roof of your mouth.',
    '/ʃ/': '/ʃ/ as in "shin". Place the tip of your tongue at the front of the top of your mouth, behind where the /s/ is produced. Push air between the top of your mouth and the tip of your tongue.',
    '/ʒ/': '/ʒ/ as in "vision" Place the tip of your tongue at the front of the top of your mouth, behind where the /s/ is produced. Vibrate your vocal cords as you push air between the top of your mouth and the tip of your tongue.',
    '/h/': '/h/ as in "hat" /h/ is made in your throat, with the glottis. Your vocal folds should be slightly tightened, to narrow your airway. Push air up through your airway into your mouth. You should feel some friction.',
    '/m/': '/m/ as in "man". Close your lips and push air through the nose. No air should leave your mouth. Vibrate your vocal cords.',
    '/n/': '/n/ as in "net" Place the front of your tongue against the roof of your mouth, behind your teeth. The tip and sides of your tongue should touch the roof of your mouth.',
    '/ŋ/': '/ŋ/ as in "sing" Lift the back of your tongue and place it against the soft palate at the back of your mouth. Vibrate your vocal cords.',
    '/l/': '/l/ as in "lie". The tip of your tongue should touch the top of your mouth, behind your teeth. Now, vibrate your vocal cords and let the air flow around the sides of your tongue.',
    '/r/': '/r/ as in "rid". Pull your tongue back so the tip is positioned around center of your mouth. Point the tip up slightly. Now, vibrate your vocal cords and let the air flow around and over your tongue.',
    '/w/': '/w/ as in "win". To make it, start by rounding your lips into an “O” shape. Vibrate your vocal cords, and widen your lips',
    '/j/': '/j/ as in "young". Begin with your tongue in a high-front position like the sound “ee” in “free.” Vibrate your vocal cords, and pull your tongue back and down slightly.',
    '/aɪ/': '/aɪ/ as in "tie". To begin, place your tongue low in your mouth, and shifted toward the back, to say /ɑ/. Then, as you vibrate your vocal cords, lift your tongue high in the mouth and shift it forward, to say /ɪ/. The transition between these two positions should be very quick.',
    '/aʊ/': '/aʊ/ as in "cow". To begin, place your tongue low in your mouth, and shifted toward the back, to say /ɑ/. Then, as you vibrate your vocal cords, lift your tongue high in the mouth, but keep it shifted toward the back, to say /ʊ/. The transition between these two positions should be very quick.',
    '/ɔɪ/': '/ɔɪ/ as in "boy". To begin, place your tongue at mid-low height in your mouth, shifted toward the back, to say /o/. Round your lips into an “o” shape as you do so. Then, as you vibrate your vocal cords, lift your tongue high in the mouth and shift it toward the front, to say /ɪ/. The transition between these two positions should be very quick.',
    '/eɪ/': '/eɪ/ as in "day". The /eɪ/ sound is made as you move your mouth. You need to move your tongue up from /e/ to /ɪ/, and close your mouth slightly',
    '/iə/': '/iə/ as in "near". To make this sound, say /i/, then move your tongue back and down and your lips less wide to make the /ə/ sound.',
    '/ʊə/': '/ʊə/ as in "tour". To make this sound, say /u/, then open your mouth, stop rounding your lips, and move your tongue down to say /ə/. '
}


def get_correction(arpa_char: str) -> str:
    return corrections.get(f'/{ARPAtoIPAchar(arpa_char)}/')