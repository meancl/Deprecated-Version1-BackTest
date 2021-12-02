from numpy import true_divide
import pandas as pd
import os
from typing import Tuple, Dict, List
from math import *
from pandas.core.frame import DataFrame
from pandas.core.series import Series
import time
from math import *

read_dir = 'F:/Trading/'
write_dir = 'F:/TA_PLUS_ALPHA/'
write_prefix ='full'
def get_gap(item1:int) -> int:
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



cFiles = os.listdir(read_dir)

for file_name in cFiles:

    trading_names =['time', 'tp', 'udr', 'tv',
            'trr', 'ts', 'fs', 'fb', 'market']
    trading_df = pd.read_csv(read_dir + file_name, names=trading_names)

    if trading_df.empty:
        print(file_name ,'is empty')
        continue

    trading_df['fb'] = abs(trading_df['fb'])
    trading_df['tp'] = abs(trading_df['tp'])
    trading_df['fs'] = abs(trading_df['fs'])  
    
    trading_df['pc'] = 0
    trading_df['mc'] = 0

    trading_df['apv'] = 0
    trading_df['amv'] = 0 

    trading_df['pvb15t'] = 0
    trading_df['mvb15t'] = 0
    trading_df['pvb40t'] = 0
    trading_df['mvb40t'] = 0
    trading_df['pvb60t'] = 0
    trading_df['mvb60t'] = 0
    trading_df['pvb100t'] = 0
    trading_df['mvb100t'] = 0
    trading_df['pvb300t'] = 0
    trading_df['mvb300t'] = 0

    trading_df['cur_loc'] = 0 
    trading_df['speed'] = 0

    
    prev_plus_count =  0
    prev_minus_count = 0
    
    accum_plus_volume = 0
    accum_minus_volume = 0

    time_idx = 1 
    

    prev_fs = trading_df['fs'].iat[0]
    cur_loc = 0
    prev_time = trading_df['time'].iat[0]
    time_count = 0
    time_list = []

    # 반복문 시작 #
    for idx in range(trading_df.shape[0]):
        
        mean_speed = 0
        time_count += 1
        standard_gap = get_gap(trading_df['fs'].iat[idx])

        if trading_df['time'].iat[idx] != prev_time:
            time_list.append(time_count)
            time_count = 0
            prev_time = trading_df['time'].iat[idx]

        if len(time_list) > 5:
            time_list.pop(0)

        len_time_list = len(time_list)
        mean_speed = sum(time_list) / ( 1 if len_time_list == 0 else len_time_list)
        mean_speed = round(mean_speed,1)
        trading_df['speed'].iat[idx] = mean_speed

        if prev_fs != trading_df['fs'].iat[idx]:
            diff = round(((trading_df['fs'].iat[idx] - prev_fs) / standard_gap),1)
            cur_loc += diff
            prev_fs = trading_df['fs'].iat[idx]
        
        trading_df['cur_loc'].iat[idx] = cur_loc

        
        if trading_df['tv'].iloc[idx] > 0 :
            prev_plus_count += 1
            accum_plus_volume += trading_df['tv'].iat[idx]
            trading_df['pc'].iat[idx] = prev_plus_count 
            
        else:
            prev_minus_count += 1
            accum_minus_volume -= trading_df['tv'].iat[idx]
            trading_df['mc'].iat[idx] = prev_minus_count
            
    
        trading_df['apv'].iat[idx] = accum_plus_volume
        trading_df['amv'].iat[idx] = accum_minus_volume

        if idx >= 15 :
            trading_df['pvb15t'].iat[idx] = round((trading_df['apv'].iat[idx] - trading_df['apv'].iat[idx - 15])/standard_gap , 2)
            trading_df['mvb15t'].iat[idx] =round((trading_df['amv'].iat[idx] - trading_df['amv'].iat[idx - 15])/standard_gap , 2)
           
        if idx >= 40 :
            trading_df['pvb40t'].iat[idx] = round((trading_df['apv'].iat[idx] - trading_df['apv'].iat[idx - 40])/standard_gap , 2)
            trading_df['mvb40t'].iat[idx] =round((trading_df['amv'].iat[idx] - trading_df['amv'].iat[idx - 40])/standard_gap , 2)
           
        if idx >= 60 :
            trading_df['pvb60t'].iat[idx] = round((trading_df['apv'].iat[idx] - trading_df['apv'].iat[idx - 60])/standard_gap , 2)
            trading_df['mvb60t'].iat[idx] =round((trading_df['amv'].iat[idx] - trading_df['amv'].iat[idx - 60])/standard_gap , 2)
            
        if idx >= 100 :
            trading_df['pvb100t'].iat[idx] = round((trading_df['apv'].iat[idx] - trading_df['apv'].iat[idx - 100])/standard_gap , 2)
            trading_df['mvb100t'].iat[idx] =round((trading_df['amv'].iat[idx] - trading_df['amv'].iat[idx - 100])/standard_gap , 2)
            
        if idx >= 300 :
            trading_df['pvb300t'].iat[idx] = round((trading_df['apv'].iat[idx] - trading_df['apv'].iat[idx - 300])/standard_gap , 2)
            trading_df['mvb300t'].iat[idx] =round((trading_df['amv'].iat[idx] - trading_df['amv'].iat[idx - 300])/standard_gap , 2)
            
         
    trading_df.to_csv(write_dir+write_prefix+file_name, sep ='\t')
    



    
    







