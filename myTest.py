import pandas as pd
import os

ta_dir = 'F:/TA/'
sub_folder ='1117/'

file_names = os.listdir(ta_dir+sub_folder)


adding = 59
w = open('F:/Result/good1117.txt','w')


time_entrance = [90300]
def plus_time(time_to_add:int ,adding:int= 1) -> int:
    chance = int(adding/61) + 1 
    second = (time_to_add) % 100
    minute = int(time_to_add / 100) % 100
    hour = int(time_to_add/ 10000)
    for _ in range(chance):
        temp_adding = 60 if adding > 60 else adding
        second += temp_adding 
        if second >= 60:
            minute += 1 
            second = ( second - 60 )
        if minute >= 60 :
            hour += 1 
            minute = (minute - 60)
        adding -= 60
    return hour * 10000 + minute * 100 + second
cur_time = 90500

while True:
    if cur_time >= 150000:
        break
    time_entrance.append(cur_time)
    cur_time = plus_time(cur_time, 60)

before_count_rate  = 1
before_volume_rate = 1
after_count_rate = 1
after_volume_rate = 1
before_cont_volume_rate = 1
after_cont_volume_rate = 1
rate_calc = []
prev_p_c_list = []
prev_m_c_list = [] 

for file_name in file_names:
    cur_df = pd.read_csv(ta_dir+sub_folder+file_name, sep='\t')
    if cur_df.empty:
        print(file_name ,' empty')
        continue
    time_idx = 0
    wall_time_idx = len(time_entrance)
    buyed = False
    selled = False
    sig_brk = False
    reverse_cnt = False
    buying_price = 0
    buying_time = 0
    selling_price = 0
    selling_time = 0
    prev_plus_count = 0
    prev_minus_count = 0
    time_out = False
    chance_out = False
    speed_low = False
    buying_speed = 0 
    selling_speed = 0

    for idx in range(cur_df.shape[0]):
        if time_idx >= wall_time_idx-1:
            break
        value = cur_df.iloc[idx]
        time = value['time']
        plus_count = value['plus_count']
        prev_plus_count = prev_plus_count if plus_count == 0 else plus_count
        minus_count = value['minus_count']
        prev_minus_count = prev_minus_count if minus_count == 0 else minus_count
        speed = value['speed']
        plus_volume = value['plus_v']
        minus_volume = value['minus_v']
        p_v = value['plus_volume']
        m_v = value['minus_volume']
        price = value['tp']
        cont_p_v = value['cont_plus_volume']
        cont_m_v = value['cont_minus_volume']
        #prev_p_c_list.append(prev_plus_count)
        #prev_m_c_list.append(prev_minus_count)

        # if buyed :
        #     buyed_rate =(price - buying_price)/ buying_price
        #     if buyed_rate < -6 :
        #         print(-60000000)
        #         sig_brk = True
        #         selling_time = time
        #         selling_price = price
        #         selling_speed = speed
        #         selled = True

        
        if (time_entrance[time_idx] <= time <= time_entrance[time_idx]+adding):
            # plus_diff = 1
            # minus_diff= 0 
            if buyed:
                
                # if len(prev_m_c_list) > 102 or len(prev_p_c_list) > 102:
                #     plus_diff = prev_plus_count - prev_p_c_list[-100]
                #     minus_diff = prev_minus_count - prev_m_c_list[-100]

                if (prev_plus_count > prev_minus_count * after_count_rate)  and (plus_volume > minus_volume * after_volume_rate) and cont_p_v > (cont_m_v * after_cont_volume_rate):
                    _=1
                    pass
                elif plus_volume <= minus_volume * after_volume_rate:
                    temp_idx = idx
                    while True:
                        temp_value = cur_df.iloc[temp_idx]
                        temp_time = temp_value['time']
                        temp_idx += 1
                        if temp_time <= time +adding :
                            if temp_value['plus_v'] > temp_value['minus_v'] :#* after_volume_rate:
                                break
                        else:
                            selling_time = temp_time
                            selling_price = price
                            selled = True
                            sig_brk = True
                            time_out = True
                            selling_speed = speed
                            break

                elif prev_plus_count <= prev_minus_count *after_count_rate:
                    sig_brk = True
                    reverse_cnt = True
                    selling_time = time
                    selling_price = price
                    selling_speed = speed
                    selled = True

                else: # plus_diff <= minus_diff 
                    print(file_name, ' pass')
            else:
                if speed < 2:
                    speed_low =True
                    sig_brk = True

                elif (prev_plus_count > prev_minus_count * before_count_rate) and (plus_volume > minus_volume * before_volume_rate) and cont_p_v > (cont_m_v* before_cont_volume_rate):
                    buyed = True
                    buying_price = price
                    buying_time = time
                    buying_speed = speed

                elif time >=  145500: #강제청산
                    sig_brk = True
                    selling_time = time
                    selling_price = price
                    selling_speed = speed
                    selled = True

            time_idx += 1

        if sig_brk :
            rate = 0 
            if buyed :
                rate = (selling_price - buying_price)/ buying_price 
                
                rate -= 0.0026
                rate *= 100
                rate_calc.append(rate)
          
                
            rate = round(rate,3)
            w.writelines([file_name ,'\t', str(buyed),'\t', str(buying_price),'\t', str(buying_time), '\t',
                str(buying_speed), '\t'
             ,'\t',str(selled),'\t', str(selling_price),'\t', str(selling_time),'\t', str(selling_speed)
             ,'\t',str(speed_low) ,'\t', str(chance_out) ,'\t', str(reverse_cnt),'\t',
              str(time_out),'\t', str(rate), '\n' ])

            buyed = False
            selled =False
            sig_brk = False
            chance_out = False
            reverse_cnt = False
            time_out = False
            buying_price = 0
            buying_time= 0 
            selling_price =0 
            selling_time = 0
            selling_speed = 0 
            buying_speed = 0
            time_idx += 1
            continue
        
sum_= sum(rate_calc)
mean_ = sum_/len(rate_calc)
print('sum : ', sum_)
print('mean : ', mean_)
