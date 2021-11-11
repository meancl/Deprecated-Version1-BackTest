import pandas as pd
import os
from typing import Tuple, Dict, List

from pandas.core.frame import DataFrame
from pandas.core.series import Series

file_name = '2021-11-10-086980.txt'
hoga_dir = './Hoga/'
trading_dir = './Trading/'

hoga_names = ['time', 'b10', 'bv10', 'b9', 'bv9', 'b8', 'bv8', 'b7', 'bv7', 'b6', 'bv6',
            'b5', 'bv5', 'b4', 'bv4', 'b3', 'bv3', 'b2', 'bv2', 'b1', 'bv1',
            's1', 'sv1', 's2', 'sv2', 's3', 'sv3', 's4', 'sv4', 's5', 'sv5', 's6', 'sv6',
            's7', 'sv7', 's8', 'sv8', 's9', 'sv9', 's10', 'sv10', 
            'sav', 'savd', 'bav', 'bavd', 'pbv', 'br', 'sr']
hoga_df = pd.read_csv(hoga_dir + file_name, names=hoga_names)

trading_names =['time', 'cv', 'acv', 'cs', 'group'] 
trading_df = pd.read_csv(trading_dir + file_name, names=trading_names)

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
    diff = s1 - b1
    gap = get_kosdaq_gap(b1)
    return diff > gap, diff 

    

def check_movement_per_tick(price_series:Series) -> Series:
    """ 한 틱이전과 지금이 가격변화가 있느냐를 bool로 나타내는 리스트를 반환한다.
    """
    tick_before = price_series.shift(1)
    diff = price_series- tick_before
    diff.iat[0] = 0
    
    return diff != 0
    

def get_change_list(time_series:Series)-> List[int]:
    """ tick이 아닌 시간이 바꼇을 때의 인덱스를 리스트화하여 반환한다.
    """
    prev = time_series.iat[0]
    change_list = [0] 
    idx = 0
    for f in time_series:
        if (f - prev) > 0 :
            change_list.append(idx)
            prev = f
        idx += 1 
    return change_list

trading_change_list = get_change_list(trading_df['time'])
hoga_change_list = get_change_list(hoga_df['time'])

now = hoga_df['time'].iat[0]

hoga_tracking = 0
trading_tracking = 0


# for row in hoga_df.values:
#     # 2021-11-11부터는 19와 21위치 스위치 해야함
#     tup = check_missing_exist(row[19],row[21])
#     if tup[0]:
#         print(row[0],' gap error : ', tup[1])

