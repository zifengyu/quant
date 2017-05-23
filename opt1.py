import concurrent.futures
import multiprocessing
from rqalpha import run


tasks = []
for bw in range(15, 46, 1):
    for atrlen in range(5, 51, 1):
        for malen in range(1, 26, 1):
            config = {
                "extra": {
                    "context_vars": {
                        "malen": malen,
                        "atrlen": atrlen,
                        "bw": bw / 10.0
                    },
                    "log_level": "error",
                },
                "base": {
                    "securities": "stock",
                    "matching_type": "next_bar",
                    "frequency": "1d",
                    "strategy_file": "breakout_volatility.py",
                    "commission_multiplier": 1,
                    "slippage": 0,
                    "start_date": "2010-01-01",
                    "end_date": "2016-12-31",
                    "stock_starting_cash": 100000,
                    "benchmark": "000300.XSHG",
                },
                "mod": {
                    "sys_progress": {
                        "enabled": True,
                        "show": True,
                    },
                    "sys_analyser": {
                        "enabled": True,
                        "output_file": "results/out-{}-{}-{}.pkl".format(
                            bw, atrlen, malen
                        ),
                        "matching_type": "next_bar"
                    },
                },
            }

            tasks.append(config)


def run_bt(config):
    run(config)


with concurrent.futures.ProcessPoolExecutor(max_workers=2) as executor:
    for task in tasks:
        executor.submit(run_bt, task)