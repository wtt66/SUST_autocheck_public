#易班打卡,python接口封装
from requests import post, get
from re import search
from utils import *
import sys

__all__ = ['checkInByCookies','checkInByPwd','checkUser','userSure','getTokenByPwd']

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

def getTokenByPwd(mobile:str, pwd:str) -> str:
    return getToken(login(mobile, pwd))

def userSure(data:str, cookies:str, token:str) -> bool:
    '''
    仅当需要授权并且授权成功会返回True, 其余返回False
    '''
    if data.find('易班授权') == -1:
        return False
    client_id = search(r'id="client_id" value="(.+?)"', data)
    redirect_uri = search(r'id="redirect_uri" value="(.+?)"',data)
    state = search(r'id="state" value="(.*?)"',data)
    display = search(r'id="display" value="(.+?)"',data)
    if client_id == None or redirect_uri == None or state == None or display == None:
        return False
    url = 'https://oauth.yiban.cn/code/usersure'
    data1 = {
        'client_id':client_id.group(),
        'redirect_uri':redirect_uri.group(),
        'state':state.group(),
        'display':display.group(),
        'scope':'1,2,3,4,'
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'cookies': cookies,
        'logintoken': token,
        'Authorization': token,
        'Origin': 'https://oauth.yiban.cn'
    }
    res = post(url, data=data1, headers=headers)
    if res.status_code != 200:
        raise ValueError("认证失败")
    return True

def getCookies(token:str, shouldEnsure = True) -> str:
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
    cookies:str = ''.join(map(lambda x:x.split(';')[0] ,(filter(lambda a:a.find('waf_cookie=') == -1 ,(cookies if isinstance(cookies, list) else [cookies])))))
    if shouldEnsure and userSure(res.content.decode(), cookies, token):
        return getCookies(token, False)
    return cookies

def checkInByCookies(code:int, cookies:str, location:str = None) -> dict:
    url = 'http://yiban.sust.edu.cn/v4/public/index.php/Index/formflow/add.html?desgin_id=13&list_id=9' if code == 13 else f'http://yiban.sust.edu.cn/v4/public/index.php/Index/formflow/add.html?desgin_id={code}&list_id=12'
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
    return checkInByCookies(code, cookies, location)

def checkUser(userData:dict, code:int) -> dict:
    '''
    单个用户打卡
    :param userData:用户数据, 必须包含name, mobile, password. 可以包含location
    :param code:打卡的代码
    '''
    loc = None if 'location' not in userData else userData['location']
    res = None
    try:
        res = checkInByPwd(userData['mobile'], userData['password'], code, loc)
    except ValueError as valueError:
        raise valueError
    except:
        raise ValueError("Something unexpect happened")
    return res

def main():
    img = '''
    =@@@@@@* @@^    *@@  =@@@@@@*@@@@@@@@@*          /@@`               ]/               /@@@@@@^ @@*                        @@*                 
   *@@       @@^    *@@ *@@         =@^             =@^@@    .]*   ,]  ]@@]]    ]]]`   ,@@*       @@*,]]*     ,]]`     ,]]]  @@*  ,]*
    ,@@\`    @@^    *@@  ,@@\`      =@^            =@/ =@\   =@^   =@^ [@@[[ ,@@` ,\@^ @@^        @@@` \@\  /@/ ,\@` /@/` ,` @@*,@@` 
       [@@@* @@^    *@@     [@@@*   =@^    @@@@@  *@@]]]@@^  =@^   =@^  @@   @@*    @@ @@`        @@*   @@ =@@@@@@@^=@^      @@@@`   
         =@^ =@^    =@^       =@^   =@^           @@[[[[[@@` =@^   @@^  @@   \@`   .@@ =@@        @@*   @@ =@\      ,@\      @@,@@`  
   *@@@@@@/*  \@@@@@@/  *@@@@@@/*   =@^          =@^     ,@@ .@@@@@@@^  =@@@` \@@@@@/   *\@@@@@@^ @@*   @@  ,@@\/@@  ,@@@@@^ @@* =@@`
    '''
    print(img)
    if len(sys.argv) < 4:
        print(f'[-]please use: python SUSTYiBan.py [code] [phone] [password] [None|location]')
        print(f'24 -> 晨检查\n25 -> 午检')
        print('location -> 一定要加上双引号,地区之吉间空格隔开')
        return
    checkInByPwd(sys.argv[2], sys.argv[3], sys.argv[1])

if __name__ == '__main__':
    main()