import requests
import work as w
import json
from pytesseract import image_to_string as im
from PIL import Image
from urllib.request import urlretrieve
import os
from pydub import AudioSegment
import speech_recognition as sr
from googletrans import Translator
from bs4 import BeautifulSoup as bs
from gtts import gTTS as gt
import vk_api

#приветствие
chi = ['привет','Привет','ку','qq']
bhi = ['привет','qq','Привет','хай']

def Weather(us,to,info):
    url ='http://api.openweathermap.org/data/2.5/weather?q='+info+'&appid=99e787ee0d65dd2aafc27050db21177b'
    site = requests.get(url).text
    js = json.loads(site)
    weather = int(js['main']['temp'])-273
    w.write_msg(us,to,'Погода в указаном городе:'+str(weather)+'\xB0С')

def itsd(us,to,url):
             urlretrieve(url,'check.jpg')
             doc = Image.open('/home/prazd/check.jpg')
             text = im(doc)
             os.remove('/home/prazd/check.jpg')
             w.write_msg(us,to,text)
def itsf(us,to,url):
             urlretrieve(url,'PHOTO.jpg')
             img = Image.open('/home/prazd/PHOTO.jpg')
             ttext = im(img)
             os.remove('/home/prazd/PHOTO.jpg')
             w.write_msg(us,to,ttext)

def Golos(us,to,url):
        try:
          #из mp3 в англ текст
          urlretrieve(url,'1.mp3')
          sound = AudioSegment.from_mp3("/home/prazd/1.mp3")
          sound.export("/home/prazd/test.wav", format="wav")
          r = sr.Recognizer()
          with sr.AudioFile('test.wav') as s:
                audio = r.record(s)
          command = r.recognize_google(audio)
          # Перевод
          strok = None
          trans = Translator()
          translate = trans.translate(command,dest='ru')
          translate = str(translate)
          translate = translate.split(',')
          for i in range(len(translate)):
              if 'text' in translate[i]:
                  strok = translate[i].replace('text=','')
          w.write_msg(us,to, 'Вы сказали: '+command+'\n'+'Перевод на русский:'+strok)
        except:
              w.write_msg(us,to,'Не получилось')
        finally:
              os.remove('/home/prazd/test.wav')
              os.remove('/home/prazd/1.mp3')
def USD(us,to):
            url = 'http://www.cbr.ru/scripts/XML_daily.asp'
            site = requests.get(url).text
            soup = bs(site,'lxml')
            f = soup.find_all('valute')[10].find('value')
            dol = str(f).replace('<value>','')
            dol = dol.replace('</value>','')
            w.write_msg(us,to,dol)
def EUR(us,to):
            url = 'http://www.cbr.ru/scripts/XML_daily.asp'
            site = requests.get(url).text
            soup = bs(site,'lxml')
            f = soup.find_all('valute')[11].find('value')
            eur = str(f).replace('<value>','')
            eur = eur.replace('</value>','')
            w.write_msg(us,to,eur)
def Audio(us,to,info):
            spis = info.split(",")
            tts = gt(text=spis[1],lang=spis[0])
            tts.save("audio.ogg")
            vk2 = vk_api.VkApi(login=os.environ(['vkLogin']),password=os.environ(['vkPassword']))
            o = {"type":"audio_message"}
            z = vk2.method('docs.getMessagesUploadServer',o)
            url = z['upload_url']
            files = {"file": open("/home/prazd/audio.ogg","rb")}
            r = requests.post(url,files=files)
            l = json.loads(r.text)
            save = vk2.method("docs.save",{"file":l["file"]})
            we = save[0]["preview"]["audio_msg"]["link_mp3"]
            w.write_msg(us,to,str(we))
            os.remove('/home/prazd/audio.ogg')