import pandas as pd
import os
from datetime import datetime, date, timedelta
import numpy as np
import matplotlib.pyplot as plt

__author__ = 'Duy Cao'
__copyright__ = 'Duy Cao, 2020'
__license__ = 'MIT'
__status__ = 'release'
__url__ = 'https://github.com/caominhduy/bitcoin-indicated'
__version__ = '1.0'


def macd(df, columns, auto=False):

    """
    Moving Average Convergence / Divergence (MACD) is:
        - a strong trend-confirming indicator
        - more useful for confirming trend, not predicting trend
        - prone to false positives
        - auto = True/False running script only, do not show figures
    Inputs:
        - df = Pandas DataFrame
        - columns = Column names that contain BTC-USD values
    Outputs: (uptrend, crossover)
        - uptrend = 1 (uptrending), -1 (downtrending), 0 (unclear)
        - crossover = values ranging from -1 (bearish) to 1 (bullish)
    """

    # the output we care for includes uptrend and MACD-Signal Relative Position
    for c in columns:
        ema_26 = df[c].ewm(span=26, adjust=False).mean()
        ema_12 = df[c].ewm(span=12, adjust=False).mean()

        macd = ema_12 - ema_26

        signal = macd.ewm(span=9, adjust=False).mean()
        baseline = [0]*len(signal)


        bullish = ((macd > signal) & (macd.shift(1) <= signal.shift(1)))*1
        bearish = ((macd < signal) & (macd.shift(1) >= signal.shift(1)))*-1
        macd_crossover = bullish + bearish

        '''
        macd_crossover values will be -1 (bearish), 0, or 1 (bullish):
            * When MACD line crosses over signal line, it signals bullish and
            vice versa
        '''

        if 'macd_crossover' not in df.columns.values.tolist():
            df['macd_crossover'] = macd_crossover
        else:
            df['macd_crossover'] = ((df['macd_crossover'] + macd_crossover)/2).astype('int')

        plt.plot(df['date'], baseline, '--')
        plt.plot(df['date'], macd, label='MACD', color='blue')
        plt.plot(df['date'], signal, label='Signal', color='tomato')

        plt.legend()
        plt.suptitle(f'MACD', fontsize=16)
        plt.title(f'Data source: {c}', fontsize=10)
        plt.savefig(f'docs/images/macd-{c}.jpg', dpi=300, pil_kwargs={'quality': 95})
        plt.savefig(f'docs/images/macd-{c}.svg')
        if auto == False:
            plt.show()

    if macd[len(macd)-1] > 0:
        uptrend = 1
    elif macd[len(macd)-1] < 0:
        uptrend = -1 # aka downtrend
    else:
        uptrend = 0

    cross = df[df['macd_crossover']!=0]['date'].max()

    return uptrend, df[df['date']==cross]['macd_crossover'].iloc[0] # uptrend and MACD-Signal crossover


def rsi(df, columns, n, auto=False): # n is period

    """
    Relative Strength Index (RSI) is useful for
        - indicating momentum
        - signaling oversold / overbought
    Inputs:
        - df = Pandas DataFrame
        - columns = Column names that contain BTC-USD values
        - n = period (14 by default)
        - auto = True/False running script only, do not show figures
    Outputs: (overbought, latest_rsi)
        - overbought = 1 (overbought), -1 (oversold), 0 (unclear)
        - latest_rsi = the most recent index
    """

    for c in columns:
        moving = df[c].diff()
        gain = moving
        gain = gain.clip(lower=0)
        loss = -moving
        loss = loss.clip(lower=0)

        aver_gain = gain.rolling(n).mean().abs()
        aver_loss = loss.rolling(n).mean().abs()

        # aver_gain = gain.ewm(alpha=1.0 / n, adjust=True).mean()
        # aver_loss = loss.abs().ewm(alpha=1.0 / n, adjust=True).mean()

        rs = aver_gain/aver_loss
        rsi = (100 - (100 / (1 + rs))).rolling(3).mean()

        plt.plot(df['date'], rsi, label='RSI', color='tomato')
        plt.ylim(bottom=0)
        plt.fill_between(df['date'], 30, 70, alpha=0.3, color='indigo')
        plt.legend()
        plt.suptitle(f'RSI', fontsize=16)
        plt.title(f'Data source: {c}', fontsize=10)
        plt.savefig(f'docs/images/rsi-{c}.jpg', dpi=300, pil_kwargs={'quality': 95})
        plt.savefig(f'docs/images/rsi-{c}.svg')
        if auto == False:
            plt.show()

        if 'rsi' not in df.columns.values.tolist():
            df['rsi'] = rsi
        else:
            df['rsi'] = (df['rsi'] + rsi)/2

    latest_rsi = df['rsi'].iloc[-1]
    if latest_rsi > 70:
        overbought = 1
    elif latest_rsi < 30:
        overbought = -1 # aka oversold
    else:
        overbought = 0

    return overbought, latest_rsi

