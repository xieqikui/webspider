import re
import time
import threading
from urllib import request
from urllib import robotparser
from urllib.parse import urlparse
from urllib.parse import urljoin
from urllib.parse import urldefrag
from downloader import Downloader

SLEEP_TIME = 1

def threaded_crawler(seed_url, link_regex=None, delay=2, max_depth=-1, max_urls=-1, user_agent='wswp', proxies=None, num_retries=1, scrape_callback=None, cache=None, max_threads=10):
	crawl_queue = [seed_url]
	seen = {seed_url:0}
	# num_urls = 0
	rp = get_robots(seed_url)
	dwnlder = Downloader(delay=delay, user_agent=user_agent, proxies=proxies, num_retries=num_retries, cache=cache)
	def process_queue():
		# global num_urls
		while True:
			try:
				url = crawl_queue.pop()
			except IndexError as e:
				# crawl queue is empty
				break
			else:
				if not rp.can_fetch(user_agent, url):
					print ('%s cannot be crawled!' %url)
					continue
				depth = 0
				html = dwnlder(url)
				print ('url:{}, seen[url]:{}'.format(url, seen[url]))
				if url in seen:
					depth = seen[url]
				links = []
				if depth != max_depth:
					if link_regex:
						links.extend(link for link in get_links(html) if re.search(link_regex, link))
					for link in links:
						link = normalize(seed_url, link)
						# print ('link:{}, seen[link]:{}'.format(link, seen[link]))
						# print ('link:{}'.format(link))
						# print ('seen[link]:{}'.format(seen[link]))
						if link not in seen:
							seen[link] = depth + 1
							if same_domain(seed_url, link):
								crawl_queue.append(link)
				# num_urls += 1
				# if num_urls == max_urls:
				# 	break
	threads = []
	while threads or crawl_queue:
		for thread in threads:
			if not thread.is_alive():
				threads.remove(thread)
		while len(threads) < max_threads and crawl_queue:
			thread = threading.Thread(target=process_queue)
			thread.setDaemon(True)
			thread.start()
			threads.append(thread)
		time.sleep(SLEEP_TIME)

def normalize(seed_url, link):
	link, _ = urldefrag(link)
	return urljoin(seed_url, link)

def same_domain(url1, url2):
	return urlparse(url1).netloc == urlparse(url2).netloc

def get_robots(url):
	rp = robotparser.RobotFileParser()
	rp.set_url(urljoin(url, 'robots.txt'))
	rp.read()
	return rp

def get_links(html):
	webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
	return webpage_regex.findall(html)



if __name__ == '__main__':
	pass