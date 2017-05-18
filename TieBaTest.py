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
    def __init__(self, baseUrl, seeLZ):
        self.baseURL = baseUrl
        self.seeLZ = '?seeLZ' + str(seeLZ)
        self.tool = Tool()

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
    def getTitle(self):
        page = self.getPage(1)
        pattern = re.compile('<h3 class="core_title_txt.*?>(.*?)</h3>', re.S)
        result = re.search(pattern, page)
        if result:
            # print(result.group(1).strip())
            return result.group(1).strip()
        else:
            return None

    # 获取帖子总页数
    def getPageNum(self):
        page = self.getPage(1)
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
        floor = 1
        for item in items:
            print(floor,u"楼-----------------------------------------------------------------------")
            print(self.tool.replace(item))
            floor +=1


baseURL = 'http://tieba.baidu.com/p/3138733512'
bdtb = BDTB(baseURL, 1)
bdtb.getContent(bdtb.getPage(1))
