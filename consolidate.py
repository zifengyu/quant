import pickle
import os
import utils

strategy = 'moving_average_atype2_mtype2'
meta = '510050_20100101_20161231'

root_folder = os.path.join('results', strategy, meta)

with open('{}_{}.csv'.format(strategy, meta), 'w') as rf:
    for file_name in os.listdir(root_folder):
        result_dict = pickle.load(open(os.path.join(root_folder, file_name), "rb"))

        total_value = result_dict['portfolio']['total_value']
        rrr = utils.cal_reward_to_risk(total_value)

        rf.write('{},{},{},{}\n'.format(
            file_name[:file_name.find('.')],
            rrr,
            total_value[-1] - total_value[0],
            int(len(result_dict['trades']) / 2)
        ))
