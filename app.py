import telebot
from telebot import types
from configurations import TOKEN, keys
from extensions import ConvertionExeption, CryptoConverter


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start(message):
    marcup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Помощь')
    item2 = types.KeyboardButton('Список доступных валют:')
    item3 = types.KeyboardButton('API предоставлен')
    item4 = types.KeyboardButton('Информация')

    marcup.add(item1, item2, item3, item4)

    bot.send_message(message.chat.id, 'Привет, я могу помочь тебе с конвертацией валюты'.format(message.from_user),
                     reply_markup=marcup)


@bot.message_handler(content_types=['text'])
def bot_message(message):
    if message.chat.type == 'private':
        if message.text == 'Помощь':
            bot.send_message(message.chat.id, 'Чтобы начать процесс конвертации, введите команду боту в следующем формате: '
                                              '\n <Название валюты> '
                                              '\n <В какую валюту нужно перевести> '
                                              '\n <Количество переводимой валюты> ')
        elif message.text == 'API предоставлен':
            bot.send_message(message.chat.id, 'cryptocompare.com')

        elif message.text == 'Список доступных валют:':
            for key in keys.keys():
                message.text = '\n'.join((message.text, key,))
            bot.send_message(message.chat.id, message.text)

        elif message.text == 'Информация':
            bot.send_message(message.chat.id, 'Бот использует бесплатный API, возможности ограничены!')
        else:
            try:
                value = message.text.split(' ')

                if len(value) != 3:
                    raise ConvertionExeption('Слишком много параметров.')

                quote, base, amount = value
                total_base = CryptoConverter.convert(quote, base, amount)

            except ConvertionExeption as e:
                bot.reply_to(message, f'Ошибка ввода. \n{e}')

            except Exception as e:
                bot.reply_to(message, f'Не удалось выполнить команду\n{e}')

            else:
                text = f'Цена {amount} - {quote} на данный момент составляет \n{total_base * int(amount)} - {base} ' \
                       f'\n данные с cryptocompare.com'
                bot.send_message(message.chat.id, text)


bot.polling()
