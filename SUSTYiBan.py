#易班打卡,python接口封装
from requests import post, get
from utils import *


__all__ = ['checkInByCookies','checkInByPwd']

def login(mobile:str, pwd:str) -> dict:
    data = {
        'device': 'vivo AV1938T',
        'v': '5.0',
        'password': passworldEncode(pwd),
        'token': '',
        'mobile':mobile,
        'ct': '2',
        'identify': getIMEI(),
        'sversion': '25',
        'app': '1',
        'apn': 'wifi',
        'authCode': '',
        'sig': '5692393ff332462c'
    }
    header = {
        'User-Agent': USER_AGENT_YIBAN,
        'AppVersion': '5.0',
        'X-Requested-With': 'com.yiban.app',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://mobile.yiban.cn',
        'Referer': 'https://mobile.yiban.cn',
        'logintoken': ''
    }
    res = post('https://mobile.yiban.cn/api/v4/passport/login', headers=header, data=data)
    return res.json()

def getToken(response:dict) -> str:
    if 'data' not in response or 'access_token' not in response['data']:
        raise KeyError('target has not access_token')
    return response['data']['access_token']

def getCookies(token:str) -> str:
    header = {
        'User-Agent': USER_AGENT,
        'AppVersion': '5.0',
        'X-Requested-With': 'com.yiban.app',
        'Origin': 'http://f.yiban.cn',
        'logintoken': token,
        'Authorization': token,
        'Cookie': 'loginToken=' + token
    }
    res = get('http://f.yiban.cn/iapp610661', headers=header)
    cookies: str or list = res.headers['set-cookie']
    return ''.join(map(lambda x:x.split(';')[0] ,(filter(lambda a:a.find('waf_cookie=') == -1 ,(cookies if isinstance(cookies, list) else [cookies])))))

def checkInByCookies(code:int, cookies:str, location:str = None) -> dict:
    url = 'http://yiban.sust.edu.cn/v4/public/index.php/Index/formflow/add.html?desgin_id=13&list_id=9' if code == 13 else f' http://yiban.sust.edu.cn/v4/public/index.php/Index/formflow/add.html?desgin_id={code}&list_id=12'
    header = {
        'User-Agent': USER_AGENT,
        'AppVersion': '5.0',
        'X-Requested-With': 'com.yiban.app',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'http://yiban.sust.edu.cn',
        'Referer': url,
        'Cookie': cookies
    }
    data = getCheckData(code, randomTemperature(), location)
    res = post(url, data=data, headers=header)
    return res.json()

def checkInByPwd(mobile:str, pwd:str, code:int, location:str = None) -> dict:
    cookies = getCookies(getToken(login(mobile, pwd)))
    checkInByCookies(code, cookies, location)