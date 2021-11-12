from pykiwoom.kiwoom import *
import pandas as pd

kiwoom = Kiwoom()
kiwoom.CommConnect(block=True)

def removeRedun(li):

    li.sort()
    len_li = len(li)
    i= 0 
    while True:
        if len_li <= 1 or i >= len_li -1:
            break
        if li[i] == li[i+1]:
            del li[i]
            len_li -= 1
            i-=1
        i+=1
    return len_li,li
    
def request_stock(code,msg):
    res =  kiwoom.block_request(code,
                          시장구분="101",
                          조회구분="1",
                          순위시작='0',
                          순위끝="100",
                          output=msg,
                          next=0)
    return res

def extract_stock_code(value):

    #print(value)
    if value[0].isalpha():
        value = value[1:7]
        
    return value
        

df_yester = request_stock("opt10031","전일거래량상위요청")           
df_today = request_stock("opt10030","당일거래량상위요청")
                          

df_yester_stock_code = df_yester['종목코드']
df_today_stock_code  =  df_today['종목코드']


df_y = df_yester_stock_code.tolist()
df_t = df_today_stock_code.tolist()

df = df_y + df_t

for i,v in enumerate(df):
    df[i]= extract_stock_code(v)
    
stock_len, df = removeRedun(df)
STOCK_LEN_LIMIT= stock_len

with open('stock_code.txt','w') as f:
    for index,item in enumerate(df):
        f.write(item)
        if index != STOCK_LEN_LIMIT-1:
            f.write('\n')


        