def bollinger_band(df, columns, n, mul, auto=False):

    """
    Relative Strength Index (RSI) is useful for
        - indicating volatility
        - showing the noise in the market (aka loud / quiet)
    Inputs:
        - df = Pandas DataFrame
        - columns = Column names that contain BTC-USD values
        - n = period (20 by default)
        - mul = number of standard deviation (2 by default)
        - auto = True/False running script only, do not show figures
    Outputs: (bounce, squeeze)
        - bounce = 1 (bouncing up), -1 (bouncing down), 0 (unclear)
        - squeeze = 1 (contracting), -1 (widening), 0 (unclear)
    """

    for c in columns:
        ma = df[c].rolling(n).mean() # Simple MA
        stdevs = df[c].rolling(n).std() # Standard deviations

        upper = ma + mul * stdevs
        lower = ma - mul * stdevs

        plt.plot(df['date'], upper, label='Upper Band')
        plt.plot(df['date'], lower, label='Lower Band')
        plt.plot(df['date'], ma, label='MA')
        plt.plot(df['date'], df[c], label='BTC-USD')
        plt.fill_between(df['date'], upper, lower, alpha=0.3, color='indigo')
        plt.legend()
        plt.suptitle(f'Bollinger Band', fontsize=16)
        plt.title(f'Data source: {c}', fontsize=10)
        plt.savefig(f'docs/images/bollinger-{c}.jpg', dpi=300, pil_kwargs={'quality': 95})
        plt.savefig(f'docs/images/bollinger-{c}.svg')
        if auto == False:
            plt.show()

        if 'upper' not in df.columns.values.tolist() and 'lower' not in df.columns.values.tolist():
            df['upper'] = upper
            df['lower'] = lower
            df['ma'] = ma
        else:
            df['upper'] = (df['upper'] + upper)/2
            df['lower'] = (df['lower'] + lower)/2
            df['ma'] = (df['ma'] + ma)/2

    if abs(df[columns[0]].iloc[-1] - df['upper'].iloc[-1]) <= 0.3*abs(df[columns[0]].iloc[-1] - df['ma'].iloc[-1]):
        bounce = -1
    elif abs(df[columns[0]].iloc[-1] - df['lower'].iloc[-1]) <= 0.3*abs(df[columns[0]].iloc[-1] - df['ma'].iloc[-1]):
        bounce = 1
    else:
        bounce = 0

    # See if the band squeeze in the last 20 days
    width = (df['upper']-df['lower']).abs().iloc[-20:].diff().mean()

    if width > 0:
        squeeze = -1
    elif width < 0:
        squeeze = 1
    else:
        squeeze = 0

    return bounce, squeeze

