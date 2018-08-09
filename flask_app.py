from flask import Flask, request, json
import work as w
import fun
import random
import os

app = Flask(__name__)

@app.route('/', methods=['POST'])
def processing():
    token = os.environ(['token'])
    confirmation_token = 'alexokdaPrazd'
    #Распаковываем json из пришедшего POST-запроса
    data = json.loads(request.data)
    #Вконтакте в своих запросах всегда отправляет поле типа
    if 'type' not in data.keys():
        return 'not vk'
    if data['type'] == 'confirmation':
        return confirmation_token
    elif data['type'] == 'message_new':
        user_id = data['object']['user_id']
        if data['object']['body'] == 'как сам?':
                   w.write_msg(user_id,token,'хорошо')
        elif data['object']['body'] == 'USD':
                   fun.USD(user_id,token)
        elif data['object']['body'] == 'EUR':
                   fun.EUR(user_id,token)
        elif "aud" in data['object']['body']:
                   audio = data['object']['body'].replace("aud ","")
                   fun.Audio(user_id,token,audio)
        elif data['object']['body'] in fun.chi:
            ran = random.choice([0,1,2,3])
            w.write_msg(user_id,token,fun.bhi[ran])
        elif '!'in data['object']['body']:
                   m = data['object']['body']
                   place = m.replace('!','')
                   fun.Weather(user_id,token, place)
        elif data['object']['attachments'][0]['doc']['title'] == 'audio_msg.opus':
                  URL = data['object']['attachments'][0]['doc']['preview']['audio_msg']['link_mp3']
                  fun.Golos(user_id,token,URL)
        # Сообщение о том, что обработка прошла успешно
        return 'ok'


