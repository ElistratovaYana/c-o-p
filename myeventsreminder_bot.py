import telebot
from datetime import datetime

TOKEN = 'мой токен'

bot = telebot.TeleBot(TOKEN)

user_plans = {}  # Словарь для хранения планов каждого пользователя

add_request = {}  # Словарь для хранения запросов на добавление планов

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Добро пожаловать! Я бот для записи планов.')

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, 'Чтобы записать план, используйте команду /add в одном сообщении, а затем бот запросит дату с планом.')

@bot.message_handler(commands=['add'])
def add(message):
    add_request[message.chat.id] = True
    bot.send_message(message.chat.id, 'Укажите дату и план в формате: дд.мм.гггг План')

@bot.message_handler(func=lambda message: message.chat.id in add_request and add_request[message.chat.id])
def add_plan(message):
    try:
        date, *text = message.text.split(maxsplit=1)
        date_obj = datetime.strptime(date, '%d.%m.%Y').date()
        plan = ' '.join(text)
        if message.chat.id in user_plans:
            user_plans[message.chat.id][date_obj] = user_plans[message.chat.id].get(date_obj, []) + [plan]
        else:
            user_plans[message.chat.id] = {date_obj: [plan]}
        bot.send_message(message.chat.id, 'План успешно добавлен!')
        add_request[message.chat.id] = False
    except:
        bot.send_message(message.chat.id, 'Ошибка в формате команды. Попробуйте еще раз.')

@bot.message_handler(commands=['remind'])
def remind(message):
    user_id = message.chat.id
    current_month_plans = []
    current_month = datetime.now().month
    if user_id in user_plans:
        for date, plan_list in user_plans[user_id].items():
            if date.month == current_month:
                for plan in plan_list:
                    current_month_plans.append(f'{date.strftime("%d.%m.%Y")}: {plan}')
        if current_month_plans:
            bot.send_message(user_id, 'Планы на текущий месяц:\n' + '\n'.join(current_month_plans))
        else:
            bot.send_message(user_id, 'Нет планов на текущий месяц.')
    else:
        bot.send_message(user_id, 'У вас пока нет записанных планов.')

bot.polling() 
