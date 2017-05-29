import talib
from rqalpha.api import *


def init(context):
    context.s1 = "510050.XSHG"

    # context.avg_type moving average type
    # 1 - Simple Moving Average
    # 2 - Exponeential Moving Average
    # 3 - Weighted Moving Average
    context.avg_type = 1

    # context.model_type
    # 1 - Classic trend-following crossover model
    # 2 - Slope-based trend-following model
    # 3 - Counter-trend crossover model
    # 4 - Counter-trend support-resistance model
    context.model_type = 1

    context.short_period = 2
    context.long_period = 5

    context.sample = 200

    context.atr_bar = 50
    context.maxhold = 10
    context.ptlim = 4.0
    context.mmstp = 1.0


def handle_bar(context, bar_dict):
    close = history_bars(context.s1, context.sample, '1d', 'close')
    high = history_bars(context.s1, context.sample, '1d', 'high')
    low = history_bars(context.s1, context.sample, '1d', 'low')

    if context.avg_type == 1:
        fastma = talib.SMA(close, timeperiod=context.short_period) if context.short_period > 1 else close
        slowma = talib.SMA(close, timeperiod=context.long_period)
    elif context.avg_type == 2:
        fastma = talib.EMA(close, timeperiod=context.short_period) if context.short_period > 1 else close
        slowma = talib.EMA(close, timeperiod=context.long_period)
    elif context.avg_type == 3:
        fastma = talib.WMA(close, timeperiod=context.short_period) if context.short_period > 1 else close
        slowma = talib.WMA(close, timeperiod=context.long_period)

    signal = 0
    if context.model_type == 1:
        if fastma[-1] >= slowma[-1] and fastma[-2] < slowma[-2]:
            signal = 1
        elif fastma[-1] < slowma[-1] and fastma[-2] >= slowma[-2]:
            signal = -1
    elif context.model_type == 2:
        if fastma[-1] >= fastma[-2] and fastma[-2] < fastma[-3]:
            signal = 1
        elif fastma[-1] < fastma[-2] and fastma[-2] >= fastma[-3]:
            signal = -1
    elif context.model_type == 3:
        if fastma[-1] >= slowma[-1] and fastma[-2] < slowma[-2]:
            signal = -1
        elif fastma[-1] < slowma[-1] and fastma[-2] >= slowma[-2]:
            signal = 1
    elif context.model_type == 4:
        if slowma[-1] > slowma[-2] and fastma[-1] < slowma[-1] and fastma[-2] >= slowma[-2]:
            signal = 1
        elif slowma[-1] < slowma[-2] and fastma[-1] >= slowma[-1] and fastma[-2] < slowma[-2]:
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
