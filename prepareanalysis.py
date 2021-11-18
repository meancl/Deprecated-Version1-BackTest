import pandas as pd
import os
from typing import Tuple, Dict, List
from math import *
from pandas.core.frame import DataFrame
from pandas.core.series import Series

import matplotlib.pyplot as plt


file_name = '2021-11-12-013310.txt'
hoga_dir = 'F:/Hoga/'
trading_dir = './Trading/'

hoga_names = ['time', 's10', 'sv10', 's9', 'sv9', 's8', 'sv8', 's7', 'sv7', 's6', 'sv6',
            's5', 'sv5', 's4', 'sv4', 's3', 'sv3', 's2', 'sv2', 's1', 'sv1',
            'b1', 'bv1', 'b2', 'bv2', 'b3', 'bv3', 'b4', 'bv4', 'b5', 'bv5', 'b6', 'bv6',
            'b7', 'bv7', 'b8', 'bv8', 'b9', 'bv9', 'b10', 'bv10', 
            'sav', 'savd', 'bav', 'bavd', 'pbv', 'br', 'sr']

hoga_df = pd.read_csv(hoga_dir + file_name, names=hoga_names)

hoga_df['s10'] = abs(hoga_df['s10'])
hoga_df['s9'] = abs(hoga_df['s9'])
hoga_df['s8'] = abs(hoga_df['s8'])
hoga_df['s7'] = abs(hoga_df['s7'])
hoga_df['s6'] = abs(hoga_df['s6'])
hoga_df['s5'] = abs(hoga_df['s5'])
hoga_df['s4'] = abs(hoga_df['s4'])
hoga_df['s3'] = abs(hoga_df['s3'])
hoga_df['s2'] = abs(hoga_df['s2'])
hoga_df['s1'] = abs(hoga_df['s1'])

hoga_df['b1'] = abs(hoga_df['b1'])
hoga_df['b2'] = abs(hoga_df['b2'])
hoga_df['b3'] = abs(hoga_df['b3'])
hoga_df['b4'] = abs(hoga_df['b4'])
hoga_df['b5'] = abs(hoga_df['b5'])
hoga_df['b6'] = abs(hoga_df['b6'])
hoga_df['b7'] = abs(hoga_df['b7'])
hoga_df['b8'] = abs(hoga_df['b8'])
hoga_df['b9'] = abs(hoga_df['b9'])
hoga_df['b10'] = abs(hoga_df['b10'])



hoga_df.drop(hoga_df[hoga_df['sav']==0].index, inplace=True)


plt.plot(hoga_df['time'], hoga_df['s1'])
plt.show()


trading_names =['time', 'tp', 'udr', 'ta',
            'trr', 'ts', 'fs', 'fb', 'market']
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
    
# for row in hoga_df.values:
#     # 2021-11-11부터는 19와 21위치 스위치 해야함
#     tup = check_missing_exist(row[19],row[21])
#     if tup[0]:
#         print(row[0],' gap error : ', tup[1])
    """
    diff = s1 - b1
    gap = get_kosdaq_gap(b1)
    return diff > gap, diff 

    

# def check_movement_per_tick(price_series:Series) -> Series:
#     """ 한 틱이전과 지금이 가격변화가 있느냐를 bool로 나타내는 리스트를 반환한다.
#     """
#     tick_before = price_series.shift(1)
#     diff = price_series- tick_before
#     diff.iat[0] = 0
    
#     return diff != 0
    

# def get_change_list(series:Series,first_replace:int=0)-> List[int]:
#     """ tick이 아닌 시간이 바꼇을 때의 인덱스를 리스트화하여 반환한다.
#     """
#     prev = series.iat[0]
#     change_list = [first_replace] 
#     idx = 0
#     for f in series:
#         if (f - prev) != 0 :
#             change_list.append(idx)
#             prev = f
#         idx += 1 
#     return change_list

