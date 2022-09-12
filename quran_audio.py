import requests
import json


def choose_reciter(reciter):
    reciter = reciter.lower()
    if reciter == "abdul basit":
        return "ar.abdulbasitmurattal"
    elif reciter == "abdullah basfar":
        return "ar.abdullahbasfar"
    elif reciter == "abdurrahmaan as-sudais":
        return "ar.abdurrahmaansudais"
    elif reciter == "abdul samad":
        return "ar.abdulsamad"
    elif reciter == "abu bakr ash-shaatree":
        return "ar.shaatree"
    elif reciter == "ahmed ibn ali al-ajamy":
        return "ar.ahmedajamy"
    elif reciter == "alafasy":
        return "ar.alafasy"
    elif reciter == "hani rifai":
        return "ar.hanirifai"
    elif reciter == "husary":
        return "ar.husary"
    elif reciter == "husary (mujawwad)":
        return "ar.husarymujawwad"
    elif reciter == "hudhaify":
        return "ar.hudhaify"
    elif reciter == "ibrahim akhdar":
        return "ar.ibrahimakhbar"
    elif reciter == "maher al muaiqly":
        return "ar.mahermuaiqly"
    elif reciter == "minshawi":
        return "ar.minshawi"
    elif reciter == "minshawy (mujawwad)":
        return "ar.minshawimujawwad"
    elif reciter == "muhammad ayyoub":
        return "ar.muhammadayyoub"
    elif reciter == "muhammad jibreel":
        return "ar.muhammadjibreel"
    elif reciter == "saood bin ibraaheem ash-shuraym":
        return "ar.saoodshuraym"
    elif reciter == "ibrahim walk":
        return "en.walk"
    elif reciter == "fooladvand - hedayatfar":
        return "fa.hedayatfarfooladvand"
    elif reciter == "parhizgar":
        return "ar.parhizgar"
    elif reciter == "shamshad ali khan":
        return "ur.khan"
    elif reciter == "chinese":
        return "zh.chinese"
    elif reciter == "youssouf leclerc":
        return "fr.leclerc"
    elif reciter == "ayman sowaid":
        return "ar.aymanswoaid"
    else:
        return "ar.alafasy"
    

def request_audio(surah, ayah, reciter = "Alafasy"):
    reciter = choose_reciter(reciter)
    
    something1 = requests.get(f'https://api.alquran.cloud/ayah/{surah}:{ayah}')
    something1 = something1.json()
    
    ayah_number_in_quran = something1['data']['number']
    
    return f'http://cdn.alquran.cloud/media/audio/ayah/{reciter}/{ayah_number_in_quran}'
    
