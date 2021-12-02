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

def sub_time_to_time(time_to_be_sub:int, time_to_sub:int) -> int:
    """
    키움 time형은 시간을 int로 표현하기에
    int 간 차감연산을 지원하는 함수 
    """
    diff = time_to_be_sub - time_to_sub
    second = diff % 100
    minute = int(diff/100) % 100
    hour = int(diff/10000)

    second_to_be_sub = time_to_be_sub % 100
    second_to_sub = time_to_sub % 100
    
    minute_to_be_sub = int(time_to_be_sub/100) % 100
    minute_to_sub = int(time_to_sub/100) % 100
    
    if (second_to_sub - second_to_be_sub) > 0 :
        second = second + 20
        second %= 60
        minute_to_sub += 1 

    if (minute_to_sub - minute_to_be_sub) > 0:
        minute = minute + 20
        minute %= 60

    return hour *10000 + minute* 100 + second


#file_name= '2021-11-23-112040.txt'
hoga_dir = 'F:/TA/1115/'
file_names= os.listdir(hoga_dir)

for file_name in file_names:

    hoga_df = pd.read_csv(hoga_dir + file_name,sep='\t')
    write_file = open('F:/Temp/ccc'+file_name,'w')
    
    hoga_df.drop(hoga_df[hoga_df['fs'] == 0].index, inplace=True)
    hoga_df.drop(hoga_df[hoga_df['fb'] == 0].index, inplace=True)
    hoga_df.drop(hoga_df[hoga_df['time']<90000].index, inplace=True)
    cur_loc =  0
    

    prev_s1 = hoga_df['fs'].iat[0]
    prev_time = hoga_df['time'].iat[0]
    prev_tick = 0
    changes = []


    sum = 0
    simple_volatility_sum = 0 
    timeout_sec = 1
    speed = 0
    up_cnt = 0
    down_cnt = 0

    value_storage = []
    standard_gap = get_gap(prev_s1)

    up_jar = 0
    down_jar = 0

    for i in range(hoga_df.shape[0]):

        time = hoga_df['time'].iat[i]
        cur_s1 = hoga_df['fs'].iat[i]
        sum = 0
   
        while True:
                if len(value_storage) == 0:
                    speed = 0
                    break
                elif value_storage[0][0] < minus_time(time, timeout_sec) :
                    diff = value_storage[0][1]
                    simple_volatility_sum -= abs(diff)
                    value_storage.pop(0)
                    changes.pop(0)
                else:
                    speed = len(value_storage)
                    break
        
        for ch in changes:
            sum = ch[1] / (1 + (ch[2] ) * (ch[3]))
            if sum > 0:
                up_jar += sum
            else :
                down_jar -= sum
        string = str(time) + ' : ' + str(round(up_jar,2)) + ' and ' + str(round(down_jar,2))
        write_file.write(string+'\n')
        
  
        if cur_s1 != prev_s1:
            
            tick_gap = i - prev_tick #가격 바뀔때마다의 틱 갯수
            time_gap = sub_time_to_time(time,prev_time) #가격 바뀔때마다의 시간 
            
            difference = (cur_s1 - prev_s1)/ standard_gap # 가격이 바뀐 크기

            changes.append((time, difference, time_gap, tick_gap))
               
            cur_loc += difference
            simple_volatility_sum += abs(difference)
            value_storage.append((time,difference))
           
            prev_tick =  i
            prev_time = time
           
            speed += 1

            

        prev_s1 = cur_s1


    write_file.close()
    