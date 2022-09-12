import json
import requests

def choose_language(lang):
    lang = lang.lower()
    if lang == 'albanian':
        return 'sq.ahmeti'
    elif lang == 'arabic':
        return 'ar'
    elif lang == 'chinese':
        return 'zh.jian'
    elif lang == 'dutch':
        return 'nl.keyzer'
    elif lang == 'english':
        return 'en.sahih'
    elif lang == 'farsi':
        return 'fa.ayati'
    elif lang == 'french':
        return 'fr.hamidullah'
    elif lang == 'german':
        return 'de.aburida'
    elif lang == 'hausa':
        return 'ha.gumi'
    elif lang == 'hindi':
        return 'hi.hindi'
    elif lang == 'indonesian':
        return 'id.indonesian'
    elif lang == 'italian':
        return 'it.piccardo'
    elif lang == 'japanese':
        return 'ja.japanese'
    elif lang == 'korean':
        return 'ko.korean'
    elif lang == 'kurdish':
        return 'ku.asan'
    elif lang == 'malay':
        return 'ms.basmeih'
    elif lang == 'malayalam':
        return 'ml.abdulhameed'
    elif lang == 'norwegian':
        return 'no.berg'
    elif lang == 'polish':
        return 'pl.bielawskiego'
    elif lang == 'russian':
        return 'ru.kuliev'
    elif lang == 'somali':
        return 'so.abduh'
    elif lang == 'spanish':
        return 'es.cortes'
    elif lang == 'swahili' or lang == 'kiswahili':
        return 'sw.barwani'
    elif lang == 'swedish':
        return 'sv.bernstrom'
    elif lang == 'tajik':
        return 'tg.ayati'
    elif lang == 'tamil':
        return 'ta.tamil'
    elif lang == 'turkish':
        return 'tr.ates'
    elif lang == 'urdu':
        return 'ur.ahmedali'
    elif lang == 'uyghur':
        return 'ug.saleh'
    else:
        return 'en.asad'
    
def request_ayah(surah, verse, lang = 'en.asad'):
    lang = choose_language(lang)
    whole_surah = requests.get(f"http://api.alquran.cloud/v1/surah/{int(surah)}/editions/{lang}")
    
    whole_surah = whole_surah.json()
    
    verse = whole_surah['data'][0]['ayahs'][int(verse) - 1]['text']
    
    
    return verse
