# -*- coding:utf-8 -*-
from urllib import request
from bs4 import BeautifulSoup
import lxml.html
# import lxml.cssselect
import re

url = 'http://example.webscraping.com/places/default/view/Aland-Islands-2'
req = request.Request(url)
res = request.urlopen(req)
html = res.read().decode('utf-8')
# print (html)
# regex = r'<tr id="places_area__row"><td class="w2p_fl"><label class="readonly" or="places_area" id="places_area__label">Area: </label></td><td class="w2p_fw">(.*?)</td>'
# regex = r'<td class="w2p_fw">(.*?)</td>'
# regex = r'<td class="w2p_fw">(.*?)</td>'
# print (re.findall(regex, html))
# regex = re.compile(r'<td class="w2p_fw">(.*?)</td>')
# print (regex.findall(html))
# print (regex.findall(html)[1])
regex_str = r'''<tr id="places_area__row"><td class="w2p_fl"><label class="readonly" for="places_area" id="places_area__label">Area: </label></td><td class="w2p_fw">(.*?)</td><td class="w2p_fc"></td></tr>'''
regex = re.compile(regex_str, re.M)
print (regex.findall(html))

broken_html = '<ul class=country><li>Area<li>Population</ul'
soup = BeautifulSoup(broken_html, 'html.parser')
fixed_html = soup.prettify()
print (fixed_html)
ul = soup.find('ul', attrs={'class':'country'})
print (ul.find('li'))
print (ul.find_all('li'))

soup1 = BeautifulSoup(html, 'html.parser')
tr = soup1.find(attrs={'id':'places_area__row'})
td = tr.find(attrs={'class':'w2p_fw'})
print (td.text)
tree = lxml.html.fromstring(broken_html)
fixed_html1 = lxml.html.tostring(tree, pretty_print=True)
print (fixed_html1)
tree1 = lxml.html.fromstring(html)
td1 = tree1.cssselect('tr#places_area__row > td.w2p_fw')[0]
area1 = td1.text_content()
print (area1)
