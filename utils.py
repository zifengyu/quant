def cal_maxdrawdown(values):
    mdd = 0
    for i in range(len(values)):
        pm = values[:i].max()
        cv = values[i]
        if pm - cv > mdd:
            mdd = pm - cv
    return mdd


def cal_reward_to_risk(values):
    mdd = cal_maxdrawdown(values)
    return (values[-1] - values[0]) / cal_maxdrawdown(values) if mdd > 0 else 0
