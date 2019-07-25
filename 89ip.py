from urllib import request
import re

#爬取的网站
URL = "http://www.89ip.cn/index_%d.html"
#需要隐藏的User-Agent头部, 伪装成电脑用户访问
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"
#在网页中匹配出ip和端口号的正则表达式,预先编译,提高效率,会在getIp2Port函数中使用
RE = re.compile(r"(?:(?:[0,1]?\d?\d|2[0-4]\d|25[0-4])\.){3}(?:[0,1]?\d?\d|2[0-4]\d|25[0-4])\D*\d*", re.S)


def urlOpen(url):
	"""
	打开网页,并返回已解码的网页内容
	"""

	#创建请求
	ret = request.Request(url)
	#在请求中添加User-Agent头部
	ret.add_header("User-Agent", USER_AGENT)
	#发送请求打开网页,并接收响应
	response = request.urlopen(ret)
	#读取响应内容并解码
	html = response.read().decode("utf-8")

	return html

def getIp2Port(html):
	"""
	接收网页内容
	分析网页内容,并得到ip和端口号
	返回ip:port的列表
	"""
	#存储ip:port字符串的列表
	ip_port_list = []

	#匹配出ip和port的字符串
	ret_list = RE.findall(html)
	for ret in ret_list:
		#替换:
		ret1 = re.sub(r"</td>", ":", ret)
		#去除杂项
		ip_port = re.sub(r"[^0-9:\.]", "", ret1)
		ip_port_list.append(ip_port)

	return ip_port_list


if __name__ == "__main__":
	#创建存储ip和端口号的列表, 存储形式ip:port
	ip_port_list = []

	#循环打开网页
	for i in range(1,11):
		#构建网页地址
		url = URL % i
		#打开网页,接收网页内容
		html = urlOpen(url)
		#过滤网页并得到其中的ip和端口号列表ip:port形式
		ip_port_list.extend(getIp2Port(html))
	print(ip_port_list)