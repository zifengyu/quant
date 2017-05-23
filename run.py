import os

from rqalpha import run

import utils

config = {
    "base": {
        "strategy_file":         "breakout_volatility.py",
        "commission_multiplier": 1,
        "slippage":              0,
        "start_date":            "2010-01-01",
        "end_date":              "2016-12-31",
        "stock_starting_cash":   100000,
        "benchmark":             "000300.XSHG",
        "matching_type":         "next_bar"
    },
    "mod": {
        "sys_simulation": {
            "matching_type": "next_bar",
        }
    },
    "extra": {
        "log_level": "error",
    }
}

# for i in range(5, 101, 5):
#     os.environ['n'] = str(i)
#     a = run(config)
#     b = a['total_portfolios']['portfolio_value']
#     rrr = utils.cal_reward_to_risk(b)
#     print(i, rrr, b[-1] - b[0], len(a['trades']))
# os.environ['n'] = str(20)
# a = run(config)
# b = a['total_portfolios']['portfolio_value']
# rrr = utils.cal_reward_to_risk(b)
# print(rrr, b[-1] - b[0])
#
# mr = 0
#
# start_time = time.time()
# for bw in range(15, 16, 1):
#     for atrlen in range(5, 51, 1):
#         for malen in range(1, 26, 1):
#             os.environ['bw'] = str(bw / 10)
#             os.environ['atrlen'] = str(atrlen)
#             os.environ['malen'] = str(malen)
#             print(bw, atrlen, malen)
#             print(dir())
#
#             a = run(config)['sys_analyser']
#             b = a['total_portfolios']['total_value']
#             rrr = utils.cal_reward_to_risk(b)
#             if rrr > mr:
#                 mr = rrr
#                 print(bw, atrlen, malen, rrr, b[-1] - b[0], len(a['trades']))
#
# print('time: ', time.time() - start_time)

a = run(config)['sys_analyser']
b = a['portfolio']['total_value']
#sharpe = a['summary']['sharpe']
rrr = utils.cal_reward_to_risk(b)


with open('results.csv', 'a') as result_file:
    result_file.write('{} {} {} {} {} {}\n'.format(
        os.environ['bw'],
        os.environ['atrlen'],
        os.environ['malen'],
        rrr,
        b[-1] - b[0],
        len(a['trades'])
    ))




