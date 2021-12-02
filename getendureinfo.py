import pandas as pd
import os



ta_dir = 'F:/TA/'

file_names = os.listdir(ta_dir)
result_dir = 'F:/Result/'


rate_calc = []
for file_name in file_names:
    
    w = open(result_dir+file_name , 'w')

    cur_df = pd.read_csv(ta_dir + file_name, sep='\t')
    
    buying_volume = cur_df['plus_v']
    selling_volume = cur_df['minus_v']
    price = cur_df['tp']
    time = cur_df['time']
    speed=  cur_df['speed']
    changed = False
    enduring_time = 0
    for idx in range(cur_df.shape[0]):
        if buying_volume.iat[idx] == 0 :
            w.writelines([str(idx),'\t', str(time.iat[idx]),'\t','BOOL',
            '\t',str(enduring_time),'\t',str(price.iat[idx]),'\t', str(buying_volume.iat[idx]),'\t',
            str(selling_volume.iat[idx]),'\t', str(speed.iat[idx]),'\n'])
        else:
            if changed :
                volume_changed = buying_volume.iat[idx] > selling_volume.iat[idx] 
            else :
                volume_changed = buying_volume.iat[idx]  < selling_volume.iat[idx]

            if volume_changed :
                enduring_time += 1
                continue
            else:
                if enduring_time < 10:
                    continue
                changed = not changed
                w.writelines([str(idx),'\t', str(time.iat[idx]),'\t',str(changed),
                '\t',str(enduring_time),'\t',str(price.iat[idx]),'\t', str(buying_volume.iat[idx]),'\t',
                str(selling_volume.iat[idx]),'\t', str(speed.iat[idx]),'\n'])
                enduring_time = 0
                
            
        
        
