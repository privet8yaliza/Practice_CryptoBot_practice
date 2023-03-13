#имя бота @CryptoBot_practice

import telebot
from config import keys, TOKEN
from extensions import ConvertionException, CryptoConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands = ["start", "help"])
def start_help(message: telebot.types.Message):
	instruction_text = "Чтобы начать работу программы, введите команду боту в следующем формате:\n<Имя первоначальной валюты>\
<Имя валюты, в которую будет происходить конвертация> \
<Сумма конвертации>\n\nЧтобы просмотреть список всех доступных валют, введите команду: /values\n\nЗапись не целого числа осуществляется через '.' >> 1.5"
	bot.reply_to(message, instruction_text)


@bot.message_handler(commands = ["values"])
def values(message: telebot.types.Message):
	currency_text = "Доступные валюты:"
	for key in keys.keys():
		currency_text = "\n".join((currency_text, key.title(), ))
	bot.reply_to(message, currency_text)


@bot.message_handler(content_types = ["text", ])
def convert(message: telebot.types.Message):
	try:
		values = message.text.split(" ")

		if len(values) != 3:
			raise ConvertionException("Слишком много параметров.")

		quote, base, amount = values
		quote = quote.lower()
		base = base.lower()
		amount = float(amount)

		if amount < 0:
			raise ConvertionException("\nСумма конвертации не может принимать отрицательное значение.\nПерейти к инструкции по команде: /help")
			
		total_base = CryptoConverter.get_price(quote, base, amount)

	except ConvertionException as e:
		bot.reply_to(message, f"Ошибка пользователя.\n{e}")

	except Exception as e:
		bot.reply_to(message, "Не удалось обработать команду.\n\nПерейти к инструкции по команде: /help")

	else:
		text = f"Стоимость {amount} {keys[quote]} в {keys[base]} = {total_base}"
		bot.send_message(message.chat.id, text)


bot.polling()