# def plus_time(time_to_add:int ,adding:int= 1) -> int:
#     """ 키움time 데이터에 adding만큼 더해준 후 키움time형으로 반환해줌"""
#     second = time_to_add % 100
#     minute = int(time_to_add / 100) % 100
#     hour = int(time_to_add/ 10000)
#     if second >= 59 and minute >= 59:
#         second = 0  
#         minute = 0
#         hour += 1
#     elif second >= 59 :
#         second = 0
#         minute += 1
#     else:
#         second += 1

#     return hour * 10000 + minute* 100 + second
    
# def minus_time(time_to_minus:int , minus:int=1) -> int:
#     """ 키움time데이터에 minus만큼 차감해준 후 키움time형으로 반환해줌"""
#     second = time_to_minus % 100
#     minute = int(time_to_minus/100) % 100
#     hour = int(time_to_minus/10000)
#     if second == 0 and minute == 0 :
#         hour -= 1
#         minute = 59
#         second = 59
#     elif second == 0 :
#         minute -= 1
#         second = 59
#     else :
#         second -= 1
#     return hour * 10000 + minute * 100 + second

# def sub_time_to_time(time_to_be_sub:int, time_to_sub:int) -> int:
#     """
#     키움 time형은 시간을 int로 표현하기에
#     int 간 차감연산을 지원하는 함수 
#     """
#     diff = time_to_be_sub - time_to_sub
#     second = diff % 100
#     minute = int(diff/100) % 100
#     hour = int(diff/10000)

#     second_to_be_sub = time_to_be_sub % 100
#     second_to_sub = time_to_sub % 100
    
#     minute_to_be_sub = int(time_to_be_sub/100) % 100
#     minute_to_sub = int(time_to_sub/100) % 100
    
#     if (second_to_sub - second_to_be_sub) > 0 :
#         second = second + 20
#         second %= 60
#         minute_to_sub += 1 

#     if (minute_to_sub - minute_to_be_sub) > 0:
#         minute = minute + 20
#         minute %= 60

#     return hour *10000 + minute* 100 + second


# def move_int_to_time(time:int) -> int:
#     """키움time형을 second로 구해주어 반환한다. """
#     second = time % 100
#     minute = int(time/100) % 100
#     hour = int(time/10000)
#     return second + minute*60 + hour* 3600

# trading_change_list = get_change_list(trading_df['time'])
# hoga_time_change_list = get_change_list(hoga_df['time'])


# first_line = hoga_df.iloc[0]

# ### 주가의 변동속도와 방향을 파악하기 위한 변수들  3step까지 
# tick_move_list = []
# before_one_step = 0
# before_one_step_orientation = 0
# before_two_step = 0
# before_two_step_orientation = 0
# before_three_step = 0
# before_three_step_orientation = 0
# prev_price = first_line['s1']


# ### 호가 잔량(1,2,3)을 파악하기 위한 변수들
# prev_bv1 = first_line['bv1']
# prev_bv2 = first_line['bv2']
# prev_bv3 = first_line['bv3']
# prev_sv1 = first_line['sv1']
# prev_sv2 = first_line['sv2']
# prev_sv3 = first_line['sv3']
# volume_diff_until_third = []
# volume_until_third = []
# volume_diff_relative_rate_until_third =[]  #바로 이전과 현재 차이 대 바로이전 비율, 상대적인비율
# volume_diff_absoulte_rate_until_third =[]  #바로 이전과 현재 차이 대 총매수, 매도잔량 의 비율
# volume_absoulte_rate_until_third = []  # 현재 대 총잔량의 비율
# volume_relative_rate_until_third = [] # 현재 대 이전잔량의 비율


# ### 주가가 변경됐을 인덱스마다 True 아닌경우 False로
# moved_list = []

# for idx in range(hoga_df.shape[0]):

#     df= hoga_df.iloc[idx]

#     ##############################호가(1,2,3)잔량의 움직임을 알기위한 섹터 오픈##############################
    
#     bav = df['bav']
#     sav = df['sav']
#     if bav == 0 or sav == 0:
#         bav = 5000000
#         sav = 5000000

