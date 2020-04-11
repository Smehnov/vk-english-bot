# English-learning chatbot for vk.com  
Vk.com bot for learning english words(for russian-speaking people).  
![How it works](https://github.com/Smehnov/vk-english-bot/blob/master/work_process.gif)  
##Technologies:  
Python flask, pymongo and vkapi libs.  
Db: mongodb.  
## How to run  
1. Crate vk community with bot functions  
2. Create settings.py file with token variables  
3. Set up mongodb  
4. Run   
## How it works  
*Note: now words are sorted alphabetic without random*  
Bot communicates with vk.com using special api. There is sqlite db with en-ru words and mongodb for keeping user data like current state(learning_word 1,2,3... repeating_words main_menu etc).  
Each word is being showed to user, then user is choosing word status: already know or learn. If user knows word, word goes to long term memory(list field for each user in db). If user chooses lerning, word goes to short-term memory. After getting 3+ words in short-term memory, user can choose repeating.  
In repeating mode user has to choose right translation of each showed word.  If user chooses correct answer, word goes to long term memory.  
There is also an ability to see long and short term memory words.
