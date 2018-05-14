from pymongo import MongoClient

client = MongoClient('localhost', 27017)
url = 'http://example.webscraping.com'
url1 = 'http://example.webscraping.com/view/United-Kingdom-239'
html = '...'
db = client.cache
db.webpage.insert({'url':url, 'html':html})
db.webpage.save({'url1':url, 'html1':html})
# print (db.webpage.find_one(url=url))
# results = db.webpage.find({'url':url})
# results = db.webpage.find()
# for result in results:
	# print (result)
# db.webpage.remove({'url1':url})
# db.webpage.remove()
db.webpage.update({'_id':url}, {'$set':{'html':html}}, upsert=True)
# results = db.webpage.find()
# for result in results:
# 	print (result)
result = db.webpage.find_one({'url':url})
print (result)