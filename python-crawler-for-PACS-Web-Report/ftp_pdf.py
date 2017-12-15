from using_logger import *
# -*- coding: UTF-8 -*-
__author__ = 'test'
#http://www.cnblogs.com/hfclytze/p/ftplib.html 
#!/usr/bin/python
from ftplib import FTP       #加载FTP模块
import sys,os,socket
#定义与ftp连接相关的参数
CONST_HOST = ''  #定义常量保存ftp服务器ip
CONST_PORT = 21
CONST_TIMEOUT = 30
CONST_USERNAME = ''
CONST_PWD = ''

#定义与项目相关的参数
CONST_PRONAME = 'proname'
CONST_LOCALPATH = 'PDF\\'#定义文件下载保存到本地的路径
# CONST_VERSIONNUM = 'versionnum'#定义自动构建本次的版本号，与路径拼接形成文件下载路径

buffersize = 1024  #设置缓冲区大小

ftp = FTP()#设置变量

def ftpconnect():#定义ftp连接方法
    try:
        ftp.connect(CONST_HOST,CONST_PORT,CONST_TIMEOUT)#连接ftp服务器
    except (socket.error,socket.gaierror):
        # print('ERROR:cannot reach %s' %CONST_HOST)
        logger.error('ERROR:cannot reach %s' %CONST_HOST)
        sys.exit(0)
        return
    else:
        print('***Connected to host %s' %CONST_HOST)
        # logger.info('***Connected to host %s' %CONST_HOST)

    try:
        ftp.login(CONST_USERNAME,CONST_PWD)#登录ftp
        #ftp.set_debuglevel(2) #打开调试级别2，显示详细信息
    except ftplib.error_perm:
        print('ERROR: cannot login %s' %CONST_HOST + 'please check the host,username and password!')
        ftpdisconnect()
        return
    else:
        print('*** Logged in %s' %CONST_HOST)
        print(ftp.getwelcome()) #获得欢迎信息
        return ftp

def ftpdisconnect():
    ftp.quit()#退出FTP服务器

def downloadfile(remotepath,filename):
    # versionnum = raw_input("请输入本次部署版本号：")
    # remotepath = CONST_PRONAME + '/11.Tags/Build' + versionnum + '/Release/' #定义ftp的路径

    localpath = CONST_LOCALPATH + filename #定义本地保存的文件路径

   #***设置ftp的路径***
    try:
        ftp.cwd(remotepath)
    # except ftplib.error_perm:
    except :
        # print('ERROR cannot CD to %s ' %remotepath)
        logger.error('ERROR cannot CD to %s ' %remotepath)
        ftpdisconnect()
        return
    else:
        print('*** Check file from folder %s ' %remotepath)

    #***传一个回调函数给retrbinary() 它在每接收一个二进制数据时都会被调用
    try:
        f = open(localpath,'wb')  #打开要保存的文件，f.write是以写模式打开本地要保存的文件
        ftp.retrbinary('RETR %s' % filename,f.write,buffersize) #接收服务器上文件并保存在本地文件
    # except ftplib.error_perm:
    except :
        # print('ERROR: cannot read file %s' %filename)
        logger.error('ERROR: cannot read file %s' %filename)
        os.unlink(filename)
    else:
        print('*** Downloaded %s to ' %filename + CONST_LOCALPATH + 'Success')
        return localpath
    f.close()
    #ftp.set_debuglevel(0)#关闭调试模式
    return


if __name__ == "__main__":
    filename = '1478414.pdf'  # 定义需要下载的文件名称
    remotepath = 'report/20171102'
    ftpconnect()
    downloadfile(remotepath,filename)
    ftpdisconnect()