#     diff_bv1 = df['bv1'] - prev_bv1
#     diff_bv2 = df['bv2'] - prev_bv2
#     diff_bv3 = df['bv3'] - prev_bv3
#     diff_sv1 = df['sv1'] - prev_sv1 
#     diff_sv2 = df['sv2'] - prev_sv2
#     diff_sv3 = df['sv3'] - prev_sv3  

#     relative_rate_bv1 = df['bv1'] / prev_bv1
#     relative_rate_bv2 = df['bv2'] / prev_bv2
#     relative_rate_bv3 = df['bv3'] / prev_bv3
#     relative_rate_sv1 = df['sv1'] / prev_sv1
#     relative_rate_sv2 = df['sv2'] / prev_sv2
#     relative_rate_sv3 = df['sv3'] / prev_sv3

#     absoulte_rate_bv1 = df['bv1'] / bav
#     absoulte_rate_bv2 = df['bv2'] / bav
#     absoulte_rate_bv3 = df['bv3'] / bav
#     absoulte_rate_sv1 = df['sv1'] / sav
#     absoulte_rate_sv2 = df['sv2'] / sav
#     absoulte_rate_sv3 = df['sv3'] / sav

#     relative_rate_diff_bv1 = diff_bv1 / prev_bv1
#     relative_rate_diff_bv2 = diff_bv2 / prev_bv2
#     relative_rate_diff_bv3 = diff_bv3 / prev_bv3
#     relative_rate_diff_sv1 = diff_sv1 / prev_sv1
#     relative_rate_diff_sv2 = diff_sv2 / prev_sv2
#     relative_rate_diff_sv3 = diff_sv3 / prev_sv3

#     absolute_rate_diff_bv1 = diff_bv1 / bav
#     absolute_rate_diff_bv2 = diff_bv2 / bav
#     absolute_rate_diff_bv3 = diff_bv3 / bav
#     absolute_rate_diff_sv1 = diff_sv1 / sav
#     absolute_rate_diff_sv2 = diff_sv2 / sav
#     absolute_rate_diff_sv3 = diff_sv3 / sav
    
#     prev_bv1 = df['bv1']
#     prev_bv2 = df['bv2']
#     prev_bv3 = df['bv3']
#     prev_sv1 = df['sv1']
#     prev_sv2 = df['sv2']
#     prev_sv3 = df['sv3']

#     volume_until_third.append([df['time'], df['s3'], df['s2'], df['s1'],
#                                  df['b1'], df['b2'], df['b3'] ])

#     volume_relative_rate_until_third.append([df['time'], relative_rate_sv3, relative_rate_sv2,
#                                                     relative_rate_sv1, relative_rate_bv1,
#                                                     relative_rate_bv2, relative_rate_bv3])

#     volume_diff_until_third.append([df['time'], diff_sv3, diff_sv2, diff_sv1,
#                                                 diff_bv1, diff_bv2, diff_bv3])

#     volume_absoulte_rate_until_third.append([df['time'], absoulte_rate_sv3, absoulte_rate_sv2,
#                                                     absoulte_rate_sv1, absoulte_rate_bv1,
#                                                     absoulte_rate_bv2, absoulte_rate_bv3])

#     volume_diff_relative_rate_until_third.append([df['time'], relative_rate_diff_sv3, relative_rate_diff_sv2,
#                                                     relative_rate_diff_sv1, relative_rate_diff_bv1,
#                                                     relative_rate_diff_bv2, relative_rate_diff_bv3])

#     volume_diff_absoulte_rate_until_third.append([df['time'], absolute_rate_diff_sv3, absolute_rate_diff_sv2,
#                                                     absolute_rate_diff_sv1, absolute_rate_diff_bv1,
#                                                     absolute_rate_diff_bv2, absolute_rate_diff_bv3])
    
#     ##############################호가(1,2,3)잔량의 움직임을 알기위한 섹터 종료##############################

#     moved_signal = False

#     ########################### 주가변동속도와 방향을 알기위한 섹터오픈 ####################################

#     if  df['s1'] != prev_price:

#         before_three_step = before_two_step
#         before_three_step_orientation = before_two_step_orientation
#         before_two_step = before_one_step
#         before_two_step_orientation = before_one_step_orientation
#         before_one_step = idx
#         before_one_step_orientation = df['s1'] - prev_price
#         prev_price = df['s1']
#         moved_signal = True
#     else :
#         moved_signal =False

