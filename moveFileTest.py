import os
import shutil

Droot = 'D:/MJ/stock/getData/kiwoom/'
Croot = 'C:/'
hogaPath = Croot+'hoga_folder/'
donePath = Droot+'origin_done_hoga_folder/'
removedPath= Droot+'removed_duplicates_hoga_folder/'

cFiles = os.listdir(hogaPath)

for file in cFiles:
    os.replace(hogaPath+file,donePath+file)
