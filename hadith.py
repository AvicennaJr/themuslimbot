import requests
import json
import html2text

def format_hadith_text(html):
        h = html2text.HTML2Text()
        h.baseurl = "https://sunnah.com/"
        return h.handle(html.replace('`', 'ʿ').replace("</b>", '').replace("<i>", '*').replace("</i>", '*'))

def get_hadith(collection, hadith_number):
    hadeeth = requests.get(f'https://api.sunnah.com/v1/collections/{collection}/hadiths/{hadith_number}', headers = {"X-API-Key": "sHpT4GWNK46MgRyAQlCmf6u2MJOc1a589Ntvw5Nx"})
    
    hadeeth = hadeeth.json()
    hadeeth = hadeeth['hadith'][0]['body']
    hadeeth = format_hadith_text(hadeeth)
    return hadeeth

print(get_hadith('adab', 1))
