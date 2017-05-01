import talib


def init(context):
    context.s1 = "510050.XSHG"

    context.n = 20
    context.atr_bar = 50
    context.maxhold = 10
    context.ptlim = 4.0
    context.mmstp = 1.0


def handle_bar(context, bar_dict):
    close = history_bars(context.s1, context.n, '1d', 'close')
    logger.info(close.max())

    action = 'no_action'
    if context.portfolio.positions[context.s1].quantity > 0:
        context.hold_day += 1
        context.price = context.order.avg_price
        context.stop_loss = context.price - context.mmstp * context.atr
        context.stop_profit = context.price + context.ptlim * context.atr

        if close[-1] <= close.min() or close[-1] > context.stop_profit or close[-1] < context.stop_loss or context.hold_day > context.maxhold:
            action = 'exit'
    else:
        if close[-1] >= close.max():
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
