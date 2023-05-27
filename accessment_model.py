from binance import Client
import pandas as pd
from config import api_key, secret_key
import datetime

client = Client(api_key, secret_key)

eth_data = client.get_klines(symbol="ETHUSDT", interval="1d")


# запрашиваем цены открытия, закрытия и дневной максимум по тикеру

class AccessmentModel:

    def get_price_df(self):
        #устанавливаем выборку в 1000 дней для получения более точных результатов и минимизации погрешности
        data = client.get_klines(symbol=self, interval="1d", limit=1000)
        df = pd.DataFrame()

        #преобразуем данные в DataFrame
        for candle in range(len(data)):
            open_price = float(data[candle][1])
            high_price = float(data[candle][2])
            close_price = float(data[candle][4])

            new_df = pd.DataFrame({'High': [high_price], 'Open': [open_price], 'Close': [close_price]})
            df = pd.concat([df, new_df])

        return df


    eth_df = get_price_df("ETHUSDT")
    btc_df = get_price_df("BTCUSDT")

    #с помощью corrwith() расчитываем корреляцию между двумя датафреймами
    corr = eth_df.corrwith(btc_df)

    #найти достоверо точный способ определить долю движений цены ETHUSDT, вызванного движением BTCUSDT не представляется возможным
    #поэтому, использовал R-squared, который показался мне наиболее точным


    #используем коэффициент детерминации(R-квадрат) для расчета доли движений ETHUSDT, которая может быть объяснена движением BTCUSDT
    #корреляции цен открытия, закрытия и максимальной цены примерно равны, берем цену закрытия
    r_squared = corr["Close"] ** 2
