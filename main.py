from binance import Client
import pandas as pd
from config import api_key, secret_key
import datetime
import time
from accessment_model import AccessmentModel

# апи заданы в .env файле, откуда импортированы в конфиг
client = Client(api_key, secret_key)


# подтягиваем цену нужной валюты с бинанса

class Coin:
    def get_coin_data(self, limit=61):
        # интервал обновления данных по цене можно менять, в данном случае раз в минуту
        data = client.get_klines(symbol=self, interval="1m", limit=limit)

        df = pd.DataFrame()

        # упаковываем в датафрейм для облегчения дальнейшей работы
        for candle in range(limit):
            date_time = datetime.datetime.fromtimestamp(data[candle][0] / 1e3)
            close_price = float(data[candle][4])
            new_df = pd.DataFrame({'Time': [date_time], f'{self}': [close_price]})
            df = pd.concat([df, new_df], ignore_index=True)
        return df


# функция для расчета "амплитуды волатильности"
def calculate_change(symbol):
   
    
    #загружаем цену 
    data = Coin.get_coin_data(symbol)

    max_price = data.max()
    min_price = data.min()

    price_change = (max_price - min_price) / min_price
    
    if price_change >= (0.01 / (1 - AccessmentModel.r_squared)):
        return True
    
    return False


    #используем R-squared из AccessmentModel чтобы вычислить скорректированное изменения цены ETHUSDT
    #если R-squared = 0.69, то 69% изменений цена ETHUSDT может быть вызвано изменениями цена BTCUSDT
    #скорректированное изменение цены ETH = желаемое "очищенное" изменение(1%) / 1 - R-squared

    return significant_changes.empty


# прогоняем функцию по первичному датафрейму, далее в цикле каждую минуту по созданному новому датафрейму
def monitor_changes(symbol, interval=60):
    #df = Coin.get_coin_data(symbol)

    if calculate_change(symbol):
        print("За час цена не менялась(на 1%+)")
    else:
        print("Цена менялась более чем на 1% за прошедший час")

    while True:

        time.sleep(interval)

        if not calculate_change(symbol):
            print("Цена изменилась более чем на 1%")
        print("За час цена не менялась(на 1%+)")

