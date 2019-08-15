import vk, random
from settings import token
session = vk.Session()
api = vk.API(session, v=5.101)

def send_message(user_id, message, token=token, attachment='', keyboard=0):
    if keyboard!=0:
        api.messages.send(access_token=token, user_id=str(user_id), message=message, random_id=random.randint(1,922337203685477580), attachment=attachment, keyboard=keyboard)
    else:
        api.messages.send(access_token=token, user_id=str(user_id), message=message, random_id=random.randint(1,922337203685477580), attachment=attachment)
    print(f"Try to send message '{message}' to id{user_id}")
    
    print(f"sent message '{message}' to id{user_id}")
