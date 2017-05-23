import os
import time
from subprocess import call


for bw in range(15, 46, 1):
    for atrlen in range(5, 51, 1):
        for malen in range(1, 26, 1):
            os.environ['bw'] = str(bw / 10)
            os.environ['atrlen'] = str(atrlen)
            os.environ['malen'] = str(malen)
            start_time = time.time()
            call(["python", "run.py"])
            print('time: ', time.time() - start_time)
