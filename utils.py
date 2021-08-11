import rsa
import base64
import random

__all__ = ('passworldEncode', 'randomTemperature', 'getIMEI', 'USER_AGENT', 'USER_AGENT_YIBAN','getCheckData','randomTemperature')

pubkey = '''-----BEGIN PUBLIC KEY-----
MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEA6aTDM8BhCS8O0wlx2KzA
Ajffez4G4A/QSnn1ZDuvLRbKBHm0vVBtBhD03QUnnHXvqigsOOwr4onUeNljegIC
XC9h5exLFidQVB58MBjItMA81YVlZKBY9zth1neHeRTWlFTCx+WasvbS0HuYpF8+
KPl7LJPjtI4XAAOLBntQGnPwCX2Ff/LgwqkZbOrHHkN444iLmViCXxNUDUMUR9bP
A9/I5kwfyZ/mM5m8+IPhSXZ0f2uw1WLov1P4aeKkaaKCf5eL3n7/2vgq7kw2qSmR
AGBZzW45PsjOEvygXFOy2n7AXL9nHogDiMdbe4aY2VT70sl0ccc4uvVOvVBMinOp
d2rEpX0/8YE0dRXxukrM7i+r6lWy1lSKbP+0tQxQHNa/Cjg5W3uU+W9YmNUFc1w/
7QT4SZrnRBEo++Xf9D3YNaOCFZXhy63IpY4eTQCJFQcXdnRbTXEdC3CtWNd7SV/h
mfJYekb3GEV+10xLOvpe/+tCTeCDpFDJP6UuzLXBBADL2oV3D56hYlOlscjBokNU
AYYlWgfwA91NjDsWW9mwapm/eLs4FNyH0JcMFTWH9dnl8B7PCUra/Lg/IVv6HkFE
uCL7hVXGMbw2BZuCIC2VG1ZQ6QD64X8g5zL+HDsusQDbEJV2ZtojalTIjpxMksbR
ZRsH+P3+NNOZOEwUdjJUAx8CAwEAAQ==
-----END PUBLIC KEY-----'''

key:rsa.PublicKey = rsa.PublicKey.load_pkcs1_openssl_pem(pubkey)
USER_AGENT:str = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
USER_AGENT_YIBAN:str = 'YiBan/5.0 Mozilla/5.0 (Linux; Android 7.1.2; V1938T Build/N2G48C; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.70 Safari/537.36'

def passworldEncode(pwd:str) -> bytes:
    return base64.encodebytes(rsa.encrypt(pwd.encode(), key))

def randomTemperature()->str:
    return '36.'+str(random.randint(0,10))


def getIMEI()->str:
    s = '86'.join(random.sample('012345678900000', 12))
    return s+getMod10(s)

def getCheckData(code:int, temperature:str, loc:str = None) -> dict:
    tar_dic = None
    loc = '陕西省 西安市 未央区 111县道 111县 靠近陕西科技大学学生生活区' if loc == None else loc
    if code == 24:
        tar_dic = {
            '24[0][0][name]': 'form[24][field_1588749561_2922][]',
            '24[0][0][value]': temperature,
            '24[0][1][name]': 'form[24][field_1588749738_1026][]',
            '24[0][1][value]': loc,
            '24[0][2][name]': 'form[24][field_1588749759_6865][]',
            '24[0][2][value]': '是',
            '24[0][3][name]': 'form[24][field_1588749842_2715][]',
            '24[0][3][value]':'否',
            '24[0][4][name]': 'form[24][field_1588749886_2103][]',
            '24[0][4][value]': ''
        }
    elif code == 25:
        tar_dic = {
            '25[0][0][name]': 'form[25][field_1588750276_2934][]',
            '25[0][0][value]': temperature,
            '25[0][1][name]': 'form[25][field_1588750304_5363][]',
            '25[0][1][value]': loc,
            '25[0][2][name]': 'form[25][field_1588750323_2500][]',
            '25[0][2][value]': '是',
            '25[0][3][name]': 'form[25][field_1588750343_3510][]',
            '25[0][3][value]':'否',
            '25[0][4][name]': 'form[25][field_1588750363_5268][]',
            '25[0][4][value]': ''
        }
    elif code == 13:
        tar_dic={
            '13[0][0][name]':'form[13][field_1587635120_1722][]',
            '13[0][0][value]':temperature,
            '13[0][1][name]':'form[13][field_1587635142_8919][]',
            '13[0][1][value]':'正常',
            '13[0][2][name]':'form[13][field_1587635252_7450][]',
            '13[0][2][value]':loc,
            '13[0][3][name]':'form[13][field_1587635509_7740][]',
            '13[0][3][value]':'否',
            '13[0][4][name]':'form[13][field_1587998920_6988][]',
            '13[0][4][value]':'0',
            '13[0][5][name]':'form[13][field_1587998777_8524][]',
            '13[0][5][value]':'否',
            '13[0][6][name]':'form[13][field_1587635441_3730][]',
            '13[0][6][value]':''
        }
    return tar_dic

def getPn(n, arr1):
    if n == 1:
        return 10
    else:
        return mod10(getSn(n - 1, arr1)) * 2

# 求特定的取余10的结果
def mod10(num):
    if num % 10 == 0:
        return 10
    else:
        return num % 10

# 求Sn
def getSn(n, arr1):
    return getPn(n, arr1) % 11 + int(arr1[14-n+1])

# 求校验码
def getMod10(code):
    c = code + 'x,'
    arr1 = []
    for i in reversed(c):
        arr1.append(i)
    for j in range(0, 10):
        arr1[1] = str(j)
        if getSn(14, arr1) % 10 == 1:
            result = ''.join(list(reversed(arr1)))
            return result[:len(result) - 1]