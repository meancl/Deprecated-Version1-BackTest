import pandas as pd
import os 
import matplotlib.pyplot as plt

file_name = '2021-11-11-027710.txt'

hoga_dir = 'F:/Temp2/'


li = os.listdir(hoga_dir)


hoga_names = ['time', 's10', 'sv10', 's9', 'sv9', 's8', 'sv8', 's7', 'sv7', 's6', 'sv6',
            's5', 'sv5', 's4', 'sv4', 's3', 'sv3', 's2', 'sv2', 's1', 'sv1',
            'b1', 'bv1', 'b2', 'bv2', 'b3', 'bv3', 'b4', 'bv4', 'b5', 'bv5', 'b6', 'bv6',
            'b7', 'bv7', 'b8', 'bv8', 'b9', 'bv9', 'b10', 'bv10', 
            'sav', 'savd', 'bav', 'bavd', 'pbv', 'br', 'sr']

for i in li:
    print(i)
    hoga_df = pd.read_csv(hoga_dir + i,sep='\t')

    # hoga_df['s10'] = abs(hoga_df['s10'])
    # hoga_df['s9'] = abs(hoga_df['s9'])
    # hoga_df['s8'] = abs(hoga_df['s8'])
    # hoga_df['s7'] = abs(hoga_df['s7'])
    # hoga_df['s6'] = abs(hoga_df['s6'])
    # hoga_df['s5'] = abs(hoga_df['s5'])
    # hoga_df['s4'] = abs(hoga_df['s4'])
    # hoga_df['s3'] = abs(hoga_df['s3'])
    # hoga_df['s2'] = abs(hoga_df['s2'])
    # hoga_df['s1'] = abs(hoga_df['s1'])

    # hoga_df['b1'] = abs(hoga_df['b1'])
    # hoga_df['b2'] = abs(hoga_df['b2'])
    # hoga_df['b3'] = abs(hoga_df['b3'])
    # hoga_df['b4'] = abs(hoga_df['b4'])
    # hoga_df['b5'] = abs(hoga_df['b5'])
    # hoga_df['b6'] = abs(hoga_df['b6'])
    # hoga_df['b7'] = abs(hoga_df['b7'])
    # hoga_df['b8'] = abs(hoga_df['b8'])
    # hoga_df['b9'] = abs(hoga_df['b9'])
    # hoga_df['b10'] = abs(hoga_df['b10'])



    #hoga_df.drop(hoga_df[hoga_df['sav']==0].index, inplace=True)


    plt.plot(hoga_df['time'], hoga_df['s1'])
    plt.show()


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


















































