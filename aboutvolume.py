import pandas as pd
import os

ta_dir = 'F:/TA/'
sub_folder ='1115/'

file_names = os.listdir(ta_dir+sub_folder)

for file_name in file_names:
    cur_df = pd.read_csv(ta_dir+sub_folder+file_name, sep='\t')
    plus_count = 0
    minus_count = 0
    w = open('F:/Temp/'+file_name, 'w')
    for i in range(cur_df.shape[0]):
        data = cur_df.iloc[i]
        diff_degree = 0
        
        if data['plus_v'] == 0 :
            continue
        elif data['plus_v'] > data['minus_v']:
            plus_count += 1
        else :
            minus_count += 1
        diff_degree =(data['plus_v'] - data['minus_v']) / (data['plus_v']+ data['minus_v']) 
        w.writelines([str(data['time']), '\t',str(plus_count),'\t', str(minus_count) ,'\t',str(round(diff_degree,2)),'\n'])

    w.close()