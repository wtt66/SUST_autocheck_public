from SUSTYiBan import *

a = checkInByPwd('1234234','1213321', 24, '中国 西藏 拉萨 靠近珠穆朗玛峰')
if 'code' not in a or a['code'] != 1:
    print('error in check')
else:
    print('check in success')