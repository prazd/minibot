import vk

def write_msg(us, tok, mes, at=""):
    session = vk.Session()
    api = vk.API(session, v=5.0)
    api.messages.send(access_token=tok, user_id=str(us),message=mes,attachment=at)

