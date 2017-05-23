import os
import json
import concurrent.futures
import multiprocessing


tasks = []

# breakout
# for n in range(5, 101, 5):
#     extra_vars = {
#         "n": n
#     }
#     vars_params = json.dumps(extra_vars).encode("utf-8").decode("utf-8")
#
#     cmd = ("rqalpha run -fq 1d -f breakout.py --start-date 2010-01-01 --end-date 2016-12-31 "
#            "-o results/breakout/510050_20100101_20161231/n{}.pkl -sc 100000 -bm 000300.XSHG "
#            "-me next_bar --extra-vars '{}' ").format(
#         n,
#         vars_params)
#
#     tasks.append(cmd)
# breakout end

# breakout_valotility
for bw in range(15, 46, 1):
    for atrlen in range(5, 51, 1):
        for malen in range(1, 26, 1):
            extra_vars = {
                "malen": malen,
                "atrlen": atrlen,
                "bw": bw / 10.0
            }
            vars_params = json.dumps(extra_vars).encode("utf-8").decode("utf-8")

            cmd = ("rqalpha run -fq 1d -f breakout_volatility.py --start-date 2010-01-01 --end-date 2016-12-31 "
                   "-o results/breakout_volatility/510050_20100101_20161231/bw{}-atrlen{}-malen{}.pkl "
                   "-sc 100000 -bm 000300.XSHG -me next_bar --extra-vars '{}' ").format(
                       bw, atrlen, malen,
                       vars_params)

            tasks.append(cmd)
# breakout_valotility end


def run_bt(cmd):
    print(cmd)
    os.system(cmd)


with concurrent.futures.ProcessPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
    for task in tasks:
        executor.submit(run_bt, task)