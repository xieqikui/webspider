# -*- coding:utf-8 -*-
import re
import logging
import time
import lxml.html
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
if __name__ == '__main__':
	link_crawler('http://example.webscraping.com/', '/(index|view)', scrape_callback=scrape_callback)