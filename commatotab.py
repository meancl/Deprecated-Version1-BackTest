import pandas as pd


file_name = '2021-11-12-206560.txt'

hoga_dir = 'F:/Hoga/'
trading_dir = 'F:/Trading/'
write_hoga_dir = 'D:/MJ/MyProject/Trading_Proj/Tab_Seperated_Hoga/'
write_trading_dir = 'D:/MJ/MyProject/Trading_Proj/Tab_Seperated_Trading/'



hoga_names = ['time', 's10', 'sv10', 's9', 'sv9', 's8', 'sv8', 's7', 'sv7', 's6', 'sv6',
            's5', 'sv5', 's4', 'sv4', 's3', 'sv3', 's2', 'sv2', 's1', 'sv1',
            'b1', 'bv1', 'b2', 'bv2', 'b3', 'bv3', 'b4', 'bv4', 'b5', 'bv5', 'b6', 'bv6',
            'b7', 'bv7', 'b8', 'bv8', 'b9', 'bv9', 'b10', 'bv10', 
            'sav', 'savd', 'bav', 'bavd', 'pbv', 'br', 'sr']

hoga_df = pd.read_csv(hoga_dir + file_name, names=hoga_names)


trading_names =['time', 'tp', 'udr', 'ta',
            'trr', 'ts', 'fs', 'fb', 'market']

trading_df = pd.read_csv(trading_dir + file_name, names=trading_names)

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

trading_df['tp'] = abs(trading_df['tp'])
trading_df['fs'] = abs(trading_df['fs'])
trading_df['fb'] = abs(trading_df['fb'])


hoga_df.drop(hoga_df[hoga_df['sav']==0].index, inplace=True)

hoga_df.to_csv(write_hoga_dir + file_name, sep='\t')
trading_df.to_csv(write_trading_dir + file_name, sep='\t')