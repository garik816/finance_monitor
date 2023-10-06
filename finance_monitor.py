import telebot
from telebot import types
import requests
import time
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

bot = telebot.TeleBot('6403679692:AAEsWVBHb4GDW-iwEAixb5wZTHZdQF3-rEE')
api_key = '1cff9533-acc5-48b5-883f-6ce4c6dc6749'
address = 'TJ2piYDAUdviRHUgdYYnJR877nNiomwerY'

KulishID = '451168608'
garikID  = '433458619'

 #Флаг, чтобы отслеживать, было ли уже отправлено сообщение
balance_message_sent = False

 #Определите функцию, которую вы хотите выполнить с интервалом
def send_balance_message_job():
    send_balance_message()
    bot.polling(none_stop=True)

def get_tron_account_info(address, api_key):
    url = f'https://apilist.tronscanapi.com/api/accountv2?address={address}'
    headers = {'TRON-PRO-API-KEY': api_key}
    response = requests.get(url, headers=headers)

    # Проверяем успешность запроса
    if response.status_code == 200:
        # Получаем данные в формате JSON
        data = response.json()
        
        # Извлекаем "balance" и "tokenName"
        balance = data.get("balance")
        token_name = data.get("withPriceTokens")[0].get("tokenName")
        
        return token_name, balance/1000000
    else:
        # В случае ошибки выводим сообщение об ошибке
        print(f'Ошибка при выполнении запроса: {response.status_code}')
        return None, None
        
def send_balance_message():
    global balance_message_sent  # Используем глобальный флаг
    token_name, balance = get_tron_account_info(address, api_key)
    if balance > 100 and not balance_message_sent:  # Проверяем баланс и флаг
        message = f"Баланс {token_name}: {balance}"
        bot.send_message(garikID, message)
        bot.send_message(KulishID, message)
        balance_message_sent = True  # Устанавливаем флаг в True после отправки сообщения
        if balance < 100:
        	balance_message_sent = False  # Сбрасываем флаг, если баланс меньше 100

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    # Добавляем кнопку на клавиатуру
    button = types.KeyboardButton("проверить баланс")
    # Добавляем кнопку к клавиатуре
    markup.add(button)
    # Отправляем сообщение с клавиатурой
    bot.send_message(message.chat.id, "жми кнопку меню в низу", reply_markup=markup)
    
# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    #bot.reply_to(message, message.text)
    token_name, balance = get_tron_account_info(address, api_key)
    bot.send_message(message.chat.id, f"{token_name} = {str(balance)}")

sched.add_job(send_balance_message_job, 'interval', seconds=5)

# Запускаем бота
if __name__ == "__main__":
    sched.start()
