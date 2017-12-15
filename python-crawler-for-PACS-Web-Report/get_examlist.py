# coding=utf-8

#爬取并筛选某一天的报告
#系统的网址信息已删除

#通用电气医疗放射信息系统软件
#先登录网页，搜索条件，再从搜索结果中点开PDF链接。因此，主要流程就是先模拟登录，爬取搜索结果，进行筛选，最后用解析PDF内容。

import requests
import time
import datetime
import pandas as pd
from pandas import Series


from get_cookies import get_cookies
from get_specific_page import get_page
from ftp_pdf import *
from process_pdf import *


def image_report_crawler(date,sex='',department=''):
    cookies = get_cookies()
    headers = {        
        'Accept': '*/*',
        'Referer': 'http://*/webreport/worklist.jsp',
        'Accept-Language':'zh-CN',
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0)',
        'Content-Type':'application/x-www-form-urlencoded',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'Keep-Alive',
        'Content-Length': '87',
        'DNT': '1',
        'Host': '',
        'Pragma': 'no-cache',
        'Cookie': cookies
    }
    request_url = 'http://*/webreport/WebReportAction.do?ran=0.9087775843843873'
    params_data = {
        'eventaction':'search',
        '2':'',
        '3':'',
        '4':'',
        '5':'',
        '6':date.strftime('%Y-%m-%d'),
        '7':'6', # 已审核
        'sex':sex.encode('GBK'),
        # 'sex':'男',
        'level':'',
        'department': department.encode('GBK'),  #charset=GBK
        # 'department': '',
        'modality':''
    }
    response = requests.post(request_url, data= params_data,headers=headers)
    #requests.post的参数是data，requests.get的参数是 params
    # response.apparent_encoding=GB2312
    response.encoding = 'GBK'

    html = response.text
    # print(html)
    if re.search('没有查询到任何记录',html) is not None:
        logger.info('{0} 没有查询到任何记录'.format(date))
    else:
        if re.search('top\.location\.replace',html)!=None:
            cookies = get_cookies()
            headers['Cookie']=cookies
            response = requests.post(request_url, data=params_data, headers=headers)
            response.encoding = 'GBK'
            html=response.text

        pdflinks = re.compile(r'openReport\(\'(.*?\.pdf).*?(\d{2,}).*?\)',re.S).findall(html)
        s = Series({eval(pdflink[1]):pdflink[0] for pdflink in pdflinks})
        tables = pd.read_html(html)
        sp500_table = tables[0]
        sp500_table.index = sp500_table[2] #第3列数据是检查号，把它设为index
        sp500_table['pdflink']= s #将链接合并入文字表格
        sp500_table = sp500_table.dropna(how='all') #删除全空的行
        page_sum = eval(re.search(r'当前(\d+)/(\d+)页',html)[2])
        print(page_sum)
        if page_sum >1: #从首页读取总页数，若有多页就继续请求分页数据并进行合并
            for page in range(2,page_sum+1):
                # page_table=get_page(page,cookies)
                # print(page_table.shape)
                sp500_table=sp500_table.append(get_page(page,cookies))
        print(sp500_table.shape)
        sp500_table= sp500_table.loc[sp500_table[12].str.contains('CT|MR')]
        get_count, pass_count, error_pdf = 0,0,0
        for exam in sp500_table.index:
            try:
                exam_report = sp500_table.loc[exam][16]
                print('exam_report: {0}'.format(exam_report))
                file_name = exam_report[(exam_report.rfind('/') + 1):]
                print('file_name: {0}'.format(file_name))
                remotepath = exam_report[(exam_report.rfind('ftprazor')+9):(exam_report.rfind('/') + 1)]
                print('remotepath: {0}'.format(remotepath))
            except Exception as e:
                logger.error('{0}\n{1} error\n Failed to fetch examreport url'.format(e,exam))
                continue
            else:
                try:
                    ftpconnect()
                    localpath=downloadfile(remotepath,file_name)
                    ftpdisconnect()
                    if localpath is not None:
                        get_count, pass_count, error_pdf=process_pdf(exam,localpath,get_count, pass_count, error_pdf)
                except Exception as e:
                    logger.critical(e)
                    time.sleep(5)
                    try:
                        ftpconnect()
                        localpath = downloadfile(remotepath, file_name)
                        ftpdisconnect()
                        if localpath is not None:
                            get_count, pass_count, error_pdf = process_pdf(exam, localpath, get_count, pass_count,
                                                                           error_pdf)
                    except Exception as e2:
                        logger.exception(e2)
                        continue
                else:
                    print('date:{0},page: {1},filter results:{2},\n {3} get, {4} pass, {5} error pdf'.format(
                        date.strftime('%Y-%m-%d'), page_sum, sp500_table.shape, get_count, pass_count, error_pdf))
        logger.critical('date:{0},page: {1},filter results:{2},\n {3} get, {4} pass, {5} error pdf'.format(date.strftime('%Y-%m-%d'),page_sum,sp500_table.shape,get_count, pass_count, error_pdf))



if __name__ == '__main__':
    date = datetime.datetime(2016, 1, 5)
    print(date)

    image_report_crawler(date,'男')
    #todo for sex ='男' check '子宫'
