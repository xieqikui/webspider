import pickle
import zlib
from bson.binary import Binary
from datetime import datetime, timedelta
from pymongo import MongoClient
from link_crawler import link_crawler

class MongoCache:
	def __init__(self, client=None, expires=timedelta(days=30)):
		self.client = MongoClient('localhost', 27017) if client is None else client
		self.db = self.client.cache
		self.db.webpage.create_index('timestamp', expireAfterSeconds=expires.total_seconds())

	def __contains__(self, url):
		try:
			self[url]
		except KeyError as e:
			return False
		else:
			return True

	def __getitem__(self, url):
		record = self.db.webpage.find_one({'_id':url})
		if record:
			return pickle.loads(zlib.decompress(record['result']))
		else:
			raise KeyError(url + ' does not exist')
	def __setitem__(self, url, result):
		record = {'result':Binary(zlib.compress(pickle.dumps(result))), 'timestamp':datetime.utcnow()}
		self.db.webpage.update({'_id':url}, {'$set':record}, upsert=True)

	def clear(self):
		self.db.webpage.drop()

if __name__ == '__main__':
	cache = MongoCache()
	# url = 'http://example.webscraping.com'
	# result = {'html':'_'}
	# cache[url] = result
	# print (cache[url])
	link_crawler('http://example.webscraping.com', link_regex='/(index|view)', cache=cache)