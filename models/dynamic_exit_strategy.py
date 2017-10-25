import random

import talib
from rqalpha.api import *


def init(context):
    context.s1 = "510050.XSHG"

    context.atr_bar = 50
    context.maxhold = 10
    context.ptlim = 4.0
    context.mmstp = 1.0

    context.model_type = 1

    context.rand = 1984

    random.seed(context.rand)


def handle_bar(context, bar_dict):
    close = history_bars(context.s1, 200, '1d', 'close')
    high = history_bars(context.s1, 200, '1d', 'high')
    low = history_bars(context.s1, 200, '1d', 'low')

    exit_atr = talib.ATR(high, low, close, context.atr_bar)

    signal = 0
    rnum = random.random()
    if rnum < 0.025:
        signal = -1
    elif rnum > 0.975:
        signal = 1

    action = 'no_action'
    if context.portfolio.positions[context.s1].quantity > 0:
        context.hold_day += 1
        context.price = context.order.avg_price

        if context.model_type == 1:
            context.limprice = context.price - context.ptlim * context.atr
            context.stpprice = min(low[-1], low[-2], context.price - context.mmstp * context.atr)
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
        context.atr = exit_atr[-1]
        context.hold_day = 0

    elif action == 'exit':
        order_target_value(context.s1, 0)
