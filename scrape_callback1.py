# -*- coding:utf-8 -*-
import re
import logging
import time
import lxml.html
import csv
from linkcrawler import link_crawler

FIELDS = ('area', 'population', 'iso', 'country', 'capital', 'continent', 'tld', 'currency_code','currency_name', 'phone', 'postal_code_format',
'postal_code_regex', 'languages', 'neighbours')

filename = '.'.join(('log_%s' %time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime()), 'log'))
logging.basicConfig(filename=filename, level=logging.DEBUG)

def scrape_callback(url, html):
	rows = []
	tree = lxml.html.fromstring(html)
	if re.search(r'/view/', url):
		for field in FIELDS:
			td = tree.cssselect('table > tr#places_%s__row > td.w2p_fw' %field)
			if td:
				rows.append(td[0].text_content())
	print ('%s:%s' %(url, rows))
class ScrapeCallback:
	def __init__(self):
		self.writer = csv.writer(open('countries.csv', 'w'))
		self.fields = FIELDS
		self.writer.writerow(self.fields)
	def __call__(self, url, html):
		rows = []
		tree = lxml.html.fromstring(html)
		if re.search(r'/view/', url):
			for field in self.fields:
				td = tree.cssselect('table > tr#places_%s__row > td.w2p_fw' %field)
				if td:
					rows.append(td[0].text_content())
			self.writer.writerow(rows)
if __name__ == '__main__':
	link_crawler('http://example.webscraping.com/', '/(index|view)', scrape_callback=ScrapeCallback())