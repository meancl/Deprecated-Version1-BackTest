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


class ParameterTypeError(Exception):
    """ 파라미터 타입이 일치하지 않을 경우 발생하는 예외 """

    def __init__(self, msg="파라미터 타입이 일치하지 않습니다."):
        self.msg = msg

    def __str__(self):
        return self.msg


class KiwoomConnectError(Exception):
    """ 키움서버에 로그인 상태가 아닐 경우 발생하는 예외 """

    def __init__(self, msg="로그인 여부를 확인하십시오"):
        self.msg = msg

    def __str__(self):
        return self.msg

# QAxWidget 상속받음
class Kiwoom(QAxWidget):
    def __init__(self):

        super().__init__()
        print("start")
        self._create_kiwoom_instance()
        self._set_signal_slots()
        self.fs={}  # files number
        self.cnt={} # count of each file inputs
        self.screenNo = []
        self.entranceCnt = 0
        
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
     
    def wait(self):
        self.waitThread = QEventLoop()
        self.waitThread.exec_()


    def _handler_login(self, err_code):

        if err_code == 0:
            print("login 완료")
        else:
            print("disconnected")
        self.login_event_loop.exit()


    def _handler_real_data(self, code, real_type, data):

        now = datetime.now()
        now_time = now.hour * 60 + now.minute 

        if  now_time >= 928:

            print('time to finish')

                # _handler_real_data가  thread 형식으로 운용된다면
                # 다른 종목의 thread와 파일클로즈를 같이 여러번 할 수 있기 때문에 
                # 임계영역의 락과 같이 카운트가 0이었을 한 thread만 접근 가능하게 함.
            if not self.entranceCnt:
                self.entranceCnt +=1 
                for screen in self.screenNo:
                    self.disconnect_realdata(screen)
                self.filesClose()
                self.waitThread.exit()
                    
                sys.exit(0)

        if real_type == "주식호가잔량":

            # 장마감시간이 되면 파일 전부 닫음
           
            hoga_time = self.get_comm_realdata(code, 21)

            s10 = self.get_comm_realdata(code, 50)
            sv10 = self.get_comm_realdata(code, 70)
            s9 = self.get_comm_realdata(code, 49)
            sv9 = self.get_comm_realdata(code, 69)
            s8 = self.get_comm_realdata(code, 48)
            sv8 = self.get_comm_realdata(code, 68)
            s7 = self.get_comm_realdata(code, 47)
            sv7 = self.get_comm_realdata(code, 67)
            s6 = self.get_comm_realdata(code, 46)
            sv6 = self.get_comm_realdata(code, 66)
            s5 = self.get_comm_realdata(code, 45)
            sv5 = self.get_comm_realdata(code, 65)
            s4 = self.get_comm_realdata(code, 44)
            sv4 = self.get_comm_realdata(code, 64)
            s3 = self.get_comm_realdata(code, 43)
            sv3 = self.get_comm_realdata(code, 63)
            s2 = self.get_comm_realdata(code, 42)
            sv2 = self.get_comm_realdata(code, 62)
            s1 = self.get_comm_realdata(code, 41)
            sv1 = self.get_comm_realdata(code, 61)

            b10 = self.get_comm_realdata(code, 60)
            bv10 = self.get_comm_realdata(code, 80)
            b9 = self.get_comm_realdata(code, 59)
            bv9 = self.get_comm_realdata(code, 79)
            b8 = self.get_comm_realdata(code, 58)
            bv8 = self.get_comm_realdata(code, 78)
            b7 = self.get_comm_realdata(code, 57)
            bv7 = self.get_comm_realdata(code, 77)
            b6 = self.get_comm_realdata(code, 56)
            bv6 = self.get_comm_realdata(code, 76)
            b5 = self.get_comm_realdata(code, 55)
            bv5 = self.get_comm_realdata(code, 75)
            b4 = self.get_comm_realdata(code, 54)
            bv4 = self.get_comm_realdata(code, 74)
            b3 = self.get_comm_realdata(code, 53)
            bv3 = self.get_comm_realdata(code, 73)
            b2 = self.get_comm_realdata(code, 52)
            bv2 = self.get_comm_realdata(code, 72)
            b1 = self.get_comm_realdata(code, 51)
            bv1 = self.get_comm_realdata(code, 71)

            sav = self.get_comm_realdata(code, 121) # sell all volume
            savn = self.get_comm_realdata(code, 122) # sell all volume now
            bav = self.get_comm_realdata(code, 125) # buy all volume
            bavn = self.get_comm_realdata(code, 126)
            pbv = self.get_comm_realdata(code, 128) #순매수잔량 pure buy volume
            br = self.get_comm_realdata(code, 129) # 매수비율
            sr = self.get_comm_realdata(code, 139) # 매도비율

                
            #  해당 파일에 삽입
           
            self.fs[code][0].writelines([   hoga_time, ',', b10, ',', bv10, ',', b9, ',', bv9, ',', b8,',', bv8,',',                                  
                                      b7, ',', bv7, ',', b6, ',', bv6, ',', b5, ',', bv5, ',', b4, ',', bv4, ',',
                                      b3, ',', bv3, ',', b2, ',', bv2, ',', b1, ',', bv1, ',',
                                      s1, ',', sv1, ',', s2, ',', sv2, ',', s3, ',', sv3, ',', s4, ',', sv4, ',', 
                                      s5, ',', sv5, ',', s6, ',', sv6, ',', s7, ',', sv7, ',', s8, ',', sv8, ',',
                                      s9, ',', sv9, ',', s10, ',', sv10, ',',
                                      sav,',', savn,',', bav,',', bavn,',', pbv,',', br,',', sr,
                                     '\n'])
        
        elif real_type == '주식체결':
            
            trading_time = self.get_comm_realdata(code, 20)
            ta = self.get_comm_realdata(code, 15)  # trading amount
            ata = self.get_comm_realdata(code, 13) # accumulating trading amount
            ts = self.get_comm_realdata(code, 228) # trading strength

            self.fs[code][1].writelines([trading_time, ',', ta, ',', ata, ',', ts, '\n'])


          

       

                

    def setRealReg(self, screen_no, code_list, fid_list, real_type):

        self.screenNo.append(screen_no)
        #print(screen_no)
        #print('screen No append with real_type ',real_type)

        self.dynamicCall("SetRealReg(QString, QString, QString, QString)",
                         screen_no, code_list, fid_list, real_type)
        
        print("구독 신청 완료")




    def disconnect_realdata(self, screenNo):

        self.dynamicCall("DisconnectRealData(QString)", screenNo)

        print("구독 해지 완료")


    def get_comm_realdata(self, code, fid):

        data = self.dynamicCall("GetCommRealData(QString, int)", code, fid)

        return data

    ''' 
     현재시간 + 종목코드.txt 생성 혹은 추가
     fs 딕셔너리 변수에 키가 종목코드 , 값이 해당 파일넘버로 추가한다.
    '''

    def filesOpen(self,l):

        hoga_path = 'C:/StockData/Hoga/'
        trading_path = 'C:/StockData/Trading/'
        
        today = datetime.now().strftime("%Y-%m-%d")
        
        for i in l:
            f_hoga = open(hoga_path + today + '-' + i + '.txt', 'w')
            f_trading = open(trading_path + today + '-' + i + '.txt', 'w')

            self.fs[i] = [ f_hoga, f_trading ]
            self.cnt[i] = 1
    
    def filesClose(self):

        for hoga, trading in self.fs.values():
            hoga.close()
            trading.close()

        print('files Closed')

 




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
    
    df = []
    with open('stock_code.txt','r') as f:
        while True:
            line = f.readline()
            if not line: break
            df.append(line[:6])

    nLen = len(df)
    print(nLen)
    collector = Kiwoom()
    collector.login(df)
    nSep = 100
    
    collector.setRealReg("1001", ltos(df[:nSep]), "41;15", 0)
    collector.setRealReg("1002", ltos(df[nSep:]), "41;15", 1)
    
    collector.wait()