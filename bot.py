import vkapi
import pymongo
import sqlite3
import json
import random

client = pymongo.MongoClient()
users  = client.bot.users

def message_processing(user_id, user_message):
    if (users.find_one({"user_id":user_id})):
        user = users.find_one({"user_id":user_id})

        
        
        if user["current_action"] == "none":

            if(user_message=="/recreate_me"):
                recreate_user(user_id)
                vkapi.send_message(user_id=user_id, message=f"Твой прогресс сброшен")
                send_keyboard(user_id, "none")

            elif(user_message=="/delete_me"):
                delete_user(user_id)
                vkapi.send_message(user_id, f"Ты удален из базы пользователей")
                send_keyboard(user_id, "start")
            

            elif user_message in ["учить слова", "учить слова💡"]:
                change_action(user_id, "learning")
                change_stage(user_id, 0)
                vkapi.send_message(user_id,"Ты начал учить слова")
                word_en, word_ru = get_word(user_id,(user['last_showed_word_num']+1), user['used_db'])
                vkapi.send_message(user_id, f"{change_string_font(word_en, 'big')} \n Перевод: {word_ru}")
                send_keyboard(user_id, "learning")

            elif user_message in ["мои слова", "мои слова📒"]:
                words1 = get_words_from_memory(user_id,"memory1")
                words2 = get_words_from_memory(user_id,"memory2")
                s_words1 =""
                s_words2=""
                for w in words1:
                    s_words1 += (f"{w} — {get_translation_of_word(w)}\n")
                for w in words2:
                    s_words2 += (f"{w} — {get_translation_of_word(w)}\n")               
                vkapi.send_message(user_id,f"Ты учишь эти слова: \n Память 1:\n {s_words1} \n Память 2:\n {s_words2}")
                send_keyboard(user_id, "none")

            elif user_message in ["повторять слова", "повторять слова🔁"]:
                words = get_words_from_memory(user_id, "memory1")
                if len(words)>=3:
                    vkapi.send_message(user_id, f"Повторение слов")
                    change_action(user_id, "repeating")
                    change_stage(user_id, 0)
                    set_repeating_words(user_id)

                    words = get_repeating_words(user_id)
                    word = words[0]
                    set_current_repeating_word(user_id, word)
                    words.remove(word)
                    random.shuffle(words)
                    words = words[0:2]
                    words.append(word)
                    random.shuffle(words)
                    set_other_words(user_id, words)
                    words_ru = []
                    for w in words:
                        words_ru.append(get_translation_of_word(w))
                    vkapi.send_message(user_id, f"Слово {change_string_font(word, 'big')}")
                    send_special_keyboard(user_id, "Выберите перевод", words_ru)
                    




                else:
                    vkapi.send_message(user_id, f"Нужно учить минимум 3 слова для повторения")

            else:
                vkapi.send_message(user_id,"Извини, я тебя не понимаю")
                send_keyboard(user_id, "none")
        elif user["current_action"]=="learning":
            if user_message in ["уже знаю", "уже знаю🤓"]:
                if user["current_stage_in_action"]<9:
                    inc_last_showed_word_num(user_id)
                    word_en, word_ru = get_next_user_word(user_id)
                    inc_current_stage_in_action(user_id)
                    vkapi.send_message(user_id, f"{change_string_font(word_en, 'big')} \n Перевод: {word_ru}")
                    send_keyboard(user_id, "learning")
                    
                else:
                    vkapi.send_message(user_id, f"10 слов пройдено")
                    inc_last_showed_word_num(user_id)
                    send_keyboard(user_id, "none")
                    change_action(user_id, "none")
                    change_stage(user_id, 0)
            

            elif user_message  in ["учить слово", "учить слово🤔"] :
                word_en, word_ru = get_next_user_word(user_id)
                add_word_to_memory(user_id, "memory1", word_en)
                inc_current_stage_in_action(user_id)

                if user["current_stage_in_action"]<9:
                    inc_last_showed_word_num(user_id)
                    word_en, word_ru = get_next_user_word(user_id)
                    vkapi.send_message(user_id, f"{change_string_font(word_en, 'big')} \n Перевод: {word_ru}")
                    send_keyboard(user_id, "learning")
                    
                else:
                    inc_last_showed_word_num(user_id)
                    vkapi.send_message(user_id, f"10 слов пройдено")
                    send_keyboard(user_id, "none")
                    change_action(user_id, "none")
                    change_stage(user_id, 0)
            elif user_message in ["стоп", "стоп 🛑"]:
                
                vkapi.send_message(user_id,"Изучение слов окончено")
                send_keyboard(user_id, "none")
                change_action(user_id, "none")
                change_stage(user_id, 0)
            else:
                vkapi.send_message(user_id, "Извини, я тебя не понимаю")
        
        elif user['current_action']=="repeating":
            if user_message in ["стоп", "стоп 🛑"]:
                vkapi.send_message(user_id,"Повторение слов окончено")
                send_keyboard(user_id, "none")
                change_action(user_id, "none")
                change_stage(user_id, 0)
            else:
                if user_message == get_translation_of_word(get_current_repeating_word(user_id)):
                    word=get_current_repeating_word(user_id)
                    vkapi.send_message(user_id, f"Всё, верно, следущее слово")
                    remove_word_from_memory(user_id, "memory1", word)
                    add_word_to_memory(user_id, "memory2", word)

                    words = get_words_from_memory(user_id, "memory1")
                    if len(words)>=3:
                        set_repeating_words(user_id)
                        words = get_repeating_words(user_id)
                        word = words[0]
                        set_current_repeating_word(user_id, word)
                        words.remove(word)
                        random.shuffle(words)
                        words = words[0:2]
                        words.append(word)
                        random.shuffle(words)
                        set_other_words(user_id, words)
                        words_ru = []
                        for w in words:
                            words_ru.append(get_translation_of_word(w))
                        vkapi.send_message(user_id, f"Слово {change_string_font(word, 'big')}")
                        send_special_keyboard(user_id, "Выбери перевод", words_ru)
                    else:
                        change_action(user_id,"none")
                        change_stage(user_id, 0)
                        vkapi.send_message(user_id, f"Изучи больше слов для повторения ")
                        change_stage(user_id, 0)
                        change_action(user_id, "none")
                        send_keyboard(user_id,"none")
                else:
                    vkapi.send_message(user_id, f"Ты ошибся")
                    set_repeating_words(user_id)
                    words = get_repeating_words(user_id)
                    word = words[0]
                    set_current_repeating_word(user_id, word)
                    words.remove(word)
                    random.shuffle(words)
                    words = words[0:2]
                    words.append(word)
                    random.shuffle(words)
                    set_other_words(user_id, words)
                    words_ru = []
                    for w in words:
                        words_ru.append(get_translation_of_word(w))
                    vkapi.send_message(user_id, f"Слово {change_string_font(word, 'big')}")
                    send_special_keyboard(user_id, "Выберите перевод", words_ru)

                
    else:
        create_user(user_id)
        vkapi.send_message(user_id=user_id, message=f"Привет, новый пользователь id'{user_id}', ты успешно зарегестрирован\n Время учить английский! ")
        send_keyboard(user_id, "none")

