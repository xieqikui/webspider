# -*- coding:utf-8 -*-
import logging
import time

filename = 'log_'+ time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime()) + '.log'
logging.basicConfig(filename=filename, level=logging.DEBUG)

class Download(object):
	def __init__(self, delay=5, user_agent='wswp', proxies=None, num_retries=1, cache=None):
		self.throttle = Throttle(delay)
		self.user_agent = user_agent
		self.proxies = proxies
		self.num_retries = num_retries
		self.cache = cache
	def __call__(self, url):
		result = None
		if self.cache:
			try:
				result = self.cache[url]
			except KeyError as e:
				log.info('The url "%s" is not available in cache')
				# raise e
				pass
			else:
				if self.num_retries > 0 and 500 <= result['code'] < 600:
					log.info('server error, so abandon the result and re-download')
					result = None
		if result is None:
			log.info('result was not in cache, so still need to download')	
			self.throttle.wait(url)
			proxy = random.choice(self.proxies) if self.proxies else None
			headers = {'User-agent', self.user_agent}
			result = self.download(url, headers, proxy, self.num_retries)
			if self.cache:
				log.info('save result to cache')
				self.cache[url] = result
			return return['html']

	def download(self, url, headers, proxy, num_retries, data=None):
		return {'html':html, 'code':code}