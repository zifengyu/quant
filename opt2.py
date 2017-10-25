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
#         if lp > sp:
#             avg_type = 3
#             model_type = 4
#             extra_vars = {
#                 "avg_type": avg_type,
#                 "model_type": model_type,
#                 "short_period": sp,
#                 "long_period": lp,
#             }
#             vars_params = json.dumps(extra_vars).encode("utf-8").decode("utf-8")
#
#             root_folder = os.path.join('results',
#                                        'moving_average_atype{}_mtype{}'.format(avg_type, model_type),
#                                        '510050_20100101_20161231')
#
#             if not os.path.exists(root_folder):
#                 os.makedirs(root_folder)
#
#             cmd = ("rqalpha run -fq 1d -f moving_average.py --start-date 2010-01-01 --end-date 2016-12-31 "
#                    "-o {}/atype{}-mtype{}-short{}-long{}.pkl "
#                    "-sc 100000 -bm 000300.XSHG -me next_bar --extra-vars '{}' ").format(
#                 root_folder, avg_type, model_type, sp, lp,
#                 vars_params)
#
#             tasks.append(cmd)
# moving_average end

# moving_average slope
# for sp in range(3, 41, 1):
#     avg_type = 3
#     model_type = 2
#     extra_vars = {
#         "avg_type": avg_type,
#         "model_type": model_type,
#         "short_period": sp
#     }
#     vars_params = json.dumps(extra_vars).encode("utf-8").decode("utf-8")
#
#     root_folder = os.path.join('results',
#                                'moving_average_atype{}_mtype{}'.format(avg_type, model_type),
#                                '510050_20100101_20161231')
#
#     if not os.path.exists(root_folder):
#         os.makedirs(root_folder)
#
#     cmd = ("rqalpha run -fq 1d -f moving_average.py --start-date 2010-01-01 --end-date 2016-12-31 "
#            "-o {}/atype{}-mtype{}-short{}.pkl "
#            "-sc 100000 -bm 000300.XSHG -me next_bar --extra-vars '{}' ").format(
#         root_folder, avg_type, model_type, sp,
#         vars_params)
#
#     tasks.append(cmd)
# moving_average slope end

# oscillator: stochastic
# for len1 in range(5, 26, 1):
#     osc_type = 2
#     model_type = 2
#     extra_vars = {
#         "osc_type": osc_type,
#         "model_type": model_type,
#         "len1": len1,
#     }
#     vars_params = json.dumps(extra_vars).encode("utf-8").decode("utf-8")
#
#     root_folder = os.path.join('results',
#                                'oscillator_otype{}_mtype{}'.format(osc_type, model_type),
#                                '510050_20100101_20161231')
#
#     if not os.path.exists(root_folder):
#         os.makedirs(root_folder)
#
#     cmd = ("rqalpha run -fq 1d -f oscillator.py --start-date 2010-01-01 --end-date 2016-12-31 "
#            "-o {}/otype_{}-mtype_{}-len1_{}.pkl "
#            "-sc 100000 -bm 000300.XSHG -me next_bar --extra-vars '{}' ").format(
#         root_folder, osc_type, model_type, len1,
#         vars_params)
#
#     tasks.append(cmd)

# oscillator: MACD
# for len1 in range(3, 16, 2):
#     for len2 in range(10, 41, 5):
#         if len1 < len2:
#             osc_type = 4
#             model_type = 2
#             extra_vars = {
#                 "osc_type": osc_type,
#                 "model_type": model_type,
#                 "len1": len1,
#                 "len2": len2
#             }
#             vars_params = json.dumps(extra_vars).encode("utf-8").decode("utf-8")
#
#             root_folder = os.path.join('results',
#                                        'oscillator_otype{}_mtype{}'.format(osc_type, model_type),
#                                        '510050_20100101_20161231')
#
#             if not os.path.exists(root_folder):
#                 os.makedirs(root_folder)
#
#             cmd = ("rqalpha run -fq 1d -f oscillator.py --start-date 2010-01-01 --end-date 2016-12-31 "
#                    "-o {}/otype_{}-mtype_{}-len1_{}-len2_{}.pkl "
#                    "-sc 100000 -bm 000300.XSHG -me next_bar --extra-vars '{}' ").format(
#                 root_folder, osc_type, model_type, len1, len2,
#                 vars_params)
#
#             tasks.append(cmd)

