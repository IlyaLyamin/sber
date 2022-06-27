#Для удобства нажми на ctr+F
#и замение '/home/dmk/Загрузки/web(2).sqlite'
#на свой путь

#token = '5399889380:AAEkrl5yNOQUTge7QDUMqthhg2gM_Kwd5bw'
#==Подключение библиотек==
import sqlite3
import telebot
from telebot import types
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

exp = ''
answer = ''
answers = []
actual_question_index = 0

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
        bot.send_message(message.from_user.id, '/exer - начать занятие')
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
        bot.send_message(message.from_user.id, 'Не забудьте пройти тест после изучения материала\nВведите /test для прохождения теста')
    else:
        global name
        global surname
        bot.send_message(message.from_user.id, f'Поздравляю {name} {surname}, вы завершили обучение')

@bot.message_handler(commands=['test'])
def handle_poll(message):
    global id
    global lvl
    global API_TOKEN
    if 1<=lvl<10:
        connection = sqlite3.connect('/home/dmk/Загрузки/web(2).sqlite')
        cursor = connection.cursor()
        cursor.execute(f"""SELECT * from QUESTION WHERE lvl = {lvl}""")
        records = cursor.fetchall()
                
        epi_send_test(records, message.from_user.id)
        
        lvl = lvl + 1
        cursor.execute(f"""UPDATE USERS SET lvl = {lvl} WHERE id = {id}""")
        connection.commit()
    else:
        global name
        global surname
        bot.send_message(message.from_user.id, f'Поздравляю {name} {surname}, вы завершили обучение')

def epi_send_test(records, chat_id):
    global actual_question_index
    if 0<=actual_question_index<(len(records)-1):
        send_test(records, actual_question_index, chat_id)
        actual_question_index = actual_question_index + 1
        
    elif actual_question_index==(len(records)-1):
        send_test(records, actual_question_index, chat_id)
        actual_question_index = 0

def send_test(records, question_index, chat_id):
    global exp
    global answer
    global answers
    row = records[question_index]
    q = row[1]
    answers = row[2].split()
    answer = row[3]
    exp = row[4]
        
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for ans in answers:
        key = types.KeyboardButton(ans)
        keyboard.add(key); #добавляем кнопку в клавиатуру
    bot.send_message(chat_id, q, reply_markup=keyboard)


@bot.message_handler(content_types=["text"])
def handle_text(message):
    global exp
    global answer
    if message.text.strip() == answer:
        bot.send_message(message.from_user.id, f'right\n{exp}', reply_markup=types.ReplyKeyboardRemove())
    elif message.text.strip() in answers:
        bot.send_message(message.from_user.id, f'wrong\n{exp}', reply_markup=types.ReplyKeyboardRemove())


@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Привет, I'm UDILIYA\nЯ буду обучать вас цифровой грамотности")
    bot.send_message(message.chat.id, "Цифровая грамотность — способность находить, оценивать и чётко передавать информацию с помощью набора текста и других средств массовой информации на различных цифровых платформах.")
    bot.send_message(message.chat.id, "/reg - регистриция")
    
@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.send_message(message.chat.id, "Если вам понадобится помощь\nПишите сюда:\nt.me/Enciof")

bot.infinity_polling()