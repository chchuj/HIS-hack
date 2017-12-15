# coding=utf-8
#获取分页的数据
import requests
import re
import pandas as pd
from pandas import Series

from get_cookies import get_cookies
'''
发送于一个POST请求之后，查询的信息储存于cookies中
请求第2页之后的信息，只需要用POST时用的cookies去GET就行了
'''

def get_page(page_num,cookies):
    headers = {
        # 'Accept': 'image/jpeg, application/x-ms-application, image/gif, application/xaml+xml, image/pjpeg, application/x-ms-xbap, application/vnd.ms-excel, application/vnd.ms-powerpoint, application/msword, */*',
        'Accept': '*/*',
        'Referer': 'http://*/webreport/WebReportAction.do?ran=0.822530304614348',
        'Accept-Language':'zh-CN',
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0)',
        'Content-Type':'application/x-www-form-urlencoded',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'Keep-Alive',
        # 'Content-Length': '87',
        'DNT': '1',
        'Host': '*',
        # 'Pragma': 'no-cache',
        'Cookie': cookies
    }
    request_url = 'http://*/webreport/searchreportlist.jsp'
    # page可以直接放在request_url里面，也可以做为requests.get.params传递
    response = requests.get(request_url,params=dict(page=page_num),headers=headers) #这里用post也行

    response.encoding = 'GBK'
    html = response.text
    if re.search('top\.location\.replace', html) != None:
        headers['Cookie'] = get_cookies()
        response = requests.post(request_url, data=params_data, headers=headers)
        response.encoding = 'GBK'
        html = response.text
    pdflinks = re.compile(r'openReport\(\'(.*?\.pdf).*?(\d{2,}).*?\)', re.S).findall(html)
    s = Series({eval(pdflink[1]): pdflink[0] for pdflink in pdflinks})
    tables = pd.read_html(html)
    sp500_table = tables[0]
    sp500_table.index = sp500_table[2]
    sp500_table['pdflink'] = s  # 将链接合并入文字表格
    sp500_table = sp500_table.dropna(how='all')  # 删除全空的行
    return sp500_table
if __name__ == '__main__':
    cookies = ''
    page_num = 2
    get_page(2,cookies)
