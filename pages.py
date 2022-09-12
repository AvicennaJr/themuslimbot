import requests
import json

def get_mushaf(surah, ayah):
    try:
        something = requests.get(f'https://api.alquran.cloud/ayah/{surah}:{ayah}')
        something = something.json()
        page = something['data']['page']
        formatted_page = str(page).zfill(3)
        
        return f'https://www.searchtruth.org/quran/images2/large/page-{formatted_page}.jpeg'
    
    except:
        return f'Could not get requested page'
    
#print(get_mushaf(1, 1))
