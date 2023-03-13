import requests
import json
from config import keys


class ConvertionException(Exception):
	pass

class CryptoConverter:
	@staticmethod
	def get_price(quote: str, base: str, amount: str):

		if quote == base:
			raise ConvertionException("Ошибка: одинаковые параметры.")

		try:
			quote_ticker = keys[quote]
		except KeyError:
			raise ConvertionException(f"\nНе удалось обработать валюту '{quote}'.\nПросмотреть доступные валюты - /values.")

		try:
			base_ticker = keys[base]
		except KeyError:
			raise ConvertionException(f"\nНе удалось обработать валюту '{base}'.\nПросмотреть доступные валюты - /values.")

		try:
			amount = float(amount)
		except ValueError:
			raise ConvertionException(f"\nНе удалось обработать количество '{amount}'.")


		r = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}")
		total_base = json.loads(r.content)[keys[base]]

		return total_base