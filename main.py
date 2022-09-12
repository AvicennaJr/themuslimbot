from pyrogram import Client, filters
import json
import requests
from quranInfo import *
import quran_finder
from hijri_converter import convert
import html2text
import quran_audio



app = Client("my_bot")

################### SALAH API ########################

def get_prayer_time(city):
    prayer = requests.get(f"http://api.aladhan.com/timingsByAddress?address={city}&method=4&school=0")

    prayer = prayer.json()
    fajr = prayer['data']['timings']['Fajr']
    dhuhr = prayer['data']['timings']['Dhuhr']
    asr = prayer['data']['timings']['Asr']
    maghrib = prayer['data']['timings']['Maghrib']
    isha = prayer['data']['timings']['Isha']
    
    salah_times = f'''\U0001f54b Salah times in {city.capitalize()} are as follows:

\U0001f554 Fajr: {fajr}
        
\U0001f550 Dhuhr: {dhuhr}
        
\U0001f55f Asr: {asr}
        
\U0001f556 Maghrib: {maghrib}
        
\U0001f563 Isha: {isha}'''
    return salah_times


##################### QURAN BIT #########################################

def confirm_surah(surah, verse):
    surah = int(surah)
    verse = int(verse)
    if not 0<surah<115:
        return 'There are only 114 Surahs, please try again.'

    else:
        if verse > quranInfo['surah'][surah][1]:
            return 'Invalid ayah'
        else:
            return 'success'


######################## HIJRI CALENDER #################################

def get_current_hijri():
    hijri = convert.Gregorian.today().to_hijri()
    return f'\U0001f5d3\ufe0f {hijri.day} {hijri.month_name()} {hijri.year} {hijri.notation(language="en")}'
    


####################### FORMATTING BIT ###################################

def format_hadith_text(html):
        h = html2text.HTML2Text()
        h.baseurl = "https://sunnah.com/"
        return h.handle(html.replace('`', 'ʿ').replace("</b>", '').replace("<i>", '*').replace("</i>", '*'))
    
    
def format_english_collection_name(collection_name):
    english_hadith_collections = {
        'ahmad': 'Musnad Ahmad ibn Hanbal',
        'bukhari': 'Sahīh al-Bukhārī',
        'muslim': 'Sahīh Muslim',
        'tirmidhi': 'Jamiʿ at-Tirmidhī',
        'abudawud': 'Sunan Abī Dāwūd',
        'nasai': "Sunan an-Nāsaʿī",
        'ibnmajah': 'Sunan Ibn Mājah',
        'malik': 'Muwatta Mālik',
        'riyadussalihin': 'Riyadh as-Salihīn',
        'adab': "Al-Adab al-Mufrad",
        'bulugh': 'Bulugh al-Maram',
        'shamail': "Shamā'il Muhammadiyyah",
        'mishkat': 'Mishkat al-Masabih',
        'qudsi40': 'Al-Arbaʿīn al-Qudsiyyah',
        'nawawi40': 'Al-Arbaʿīn al-Nawawiyyah',
        'hisn': 'Fortress of the Muslim (Hisn al-Muslim)'
    }

    return english_hadith_collections[collection_name]
    
    

####################### HADITH BIT ######################################

def get_hadith(collection, hadith_number):
    hadeeth_list = requests.get(f'https://api.sunnah.com/v1/collections/{collection}/hadiths/{hadith_number}', headers = {"X-API-Key": "sHpT4GWNK46MgRyAQlCmf6u2MJOc1a589Ntvw5Nx"})
    
    hadeeth_list = hadeeth_list.json()
    
    hadeeth = hadeeth_list['hadith'][0]['body']
    
    hadeeth = format_hadith_text(hadeeth)
    
    chapter_name = hadeeth_list['hadith'][0]['chapterTitle']
    
    chapter_name = format_hadith_text(chapter_name)
    
    try:
        grading = hadith_list['hadith'][0]["grades"][0]["grade"]
        #graded_by = hadith_list['hadith'][0]["grades"][0]["graded_by"]
    except:
        grading = ""
    
    combined = f"""**{chapter_name}**

{hadeeth}
__Reference: {format_english_collection_name(collection)} {hadith_number} \U0001f4ab__
"""
    
    return combined


####################### MUSHAF PAGES ###################################

def get_mushaf(surah, ayah):
    try:
        something = requests.get(f'https://api.alquran.cloud/ayah/{surah}:{ayah}')
        something = something.json()
        page = something['data']['page']
        formatted_page = str(page).zfill(3)
        
        return f'https://www.searchtruth.org/quran/images2/large/page-{formatted_page}.jpeg'
    
    except:
        return f'Could not get requested page \U0001f4dc'
    

