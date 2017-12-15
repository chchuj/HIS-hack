#循环爬取某段日期内的报告

from datetime import datetime,timedelta
import datetime
from get_examlist import *


begin = datetime.date(2016, 9, 2)
end = datetime.date(2016, 12, 12)

date = begin
delta = datetime.timedelta(days=1)
while date <= end:
    try:
        image_report_crawler(date,'男')
    except Exception as e:
        logger.exception(e) #将会输出堆栈追踪信息
        continue
    finally:
        date += delta
