import numpy as np
import talib
from rqalpha.api import *


def crosses_above(a, b, c=-1):
    return a[c] >= b[c] and a[c - 1] < b[c - 1]


def crosses_below(a, b, c=-1):
    return a[c] < b[c] and a[c - 1] >= b[c - 1]


def turns_up(a, c=-1):
    return a[c] >= a[c - 1] and a[c - 1] < a[c - 2]


def turns_dn(a, c=-1):
    return a[c] < a[c - 1] and a[c - 1] >= a[c - 2]


def init(context):
    context.s1 = "510050.XSHG"

    # context.osc_type oscillator type
    # 1 - Classic fast stochastics
    # 2 - Classic slow stochastics
    # 3 - Classic RSI
    # 4 - Classic MACD
    context.osc_type = 4

    # context.model_type
    # 1 - Overbought-oversold model
    # 2 - Signal line model
    # 3 - Divergence model
    context.model_type = 3

    # context.len1 shorter or first length parameter
    # context.len2 longer or second length parameter
    # context.len3 length of divergence test
    context.len1 = 12
    context.len2 = 26
    context.len3 = 20

    context.sample = 200

    context.atr_bar = 50
    context.maxhold = 10
    context.ptlim = 4.0
    context.mmstp = 1.0


def handle_bar(context, bar_dict):
    close = history_bars(context.s1, context.sample, '1d', 'close')
    high = history_bars(context.s1, context.sample, '1d', 'high')
    low = history_bars(context.s1, context.sample, '1d', 'low')

    if context.osc_type == 1:  # Classic fast stochastics
        oscline, sigline = talib.STOCHF(high, low, close, fastk_period=context.len1, fastd_period=3, fastd_matype=0)
        upperband = np.zeros(len(oscline)) + 80.0
        lowerband = np.zeros(len(oscline)) + 20.0
    elif context.osc_type == 2:  # Classic slow stochastics
        oscline, sigline = talib.STOCH(high, low, close, fastk_period=context.len1)
        upperband = np.zeros(len(oscline)) + 80.0
        lowerband = np.zeros(len(oscline)) + 20.0
    elif context.osc_type == 3:  # Classic RSI
        oscline = talib.RSI(close, timeperiod=context.len1)
        sigline = talib.SMA(oscline, timeperiod=3)
        upperband = np.zeros(len(oscline)) + 70.0
        lowerband = np.zeros(len(oscline)) + 30.0
    elif context.osc_type == 4:  # Classic MACD
        oscline, sigline, macdhist = talib.MACD(close, fastperiod=context.len1, slowperiod=context.len2, signalperiod=9)
        lowerband = abs(oscline) * 1.5
        upperband = talib.SMA(lowerband, timeperiod=120)
        lowerband = -upperband

    signal = 0
    if context.model_type == 1:  # Overbought-oversold model
        if crosses_above(oscline, lowerband):
            signal = 1
        elif crosses_below(oscline, upperband):
            signal = -1
    elif context.model_type == 2:  # Signal line model
        if crosses_above(oscline, sigline):
            signal = 1
        elif crosses_below(oscline, sigline):
            signal = -1
    elif context.model_type == 3:  # Divergence model
        m = close[-context.len3:].min()
        i = len(close) - 1
        while close[i] - m > 0.000000001:
            i = i - 1

        m = oscline[-context.len3:].min()
        j = len(oscline) - 1
        while oscline[j] - m > 0.000000001:
            j = j - 1

        if len(close) - 1 > i > len(close) - 7 and j > len(close) - context.len3 and i - j > 4 and turns_up(oscline):
            signal = 1
        else:
            m = close[-context.len3:].max()
            i = len(close) - 1
            while m - close[i] > 0.000000001:
                i = i - 1

            m = oscline[-context.len3:].max()
            j = len(oscline) - 1
            while m - oscline[j] > 0.000000001:
                j = j - 1

            if len(close) - 1 > i > len(close) - 7 and j > len(close) - context.len3 and i - j > 4 and turns_dn(oscline):
                signal = -1

    action = 'no_action'
    if context.portfolio.positions[context.s1].quantity > 0:
        context.hold_day += 1
        context.price = context.order.avg_price
        context.stop_loss = context.price - context.mmstp * context.atr
        context.stop_profit = context.price + context.ptlim * context.atr

        if signal == -1 or close[-1] > context.stop_profit or close[-1] < context.stop_loss \
                or context.hold_day > context.maxhold:
            action = 'exit'
    else:
        if signal == 1:
            action = 'entry'

    if action == 'entry':
        context.order = order_value(context.s1, 10000.0)
        context.atr = talib.ATR(high, low, close, timeperiod=context.atr_bar)[-1]
        context.hold_day = 0

    elif action == 'exit':
        order_target_value(context.s1, 0)