###################### BOT COMMANDS ######################################


@app.on_message(filters.command(commands='salah', prefixes=['!','/'],case_sensitive=False))
def salah(client, message):
    cities = message.text.lower().split()
    city = cities [1]
    try:
        message.reply_text(text = get_prayer_time(city), quote = True)
        
    except:
        message.reply_text(text = "Prayer time for {city} has not been found")
        

@app.on_message(filters.command(commands='quran', prefixes=['!','/'], case_sensitive = False))
def quran(client, message):
    words = message.text.lower().split()
    try:
        surah, verse = words[1].split(':')
        if confirm_surah(surah, verse) == 'success':
            if len(words) == 2:
                message.reply_text(text = f'__"{quran_finder.request_ayah(surah,verse)}"__\n\n**\u2728 Quran {surah}:{verse}**', quote = True)
            elif len(words) > 2:
                message.reply_text(text = f'__"{quran_finder.request_ayah(surah,verse,words[2])}"__\n\n**\u2728 Quran {surah}:{verse}**', quote = True)
        else:
            message.reply_text(text = confirm_surah(surah, verse), quote = True)
    except:
        message.reply_text(text = """The Correct format is:

```!quran [surah:verse] <language>```
                           
For Example:
                           
```!quran 1:1 japanese```

Use !translations to get a list of available translations \U0001f30d""", quote = True)
        


@app.on_message(filters.command(commands='hijri', prefixes=['!','/'], case_sensitive = False))
def hijri_date(client, message):
    message.reply_text(text = get_current_hijri(), quote=True)
            
    
@app.on_message(filters.command(commands='hadith', prefixes=['!', '/'], case_sensitive = False))
def hadith_message(client, message):
    words = message.text.lower().split()
    try:
        collection, hadith_number = words[1], words[2]
        message.reply_text(text = get_hadith(collection, hadith_number) , quote = True)
        
    except:
        message.reply_text(text = '''The Correct format is:

```!hadith [book collection] [hadith number]

For Example:

```!hadith bukhari 1```

Use !hadithbooks to get a list of Hadith Collections \U0001f4d6''', quote = True)
    
@app.on_message(filters.command(commands='mushaf', prefixes=['!', '/'], case_sensitive = False))
def get_mushaf_page(client, message):
    words = message.text.split()
    try:
        surah, ayah = map(int, words[1].split(':'))
        message.reply_text(text = get_mushaf(surah, ayah), quote = True)
    except:
        message.reply_text(text = '''The Correct format is:
                           
```!mushaf [surah number]:[ayah number]```

For Example:

```!mushaf 2:255```''', quote = True)
        
@app.on_message(filters.command(commands='ayah', prefixes=['!', '/'], case_sensitive = False))
def get_ayah(client, message):
    words = message.text.lower().split()
    try:
        surah, ayah = map(int, words[1].split(':'))
        message.reply_text(text = f'http://cdn.alquran.cloud/media/image/{surah}/{ayah}', quote = True)
        
    except:
        message.reply_text(text = '''The correct format is:

```!ayah [surah number]:[verse number]```

For Example: 

```!ayah 2:255```''', quote = True)
        
@app.on_message(filters.command(commands='audio', prefixes=['!', '/'], case_sensitive = False))
def quran_audio_send(client, message):
    words = message.text.split()
    try:
        surah, ayah = map(int, words[1].split(':'))
        if len(words)>2:
            reciter = ' '.join(words[2:])
            message.reply_text(text = quran_audio.request_audio(surah, ayah, reciter), quote = True)
        else:
            message.reply_text(text = quran_audio.request_audio(surah, ayah), quote = True)
    except:
        message.reply_text(text = '''Correct format is:
                           
```!audio [surah]:[verse] [reciter]```

For Example:

```!audio 2:255 Hani Rifai```

Use !reciters to get a list of available reciters \U0001f399\ufe0f''', quote = True)
        

