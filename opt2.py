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

# breakout_hhll
# for n in range(5, 101, 5):
#     extra_vars = {
#         "n": n
#     }
#     vars_params = json.dumps(extra_vars).encode("utf-8").decode("utf-8")
#
#     cmd = ("rqalpha run -fq 1d -f breakout_hhll.py --start-date 2010-01-01 --end-date 2016-12-31 "
#            "-o results/breakout_hhll/510050_20100101_20161231/n{}.pkl -sc 100000 -bm 000300.XSHG "
#            "-me next_bar --extra-vars '{}' ").format(
#         n,
#         vars_params)
#
#     tasks.append(cmd)
# breakout_hhll end

# breakout_valotility
# for bw in range(15, 46, 1):
#     for atrlen in range(5, 51, 1):
#         for malen in range(1, 26, 1):
#             extra_vars = {
#                 "malen": malen,
#                 "atrlen": atrlen,
#                 "bw": bw / 10.0
#             }
#             vars_params = json.dumps(extra_vars).encode("utf-8").decode("utf-8")
#
#             cmd = ("rqalpha run -fq 1d -f breakout_volatility.py --start-date 2010-01-01 --end-date 2016-12-31 "
#                    "-o results/breakout_volatility/510050_20100101_20161231/bw{}-atrlen{}-malen{}.pkl "
#                    "-sc 100000 -bm 000300.XSHG -me next_bar --extra-vars '{}' ").format(
#                        bw, atrlen, malen,
#                        vars_params)
#
#             tasks.append(cmd)
# breakout_volatility end

# breakout_volatility_adx
# for bw in range(15, 46, 1):
#     for atrlen in range(5, 51, 1):
#         for malen in range(1, 26, 1):
#             extra_vars = {
#                 "malen": malen,
#                 "atrlen": atrlen,
#                 "bw": bw / 10.0
#             }
#             vars_params = json.dumps(extra_vars).encode("utf-8").decode("utf-8")
#
#             cmd = ("rqalpha run -fq 1d -f breakout_volatility_adx.py --start-date 2010-01-01 --end-date 2016-12-31 "
#                    "-o results/breakout_volatility_adx/510050_20100101_20161231/bw{}-atrlen{}-malen{}.pkl "
#                    "-sc 100000 -bm 000300.XSHG -me next_bar --extra-vars '{}' ").format(
#                        bw, atrlen, malen,
#                        vars_params)
#
#             tasks.append(cmd)
# breakout_volatility_adx end

# moving_average
# for sp in range(1, 6, 1):
#     for lp in range(5, 51, 5):
#         avg_type = 3
#         model_type = 1
#         extra_vars = {
#             "avg_type": avg_type,
#             "model_type": model_type,
#             "short_period": sp,
#             "long_period": lp,
#         }
#         vars_params = json.dumps(extra_vars).encode("utf-8").decode("utf-8")
#
#         root_folder = os.path.join('results',
#                                    'moving_average_atype{}_mtype{}'.format(avg_type, model_type),
#                                    '510050_20100101_20161231')
#
#         if not os.path.exists(root_folder):
#             os.makedirs(root_folder)
#
#         cmd = ("rqalpha run -fq 1d -f moving_average.py --start-date 2010-01-01 --end-date 2016-12-31 "
#                "-o {}/atype{}-mtype{}-short{}-long{}.pkl "
#                "-sc 100000 -bm 000300.XSHG -me next_bar --extra-vars '{}' ").format(
#             root_folder, avg_type, model_type, sp, lp,
#             vars_params)
#
#         tasks.append(cmd)
# moving_average end

# moving_average slope
for sp in range(3, 41, 1):
    avg_type = 3
    model_type = 2
    extra_vars = {
        "avg_type": avg_type,
        "model_type": model_type,
        "short_period": sp
    }
    vars_params = json.dumps(extra_vars).encode("utf-8").decode("utf-8")

    root_folder = os.path.join('results',
                               'moving_average_atype{}_mtype{}'.format(avg_type, model_type),
                               '510050_20100101_20161231')

    if not os.path.exists(root_folder):
        os.makedirs(root_folder)

    cmd = ("rqalpha run -fq 1d -f moving_average.py --start-date 2010-01-01 --end-date 2016-12-31 "
           "-o {}/atype{}-mtype{}-short{}.pkl "
           "-sc 100000 -bm 000300.XSHG -me next_bar --extra-vars '{}' ").format(
        root_folder, avg_type, model_type, sp,
        vars_params)

    tasks.append(cmd)
# moving_average slope end


def run_bt(cmd):
    print(cmd)
    os.system(cmd)


with concurrent.futures.ProcessPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
    for task in tasks:
        executor.submit(run_bt, task)