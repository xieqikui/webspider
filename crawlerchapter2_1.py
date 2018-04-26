# -*- coding:utf-8 -*-
import re
import lxml.html
import time
from datetime import datetime
import logging
from urllib import request
from bs4 import BeautifulSoup

fields = ('area', 'population', 'iso', 'country', 'capital', 'continent', 'tld', 'currency_code','currency_name', 'phone', 'postal_code_format',
'postal_code_regex', 'languages', 'neighbours')

filename = '.'.join(('log_' + time.strftime('%Y-%m-%d_%H:%M:%S', time.localtime()), 'log'))

logging.basicConfig(filename='log.log', level=logging.DEBUG)

def info(msg):
	logging.info(msg)

def getHtml(url):
	req = request.Request(url)
	res = request.urlopen(req)
	return res.read().decode('utf-8')

def re_scraper(html):
	results = {}
	for field in fields:
		regex = r'<tr id="places_%s__row">.*?<td class="w2p_fw">(.*?)</td>' %field
		regexobjs = re.search(regex, html)
		if regexobjs:
			results[field] = regexobjs.groups()[0]
		else:
			results[field] = '' or None
	return results
def bs_scraper(html):
	results = {}
	soup = BeautifulSoup(html, 'html.parser')
	for field in fields:
		isFound = True
		table = soup.find('table')
		if not table:
			isFound = False
		else:
			tr = table.find('tr', id='places_%s__row' %field)
			if not tr:
				isFound = False
			else:
				td = tr.find('td', class_='w2p_fw')
				if not td:
					isFound = False
				else:
					results[field] = td.text
		if not isFound:
			results[field] = '' or None
		# print ('field=', field)
		# text = soup.find('table').find('tr', id='places_%s__row' %field).find('td', attrs={'class':'w2p_fw'}).text
		# text = soup.find('table').find('tr', id='places_%s__row' %field).find('td', class_='w2p_fw').text
		# print(text)
		# results[field] = text
	return results
def lxml_scraper(html):
	results = {}
	tree = lxml.html.fromstring(html)
	for field in fields:
		td = tree.cssselect('table > tr#places_%s__row > td.w2p_fw' %field)
		if td:
			results[field] = td[0].text_content()
		else:
			results[field] = '' or None
	return results

if __name__ == '__main__':
	NUM_ITERATIONS = 1000
	url = 'http://example.webscraping.com/places/default/view/Aland-Islands-2'
	html = getHtml(url)
	# print (len(html))
	# print (re_scraper(html))
	# print (bs_scraper(html))
	# print (lxml_scraper(html))
	info('html:%s' %html)
	for name, scraper in [('Regular expressions', re_scraper), ('BeautifulSoup', bs_scraper), ('lxml', lxml_scraper)]:
		start = time.time()
		for i in range(NUM_ITERATIONS):
			if scraper == re_scraper:
				re.purge()
			results = scraper(html)
			info('%s:%s' %(name, results))
			assert(results['area'] == '1,580 square kilometres')
		end = time.time()
		print ('%s: %.2f seconds' %(name, end-start))