def create_user(user_id):
    users.insert_one({"user_id":user_id,"current_action":"none","current_stage_in_action":0, "used_db":"words1", "last_showed_word_num":1, "memory1":[], "memory2":[], "memory3":[], "memory4":[], "memory5":[], "repeating_words":[], "other_words":[], "current_repeating_word":""})
    print(f"user {user_id} was created")

def delete_user(user_id):
    print(f"user {user_id} was deleted")
    users.delete_one({"user_id":user_id})

def recreate_user(user_id):
    delete_user(user_id)
    create_user(user_id)

def change_action(user_id, new_action):
    users.update({"user_id":user_id},{"$set":{"current_action":new_action}})

def change_stage(user_id, new_stage):
    users.update({"user_id":user_id},{"$set":{"current_stage_in_action":new_stage}})

def get_word(user_id, word_id, table):
    conn = sqlite3.connect("./words/words.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT word_en FROM words2 WHERE rowid = {word_id}")
    word_en = cursor.fetchone()
    cursor.execute(f"SELECT word_ru FROM words2 WHERE rowid = {word_id}")
    word_ru = cursor.fetchone()

    if word_en:
        return word_en[0], word_ru[0]
    else:
        user=users.find_one({"user_id":user_id})
        inc_last_showed_word_num(user_id)
        return get_word(user_id, user['last_showed_word_num'],table)

def get_next_user_word(user_id):
    user = users.find_one({"user_id":user_id})
    return get_word(user_id,(user['last_showed_word_num']+1), user['used_db'])

