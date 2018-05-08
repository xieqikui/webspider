import re
import os
import pickle
from urllib.parse import urlparse
from link_crawler import link_crawler

class DiskCache:
	def __init__(self, dir_cache='cache'):
		self.dir_cache = dir_cache
		# self.max_length = max_length
	def url_to_path(self, url):
		components = urlparse(url)
		path = components.path
		if not path:
			path = '/index.html'
		elif path.endswith('/'):
			path += 'index.html'
		elif path.endswith('index'):
			path += 'page'
		filename = components.netloc + path + components.query
		filename = re.sub('[^/0-9a-zA-Z\-.;_]', '_', filename)
		filename = '/'.join([segment[:255] for segment in filename.split('/')])
		return os.path.join(self.dir_cache, filename)
	def __getitem__(self, url):
		path = self.url_to_path(url)
		if os.path.exists(path):
			with open(path, 'rb') as fp:
				return pickle.load(fp)
		else:
			raise KeyError('{} does not exists'.format(url))
	def __setitem__(self, url, result):
		path = self.url_to_path(url)
		folder = os.path.dirname(path)
		if not os.path.exists(folder):
			os.makedirs(folder)
		with open(path, 'wb') as fp:
			fp.write(pickle.dumps(result))

if __name__ == '__main__':
	link_crawler('http://example.webscraping.com', link_regex='/(index|view)', cache=DiskCache())