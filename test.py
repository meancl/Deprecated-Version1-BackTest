import pandas as pd
import os
from typing import Tuple, Dict, List
from math import *
from pandas.core.frame import DataFrame
from pandas.core.series import Series

file_name = '2021-11-11-064260.txt'
trading_dir = './Trading/'


trading_names =['time', 'tp', 'udr', 'tv',
            'trr', 'ts', 'fs', 'fb', 'market']
trading_df = pd.read_csv(trading_dir + file_name, names=trading_names)

trading_df['tp'] = abs(trading_df['tp'])
trading_df['fb'] = abs(trading_df['fb'])
trading_df['fs'] = abs(trading_df['fs'])

t_first_line = trading_df.iloc[0]

t_tick_move_list = []
t_moved_list = []
t_price_gap_list = []
t_volume_list = []
t_before_one_step = 0
t_before_one_step_orientation = 0
t_before_two_step = 0
t_before_two_step_orientation = 0
t_before_three_step = 0
t_before_three_step_orientation = 0
t_prev_price = t_first_line['tp']
t_short_trading_strength = []
t_short_trading_strength_list = []

for idx in range(trading_df.shape[0]):
    t_df= trading_df.iloc[idx]
    
    t_moved_signal = False

    ########################### 주가변동속도와 방향을 알기위한 섹터오픈 ####################################

    if  t_df['tp'] != t_prev_price:
        t_before_three_step = t_before_two_step
        t_before_three_step_orientation = t_before_two_step_orientation
        t_before_two_step = t_before_one_step
        t_before_two_step_orientation = t_before_one_step_orientation
        t_before_one_step = idx
        t_before_one_step_orientation = t_df['tp'] - t_prev_price
        t_prev_price = t_df['tp']
        t_moved_signal = True
    else :
        t_moved_signal =False

    t_staying_tick = idx - t_before_one_step + 1 

    t_trading_diff = t_df['tp'] - t_df['fs']

    #########단기체결강도(최근10번의 체결에서의 양으로 계산) 구하기#################
    if len(t_short_trading_strength) >= 10:
        t_short_trading_strength.pop(0)

    if t_trading_diff < 0: # 최우선매수호가에 매도함
        t_trading_record = [True, t_df['tv']]
    else : # 최우선매도호가에 매수함 
        t_trading_record = [False, t_df['tv']]

    t_short_trading_strength.append(t_trading_record)
    

    sell_sum = 1
    buy_sum = 1
    for a_list in t_short_trading_strength: 
        if a_list[0] :
            sell_sum += a_list[1]
        else :
            buy_sum += a_list[1]
    
    

    ##########################################

    t_short_trading_strength_list.append(round((sell_sum/buy_sum),4) * 100)
    t_volume_list.append([t_df['time'], t_df['tv']])
    t_price_gap_list.append([t_df['time'], t_trading_diff]) #체결가와 최우선매도호가의 차
    t_tick_move_list.append([ t_df['time'], t_staying_tick, t_before_one_step_orientation,
                         t_before_one_step - t_before_two_step , t_before_two_step_orientation,
                         t_before_two_step - t_before_three_step, t_before_three_step_orientation
                          ])
    t_moved_list.append(t_moved_signal)



def find_inclination_and_variance(segment:list) -> Tuple[int]:
    """
    tick_move_list의 sub리스트를 받아서
    변동률과 기울기를 반환한다.
    반환받은 값은 get_kosdaq_gap값을 나눠주면 좋다.
    """
    seg_len = len(segment)
    front_variance = abs(segment[0][6]) # 6: third_orientation 4: second_orientation 2: first_orientation
    inclination = segment[0][6]
    check_val = segment[0][1] # 1 : stayting_tick
    last_signal = False
    count = 3
    for idx in range(1, seg_len):

        s = segment[idx]
        last_signal = (s[1] - check_val)!= 1
        if last_signal :
            check_val = s[1]
            front_variance += abs(s[6])
            inclination += s[6]
            count += 1
        else:
            check_val += 1
            
    if not last_signal: # 마지막에 third_orientation을 못넣었다면
        front_variance += abs(s[6])
        inclination += s[6]

    front_variance += abs(s[4]) + abs(s[2])
    inclination += s[4] + s[2]

    return front_variance, inclination
