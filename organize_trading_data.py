"""
    n 틱 전 누적체결량을 비교한 파일들을 읽어서
    파일마다 누적매수체결량 - 누적매도체결량 / 누적체결량 의 값을
    n(15, 40, 60, 100, 300) 값별로 만들고 
    특정조건에 부합될 시 그 조건의 지속성을 확인하는 변수,
    그를 점수로 나타내는 변수와 누적합시키는 변수, 
    60tick동안의 경향값을 나타내는 변수와 틱의 속도를 측정하는 변수를 데이터프레임화하여
    다른 디렉터리에 저장함.

"""

import os
import pandas as pd
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

read_dir = 'F:/TA_PLUS_ALPHA/'
write_dir = 'F:/Result/'

cFiles = os.listdir(read_dir)

def s(string1):
    return str(string1)
def r(rounded):
    return round(rounded, 2)

for file_name in cFiles:

    trading_df = pd.read_csv(read_dir + file_name, sep='\t')
    if trading_df.empty:
        print(file_name ,' is empty dataframe')
        break

    accum_price_20 = 0 
    accum_price_30 = 0
    accum_price_40 = 0
    accum_price_60 = 0
    accum_price_100 = 0
    
    len_price = 0
    prev_loc = trading_df['cur_loc'].iat[0]

    price_list_20 = []
    price_list_30 = []
    price_list_40 = []
    price_list_60 = []
    price_list_100 = []
    
    pd_list= []
    
    luck_time = 0
    ready_time = 0
    prepare_time = 0
    shot_time = 0 

    continuous_jar = 0

    #tendency_len = 40
    for idx in range(trading_df.shape[0]):
        
        mean_tendency_20 = 0
        mean_tendency_30 = 0
        mean_tendency_40 = 0
        mean_tendency_60 = 0
        mean_tendency_100 = 0


        cur_loc = trading_df['cur_loc'].iat[idx]
        

        div_20 = len(price_list_20)
        div_30 =len(price_list_30)
        div_40 = len(price_list_40)
        div_60 =len(price_list_60)
        div_100 = len(price_list_100)
       
        mean_tendency_20 = cur_loc - accum_price_20 / (1 if div_20 == 0 else div_20)
        mean_tendency_30 = cur_loc - accum_price_30 / (1 if div_30 == 0 else div_30)
        mean_tendency_40 = cur_loc - accum_price_40 / (1 if div_40 == 0 else div_40)
        mean_tendency_60 = cur_loc - accum_price_60 / (1 if div_60 == 0 else div_60)
        mean_tendency_100 = cur_loc - accum_price_100 / (1 if div_20 == 0 else div_100)

        mean_tendency_20 = round(mean_tendency_20, 1)
        mean_tendency_30 = round(mean_tendency_30, 1)
        mean_tendency_40 = round(mean_tendency_40, 1)
        mean_tendency_60 = round(mean_tendency_60, 1)
        mean_tendency_100 = round(mean_tendency_100, 1)

        if idx < 20 :
            mean_tendency_20 = 0.0
        if idx < 30 :
            mean_tendency_30 = 0.0
        if idx < 40 :
            mean_tendency_40 = 0.0
        if idx < 60 :
            mean_tendency_60 = 0.0
        if idx < 100 :
            mean_tendency_100 = 0.0
           



        if len(price_list_20) >= 20:
            popped = price_list_20.pop(0)
            accum_price_20 -= popped
        else :
            len_price += 1

        accum_price_20 += cur_loc
        price_list_20.append(cur_loc)

        if len(price_list_40) >= 40:
            popped = price_list_40.pop(0)
            accum_price_40 -= popped
        else :
            len_price += 1

        accum_price_40 += cur_loc
        price_list_40.append(cur_loc)

        if len(price_list_30) >= 30:
            popped = price_list_30.pop(0)
            accum_price_30 -= popped
        else :
            len_price += 1

        accum_price_30 += cur_loc
        price_list_30.append(cur_loc)

        if len(price_list_60) >= 60:
            popped = price_list_60.pop(0)
            accum_price_60 -= popped
        else :
            len_price += 1

        accum_price_60 += cur_loc
        price_list_60.append(cur_loc)

        if len(price_list_100) >= 100:
            popped = price_list_100.pop(0)
            accum_price_100 -= popped
        else :
            len_price += 1

        accum_price_100 += cur_loc
        price_list_100.append(cur_loc)
            
        first_bigger = (trading_df['pvb15t'].iat[idx] - trading_df['mvb15t'].iat[idx]) / (trading_df['pvb15t'].iat[idx] + trading_df['mvb15t'].iat[idx] + 1)
        second_bigger = (trading_df['pvb40t'].iat[idx] - trading_df['mvb40t'].iat[idx]) / (trading_df['pvb40t'].iat[idx] + trading_df['mvb40t'].iat[idx] + 1)
        third_bigger = (trading_df['pvb60t'].iat[idx] - trading_df['mvb60t'].iat[idx]) / (trading_df['pvb60t'].iat[idx] + trading_df['mvb60t'].iat[idx] + 1)
        fourth_bigger = (trading_df['pvb100t'].iat[idx] - trading_df['mvb100t'].iat[idx]) / (trading_df['pvb100t'].iat[idx] + trading_df['mvb100t'].iat[idx]+ 1)
        fifth_bigger = (trading_df['pvb300t'].iat[idx] - trading_df['mvb300t'].iat[idx]) / (trading_df['pvb300t'].iat[idx] + trading_df['mvb300t'].iat[idx] + 1)

        first_bigger = round(first_bigger, 2)
        second_bigger = round(second_bigger, 2)
        third_bigger = round(third_bigger, 2)
        fourth_bigger = round(fourth_bigger, 2)
        fifth_bigger = round(fifth_bigger, 2)

        if ( first_bigger > 0 or second_bigger > 0 ) and third_bigger > 0 :
            luck_time += 1
        else:
            luck_time = 0 

        if third_bigger > 0 and fourth_bigger > 0 :
            prepare_time += 1
        else :
            prepare_time = 0 

        if (first_bigger > 0 or second_bigger > 0) and fifth_bigger > 0 :
            ready_time += 1
        else:
            ready_time = 0 

        if fifth_bigger > 0 :
            shot_time += 1
        else :
            shot_time = 0 

        speed = trading_df['speed'].iat[idx]
        temporary_score = round(first_bigger * 0.3 + second_bigger * 0.3 + third_bigger *0.3 + fourth_bigger * 0.5 + fifth_bigger * 0.7, 2)
        continuous_jar += temporary_score

        pd_list.append([trading_df['time'].iat[idx], cur_loc,
                        first_bigger, second_bigger, third_bigger, fourth_bigger, fifth_bigger,
                        luck_time, prepare_time, ready_time, shot_time,
                        temporary_score, round(continuous_jar, 2),
                        mean_tendency_20,mean_tendency_30,mean_tendency_40,
                        mean_tendency_60,mean_tendency_100, speed,
                        trading_df['fs'].iat[idx], trading_df['fb'].iat[idx]])
    
    col_names = ['t','cur','s1','s2','s3','s4','s5','lt','pt','rt','st','tscore','cjar','mt2','mt3','mt4','mt6','mt10','spd','fs','fb']
    pd_df = pd.DataFrame(pd_list, columns=col_names)
    pd_df.to_csv(write_dir+file_name, sep='\t')