# oscillator: Divergence
# for len1 in range(5, 26, 1):
#     for len3 in range(15, 26, 5):
#         osc_type = 3
#         model_type = 3
#         extra_vars = {
#             "osc_type": osc_type,
#             "model_type": model_type,
#             "len1": len1,
#             "len3": len3
#         }
#         vars_params = json.dumps(extra_vars).encode("utf-8").decode("utf-8")
#
#         root_folder = os.path.join('results',
#                                    'oscillator_otype{}_mtype{}'.format(osc_type, model_type),
#                                    '510050_20100101_20161231')
#
#         if not os.path.exists(root_folder):
#             os.makedirs(root_folder)
#
#         cmd = ("rqalpha run -fq 1d -f oscillator.py --start-date 2010-01-01 --end-date 2016-12-31 "
#                "-o {}/otype_{}-mtype_{}-len1_{}-len3_{}.pkl "
#                "-sc 100000 -bm 000300.XSHG -me next_bar --extra-vars '{}' ").format(
#             root_folder, osc_type, model_type, len1, len3,
#             vars_params)
#
#         tasks.append(cmd)

# oscillator: Divergence MACD
# for len1 in range(3, 16, 2):
#     for len2 in range(10, 41, 5):
#         if len1 < len2:
#             for len3 in range(15, 26, 5):
#                 osc_type = 4
#                 model_type = 3
#                 extra_vars = {
#                     "osc_type": osc_type,
#                     "model_type": model_type,
#                     "len1": len1,
#                     "len2": len2,
#                     "len3": len3
#                 }
#                 vars_params = json.dumps(extra_vars).encode("utf-8").decode("utf-8")
#
#                 root_folder = os.path.join('results',
#                                            'oscillator_otype{}_mtype{}'.format(osc_type, model_type),
#                                            '510050_20100101_20161231')
#
#                 if not os.path.exists(root_folder):
#                     os.makedirs(root_folder)
#
#                 cmd = ("rqalpha run -fq 1d -f oscillator.py --start-date 2010-01-01 --end-date 2016-12-31 "
#                        "-o {}/otype_{}-mtype_{}-len1_{}-len2_{}-len3_{}.pkl "
#                        "-sc 100000 -bm 000300.XSHG -me next_bar --extra-vars '{}' ").format(
#                     root_folder, osc_type, model_type, len1, len2, len3,
#                     vars_params)
#
#                 tasks.append(cmd)

# standard exit
for mmstp in range(5, 36, 5):
    for ptlim in range(5, 51, 5):
        extra_vars = {
            "ptlim": ptlim / 10.0,
            "mmstp": mmstp / 10.0
        }
        vars_params = json.dumps(extra_vars).encode("utf-8").decode("utf-8")

        root_folder = os.path.join('results',
                                   'standard_exit_strategy',
                                   '510050_20100101_20161231')

        if not os.path.exists(root_folder):
            os.makedirs(root_folder)

        cmd = ("rqalpha run -fq 1d -f models/standard_exit_strategy.py --start-date 2010-01-01 --end-date 2016-12-31 "
               "-o {}/mmstp_{}_ptlim_{}.pkl "
               "-sc 100000 -bm 000300.XSHG -me next_bar --extra-vars '{}' ").format(
            root_folder, mmstp / 10.0, ptlim / 10.0,
            vars_params)

        tasks.append(cmd)


def run_bt(cmd):
    print(cmd)
    os.system(cmd)


with concurrent.futures.ProcessPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
    for task in tasks:
        executor.submit(run_bt, task)