@app.on_message(filters.command(commands=['help','start'], prefixes=['!', '/'], case_sensitive = False))
def help_message(client, message):
    message.reply_text(text= '''**HELP MENU**:
    
\U0001f4cc```!quran```: Use !quran [surah]:[verse] [language] to get the Quranic verse in the specified language.

\U0001f4cc```!audio```: Use !audio [surah]:[verse] [reciter] to get an audio recitation of the Quranic verse.
    
\U0001f4cc```!hadith```: Use !hadith [book name] [hadith number] to get a hadith.
    
\U0001f4cc```!mushaf```: Use !mushaf [surah]:[verse] to get the image of the page on which a verse would be on a standard Medina Mushaf.

\U0001f4cc```!ayah```: Use !ayah [surah]:[verse] to get an image of a Quranic verse.
    
\U0001f4cc```!salah```: Use !salah [city/country] to get prayer times of a City/Country.
    
\U0001f4cc```!hijri```: Use get the current Islamic date.

\U0001f4cc```!hadithbooks```: Use to get the list of available books of Hadith.

\U0001f4cc```!translations```: Use to get the list of available translations of the Quran.

\U0001f4cc```!reciters```: Use to get the list of available Quran reciters.''', quote = True)
    
@app.on_message(filters.command(commands='hadithbooks', prefixes=['!', '/'], case_sensitive = False))
def hadith_books_list(client, message):
    message.reply_text(text = '''List of available books of hadith:

```bukhari```: \u2728 Sahīh al-Bukhārī \u2728

```muslim```: \u2728 Sahīh Muslim \u2728

```tirmidhi```: \u2728 Jamiʿ at-Tirmidhī \u2728

```abudawud```: \u2728 Sunan Abī Dāwūd \u2728

```riyadussalihin```: \u2728 Riyadh as-Salihīn \u2728

```adab```: \u2728 Al-Adab al-Mufrad \u2728

```bulugh```: \u2728 Bulugh al-Maram \u2728

```hisn```: \u2728 Fortress of the Muslim (Hisn al-Muslim) \u2728''', quote = True)
    
@app.on_message(filters.command(commands='translations', prefixes=['!', '/'], case_sensitive = False))
def quran_languages(client, message):
    message.reply_text(text = '''List of available translations \U0001f30d:

```Albanian```  \U0001f1e6\U0001f1f1
```Arabic```  \U0001f1f8\U0001f1e6
```Chinese```  \U0001f1e8\U0001f1f3
```Dutch```  \U0001f1e9\U0001f1f0
```English```  \U0001f1ec\U0001f1e7
```Farsi```  \U0001f1ee\U0001f1f7
```French```  \U0001f1eb\U0001f1f7
```German```  \U0001f1e9\U0001f1ea
```Hausa```  \U0001f1f3\U0001f1ec
```Hindi```  \U0001f1ee\U0001f1f3
```Indonesian```  \U0001f1ee\U0001f1e9
```Italian```  \U0001f1ee\U0001f1f9
```Japanese```  \U0001f1ef\U0001f1f5
```Korean```  \U0001f1f0\U0001f1f7
```Kurdish```  \U0001f1ee\U0001f1f7
```Malay```  \U0001f1ee\U0001f1e9
```Malayalam```  \U0001f1ee\U0001f1f3
```Norwegian```  \U0001f1f3\U0001f1f4
```Polish```  \U0001f1f5\U0001f1f1
```Russian```  \U0001f1f7\U0001f1fa
```Somali```  \U0001f1f8\U0001f1f4
```Spanish```  \U0001f1ea\U0001f1f8
```Swahili```  \U0001f1f9\U0001f1ff
```Swedish```  \U0001f1f8\U0001f1ea
```Tajik```  \U0001f1f9\U0001f1ef
```Tamil```  \U0001f1ee\U0001f1f3
```Turkish```  \U0001f1f9\U0001f1f7
```Urdu```  \U0001f1f5\U0001f1f0
```Uyghur```  \U0001f1e8\U0001f1f3''', quote = True)
    
@app.on_message(filters.command(commands='reciters', prefixes=['!', '/'], case_sensitive = False))
def quran_reciters(client, message):
    message.reply_text(text = '''List of available reciters \U0001f399\ufe0f:
                       
```Abdul Basit```
```Abdullah Basfar```
```Abdurrahmaan As-Sudais```
```Abdul Samad```
```Abu Bakr Ash-Shaatree```
```Ahmed ibn Ali al-Ajamy```
```Alafasy```
```Hani Rifai```
```Husary```
```Husary (Mujawwad)```
```Hudhaify```
```Ibrahim Akhdar```
```Maher Al Muaiqly```
```Minshawi```
```Minshawy (Mujawwad)```
```Muhammad Ayyoub```
```Muhammad Jibreel```
```Saood bin Ibraaheem Ash-Shuraym```
```Parhizgar```
```Ayman Sowaid```
```Ibrahim Walk``` - __English__
```Fooladvand - Hedayatfar``` - __Farsi__
```Shamshad Ali Khan``` - __Urdu__
```Chinese``` - __Chinese__
```Youssouf Leclerc``` - __French__''', quote = True)


app.run()
