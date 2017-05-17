# 1.对百度贴吧的任意帖子进行抓取
# 2.指定是否只抓取楼主发帖内容
# 3.将抓取到的内容分析并保存到文件
import re
from urllib import request


class BDTB:
    def __init__(self, baseUrl, seeLZ):
        self.baseURL = baseUrl
        self.seeLZ = '?seeLZ' + str(seeLZ)

    # 传入页码，获取该页帖子的代码
    def getPage(self, pageNum):
        try:
            url = self.baseURL + self.seeLZ + '&pn=' + str(pageNum)
            tb_request = request.Request(url)
            tb_response = request.urlopen(tb_request)
            # print(tb_response.read())
            return tb_response
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
            return result.group(1)
        else:
            return None


baseURL = 'http://tieba.baidu.com/p/3138733512'
bdtb = BDTB(baseURL, 1)
bdtb.getPage(1)
