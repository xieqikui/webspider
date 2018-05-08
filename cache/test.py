import re
import os
from urllib.parse import urlparse
dict1 = {'name1':'value1', 'name2':'value2'}

print(dict1.get('name1'))
dict1['name1'] = 'value111'
print(dict1.get('name1'))
# print (dict1['name3'])

url = 'http://example.webscraping.com/default/view/Australia-1'

url1 = re.sub('[^/0-9a-zA-Z-\.,;_]', '_', url)

print (url1.split('/'))
print ([seg[:255] for seg in url1.split('/')])

components = urlparse(url)
print (components.netloc)
print (components.scheme)
print (components.path)
print (components.query)

path = components.path
if not path:
	path = '/index.html'
elif path.endswith('/'):
	path += 'index.html'
print (components.netloc+path+components.query)


path = 'cache/example.webscraping.com/places/default/user/login_next_/places/default/index111'
print (os.path.dirname(path))
