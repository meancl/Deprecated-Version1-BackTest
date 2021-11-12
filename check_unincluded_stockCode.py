import os

li = os.listdir('C:/hoga_folder')
li2=[]
fs= []
for i in li:
    li2.append(i[11:17])
    
with open('D:/MJ/stock/getData/kiwoom/stock_code.txt','r') as f:
    while True:
        str = f.readline()
        if not str : break
        fs.append(str[0:6])

li2.sort()
fs.sort()

print(li2)
print(fs)

for i,v in enumerate(fs):
    if v != li2[i]:
        print(v)
        
