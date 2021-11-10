import pyautogui as pg


## kiwoom windows form 이 생성되는 위치가 고정되있어 
## 현재 데스크탑에서의 그 위치로 고정해놓음
## 컴퓨터가 변경됐을 때 함께 변경해줘야함.
## 마우스 커서 위치 알려주는 소스코드 위치 : D:\MJ\python\getLocationMousePointer.py


def autoLogin():
    pg.click(x=945,y=506)
    pg.write('jin9409')
    pg.click(x=945,y=530)
    pg.write('haejin9409!@')
    pg.click(x=895,y=559)

autoLogin()
