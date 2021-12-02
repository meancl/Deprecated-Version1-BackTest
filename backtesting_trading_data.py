import os
import pandas as pd


read_dir = 'F:/Temp/'

cFiles = os.listdir(read_dir)

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

def get_proper_step(selling_price:int, buying_price:int) -> int:
    step = get_gap(selling_price)
    return round((selling_price - buying_price)/step,1)

def describe_trading_record(file_name, records):
    print('======================== ',file_name,' ========================')
    val = []
    for idx, record in enumerate(records):
        print(idx ,' --> ','BUY : ( ', record[0],' , ', record[1],' ) , ( ', record[2],' , ', record[3], ' )')
        val.append(record[3] - record[1])
    if len(val) > 0:
        print('-------------------------- ', round(sum(val)/len(val),2),' ------------------------------')

def describe_buying_record(file_name, records):
    print('======================== ',file_name,' ========================')
    val = []
    for idx, record in enumerate(records):
        print(idx ,' --> ','BUY : ( ', record[0],' , ', record[1],' )')

    print('---------------------------------------------------------------------')


for file_name in cFiles:

    trading_df = pd.read_csv(read_dir + file_name, sep='\t')
    if trading_df.empty :
        print(file_name,' : EMPTY ERROR')
        continue
   
    score_history = []
    score_history_len = 3
    sum_score = 0

    poc_history = []
    poc_history_len = 5
    sum_poc = 0 
    mt6_flag = False
    for idx in range(trading_df.shape[0]):

        lt = trading_df['lt'].iat[idx] # luck_time (s1 or s2) and s3
        pt = trading_df['pt'].iat[idx] # prepare_time s3 and s4
        rt = trading_df['rt'].iat[idx] # ready_time (s1 or s2) and s5
        st = trading_df['st'].iat[idx] # shot_time s5
        
        mt6 = trading_df['mt6'].iat[idx]

        tscore = trading_df['tscore'].iat[idx]
        cjar = trading_df['cjar'].iat[idx]
        speed = trading_df['spd'].iat[idx]
        
        time = trading_df['t'].iat[idx]
        fs_price = trading_df['fs'].iat[idx]
        fb_price = trading_df['fb'].iat[idx]
        poc = 0.0


        if mt6 >= 6:
            mt6_flag = True
        
        if len(score_history) > score_history_len:
            prev_mean_score = sum_score / score_history_len
            poc = tscore - prev_mean_score
            sum_score -= score_history.pop(0)

        # 한 틱 전까지의 sum_poc 
        if len(poc_history) > poc_history_len :
            sum_poc -=  poc_history.pop(0)
            # 리스트 맨 앞 poc를 차감한 sum_poc


        sum_score += tscore
        score_history.append(tscore)    
        sum_poc += poc
        # 현재가가 포함된 sum_poc
        poc_history.append(poc)


    if mt6_flag :
        print(file_name)

        

