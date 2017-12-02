# coding=utf-8

#出于信息安全，删除了headers和post的一些信息，使用之前请自行填写调试

import requests
from bs4 import BeautifulSoup
import re
import xlrd
from xlutils.copy import copy

xls_file = 'Prostate_Cancer_Jan_Nov.xls'  #运行之前把修改此处的文件名

def get_Gleason(blh):
    headers = { #从chrome F12中获取
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'Cookie': '', #从chrome F12中获取
        'Host': '',  #从chrome F12中获取
        'Referer': '',#从chrome F12中获取
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    request_url = '' #从chrome F12中获取
    response = requests.get(request_url, data={'blh': blh}, headers=headers)
    # response.apparent_encoding=GB2312
    response.encoding = 'GB2312'
    text = response.text
    if re.search('收到日期', text) != None:
        receive_date = re.compile('收到日期:</font>\W*?<font size="3">(.*?)</font>').findall(text)[0]
        Gleason_Expressions = re.compile(r'Gleason.*?(\d.*?[=]\d{1,2})', re.I).findall(text.replace(' ', ''))
        if len(Gleason_Expressions) >= 1:
            Gleason_Expression = Gleason_Expressions[0]
            Gleason_Score = re.compile(r'=(\d{1,2})').findall(Gleason_Expression)[0]
            for Expression in Gleason_Expressions:
                Score = re.compile(r'=(\d{1,2})').findall(Expression)[0]
                if Score > Gleason_Score:
                    Gleason_Expression = Expression
                    Gleason_Score = Score
            return blh,receive_date, Gleason_Expression, Gleason_Score
        else:
            return blh,'No Gleason'
    else:
        return blh, 'No Report'   #此报告未审核！


def get_blh(zhy):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Length': '183',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': '', #随便获取一个Cookie就能用
        'Host': '',#从chrome F12中获取
        'Origin': '', #从chrome F12中获取
        'Referer': '', #从chrome F12中获取
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    post_data = {  # post_data内容直接复制F12大法里面的data
        'keywords_name': '',
        'keywords_brbh': '',
        'keywords_zyh': zhy,
        'keywords_mzh': '',
        'keywords_blh': '',
        'keywords_sjks': '',
        'keywords_rqxz': '',#从chrome F12中获取
        'keywords_bgrq1': '',
        'keywords_bgrq2': '',
        'Submit': '%B2%E9%D1%AF'
    }
    request_url = ''#从chrome F12中获取
    response = requests.post(request_url, data=post_data, headers=headers)
    # response.apparent_encoding=GB2312
    response.encoding = 'GB2312'
    soup = BeautifulSoup(response.text, 'html.parser')
    page_sum = re.search(r'第[\d]/[\d]页', soup.text)
    if page_sum == None:
        return None   #    此条件没有查询结果！
    else:
        all_blh = soup.find_all(target='index_m', id=True)
        return (page_sum,all_blh)

def write_Gleason_data(row, initial_col, data, s):
    col = initial_col
    for cell_data in data:
        print(cell_data)
        s.write(row, col, cell_data)
        col = col + 1
    return None

book = xlrd.open_workbook(xls_file)
sh = book.sheet_by_index(0)
print('表单{0}共{1}行{2}列'.format(sh.name,sh.nrows,sh.ncols))
wb = copy(book)
s = wb.get_sheet(0)
data_col = sh.ncols + 1  #起始列
for rownum in range(1,sh.nrows):
    zhy = sh.cell(rownum, 1).value
    print(zhy)
    if get_blh(zhy) == None:
        print('No blh')
        s.write(rownum, data_col, 'No blh')
    elif get_blh(zhy) != None:
        print(get_blh(zhy)[0])
        if get_blh(zhy) != None:
            for blh in get_blh(zhy)[1]:
                Gleason_data = get_Gleason(blh.text)
                print(Gleason_data)
                write_Gleason_data(rownum,data_col,Gleason_data,s)
wb.save(xls_file)




