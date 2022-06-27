#Для удобства нажми на ctr+F
#и замение '/home/dmk/Загрузки/web(2).sqlite'
#на свой путь



#token = '5399889380:AAEkrl5yNOQUTge7QDUMqthhg2gM_Kwd5bw'
#==Подключение библиотек==
import json
import asyncio
import sqlite3
import telebot
import requests
import aioschedule
from telebot import types
from telebot.async_telebot import AsyncTeleBot
#========================

#====================Создание бота==========================
API_TOKEN = '5554097137:AAG-eYpLkg_YvlrNyI_FTc5iFF2I-V8rM-0'
bot = telebot.TeleBot(API_TOKEN)
#===========================================================



id = 0               #уникальный идентификатор в базе данных
name = ''            #имя пользователя
surname = ''         #фамилия пользователя
age = 0              #возраст пользователя
mail = ''            #адрес электронной почты пользователя
city = ''            #город пользователя
hour = 0             #время для занятий, удобный для пользователя
telegram_id = 0      #уникальный идентификатор пользователя телеграмма
lvl = 1              #уровень знаний

@bot.message_handler(commands=['reg'])
def start(message):
    id_list = []
    connection = sqlite3.connect('/home/dmk/Загрузки/web(2).sqlite')
    cursor = connection.cursor()
    cursor.execute("""SELECT * from USERS""")
    records = cursor.fetchall()
    for row in records:
        id_list.append(row[7])
    connection.commit()

    if message.from_user.id in id_list:
        global id
        global name
        global surname
        global age
        global mail
        global city
        global hour
        global telegram_id
        global lvl
        telegram_id = message.from_user.id
        
        connection = sqlite3.connect('/home/dmk/Загрузки/web(2).sqlite')
        cursor = connection.cursor()
        cursor.execute("""SELECT * from USERS""")
        records = cursor.fetchall()
        for row in records:
            if row[7]==message.from_user.id:
                id = row[0]
                name = row[1]
                surname = row[2]
                mail = row[3]
                age = row[4]
                city = row[6]
                hour = row[8]
                lvl = row[9]
        bot.send_message(message.from_user.id, f'Вы зарегистрированный пользователь\nДобро пожаловать, господин {surname}\nВаш уникальный id: {id}')
    else:
        bot.send_message(message.from_user.id, "Как тебя зовут?")
        bot.register_next_step_handler(message, get_name) #следующий шаг – функция get_name

def get_name(message): 
    global name
    name = message.text
    bot.send_message(message.from_user.id, 'Какая у тебя фамилия?')
    bot.register_next_step_handler(message, get_surname)
    
def get_surname(message): 
    global surname;
    surname = message.text;
    bot.send_message(message.from_user.id, 'Сколько тебе лет?')
    bot.register_next_step_handler(message, get_age)
    
def get_age(message):
    global age
    try:
        age = int(message.text) #проверяем, что возраст введен корректно
        bot.send_message(message.from_user.id, 'Введите адрес эдектронной почты')
        bot.register_next_step_handler(message, get_mail)
    except Exception:
        bot.send_message(message.from_user.id, 'Цифрами, пожалуйста')
        bot.register_next_step_handler(message, get_age)
    
def get_mail(message): 
    global mail
    mail = message.text
    bot.send_message(message.from_user.id, 'Из какого вы города?')
    bot.register_next_step_handler(message, get_city)
    
def get_city(message): 
    global city
    city = message.text
    bot.send_message(message.from_user.id, 'В какой час вам удобнее всего заниматься?\nЯ работаю только с 9 до 20)')
    bot.register_next_step_handler(message, get_hour)
    
