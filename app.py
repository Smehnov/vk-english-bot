from flask import Flask, request, json
from settings import confirmation_token,secret
import vk, bot
import random
app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello'

@app.route('/', methods=['POST'])
def processing():
    data = json.loads(request.data)
    print(data)
    if 'type' not in data.keys():
        return 'not vk'
    if 'secret' in data.keys():
        if data['secret']==secret:

            if data['type']=='confirmation':
                return confirmation_token
            elif data['type']=='message_new':
                user_id = data['object']['from_id']
                user_message = data['object']['text']
                bot.message_processing(user_id=user_id, user_message=user_message.lower())
        
                return 'ok'

if __name__ == "__main__":
    app.run(host= '0.0.0.0', port = '80')