#! /usr/bin/env python3
# -*- coding:utf-8 -*-
import time
import re
import queue
from urllib import robotparser
from urllib import request
from urllib.parse import urlparse
from urllib.parse import urljoin
from urllib.parse import urldefrag
from datetime import datetime
'''
记录每个domain上次被访问的时间
计算出当前访问的时间与上次访问的时间的间隔
该间隔若小于规定的间隔（delay），则需要延迟
'''
class Throttle:
	def __init__(self, delay):
		self.delay = delay	# 规定两次访问同一个domain的时间间隔
		self.domains = {}	# 记录每个domain及上次被访问的时间
	def wait(self, url):
		domain = urlparse(url).netloc	# 从url中取出域名，如http://baidu.com的domain是baidu.com
		last_accessed = self.domains.get(domain)
		if self.delay > 0 and last_accessed is not None:
			sleep_secs = self.delay - (datetime.now() - last_accessed).seconds
			if sleep_secs > 0:
				time.sleep(sleep_secs)
		self.domains[domain] = datetime.now()

'''
下载url内容
若使用了代理，则设置代理
对服务器错误码5XX做处理
'''
def download(url, headers, porxy, num_retries, data=None):
	print ('Downloading: ', url)
	req = request.Request(url, headers = headers)
	opener = request.build_opener()
	if porxy:
		proxy_params = {urlparse(url).scheme:porxy}
		opener.add_handler(request.ProxyHandler(proxy_params))
	try:
		res = opener.open(req)
		html = res.read()
		code = res.code
	except request.URLError as e:
		print ('Download error:', e.reason)
		html = ''
		if hasattr(e, 'code'):
			if num_retries > 0 and 500 <= e.code < 600:
				return download(url, headers, proxy, num_retries-1, data)
		else:
			code = None
	return html

'''
获取每个页面的超链接
'''
def get_links(html):
	pagelink_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
	return pagelink_regex.findall(str(html))

'''
考虑robots.txt中的限制
'''
def get_robots(url):
	rp = robotparser.RobotFileParser()
	rp.set_url(urljoin(url, 'robots.txt'))
	rp.read()
	return rp

'''
规范url，去除hash值，且由相对url变成绝对url
'''
def normalize(seed_url, link):
	url, fragment = urldefrag(link)
	return urljoin(seed_url, link)

'''
判断两个url是否在同一个domain
'''
def same_domain(url1, url2):
	return urlparse(url1).netloc == urlparse(url2).netloc

'''
从根url开始爬虫，对每个超链接页面做爬虫
考虑深度
考虑超链接循环嵌套
'''
def link_crawler(seed_url, link_regex=None, delay=1, max_depth=-1, max_urls=-1, headers=None, user_agent='wswp', proxy=None, num_retries=1, scrape_callback=None):
	crawl_queue = queue.deque([seed_url])
	seen = {seed_url:0}
	num_urls = 0
	rp = get_robots(seed_url)
	throttle = Throttle(delay)
	headers = headers or {}
	if user_agent:
		headers['User-agent'] = user_agent
	while crawl_queue:
		url = crawl_queue.pop()
		if rp.can_fetch(user_agent, url):
			throttle.wait(url)
			html = download(url, headers, proxy, num_retries)
			links = []
			if scrape_callback:
				scrape_callback(url, html)
			depth = seen[url]
			if depth != max_depth:
				if link_regex:
					links.extend(link for link in get_links(html) if re.search(link_regex, link))
				for link in links:
					link = normalize(seed_url, link)
					if link not in seen:
						seen[link] = depth + 1
						if same_domain(seed_url, link):
							crawl_queue.append(link)
			num_urls += 1
			if num_urls == max_urls:
				break
		else:
			print ('Blocked by robots.txt:', url)

if __name__ == '__main__':
	# link_crawler('http://example.webscraping.com', '/(index|view)', delay=0, num_retries=1, user_agent='BadCrawler')
	link_crawler('http://example.webscraping.com', '/(index|view)', delay=0, num_retries=1, max_depth=1, user_agent='GoodCrawler')