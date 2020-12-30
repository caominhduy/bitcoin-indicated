from code import fetch
from code import indicators
import pandas as pd
import os

__author__ = 'Duy Cao'
__copyright__ = 'Duy Cao, 2020'
__license__ = 'MIT'
__status__ = 'release'
__url__ = 'https://github.com/caominhduy/bitcoin-indicated'
__version__ = '1.0'

def process_macd(uptrend, crossover, max_score):
    if uptrend == 1:
        trend = 'UP'
    elif uptrend == -1:
        trend = 'DOWN'
    else:
        trend = 'UNCLEAR'

    if crossover == 1:
        pos = 'ABOVE'
    elif crossover == -1:
        pos = 'BELOW'

    print(f'MACD indicates: overall trend is {trend}, MACD crosses {pos} Signal line')
    return uptrend*max_score + crossover*max_score

def process_rsi(overbought, rsi, max_score):
    if overbought == 1:
        moment = 'OVERBOUGHT'
        print(f'RSI indicates: Bitcoin is {moment}')
    elif uptrend == -1:
        trend = 'OVERSOLD'
        print(f'RSI indicates: Bitcoin is {moment}')
    else:
        if rsi >= 50:
            trend = 'UPTREND'
            print(f'RSI indicates: probably {trend}')
        elif rsi < 50:
            trend = 'DOWNTREND'
            print(f'RSI indicates: probably {trend}')
    return overbought*max_score*1.5 + (rsi>=50)*0.5*max_score

def process_bollinger(bounce, squeeze, max_score):
    if bounce == 1:
        bouncing = 'UP'
    elif bounce == -1:
        bouncing = 'DOWN'
    else:
        bouncing = 'CLOSE TO MOVING AVERAGE'

    if squeeze == 1:
        breakout = 'EXPECTED'
    elif squeeze < 1:
        breakout = 'UNEXPECTED'
    print(f'Bollinger Band indicates: probably bouncing {bouncing}, breakout is {breakout}')

    if squeeze == 1 and bounce == 1:
        return bounce*max_score + -1*breakout*max_score
    elif squeeze == 1 and bounce == -1:
        return bounce*max_score + breakout*max_score
    else:
        return bounce*max_score*-1

def process_ichimoku(inputs, max_score):
    support, resistance, kijun_trend, chikou_trend = inputs
    if len(support) > 0:
        print(f'Predicted lower support price(s) {support}')
    if len(resistance) > 0:
        print(f'Predicted upper resistant price(s) {resistance}')
    if kijun_trend == 1:
        print('Kijun line predicts price going UP')
    else:
        print('Kijun line predicts price going DOWN')
    if chikou_trend == 1:
        print('Chikou line predicts price going UP')
    else:
        print('Chikou line predicts price going DOWN')

    return kijun_trend*max_score + chikou_trend*max_score + len(support)*0.5*max_score + len(resistance)*-0.5*max_score

def process_score(score):
    if score >= -100 and score < -70:
        return 'You DEFINITELY should BUY'
    if score >= -70 and score < -40:
        return 'You MAYBE should BUY'
    if score >= -40 and score < 40:
        return 'You DEFINITELY should HOLD'
    if score >= 40 and score < 70:
        return 'You MAYBE should SELL'
    else:
        return 'You DEFINITELY should SELL'

def web(score, date):
    data = pd.read_csv('docs/assets/data/score.csv')
    data['past_score'] = data['current_score']
    past_score = data['past_score'].iloc[0]
    data['current_score'] = score
    data['date'] = date
    data['quote'] = process_score(score)
    data.to_csv('docs/assets/data/score.csv', index=False)

