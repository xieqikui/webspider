# -*- coding:utf-8 -*-
from urllib import request
from urllib import robotparser
from urllib.parse import urljoin
from urllib.parse import urlparse
from datetime import datetime
import time
import re
import itertools

class Throttle:
	def __init__(self, delay):
		self.delay = delay
		self.domains = []
	def wait(self, url):
		domain = urlparse(url).netloc
		last_accessed = self.domains.get(domain)
		if self.delay > 0 and last_accessed is not None:
			sleep_secs = self.delay - (datetime.now() - last_accessed).seconds
			if sleep_secs > 0:
				time.sleep(sleep_secs)
		self.domains[domain] = datetime.now()

# 下载网页代码
def download(url, user_agent='wswp', proxy=None, num_retries=2):
	# return request.urlopen(url).read().decode('utf-8')
	print ('Downloading:', url)
	# 设置用户代理
	headers = {'User-agent':user_agent}
	req = request.Request(url, headers=headers)
	opener = request.build_opener()
	if proxy:
		proxy_params = {urlparse(url).scheme:proxy}
		opener.add_handler(request.ProxyHandler(proxy_params))
	try:
		# html = request.urlopen(url).read()
		res = request.urlopen(req)
		# print ('res.geturl()=', res.geturl())
		# print ('res.info()=', res.info())
		# print ('res.getcode()=', res.getcode())
		html = res.read()
	except request.URLError as e:
		print ('Download error:', e.reason)
		html = None
		# 当服务器发生错误码为5XX的异常时可以重复下载
		if num_retries > 0:
			if hasattr(e, 'code') and 500 <= e.code < 600:
				# print ('e.code=', e.code)
				# print ('num_retries=', num_retries)
				return download(url, user_agent, proxy, num_retries-1)
	return html
def crawl_sitemap(url):
	# 下载网站地图文件
	sitemap = download(url)
	print ('sitemap=', str(sitemap))
	# 提取网站链接
	pattern = re.compile('<loc>(.*?)</loc>')
	links = pattern.findall(str(sitemap))
	# 下载每一个链接指向的网页
	for link in links:
		print('link=', link)
		html = download(link)
def link_crawler(seed_url, link_regex, max_depth=2):
	crawl_queue = [seed_url]
	# seen = set(crawl_queue)
	seen = dict.fromkeys(crawl_queue, 0)
	while crawl_queue:
		url = crawl_queue.pop()
		rp = robotparser.RobotFileParser()
		rp.set_url('http://example.webscraping.com/robots.txt')
		rp.read()
		if not rp.can_fetch(user_agent, url):
			print ('Blocked by robots.txt:', url)
		else:
			html = download(url)
			depth = seen[url]
			if depth != max_depth:
				# print ('html=', html)
				for link in get_links(html):
					# if re.match(link_regex, link):
					if re.search(link_regex, link):
						link = urljoin(seed_url, link)	# 相对路径转化为绝对路径
						print ('link=', link)
						if link not in seen:
							seen[link] = depth + 1
							crawl_queue.append(link)
def get_links(html):
	webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
	return webpage_regex.findall(str(html))

if __name__ == '__main__':
	# url = 'https://www.so.com/s?ie=utf-8&src=se7_isearch&q=%E5%9C%A8%E7%BA%BF%E7%BF%BB%E8%AF%91'
	# url = 'http://httpstat.us/500'
	# url = 'http://example.webscraping.com/sitemap.xml'
	# max_errors = 5
	# num_errors = 0
	# for page in itertools.count(1):
	# 	url = 'http://example.webscraping.com/view/-{}'.format(page)
	# 	html = download(url)
	# 	if html is None:
	# 		num_errors += 1
	# 		if num_errors == max_errors:
	# 			break
	# 	else:
	# 		print(html)
	# 		num_errors = 0
	# download(url)
	# print (download(url))
	# crawl_sitemap(url)
	seed_url = 'http://example.webscraping.com'
	# link_regex = '(.*)/(index|view)'
	link_regex = '/(index|view)'
	link_crawler(seed_url, link_regex)