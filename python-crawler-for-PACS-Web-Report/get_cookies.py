# coding=utf-8
#登录并获取cookies
import requests
def get_cookies():
    headers = {
         'Accept': 'image/jpeg, application/x-ms-application, image/gif, application/xaml+xml, image/pjpeg, application/x-ms-xbap, application/vnd.ms-excel, application/vnd.ms-powerpoint, application/msword, */*',
        #'Accept': '*/*',
        'Referer': 'http://*/webreport/login.jsp',
        'Accept-Language':'zh-CN',
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0)',
        'Content-Type':'application/x-www-form-urlencoded',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'Keep-Alive',
        'Content-Length': '136',
        'DNT': '1',
        'Host': '*',
        'Pragma': 'no-cache',
        'Cookie': 'JSESSIONID=EF35D21E9D426258B720AD7C5EEE6B2E' #随便一个初始cookies
    }
    request_url = 'http://*/webreport/loginAction.jsp'
    params_data = {
        'monitorRes':'',
        'monitorResSF':'',
        'subAction':'login',
        'failCounts':'1',
        'lastUserName':'',
        'userName':'',
        'password':'',
        'hospital':'1',
        'loginButton':'%B5%C7++%C2%BC'
    }
    response = requests.post(request_url, data= params_data,headers=headers)
    print('JSESSIONID={0}'.format(response.cookies['JSESSIONID']))
    return 'JSESSIONID={0}'.format(response.cookies['JSESSIONID'])

if __name__ == '__main__':
    print(get_cookies())
