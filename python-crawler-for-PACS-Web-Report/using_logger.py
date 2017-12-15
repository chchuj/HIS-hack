#coding:utf-8

# http://www.csuldw.com/2016/11/05/2016-11-05-simulate-zhihu-login/

import logging

"""#EXAMPLE 
logger = createLogger('mylogger', 'temp/logger.log')
logger.debug('logger debug message')  
logger.info('logger info message')  
logger.warning('logger warning message')  
logger.error('logger error message')  
logger.critical('logger critical message')  
"""
def createLogger(logger_name='mylogger',log_file='log.ini',error_logfile='error_log.ini'):
    # 创建一个logger
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    # 创建一个handler，用于写入日志文件
    fh = logging.FileHandler(log_file)
    # 再创建一个handler，用于输出到控制台
    ch = logging.StreamHandler()
    # 定义handler的输出格式formatter
    formatter = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s | %(filename)s[:%(lineno)d] | %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # 给logger添加handler
    logger.addHandler(fh)
    logger.addHandler(ch)
    #创建一个handler，只收录error级别的日志
    error_handler = logging.FileHandler(error_logfile)
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    logger.addHandler(error_handler)
    return logger

logger = createLogger()

if __name__ == '__main__':
    # e = 'Errorsjflsdf'
    # index = 2
    # logger.error('\n{1}\n{0}'.format(e,index))
    # #Logger.exception()将会输出堆栈追踪信息
    # logger.exception('{1}\n{0}'.format(e,index))
    # logger.debug('debug message')
    # logger.info('info message')
    # logger.warning('warning message')
    logger.error('error message')
    # logger.critical('critical message')

    raise EOFError   #就算发生了错误，前面的log也已被写入文件
