import sys,os
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
from datetime import datetime
import time
from pykrx import stock
import random
import pandas as pd
import pyautogui as pg







# QAxWidget 상속받음
class Kiwoom(QAxWidget):
    def __init__(self):

        super().__init__()
        print("start")
        self._create_kiwoom_instance()
        self._set_signal_slots()
        self.fs={}  # files number
        self.cnt={} # count of each file inputs
        

    # COM을 사용하기 위한 메서드
    def _create_kiwoom_instance(self):

        self.setControl("KHOPENAPI.KHOpenAPICtrl.1")

    def _set_signal_slots(self):

        # 로그인할 시 OnEventConnect 이벤트 발생
        self.OnEventConnect.connect(self._handler_login)
        # 실시간 이벤트 수신 이벤트
        self.OnReceiveRealData.connect(self._handler_real_data)


    def login(self,df):

        print('파일 여는중')
        self.filesOpen(df)
        print('파일 열기 끝')
        print("login 중 ...")

        self.dynamicCall("CommConnect()")
        self.login_event_loop = QEventLoop()
        self.login_event_loop.exec_()
     
        


    def _handler_login(self, err_code):

        if err_code == 0:
            print("login 완료")
        else:
            print("disconnected")
        self.login_event_loop.exit()

    def _handler_real_data(self, code, real_type, data):

        if real_type == "주식호가잔량" and self.fs[code].closed == False:

            
            now = datetime.now().strftime('%H%M')
            
            # 장마감시간이 되면 파일 전부 닫음
            if  now == '1528' or now == '1529':
                print('time to finish')
                self.fs[code].close()
                return
                

            hoga_time = self.get_comm_realdata(code, 21)
            ask01_price = self.get_comm_realdata(code, 41)
            ask01_volume = self.get_comm_realdata(code, 61)
            bid01_price = self.get_comm_realdata(code, 51)
            bid01_volume = self.get_comm_realdata(code, 71)
            ask02_price = self.get_comm_realdata(code, 42)
            ask02_volume = self.get_comm_realdata(code, 62)
            bid02_price = self.get_comm_realdata(code, 52)
            bid02_volume = self.get_comm_realdata(code, 72)
            ask03_price = self.get_comm_realdata(code, 43)
            ask03_volume = self.get_comm_realdata(code, 63)
            bid03_price = self.get_comm_realdata(code, 53)
            bid03_volume = self.get_comm_realdata(code, 73)
            ask04_price = self.get_comm_realdata(code, 44)
            ask04_volume = self.get_comm_realdata(code, 64)
            bid04_price = self.get_comm_realdata(code, 54)
            bid04_volume = self.get_comm_realdata(code, 74)
            ask05_price = self.get_comm_realdata(code, 45)
            ask05_volume = self.get_comm_realdata(code, 65)
            bid05_price = self.get_comm_realdata(code, 55)
            bid05_volume = self.get_comm_realdata(code, 75)


                
            #  해당 파일에 삽입
           
            ### 띄어쓰기 2칸
            #print('writing...')
            self.cnt[code] = self.cnt[code] + 1
            self.fs[code].writelines([   hoga_time, '  ', ask01_price, '  ', ask01_volume, '  ', bid01_price, '  ', bid01_volume, '  ', ask02_price, '  ',                                   
                                      ask02_volume, '  ', bid02_price, '  ', bid02_volume, '  ', ask03_price, '  ', ask03_volume, '  ', bid03_price, '  ',
                                      bid03_volume, '  ', ask04_price, '  ', ask04_volume, '  ', bid04_price, '  ', bid04_volume, '  ', ask05_price, '  ',
                                      ask05_volume, '  ', bid05_price, '  ', bid05_volume, '\n'])
            

            ## file flush 와 동기화를 통해 실시간 데이터를 디스크에 삽입했는데
            ## 속도저하가 강하고 주기적으로 8시 40분부터 3시 30분까지 데이터를 받아올 예정이라 주석처리.
            #if self.cnt[code] % 2048 == 0 :
                #self.fs[code].flush()
                ##os.fsync(self.fs[code].fileno())   # 속도저하에 큰 원인이 됨.
                

            ## 프린트 또한 I/O 작업이라 시간이 많이 소모돼
            ## 실시간 데이터의 손실을 가져올 수 있어서 멈춤.
            #print(f" ======================={code}======={self.cnt[code]}===========")
            
            '''
            print(f"시간 : {hoga_time}")
            print(f"매도1 호가: {ask01_price} / 수량: {ask01_volume}")
            print(f"매수1 호가: {bid01_price} / 수량:{bid01_volume}")
            print(f"매도2 호가: {ask02_price} / 수량: {ask02_volume}")
            print(f"매수2 호가: {bid02_price} / 수량:{bid02_volume}")
            print(f"매도3 호가: {ask03_price} / 수량: {ask03_volume}")
            print(f"매수3 호가: {bid03_price} / 수량:{bid03_volume}")
            print(f"매도4 호가: {ask04_price} / 수량: {ask04_volume}")
            print(f"매수4 호가: {bid04_price} / 수량:{bid04_volume}")
            print(f"매도5 호가: {ask05_price} / 수량: {ask05_volume}")
            print(f"매수5 호가: {bid05_price} / 수량:{bid05_volume}")

 

            print("-------------------------------------------------------")

            '''

       

                

    def collect(self, screen_no, code_list, fid_list, real_type):

        self.dynamicCall("SetRealReg(QString, QString, QString, QString)",
                         screen_no, code_list, fid_list, real_type)
        print("구독 신청 완료")
        self.real_event_loop = QEventLoop()
        self.real_event_loop.exec_()

    def disconnect_realdata(self, screen_no):

        self.DisConnectRealData(screen_no)
        print("구독 해지 완료")

    def get_comm_realdata(self, code, fid):

        data = self.dynamicCall("GetCommRealData(QString, int)", code, fid)

        return data

    ''' 
     현재시간 + 종목코드.txt 생성 혹은 추가
     fs 딕셔너리 변수에 키가 종목코드 , 값이 해당 파일넘버로 추가한다.
    '''

    def filesOpen(self,l):

        #absPath = 'D:/MJ/stock/getData/kiwoom/hoga_folder/'
        absPath = 'C:/hoga_folder/'
        
        today = datetime.now().strftime("%Y-%m-%d")
        
        for i in l:
            f = open(absPath+today+'-'+i+'.txt', 'w')
            self.fs[i] = f
            self.cnt[i] = 1
          




# ex) 종목코드1;종목코드2:  -->  [종목코드1, 종목코드2]
def ltos(l):

    str = ''

    for i in l:
        str += i
        str += ';'

    str = str[:-1]
    print(str)

    return str


if __name__ == "__main__":

    '''
    Kiwoom 클래스는 QAxWiget 클래스를 상속받았기 때문에
    Kiwoom 클래스에 대한 인스턴스를 생성하려면 먼저 QApplication 클래스의 인스턴스를 생성해야함
    '''

    app = QApplication(sys.argv)
    #df=stock.get_market_ticker_list(market="KOSDAQ")
    df = []
    with open('stock_code.txt','r') as f:
        while True:
            line = f.readline()
            if not line: break
            df.append(line[:6])

    print(len(df))
    collector = Kiwoom()
    collector.login(df)
    #aInput= input()
    print('aInput')
    #exit()