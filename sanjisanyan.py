# 来自 https://gscfwid.github.io/computer/%E6%95%99%E7%A8%8B/2017/08/18/sanjisanyanpy.html


import json
import requests

# 首先将cookie文件保存：cookie文件可以理解为远端服务器对请求的计算机的辨认，如果是已经登录的用户，远端计算机会保存该cookie，并且会跟请求数据中的cookie匹配
# zsy_cookie={'JSESSIONID':'FF03EDF2907CC8995205485D52438964'}
# cookies不定期刷新
s = requests.Session()
# request.Session是requests模块中的一个类，在同一系列请求中保证服务器对其的识别
# headers是请求的头文件，这个数据尽量全，以保证服务器对该请求辨识为浏览器的请求而不是机器请求，尤其是User-Agent这一条
headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6,ja;q=0.5',
    'Connection': 'keep-alive',
    'Host':'sum.medu2011.com',
    'Cookie': 'JSESSIONID=0D7AA53641F78FF8784CC29D5F8DD7EB',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
    'Referer': 'https://sum.medu2011.com/zsy/pages/common/model_test.jsp?planlevelid=11950',
    'X-Requested-With': 'XMLHttpRequest',
    'DNT': '1'
}

# 在这里定义一个函数，通过list中的dict的某键值定位该dict的索引，用于后面数据的提取


def find_dict(lst, key, value):
    for i, d in enumerate(lst):
        if d.get(key) == value:
            return i
    raise ValueError('no dict with the key and value combination found')

# 写一个循环，请求每个试题，并且保存成不同的文件


for x in range(10130, 10140): # 包前不包后
    # file_name = './anes'+str(x)+'.txt'

    # url = r'https://sum.medu2011.com/zsy/paper/createPaperByPlanLevelId.do?planLevelId='+str(x)
    # req = s.get(url, headers=headers)
    url = r'https://sum.medu2011.com/zsy/paper/createPaperByPlanLevelId.do'
    req = s.get(url, params={'planLevelId': x}, headers=headers)
    print(req.content)
    html = json.loads(req.content)
    # html输出为前面提到的包含正确答案和题目的字典，我在文末添加了该文件字段的截图
    # 后面为对html这个json文件的处理，保存为各自的文件。这个处理的基础是对html的解读
    corr_an = html["correctAnswer"]
    print(corr_an)
    quests = json.loads(html["data"])
    print(quests)
    questions = quests['ques']
    # print type(questions)
    level_name = questions[0]['level_name']  # 试卷名称
    print(level_name)
    text = ''
    i = 0  # 起始题号
    for a in corr_an:
        i = i + 1
        select = a["text"]  # 正确选项号
        qid = a["question_id"]
        num = find_dict(questions, "id", qid)
        quest_text = questions[num]["text"] #题干
        anss = questions[num]["anss"]
        # num2 = find_dict(anss, "orderby", select)
        # ans = anss[num2]["text"]  # 正确选项文字
        # text = str(qid)+'.'+' '+quest_text+'\t'+ans+'\n'
        # # with open(file_name, "a+") as f:
        # #     f.write(text)
        text = text + str(i) + '-'+str(qid)+'.'+' '+quest_text+':\t'+'->'+select+'\n'
        # print(text)
        # for choice in ['A','B','C','D','E']:
        #     num2 = find_dict(anss, "orderby", choice)
        #     choice_text= anss[num2]['text']
        #     text = text + choice + '. '+ choice_text +'\n'
        for choice in anss:
            text = text + choice['orderby'] + '. ' + choice['text'] +'\n'
    text = level_name + str(i)+'题\n' + text
    print(text)
    file_name = './anes'+str(x)+'_'+level_name+str(i)+'.txt'
    with open(file_name, "a+", encoding='utf-8') as f:  #  系统的gbk没办法encode
        f.write(text)  #  循环结束再一波写入
