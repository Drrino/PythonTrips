from urllib import request
from urllib import parse

# 抓取静态网页
# url_request = request.Request("http://www.baidu.com")
# url_response = request.urlopen(url_request)
# print(url_response.read())



# POST请求
# values = {'username': "xxxxxx@gmail.com", 'password': "xxxxx"}
# data = parse.urlencode(values).encode(encoding='UTF8')
# url = "http://passport.csdn.net/account/login?from=http://my.csdn.net/my/mycsdn"
# login_request = request.Request(url, data)
# login_response = request.urlopen(login_request)
# print(login_response.read())



# GET请求
# values = {'username': "xxxxxx@gmail.com", 'password': "xxxxx"}
# data = parse.urlencode(values)
# url = "http://passport.csdn.net/account/login"
# geturl = url + "?" + data
# print(geturl)
# login_get_request = request.Request(geturl)
# login_get_response = request.urlopen(login_get_request)
# print(login_get_response.read())



'''
User-Agent : 有些服务器或 Proxy 会通过该值来判断是否是浏览器发出的请求
Content-Type : 在使用 REST 接口时，服务器会检查该值，用来确定 HTTP Body 中的内容该怎样解析。
application/xml ： 在 XML RPC，如 RESTful/SOAP 调用时使用
application/json ： 在 JSON RPC 调用时使用
application/x-www-form-urlencoded ： 浏览器提交 Web 表单时使用
在使用服务器提供的 RESTful 或 SOAP 服务时， Content-Type 设置错误会导致服务器拒绝服务
'''
# 设置Headers
# url = 'https://www.zhihu.com/'
# user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 ' \
#              'Safari/537.36 '
# values = {'username': 'xxxxxx', 'password': 'xxxxxx'}
# headers = {'User-Agent': user_agent}
# data = parse.urlencode(values)
# headers_request = request.Request(url, data, headers)
# headers_response = request.urlopen(headers_request)
# page = headers_response.read()

# 代理设置
# enable_proxy = True
# proxy_handler = request.ProxyHandler({"http": 'http://some-proxy.com:8080'})
# null_proxy_handler = request.ProxyHandler({})
# if enable_proxy:
#     opener = request.build_opener(proxy_handler)
# else:
#     opener = request.build_opener(null_proxy_handler)
# request.install_opener(opener)


# DebugLog
# httpHandler = request.HTTPHandler(debuglevel=1)
# httpsHandler = request.HTTPSHandler(debuglevel=1)
# opener = request.build_opener(httpHandler, httpsHandler)
# request.install_opener(opener)
# response = request.urlopen('http://www.baidu.com')



# URLError
# req = request.Request('http://blog.csdn.net/cqcre')
# try:
#     request.urlopen(req)
# except request.HTTPError as e:
#     print(e.code)
# except request.URLError as e:
#     print(e.reason)
# else:
#     print("OK")