def indicator(option):
    score = 0

    if option == 'all':
        max_score = 1/9
        data = fetch.live_data()
        uptrend, crossover = indicators.macd(data, ['coindesk', 'nomics'])
        score += process_macd(uptrend, crossover, max_score)
        overbought, rsi = indicators.rsi(data, ['coindesk', 'nomics'], 14)
        score += process_rsi(overbought, rsi, max_score)
        bounce, squeeze = indicators.bollinger_band(data, ['coindesk', 'nomics'], 20, 2)
        score += process_bollinger(bounce, squeeze, max_score)
        output = indicators.ichimoku_cloud(data, ['coindesk', 'nomics'], 9, 26, 52, 26)
        score += process_ichimoku(output, max_score)
        score = round(score*100, 1)
        if not os.path.exists('docs/assets/data/score.csv'):
            pd.DataFrame({'date': [data['date'].iloc[-1]], 'current_score': [score], 'past_score': [score], 'quote': [process_score(score)]}).to_csv('docs/assets/data/score.csv', index=False)
        print(score, data['date'].iloc[-1])
        web(score, data['date'].iloc[-1])

    if option == 'web':
        max_score = 1/9
        data = fetch.live_data()
        uptrend, crossover = indicators.macd(data, ['coindesk', 'nomics'], auto=True)
        score += process_macd(uptrend, crossover, max_score)
        overbought, rsi = indicators.rsi(data, ['coindesk', 'nomics'], 14, auto=True)
        score += process_rsi(overbought, rsi, max_score)
        bounce, squeeze = indicators.bollinger_band(data, ['coindesk', 'nomics'], 20, 2, auto=True)
        score += process_bollinger(bounce, squeeze, max_score)
        output = indicators.ichimoku_cloud(data, ['coindesk', 'nomics'], 9, 26, 52, 26, auto=True)
        score += process_ichimoku(output, max_score)
        score = round(score*100, 1)
        if not os.path.exists('docs/assets/data/score.csv'):
            pd.DataFrame({'date': [data['date'].iloc[-1]], 'current_score': [score], 'past_score': [score], 'quote': [process_score(score)]}).to_csv('docs/assets/data/score.csv', index=False)
        print(score, data['date'].iloc[-1])
        web(score, data['date'].iloc[-1])


    if option == 'macd':
        max_score = 1/2
        data = fetch.live_data()
        uptrend, crossover = indicators.macd(data, ['coindesk', 'nomics'])
        score += process_macd(uptrend, crossover, max_score)
        score = round(score*100, 1)
        pd.DataFrame({'date': [data['date'].iloc[-1]], 'score': [score], 'quote': [process_score(score)]}).to_csv('docs/assets/data/score.csv', index=False)
        print(score)

    if option == 'rsi':
        max_score = 1/2
        data = fetch.live_data()
        overbought, rsi = indicators.rsi(data, ['coindesk', 'nomics'], 14)
        score += process_rsi(overbought, rsi, max_score)
        score = round(score*100, 1)
        pd.DataFrame({'date': [data['date'].iloc[-1]], 'score': [score], 'quote': [process_score(score)]}).to_csv('docs/assets/data/score.csv', index=False)
        print(score)

    if option == 'bollinger':
        max_score = 1/2
        data = fetch.live_data()
        bounce, squeeze = indicators.bollinger_band(data, ['coindesk', 'nomics'], 20, 2)
        score += process_bollinger(bounce, squeeze, max_score)
        score = round(score*100, 1)
        pd.DataFrame({'date': [data['date'].iloc[-1]], 'score': [score], 'quote': [process_score(score)]}).to_csv('docs/assets/data/score.csv', index=False)
        print(score)

    if option == 'ichimoku':
        max_score = 1/3
        data = fetch.live_data()
        output = indicators.ichimoku_cloud(data, ['coindesk', 'nomics'], 9, 26, 52, 26)
        score += process_ichimoku(output, max_score)
        score = round(score*100, 1)
        pd.DataFrame({'date': [data['date'].iloc[-1]], 'score': [score], 'quote': [process_score(score)]}).to_csv('docs/assets/data/score.csv', index=False)
        print(score)
