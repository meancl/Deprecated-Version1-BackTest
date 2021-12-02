import pandas as pd
import os


def minus_time(time_to_minus:int , minus:int=1) -> int:
    
    chance = int(minus/61) + 1
    second = time_to_minus % 100
    minute = int(time_to_minus/100) % 100
    hour = int(time_to_minus/10000)
    sub = 0
    for _ in range(chance):
        if minus >= 60:
            sub = 60 
            minus -= 60
        else:
            sub = minus
        second -= sub
        if second < 0 :
            if minute == 0 :
                hour -= 1
                minute = 60
            minute -= 1
            second += 60
    
    return hour * 10000 + minute * 100 + second

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

#file_name= '2021-11-23-112040.txt'
hoga_dir = 'F:/TA/1115/'
file_names= os.listdir(hoga_dir)

for file_name in file_names:

    hoga_df = pd.read_csv(hoga_dir + file_name,sep='\t')
    write_file = open('F:/Temp/bbb'+file_name,'w') 

    total_sum = 0 
    cur_loc =  0
    total_simple_volatility_sum = 0
    total_volatility_sum = 0
    hoga_df.drop(hoga_df[hoga_df['time']<90000].index, inplace=True)

    prev_s1 = hoga_df['fs'].iat[-1]
    sum = 0
    volatility_sum = 0
    volatility_weight = 2
    simple_volatility_sum = 0 
    timeout_sec = 4
    speed = 0
    value_storage = []
    standard_gap = get_gap(prev_s1)

    for i in range(hoga_df.shape[0]):
        time = hoga_df['time'].iat[i]
        cur_s1 = hoga_df['fs'].iat[i]

        while True:
                if len(value_storage) == 0:
                    speed = 0
                    break
                elif value_storage[0][0] < minus_time(time, timeout_sec) :
                    diff = value_storage[0][1]
                    sum -= diff
                    simple_volatility_sum -= abs(diff)
                    value_storage.pop(0)
                else:
                    speed = len(value_storage)
                    break
        

        if cur_s1 != prev_s1:
            difference = (cur_s1 - prev_s1)/ standard_gap
            cur_loc += difference
            sum += difference
            simple_volatility_sum += abs(difference)
            total_simple_volatility_sum += abs(difference)
            value_storage.append((time,difference))
            speed += 1
            
            write_file.writelines([str(time),'\t',str(difference),'\t', str(speed),'\t',str(round(simple_volatility_sum,1)),'\t','\t',str(cur_loc), '\t',str(round(total_simple_volatility_sum,1)),'\t','\n'])
        else:
            write_file.writelines([str(time),'\t',str(0),'\n'])
        prev_s1 = cur_s1


    write_file.close()
    