#     staying_tick = idx - before_one_step + 1 
    


#     # 현재시간, 무변화기간, 한번전 움직임 방향,
#     # 두번전 움직임과 한번전 움직임 간 틱시간, 두번전 움직임 방향
#     # 세번전 움직임과 두번전 움직임 간 틱시간 , 세번전 움직임 방향
#     # 방향은 양수면 올랐다는거고 음수면 내려갔다는거
#     tick_move_list.append([ df['time'], staying_tick, before_one_step_orientation,
#                          before_one_step - before_two_step , before_two_step_orientation,
#                          before_two_step - before_three_step, before_three_step_orientation
#                           ])
#     moved_list.append(moved_signal)

#     ############################주가변동속도와 방향을 알기위한 섹터 종료######################################    


# ############### 잔량1,2,3 데이터프레임화 ###############
# volume_col_names = ['time', 'sv3', 'sv2', 'sv1', 'bv1', 'bv2', 'bv3']
# volume_relative_rate_until_third = pd.DataFrame(volume_relative_rate_until_third, columns=volume_col_names)
# volume_diff_until_third  = pd.DataFrame(volume_diff_until_third, columns=volume_col_names)
# volume_diff_absoulte_rate_until_third  = pd.DataFrame(volume_diff_absoulte_rate_until_third, columns=volume_col_names)
# volume_diff_relative_rate_until_third  = pd.DataFrame(volume_diff_relative_rate_until_third, columns=volume_col_names)
# volume_absoulte_rate_until_third = pd.DataFrame(volume_absoulte_rate_until_third, columns=volume_col_names)


# common_len = hoga_df.shape[0]
# prev_absoulte_rate = volume_absoulte_rate_until_third[0]
# prev_diff = volume_diff_until_third[0]
# prev_absoulte_diff_rate = volume_diff_absoulte_rate_until_third[0]
# prev_relative_diff_rate = volume_diff_relative_rate_until_third[0]
# prev_tick_move = tick_move_list[0]

# def find_inclination_and_variance(segment:list) -> Tuple[int]:
#     """
#     tick_move_list의 sub리스트를 받아서
#     변동률과 기울기를 반환한다.
#     반환받은 값은 get_kosdaq_gap값을 나눠주면 좋다.
#     """
#     seg_len = len(segment)
#     front_variance = abs(segment[0][6]) # 6: third_orientation 4: second_orientation 2: first_orientation
#     inclination = segment[0][6]
#     check_val = segment[0][1] # 1 : stayting_tick
#     last_signal = False
#     count = 3
#     for idx in range(1, seg_len):

#         s = segment[idx]
#         last_signal = (s[1] - check_val)!= 1
#         if last_signal :
#             check_val = s[1]
#             front_variance += abs(s[6])
#             inclination += s[6]
#             count += 1
#         else:
#             check_val += 1
            
#     if not last_signal: # 마지막에 third_orientation을 못넣었다면
#         front_variance += abs(s[6])
#         inclination += s[6]

#     front_variance += abs(s[4]) + abs(s[2])
#     inclination += s[4] + s[2]

#     return front_variance, inclination, count
           
# def find_movement_volume(sub_volume:Series, sub_moved_list:List[bool])-> List[float]:
#     pass



# for idx in range(common_len):
#     if idx == 0 :
#         continue

#     absoulte_rate = volume_absoulte_rate_until_third.iloc[idx]
#     diff = volume_diff_until_third.iloc[idx]
#     absoulte_diff_rate = volume_diff_absoulte_rate_until_third.iloc[idx]
#     relative_diff_rate = volume_diff_relative_rate_until_third.iloc[idx]
#     tick_move = tick_move_list[idx]







#     prev_absoulte_diff_rate = absoulte_diff_rate
#     prev_diff = diff
#     prev_relative_diff_rate = relative_diff_rate
#     prev_tick_move = tick_move
#     prev_absoulte_rate = absoulte_rate






















































