results = []
with open('result/breakout_volatility_510050_20100101_20161231.csv', 'r') as result_file:
    for line in result_file.readlines():
        if int(line.split()[5]) > 50:
            results.append(line.split())

sort_col = 3
results = sorted(results, key=lambda d: float(d[sort_col]))
for item in results[-100:]:
    print(item)
