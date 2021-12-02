from numpy import true_divide
import pandas as pd
import os
from typing import Tuple, Dict, List
from math import *
from pandas.core.frame import DataFrame
from pandas.core.series import Series
import time
import matplotlib.pyplot as plt
from math import *

file_name = '2021-11-12-206560.txt'

trading_dir = 'F:/Trading/'
score_dir = 'F:/Score/'
ta_dir = 'F:/TA/'


trading_names =['time', 'tp', 'udr', 'tv',
            'trr', 'ts', 'fs', 'fb', 'market']
trading_df = pd.read_csv(trading_dir + file_name, names=trading_names)

trading_df['fs'] = abs(trading_df['fs'])
trading_df['fb'] = abs(trading_df['fb'])
trading_df['tp'] = abs(trading_df['tp'])


def get_kosdaq_gap(item1:int) -> int:
    """ item1의 상향폭을 반환한다 """
    gap = 0
    
    if item1 < 1000: 
        gap =1 
    elif item1 < 5000:
        gap = 5
    elif item1 < 10000: 
        gap = 10
    elif item1 < 50000:
        gap = 50
    else :
        gap = 100
    
    return gap

def check_missing_exist(b1:int, s1:int) -> Tuple[bool, int]:
    """ 매수호가1과 매도호가1의 가격 차이가 매수호가1의 상향폭보다 높은경우
    가운데가 비어있음을 알리는 boolean과 차이폭이 어느정도인 지를 나타내는 int를 반환한다
    
    """
    if b1 ==0 or s1 == 0:
        diff = 0
        gap = 1   
    else:
        diff = s1 - b1
        gap = get_kosdaq_gap(b1)
    return diff >= gap, diff 

def operate_xor(bool1:bool, bool2:bool) -> bool:
    return (bool1 and not bool2) or (not bool1 and bool2)

def s(a):
    return str(a)


num_between_tick = 16
small_jar_size = 60

small_jar_list = []
small_jar_buy_score = 0
small_jar_sell_score = 0


volume_list = []
time_list = []
variation_list = []
ts_list =[]
price_list= []
fs_list = []

sf = open(score_dir+file_name, 'w')
jar_score = 0
cur_score = 0
short_jar_score = 0
cur_score_list = []


total_variation = 0
mean_variation = 0
rough_time_speed = 0
time_speed_check_idx = 0
time_accum_idx = 1
prev_time = trading_df['time'].iat[0]

accum_tv = 0

# 반복문 시작 #
for idx in range(trading_df.shape[0]):

    line = trading_df.iloc[idx]
    fs = line['fs']
    fb = line['fb']
    tt = line['time']
    tp = line['tp']
    tv = line['tv']
    ts = line['ts']

    if fs == 0 or fb == 0 or ts ==0:
        continue

    #########################시간 측정##########################
    if tt == prev_time:
        time_speed_check_idx += 1

    else :
        time_accum_idx += 1
        rough_time_speed = (rough_time_speed + time_speed_check_idx) /2
        prev_time = tt
        time_speed_check_idx = 1

    if time_speed_check_idx > 6:
        rough_time_speed = (rough_time_speed + time_speed_check_idx) /2

    #####################################################


    if len(volume_list) >= num_between_tick:
        volume_list.pop(0)
        fs_list.pop(0)
        ts_list.pop(0)
        
        short_jar_score -= cur_score_list.pop(0)
    
    fs_list.append(fs) 
    ts_list.append(ts)
    

    fs_gap = get_kosdaq_gap(fs)
    fb_gap = get_kosdaq_gap(fb)
    
    volume_list.append(tv)
    accum_tv += abs(tv)

    buy_sum = 0
    sell_sum = 0
    buy_cnt= 0
    volume_rate=0
    volume_cnt_rate=0
    time_gap = 0
    inclination = 0
    variation = 0
    volume_over_weight =1 

    if len(volume_list) >= num_between_tick:
        
        for i in volume_list:
            if i > 0 :
                buy_sum += i
                buy_cnt += 1
            else :
                sell_sum -= i
       

        mean_volume = accum_tv / (idx + 1)
        volume_diff = buy_sum  - sell_sum
        volume_sum = buy_sum  + sell_sum 
        volume_rate = 0
        mul_symbol = 1
        numerator_cnt = buy_cnt
        numerator = 0
        denominator = 1

        if volume_sum < mean_volume:
            volume_rate = 0
        else :
            if volume_diff > 0 :
                numerator = buy_sum
                denominator = (sell_sum if sell_sum != 0 else 1)
            else :
                numerator = sell_sum
                denominator =  (buy_sum if buy_sum != 0 else 1)
                mul_symbol = -1
                numerator_cnt = num_between_tick - buy_cnt

        numerator = 1 if numerator ==0 else numerator
        volume_rate = (numerator - denominator)/ numerator 
        # volume_rate = volume_rate * ( denominator / volume_sum)
        # volume_over_weight  = ( numerator - denominator )/ 1000 
        # volume_over_weight = log10(1+volume_over_weight)

        # volume_rate *= volume_rate
        # #volume_over_weight = 10 if volume_over_weight > 10 else volume_over_weight
        volume_rate *= mul_symbol
        volume_cnt_rate = numerator_cnt / num_between_tick  
        # volume_cnt_rate *= volume_cnt_rate
        time_gap = tt - time_list.pop(0)
    

    _, diff = check_missing_exist(fs,fb)
    time_list.append(tt)

