import talib
from rqalpha.api import *


def init(context):
    context.s1 = "510050.XSHG"

    # context.malen = int(os.environ['malen'])
    # context.atrlen = int(os.environ['atrlen'])
    # context.bw = float(os.environ['bw'])

    context.malen = 1
    context.atrlen = 10
    context.bw = 1.5

    context.sample = 200

    context.atr_bar = 50
    context.maxhold = 10
    context.ptlim = 4.0
    context.mmstp = 1.0


def handle_bar(context, bar_dict):
    close = history_bars(context.s1, context.sample, '1d', 'close')
    high = history_bars(context.s1, context.sample, '1d', 'high')
    low = history_bars(context.s1, context.sample, '1d', 'low')

    if context.malen == 1:
        ema = close
    else:
        ema = talib.EMA(close, timeperiod=context.malen)

    atr = talib.ATR(high, low, close, timeperiod=context.atrlen)

    action = 'no_action'
    if context.portfolio.positions[context.s1].quantity > 0:
        context.hold_day += 1
        context.price = context.order.avg_price
        context.stop_loss = context.price - context.mmstp * context.atr
        context.stop_profit = context.price + context.ptlim * context.atr

        if close[-1] < ema[-2] - context.bw * atr[-2] or close[-1] > context.stop_profit or close[
            -1] < context.stop_loss \
                or context.hold_day > context.maxhold:
            action = 'exit'
    else:
        if close[-1] > ema[-2] + context.bw * atr[-2]:
            action = 'entry'

    if action == 'entry':
        context.order = order_value(context.s1, 10000.0)
        context.atr = talib.ATR(high, low, close, timeperiod=context.atr_bar)[-1]
        context.hold_day = 0

    elif action == 'exit':
        order_target_value(context.s1, 0)
