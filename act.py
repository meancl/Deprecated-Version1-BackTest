import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
import time
import pandas as pd

    # QAxWidget 상속받음
class Kiwoom(QAxWidget):
    def __init__(self):

        super().__init__()
        self._create_kiwoom_instance()
        self._set_signal_slots()
        
        self.num_limit = 200

        ## 가격변화를 체크하기 위한 변수들 #### 
        self.steps_dict = {}
        self.prev_price_dict = {}
        self.price_change_list_dict = {}
        self.which_step= {}
            
    def _create_kiwoom_instance(self):
        self.setControl("KHOPENAPI.KHOpenAPICtrl.1")

    def _set_signal_slots(self):
        # 로그인할 시 OnEventConnect 이벤트 발생
        self.OnEventConnect.connect(self._handler_login)
        # 실시간 이벤트 수신 이벤트
        self.OnReceiveRealData.connect(self._handler_real_data)

    def login(self,df):

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

        if real_type == "주식호가잔량":

            time = self.get_comm_realdata(code, 21)

            s3 = self.get_comm_realdata(code, 43)
            sv3 = self.get_comm_realdata(code, 63)
            s2 = self.get_comm_realdata(code, 42)
            sv2 = self.get_comm_realdata(code, 62)
            s1 = self.get_comm_realdata(code, 41)
            sv1 = self.get_comm_realdata(code, 61)

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
            
            # 갭 구하기
            # s1 - b1 이 법적근거에 의한 차이( 5,10,50,...)을 넘어섰으면
            # 급격한 변동으로 잠시 사라진거라고 생각해볼 수 있음


            # 현재 - 10 , 현재 - 26, 현재 -  46, 인덱스들
            # 변동폭 , 기울기, 카운트, 시간차(?)
            # 이전가격과 현재가격 비교
            # 틀리다면
            # idx 를 1로 초기화한다
            # 현재인덱스와 기록인덱스가 특정값 이상이면 
            # 변동폭에 abs(가격 차이)를 더해주고
            # 기울기에 가격 차이를 더해주고
            # 카운트를 1 올려주고

           
            # 매수잔량 ,매도잔량의 차이 구하기
            # 비율로 구하는게 괜찮을 듯한데
            # 일단 매수잔량 전 잔량을 구하기 
            

            ### 분석이 나올 구간 ###


        elif real_type == '주식체결':
            
            time = self.get_comm_realdata(code, 20)
            tp = self.get_comm_realdata(code, 10) # 현재가, 체결가
            tr = self.get_comm_realdata(code, 12) # 등락률
            tv = self.get_comm_realdata(code, 15)  # trading volume
            trr = self.get_comm_realdata(code, 31) # 거래회전율
            ts = self.get_comm_realdata(code, 228) # trading strength
            fs = self.get_comm_realdata(code, 27) # 최우선 매도호가
            fb = self.get_comm_realdata(code, 28) # 최우선 매수호가
            market = self.get_comm_realdata(code, 290) #장구분
            
             # 단기체결강도
            # 상대적매수량들, 상대적매도량들, 인덱스들, 그때의 값 ,매수/매도 플래그들
            # * 들의 갯수는 구하려는 체결강도의 수와 같다
            # 현재 체결가가 매도가에 매수한거면 매수량을 늘려주고
            # 현재 체결가가 매수가에 매도했다면 매도량을 늘려준다.
            # 현재인덱스와 인덱스가 특정값 이상 차이 난다면
            # 그때의 값을 플래그에 맞는 잔량에 차감을 시켜준다.
            
            # 단기체결빈도강도 
            # 상대적매수빈도들 , 상대적매도빈도들, 인덱스들 , 매수/매도 플래그들
            # 단기체결강도 기능안에 첨가해도 된다.



    def setRealReg(self, screen_no, code_list, fid_list, real_type):
        self.dynamicCall("SetRealReg(QString, QString, QString, QString)",
                        screen_no, code_list, fid_list, real_type)
        print("구독 신청 완료")

    def disconnect_realdata(self, screenNo):
        self.dynamicCall("DisconnectRealData(QString)", screenNo)
        print("구독 해지 완료")

    def get_comm_realdata(self, code, fid):
        data = self.dynamicCall("GetCommRealData(QString, int)", code, fid)
        return data











    
    # e.g.  [종목코드1, 종목코드2]  -->  '종목코드1;종목코드2'
def make_kiwoom_code(stock_code_list):

    code_str = ''

    for stock in stock_code_list:
        code_str += stock
        code_str += ';'

    code_str = code_str[:-1]
    print(code_str)

    return code_str


'''
Kiwoom 클래스는 QAxWiget 클래스를 상속받았기 때문에
Kiwoom 클래스에 대한 인스턴스를 생성하려면 먼저 QApplication 클래스의 인스턴스를 생성해야함
'''

app = QApplication(sys.argv)
        
today_stock_list = []

with open('stock_code.txt','r') as f:
    while True:
        line = f.readline()
        if not line:
            break
        today_stock_list.append(line[:6])

len_stocks = len(today_stock_list)
print(len_stocks)
collector = Kiwoom()
collector.login(today_stock_list)
nSep = 100
        
collector.setRealReg("1001", make_kiwoom_code(today_stock_list[:nSep]), "41;15", 0)

collector.wait()