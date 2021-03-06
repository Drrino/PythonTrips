# 1.抓取糗事百科热门段子
# 2.过滤带有图片的段子
# 3.实现每按一次回车显示一个段子的发布时间，发布人，段子内容，点赞数。

# page = 1
# url = 'http://www.qiushibaike.com/hot/page/' + str(page)
# user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64)'
# headers = {'User-Agent': user_agent}
# data_request = request.Request(url, headers=headers)
# data_response = request.urlopen(data_request)
# try:
#     content = data_response.read().decode('utf-8')
#     pattern = re.compile('<div.*?class="author.*?>.*?<a.*?</a>.*?<a.*?>(.*?)</a>.*?<div.*?class' +
#                          '="content".*?title="(.*?)">(.*?)</div>(.*?)<div class="stats.*?class="number">(.*?)</i>',re.S)
#     items = re.findall(pattern, content)
#     for item in items:
#         print(item[0], item[1], item[2], item[3], item[4])
# except request.URLError as e:
#     if hasattr(e, "code"):
#         print(e.code)
#     if hasattr(e, "reason"):
#         print(e.reason)
import re
from urllib import request


class QSBK:
    # 初始化方法，定义变量
    def __init__(self):
        self.pageIndex = 1
        self.user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64)'
        self.headers = {'User-Agent': self.user_agent}
        self.stories = []
        self.enable = False

    # 传入某一页的索引获得页面代码
    def getPage(self, pageIndex):
        try:
            url = 'http://www.qiushibaike.com/hot/page/' + str(pageIndex)
            qb_request = request.Request(url, headers=self.headers)
            qb_response = request.urlopen(qb_request)
            pageCode = qb_response.read().decode('utf-8')
            return pageCode
        except request.URLError as e:
            if hasattr(e, "reason"):
                print(u"连接糗事百科失败,错误原因", e.reason)
                return None

    # 传入某一页代码，返回本页不带图片的段子列表
    def getPageItems(self, pageIndex):
        pageCode = self.getPage(pageIndex)
        if not pageCode:
            print("页面加载失败")
            return None
        print(pageCode)
        pattern = re.compile('h2>(.*?)</h2.*?content">(.*?)</.*?number">(.*?)</', re.S)
        items = re.findall(pattern, pageCode)
        pageStories = []
        for item in items:
            pageStories.append([item[0].strip(), item[1].strip(), item[2].strip()])
        return pageStories

    # 加载并提取页面的内容，加入到列表中
    def loadPage(self):
        if self.enable:
            if len(self.stories) < 2:
                pageStories = self.getPageItems(self.pageIndex)
                if pageStories:
                    self.stories.append(pageStories)
                    self.pageIndex += 1

    # 调用该方法，每次敲回车打印输出一个段子
    def getOneStory(self, pageStories, page):
        for story in pageStories:
            user_input = input()
            self.loadPage()
            if user_input == "Q":
                self.enable = False
                return
            # print(u"第%d页\t发布人:%s\t发布时间:%s\t赞:%s\n%s" % (page, story[0], story[2], story[3], story[1]))
            print(u"第%d页\t发布人：%s\t 赞：%s\n%s" % (page, story[0], story[2], story[1]))

    def start(self):
        print(u"正在读取糗事百科,按回车查看新段子，Q退出")
        self.enable = True
        self.loadPage()
        nowPage = 0
        while self.enable:
            if len(self.stories) > 0:
                pageStories = self.stories[0]
                nowPage += 1
                del self.stories[0]
                self.getOneStory(pageStories, nowPage)


spider = QSBK()
spider.start()
