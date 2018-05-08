# -*- coding:utf-8 -*-
import logging
import time
from datetime import datetime
from urllib import request
from urllib.parse import urlparse

filename = 'log_'+ time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime()) + '.log'
# logging.basicConfig(filename=filename, level=logging.DEBUG)

def log(msg):
	# logging.info(msg)
	pass

DEFAULT_AGENT = 'wswp'
DEFAULT_DELAY = 5
DEFAULT_RETRIES = 1
DEFAULT_TIMEOUT = 60

class Downloader(object):
	def __init__(self, delay=DEFAULT_DELAY, user_agent=DEFAULT_AGENT, proxies=None, num_retries=DEFAULT_RETRIES, opener=None, cache=None):
		self.throttle = Throttle(delay)
		self.user_agent = user_agent
		self.proxies = proxies
		self.num_retries = num_retries
		self.opener = opener
		self.cache = cache
	def __call__(self, url):
		result = None
		if self.cache:
			try:
				result = self.cache[url]
			except KeyError as e:
				log('The url "%s" is not available in cache')
				# raise e
				pass
			else:
				if self.num_retries > 0 and 500 <= result['code'] < 600:
					log('server error, so abandon the result and re-download')
					result = None
		if result is None:
			log('result was not in cache, so still need to download')	
			self.throttle.wait(url)
			proxy = random.choice(self.proxies) if self.proxies else None
			headers = {'User-agent':self.user_agent}
			result = self.download(url, headers, proxy, self.num_retries)
			if self.cache:
				log('save result to cache')
				self.cache[url] = result
		return result['html']

	def download(self, url, headers, proxy, num_retries, data=None):
		log('Downloading {}'.format(url))
		req = request.Request(url, data, headers or {})
		opener = self.opener or request.build_opener()
		if proxy:
			proxy_params = {urlparse(url).scheme:proxy}
			opener.add_handler(request.proxyHandler(proxy_params))
		try:
			res = opener.open(req)
			html = res.read().decode('utf-8')
			code = res.code
		except request.URLError as e:
			log('Download error, the reason is {}'.format(e.reason))
			html = ''
			if hasattr(e, 'code'):
				if num_retries>0 and 500<=e.code<600:
					return download(url, headers, proxy, num_retries-1, data)
			else:
				code = None
		return {'html':html, 'code':code}

class Throttle(object):
	def __init__(self, delay):
		self.delay = delay
		self.domains = {}
	def wait(self, url):
		domain = urlparse(url).netloc
		last_accessed = self.domains.get(domain)
		if self.delay > 0 and last_accessed is not None:
			sleep_secs = self.delay - (datetime.now() - last_accessed).seconds
			if sleep_secs > 0:
				time.sleep(sleep_secs)
		self.domains[domain] = datetime.now()