def inc_last_showed_word_num(user_id):
    users.update({"user_id": user_id}, {"$inc":{"last_showed_word_num":1}})

def inc_current_stage_in_action(user_id):
    users.update({"user_id": user_id}, {"$inc":{"current_stage_in_action":1}})

def add_word_to_memory(user_id,memory,word):
    users.update({"user_id":user_id}, {"$push":{memory : word}})
    print(f"Word {word} was added to {memory} of user {user_id}")


def get_words_from_memory(user_id, memory):
    user = users.find_one({"user_id":user_id})
    words = user[memory]
    return words

def remove_word_from_memory(user_id, memory, word):
    user = users.find_one({"user_id":user_id})
    words = user[memory]
    words.remove(word)
    users.update({"user_id":user_id}, {"$set":{memory : words}})

def get_translation_of_word(word_en):
    conn = sqlite3.connect("./words/words.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT word_ru FROM words2 WHERE word_en = '{word_en}'")
    word_ru = cursor.fetchone()[0]
    return word_ru

def set_repeating_words(user_id):
    words = get_words_from_memory(user_id, "memory1")
    random.shuffle(words)
    users.update({"user_id":user_id}, {"$set":{"repeating_words" : words}})

def get_repeating_words(user_id):
    user = users.find_one({"user_id":user_id})
    words = user["repeating_words"]
    return words

def set_other_words(user_id, words):
    users.update({"user_id":user_id}, {"$set":{"other" : words}})

def get_other_words(user_id):
    user = users.find_one({"user_id":user_id})
    words = user["other_words"]
    return words

def set_current_repeating_word(user_id, word):
    users.update({"user_id":user_id}, {"$set":{"current_repeating_word" : word}})

def get_current_repeating_word(user_id):
    user = users.find_one({"user_id":user_id})
    return user['current_repeating_word']



def send_keyboard(user_id, keyboard_name):

    vkapi.send_message(user_id=user_id, message="Твоё действие: ", keyboard=json.dumps(get_keyboard(keyboard_name)))

def change_string_font(s, font):
    if font=="bold":
        s1=""
        for c in s:
            s1+=chr(ord(c)+120205)
        return s1
    elif font=="big":
        s1=""
        for c in s:
            s1+=chr(ord(c)+120283)
        return s1
    else:
        return s

def get_keyboard(keyboard_name):
    
    keyboard_learning={
                    
                      "one_time": False,
                      "buttons": [
                        [{
                            "action": {
                              "type": "text",
                              "label": "Учить слово🤔"
                            },
                            "color": "default"
                          },
                            
                            {
                          "action": {
                            "type": "text",
                            "label": "Уже знаю🤓"
                          },
                          "color": "default"
                        }
                          ],
                          [
                              {
                                  "action":{
                                      "type": "text",
                                      "label":"Стоп 🛑"
                                  },
                                  "color":"default"
                              }
                          ]
                      ]
                    
                }
    keyboard_none={
                    
                      "one_time": False,
                      "buttons": [
                        [{
                          "action": {
                            "type": "text",
                            "label": "Учить слова💡"
                          },
                          "color": "default"
                        },
                          {
                            "action": {
                              "type": "text",
                              "label": "Мои слова📒"
                            },
                            "color": "default"
                          }],[
                              {
                                  "action":{
                                      "type":"text",
                                      "label":"Повторять слова🔁"
                                  }
                              }
                          ]
                      ]
                    
                }
    keyboard_start={
                    
                      "one_time": False,
                      "buttons": [
                        [{
                          "action": {
                            "type": "text",
                            "label": "Начать🏎️"
                          },
                          "color": "positive"
                        }]
                      ]
                    
                }
    


    if keyboard_name=="learning":
         return keyboard_learning
    elif keyboard_name=="start":
        return keyboard_start
    elif keyboard_name=="none":
        return keyboard_none 

def send_special_keyboard(user_id, message, words):
    keyboard={
                    
                      "one_time": False,
                      "buttons": [
                        [],
                          [
                              {
                                  "action":{
                                      "type": "text",
                                      "label":"Стоп 🛑"
                                  },
                                  "color":"default"
                              }
                          ]
                      ]
                    
                }
    for word in words:
        keyboard["buttons"][0].append({"action":{"type":"text","label":word}})
    vkapi.send_message(user_id=user_id, message=message, keyboard=json.dumps(keyboard))