def get_hour(message):
    global hour
    global id
            
    try:
        hour = int(message.text) #проверяем, что возраст введен корректно
    except Exception:
        bot.send_message(message.from_user.id, 'Цифрами, пожалуйста')
        bot.register_next_step_handler(message, get_hour)
    if not(9<=hour<=20):
        bot.send_message(message.from_user.id, 'Я работаю только с 9 до 20)')
        bot.register_next_step_handler(message, get_hour)
    else:
        connection = sqlite3.connect('/home/dmk/Загрузки/web(2).sqlite')
        cursor = connection.cursor()
        cursor.execute("""SELECT * from USERS""")
        records = cursor.fetchall()
        id = len(records)+1
        cursor.execute(f"INSERT INTO USERS VALUES ({id}, '{name}', '{surname}', '{mail}', {age}, {0}, '{city}', {message.from_user.id}, {hour}, {0})")
        connection.commit()
        bot.send_message(message.from_user.id, f'Поздравляю!\nРегистрация прошла успешно!\nВаш уникальный id: {id}')
        bot.send_message(message.from_user.id, '/exer - начать занятие')

@bot.message_handler(commands=['exer'])
def handle_material(message):
    global id
    global lvl
    
    if 1<=lvl<10:
        connection = sqlite3.connect('/home/dmk/Загрузки/web(2).sqlite')
        cursor = connection.cursor()
        cursor.execute(f"""SELECT * from VIDEO WHERE lvl = {lvl}""")
        record = cursor.fetchall()
    
        video = f'{record[0][1]}'
        material = f'{record[0][2]}'
        bot.send_message(message.from_user.id, video)
        bot.send_message(message.from_user.id, material)
        bot.send_message(message.from_user.id, 'Не забудьте пройти тест после изучения материала\nВведите /poll для прохождения теста')
    else:
        global name
        global surname
        bot.send_message(message.from_user.id, f'Поздравляю {name} {surname}, вы завершили обучение')

@bot.message_handler(commands=['poll'])
def handle_poll(message):
    global id
    global lvl
    global API_TOKEN
    
    if 1<=lvl<10:
        connection = sqlite3.connect('/home/dmk/Загрузки/web(2).sqlite')
        cursor = connection.cursor()
        cursor.execute(f"""SELECT * from QUESTION WHERE lvl = {lvl}""")
        records = cursor.fetchall()
        lvl = lvl + 1
        cursor.execute(f"""UPDATE USERS SET lvl = {lvl} WHERE id = {id}""")
        connection.commit()
        
    
        for row in records:
            q = row[1]
            answers = row[2].split()
            answer = row[3]
            exp = row[4]
    
            #bot.send_poll(chat_id = message.from_user.id, question=q, options=answers, type='quiz', correct_option_id=answer, explanation=exp, is_anonymous=False, open_period=30)
            #response = requests.post(f"https://api.telegram.org/bot5456850082:AAHobVZF6M_eQ5F9PRHxsRfKHX1wFBw-v2o/sendPoll?question={q}&options={answers}&type='quiz'&correct_option_id={answer}&explanation={exp}&is_anonymous={False}&open_period={30}").text
            uri = f"https://api.telegram.org/bot{API_TOKEN}/sendPoll?chat_id={message.from_user.id}&" \
                  f"question={q}&options={json.dumps(answers)}&type={'quiz'}&correct_option_id={answer}" \
                  f"&explanation={exp}&is_anonymous=false"
            requests.post(uri)
    else:
        global name
        global surname
        bot.send_message(message.from_user.id, f'Поздравляю {name} {surname}, вы завершили обучение')
    
def get_updates(offset=0):
    result = requests.get("https://api.telegram.org/bot5554097137:AAG-eYpLkg_YvlrNyI_FTc5iFF2I-V8rM-0/getUpdates?offset={offset}").json()
    return result['result']

@bot.message_handler(commands=['result'])
def handle_poll_result(message):
    global API_TOKEN
    result = get_updates()
    print(result)

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Привет, I'm UDILIYA\nЯ буду обучать вас цифровой грамотности")
    bot.send_message(message.chat.id, "Цифровая грамотность — способность находить, оценивать и чётко передавать информацию с помощью набора текста и других средств массовой информации на различных цифровых платформах.")
    bot.send_message(message.chat.id, "/reg - регистриция")
    
@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.send_message(message.chat.id, "Если вам понадобится помощь\nПишите сюда:\nt.me/Enciof")

bot.infinity_polling()