def ichimoku_cloud(df, columns, n_1, n_2, n_3, n_4, auto=False):

    """
    Ichimoku Kinko Hyo (aka Ichimoku Cloud)
    Article: https://www.investopedia.com/terms/i/ichimoku-cloud.asp

    Inputs:
        - df = Pandas DataFrame
        - columns = Column names that contain BTC-USD values
        - n_1 = Tenkan period (9 by default)
        - n_2 = Kijun period (26 by default)
        - n_3 = Senkou period (52 by default)
        - n_4 = Chikou period (26 by default)
        - auto = True/False running script only, do not show figures

    Outputs:
        - Supporting, Resistant price(s)
        - Kijun trend, Chikou trend: 1 (price likely goes up), -1 (price likely goes down)

    """

    if (df['coindesk'] - df['nomics']).mean() > (df['coindesk'] - df['nomics']).mean():
        high = df['coindesk']
        low = df['nomics']
    else:
        high = df['nomics']
        low = df['coindesk']
    close = (df['coindesk'] + df['nomics'])/2

    # Conversion Line (Tenkan sen)
    tenkan = (high.rolling(n_1).max() + low.rolling(n_1).min())/2

    # Baseline (Kijun sen)
    kijun = (high.rolling(n_2).max() + low.rolling(n_2).min())/2

    # Sankou span A (leading span A)
    sankou_a = (tenkan + kijun)/2

    # Sankou span B (leading span B)
    sankou_b = (high.rolling(n_3).max() + low.rolling(n_3).min())/2

    # Lagging span (Chikou span)
    chikou = close.shift(n_4).rolling(n_4).mean()

    plt.plot(df['date'], close, label='Price', color='black')
    plt.plot(df['date'], tenkan, label='Conversion (Tenkan)', color='crimson')
    plt.plot(df['date'], kijun, label='Baseline (Kijun)', color='darkblue')
    plt.plot(df['date'], sankou_a, label='Leading Span A (Sankou A)')
    plt.plot(df['date'], sankou_b, label='Leading Span B (Sankou B)')
    plt.fill_between(df['date'], sankou_a, sankou_b, where=sankou_a>=sankou_b, facecolor='green', alpha=0.5, interpolate=True)
    plt.fill_between(df['date'], sankou_a, sankou_b, where=sankou_b>=sankou_a, facecolor='red', alpha=0.5, interpolate=True)
    plt.plot(df['date'], chikou, label='Lagging Span (Chikou)', color='green')
    plt.legend()
    plt.suptitle(f'Ichimoku Cloud', fontsize=16)
    plt.title(f'Data source: {columns}', fontsize=10)
    plt.savefig(f'docs/images/ichimoku.jpg', dpi=300, pil_kwargs={'quality': 95})
    plt.savefig(f'docs/images/ichimoku.svg')
    if auto == False:
        plt.show()

    support = []
    resistance = []

    if close.iloc[-1] >= sankou_a.iloc[-1]:
        support.append(sankou_a.iloc[-1])
    else:
        resistance.append(sankou_a.iloc[-1])

    if close.iloc[-1] >= sankou_b.iloc[-1]:
        support.append(sankou_b.iloc[-1])
    else:
        resistance.append(sankou_b.iloc[-1])

    bullish = ((close > kijun) & (close.shift(1) <= kijun.shift(1)))*1
    bearish = ((close < kijun) & (close.shift(1) >= kijun.shift(1)))*-1
    kijun_crossover = bullish + bearish
    df['kijun_crossover'] = kijun_crossover
    cross = df[df['kijun_crossover']!=0]['date'].max()
    kijun_trend = df[df['date']==cross]['kijun_crossover'].iloc[0]

    bullish = ((chikou > close) & (chikou.shift(1) <= close.shift(1)))*1
    bearish = ((chikou < close) & (chikou.shift(1) >= close.shift(1)))*-1
    chikou_crossover = bullish + bearish
    df['chikou_crossover'] = chikou_crossover
    cross = df[df['chikou_crossover']!=0]['date'].max()
    chikou_trend = df[df['date']==cross]['chikou_crossover'].iloc[0]

    return support, resistance, kijun_trend, chikou_trend
