# Импортирую сторонние библиотеки
import telebot  # Для обработки команд telegram бота
from telebot import types   # Метод для добавление кнопок


# Присваиваю переменной bot токен полученный ранее
bot = telebot.TeleBot('5938048285:AAEGse6Zo4sAmyJswFJzxCeV_P-givSme04')


# Метод для получения текстовых сообщений
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    # Условие. Если пользователь напишет "Привет", бот должен ответить "Привет, чем я могу тебе помочь?" и спросить хочет ли пользователь зарегестрироватся.
    if message.text == "Привет" or message.text == "привет":
        bot.send_message(message.from_user.id, "Привет! Я тестовый бот который собирает информацию о своих пользователях. Напишите /reg для начала регистрации.")   # Ответ бота
    elif message.text == "/reg":
        bot.send_message(message.from_user.id, "Как тебя зовут?")
        bot.register_next_step_handler(message, get_name) #следующий шаг – функция get_name
    else:
        bot.send_message(message.from_user.id, "Пока что я немного глуповат и понимаю только команду 'Привет'. Напиши мне Привет что бы продолжить")  # Ответ бота


# Создаем переменные в которые запишем данные пользователя
name = ''
surname = ''
age = ''

# Функция получения имени
def get_name(message):
    global name
    name = message.text     # Записываем отправленное сообщение в переменную name
    bot.send_message(message.from_user.id, 'Какая у тебя фамилия?')     # Ответ бота
    bot.register_next_step_handler(message, get_surname)    # Переход на следующую стадию регистрации

# Функция получения фамилии
def get_surname(message):
    global surname
    surname = message.text  # Записываем отправленное сообщение в переменную surname
    bot.send_message(message.from_user.id, 'Сколько тебе лет?')     # Ответ бота
    bot.register_next_step_handler(message, get_age)    # Переход на следующую стадию регистрации

# Функция получения возраста
def get_age(message):
    global age
    age = message.text  # Записываем отправленное сообщение в переменную age
    bot.send_message(message.from_user.id, 'Отлично! Проверяем информацию:')    # Ответ бота
    question = f'Тебя зовут {name} {surname}. Тебе {age} лет. Всё верно?'   # Записываем информации в переменную question и выводим на экран
    keyboard(message, question)     # Запускаем клавиатуру (кнопки)


# Функция добавляющая клавиатуру в сообщение бота (кнопки)
def keyboard(message, question):  # выводим кнопки
    keyboard = types.InlineKeyboardMarkup()  # наша клавиатура
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')  # кнопка «Да»
    keyboard.add(key_yes)  # добавляем кнопку в клавиатуру
    key_no = types.InlineKeyboardButton(text='Нет', callback_data='no') # кнопка «Нет»
    keyboard.add(key_no)    # добавляем кнопку в клавиатуру
    question = 'Тебе ' + str(age) + ' лет, тебя зовут ' + name + ' ' + surname + '?'
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)

    @bot.callback_query_handler(func=lambda call: True)     # Метод проверяющий нажатие кнопки
    def callback_worker(call):
        if call.data == "yes":  # Если нажали "Да"
            bot.send_message(call.message.chat.id, 'Данные записаны!')
        elif call.data == "no":  # Если нажали "Нет"
            bot.send_message(call.message.chat.id, 'Данные удалены. Начата новая регистрация.')
            bot.send_message(call.message.chat.id, 'Как тебя зовут?')
            bot.register_next_step_handler(message, get_name)      # Отправить на повторную регистрацию

# Запуск бота с помощью метода polling
if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
