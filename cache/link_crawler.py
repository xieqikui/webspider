import re
from urllib import request
from urllib import robotparser
from urllib.parse import urlparse
from urllib.parse import urljoin
from urllib.parse import urldefrag
from downloader import Downloader


def link_crawler(seed_url, link_regex=None, delay=1, max_depth=-1, max_urls=-1, user_agent='wswp', proxies=None, num_retries=1, scrape_callback=None, cache=None):
	crawl_queue = [seed_url]
	seen = {seed_url:0}
	num_urls = 0
	rp = get_robots(seed_url)
	dwnlder = Downloader(delay=delay, user_agent=user_agent, proxies=proxies, num_retries=num_retries, cache=cache)
	while crawl_queue:
		url = crawl_queue.pop()
		if not rp.can_fetch(user_agent, url):
			print ('%s cannot be crawled!' %url)
			continue
		depth = 0
		html = dwnlder(url)
		if url in seen:
			depth = seen[url]
		links = []
		if depth != max_depth:
			if link_regex:
				links.extend(link for link in get_links(html) if re.search(link_regex, link))
			for link in links:
				link = normalize(seed_url, link)
				print ('link:', link)
				if link not in seen:
					seen[link] = depth + 1
					if same_domain(seed_url, link):
						crawl_queue.append(link)
		num_urls += 1
		if num_urls == max_urls:
			break


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