#############################################################################################################################
    
    fs_flow = 0
    ts_move = 0
    volume_score = 0
    ts_flow = 0
    volume_mul_weight =1
    mean_volume = 1
    if len(fs_list) >= num_between_tick:
        fs_flow =  fs*7 - (fs_list[num_between_tick-2] + fs_list[num_between_tick-4] + fs_list[num_between_tick-6] + fs_list[num_between_tick-8] + fs_list[num_between_tick-10] + fs_list[num_between_tick-12] + fs_list[num_between_tick-14]) 
        fs_flow = round(fs_flow /(7 * fs_gap) , 2)
        # ts_move = ts* 5 - (ts_list[num_between_tick-5] +ts_list[num_between_tick-8] +ts_list[num_between_tick-10] +ts_list[num_between_tick-12] +ts_list[num_between_tick-15] )
        # ts_move = round(ts_move/5 ,2 )

        # if ts_move > 0.35:
        #     ts_move =0.35
        # elif ts_move <-0.35:
        #     ts_move = -0.35

        ts_ = 200 if ts> 200 else ts
        ts_flow = (1.005 ** abs(ts_-100))
        ts_flow = round(ts_flow,2)
        
        volume_score = volume_rate * volume_cnt_rate
        volume_mul_weight = ( ts_flow if ( volume_score > 0 and ts> 100 ) or( volume_score < 0 and ts < 100 ) else 1)
        volume_score = round(volume_score, 2)



    cur_score = volume_score * volume_mul_weight  
    time_speed_per_sec = (idx+1) / time_accum_idx
    time_speed_per_sec = round(time_speed_per_sec,2)
    short_jar_score += cur_score
    cur_score_list.append(cur_score)
    jar_score += cur_score
    if len(small_jar_list) > small_jar_size:
        popped = small_jar_list.pop(0)
        if popped > 0:
            small_jar_buy_score -= popped
        else:
            small_jar_sell_score += popped

    small_jar_list.append(cur_score)

    if cur_score > 0:
        small_jar_buy_score += cur_score
    else:
        small_jar_sell_score -= cur_score
    

    sf.writelines([s(tt),'\t',s(time_speed_per_sec), '\t',  s(fs),'\t',  s(ts),'\t\t',
     s(round(volume_rate,2)),'\t',s(round(volume_cnt_rate,2)),'\t',
     s(round(volume_mul_weight,2)),'\t\t',
     s(round(cur_score,3)),'\t\t',
     s(round(small_jar_buy_score,2)),'\t',s(round(small_jar_sell_score,2)),'\t\t',
       s(round(jar_score,2)),'\n'])

    cur_score = 0

    



    
    







