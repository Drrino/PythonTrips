# 1.对百度贴吧的任意帖子进行抓取
# 2.指定是否只抓取楼主发帖内容
# 3.将抓取到的内容分析并保存到文件

import re
from urllib import request


class Tool:
    # 去除img标签,7位长空格
    removeImg = re.compile('<img.*?>| {7}|')
    # 删除超链接标签
    removeAddr = re.compile('<a.*?>|</a>')
    # 把换行的标签替换为\n
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    # 将表格制表<td>替换为\t
    replaceTD = re.compile('<td>')
    # 把段落开头换为\n加空两格
    replacePara = re.compile('<p.*?>')
    # 将换行符或双换行符替换为\n
    replaceBR = re.compile('<br><br>|<br>')
    # 将其余标签剔除
    removeExtraTag = re.compile('<.*?>')

    def replace(self, x):
        x = re.sub(self.removeImg, "", x)
        x = re.sub(self.removeAddr, "", x)
        x = re.sub(self.replaceLine, "\n", x)
        x = re.sub(self.replaceTD, "\t", x)
        x = re.sub(self.replacePara, "\n    ", x)
        x = re.sub(self.replaceBR, "\n", x)
        x = re.sub(self.removeExtraTag, "", x)
        # strip()将前后多余内容删除
        return x.strip()


class BDTB:
    def __init__(self, baseUrl, seeLZ, floorTag):
        self.baseURL = baseUrl
        self.seeLZ = '?see_lz=' + str(seeLZ)
        self.tool = Tool()
        # 全局file变量,文件写入操作对象
        self.file = None
        # 楼层标号
        self.floor = 1
        # 默认标题,未获取标题则使用百度贴吧
        self.defaultTitle = u"百度贴吧"
        # 是否写入楼分割符标记
        self.floorTag = floorTag

    # 传入页码，获取该页帖子的代码
    def getPage(self, pageNum):
        try:
            url = self.baseURL + self.seeLZ + '&pn=' + str(pageNum)
            tb_request = request.Request(url)
            tb_response = request.urlopen(tb_request)
            # print(tb_response.read())
            return tb_response.read().decode('utf-8')
        except request.URLError as e:
            if hasattr(e, "reason"):
                print(u"连接失败，失败原因", e.reason)
                return None

    # 帖子标题
    def getTitle(self, page):
        pattern = re.compile('<h3 class="core_title_txt.*?>(.*?)</h3>', re.S)
        result = re.search(pattern, page)
        if result:
            # print(result.group(1).strip())
            return result.group(1).strip()
        else:
            return None

    # 获取帖子总页数
    def getPageNum(self, page):
        pattern = re.compile('<li class="l_reply_num.*?</span>.*?<span.*?>(.*?)</span>', re.S)
        result = re.search(pattern, page)
        if result:
            # print(result.group(1))
            return result.group(1).strip()
        else:
            return None

    # 获取每一层楼的内容,传入页面内容
    def getContent(self, page):
        pattern = re.compile('<div id="post_content_.*?>(.*?)</div>', re.S)
        items = re.findall(pattern, page)
        contents = []
        for item in items:
            content = "\n" + self.tool.replace(item) + "\n"
            contents.append(content)
        return contents

    def setFileTitle(self, title):
        if title is not None:
            self.file = open(title + ".txt", "w+")
        else:
            self.file = open(self.defaultTitle + ".txt", "w+")

    def writeData(self, contents):
        for item in contents:
            if self.floorTag == '1':
                # 楼之间的分隔符
                floorLine = "\n" + str(self.floor) + u"-------------------------------------\n"
                self.file.write(floorLine)
            self.file.write(item)
            self.floor += 1

    def start(self):
        indexPage = self.getPage(1)
        pageNum = self.getPageNum(indexPage)
        title = self.getTitle(indexPage)
        self.setFileTitle(title)
        if pageNum is None:
            print("URL已失效,请重试")
            return
        try:
            print("该帖子共有" + str(pageNum) + "页")
            for i in range(1, int(pageNum) + 1):
                print("正在写入第" + str(i) + "页数据")
                page = self.getPage(i)
                contents = self.getContent(page)
                self.writeData(contents)
        except IOError as e:
            print("写入异常，原因" + e.message)
        finally:
            print("写入任务完成")


print(u"请输入帖子代号")
baseURL = 'http://tieba.baidu.com/p/' + str(input(u'http://tieba.baidu.com/p/'))
seeLZ = input("是否只获取楼主发言，是输入1，否输入0\n")
floorTag = input("是否写入楼层信息，是输入1，否输入0\n")
bdtb = BDTB(baseURL, seeLZ, floorTag)
bdtb.start()
