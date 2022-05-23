import requests
import json
from configurations import keys


class ConvertionExeption(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def convert(quote: str, base: str, amount: float):

        if quote == base:
            raise ConvertionExeption(f'Ошибка перевода, т.к. введен один вид валюты {base}.')

        try:
            quote_ticker = keys[quote]

        except KeyError:
            raise ConvertionExeption(f'Ошибка при обработке валюты {quote}.')

        try:
            base_ticker = keys[base]

        except KeyError:
            raise ConvertionExeption(f'Ошибка при обработке валюты {base}.')

        try:
            amount = float(amount)

        except ValueError:
            raise ConvertionExeption(f'Ошибка! Проверь количество {amount}. ')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]]

        return total_base
