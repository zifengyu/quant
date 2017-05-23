import talib
import os


def init(context):
    context.s1 = "510050.XSHG"

    context.n = int(os.environ['n'])
    context.atr_bar = 50
    context.maxhold = 10
    context.ptlim = 4.0
    context.mmstp = 1.0


def handle_bar(context, bar_dict):
    close = history_bars(context.s1, context.n + 1, '1d', 'close')
    high = history_bars(context.s1, context.n + 1, '1d', 'high')
    low = history_bars(context.s1, context.n + 1, '1d', 'low')

    action = 'no_action'
    if context.portfolio.positions[context.s1].quantity > 0:
        context.hold_day += 1
        context.price = context.order.avg_price
        context.stop_loss = context.price - context.mmstp * context.atr
        context.stop_profit = context.price + context.ptlim * context.atr

        ll = low[:-1].min()

        if close[-1] <= ll or close[-1] > context.stop_profit or close[-1] < context.stop_loss \
                or context.hold_day > context.maxhold:
            action = 'exit'
    else:
        hh = high[:-1].max()
        if close[-1] >= hh:
            action = 'entry'

    if action == 'entry':
        context.order = order_value(context.s1, 10000.0)
        context.atr = talib.ATR(history_bars(context.s1, context.atr_bar, '1d', 'high'),
                                history_bars(context.s1, context.atr_bar, '1d', 'low'),
                                history_bars(context.s1, context.atr_bar, '1d', 'close'),
                                context.atr_bar - 1)[-1]
        context.hold_day = 0

    elif action == 'exit':
        order_target_value(context.s1, 0)