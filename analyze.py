import os
import pandas as pd


ta_dir = 'F:/Result/'


cFiles = os.listdir(ta_dir)

def s(string1):
    return str(string1)
def r(rounded):
    return round(rounded, 2)


for file_name in cFiles:
  
    
    trading_df = pd.read_csv(ta_dir + file_name, sep='\t')
    if trading_df.empty:
        print(file_name ,' is empty dataframe')
        break
    trading_df.fillna(0, inplace=True)
  
    continuous_jar = 0
    temporary_jar = 0
    success_record = 0
    failure_record = 0
    luck_time = 0
    ready_time = 0
    prepare_time = 0
    shot_time = 0 
    score_list = [] 
    df_list = []
    for idx in range(trading_df.shape[0]):

        cur_loc = trading_df['cur_loc'].iat[idx]
        score1 = trading_df['s1'].iat[idx]
        score2 = trading_df['s2'].iat[idx]
        score3 = trading_df['s3'].iat[idx]
        score4 = trading_df['s4'].iat[idx]
        score5 = trading_df['s5'].iat[idx]
        tendency = trading_df['tendency'].iat[idx]
        speed = trading_df['speed'].iat[idx]
        success_point = 0

        if score1 > 0:
            success_point += 1
        if score2 > 0:
            success_point += 1
        if score3 > 0 :
            success_point += 1
        if score4 > 0 :
            success_point += 1
        if score5 > 0 :
            success_point += 1
        
        if success_point >= 3:
            success_record += 1
        else :
            failure_record += 1

        if ( score1 > 0 or score2 > 0 ) and score3 > 0 :
            luck_time += 1
        else:
            luck_time = 0 

        if score3 > 0 and score4 > 0 :
            prepare_time += 1
        else :
            prepare_time = 0 

        if score4 > 0 :
            ready_time += 1
        else:
            ready_time = 0 

        if score5 > 0 :
            shot_time += 1
        else :
            shot_time = 0 
        

        temporary_score = score1 * 0.3 + score2 * 0.3 + score3 *0.3 + score4 * 0.5 + score5 * 0.7
        score_list.append(temporary_score)
        temporary_jar += temporary_score
        continuous_jar += temporary_score

        if len(score_list) > 10 :
            temporary_jar -= score_list.pop(0)
        

        df_list.append([trading_df['t'].iat[idx],cur_loc, score1, score2, score3, score4,score5,
        luck_time,prepare_time, ready_time, shot_time,
        round(temporary_score,2),round(temporary_jar,3),round(continuous_jar,3)   ])
      
    df= pd.DataFrame(df_list, columns=['t','cur_loc','s1','s2','s3','s4','s5','lt','pt','rt','st','ts','tj','cj'])
    df.to_csv('F:/Temp2/'+file_name, sep='\t') 