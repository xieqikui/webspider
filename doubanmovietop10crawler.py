# -*- coding:utf-8 -*-
import re
import os
from urllib import request

topN = 10
rooturl = 'https://movie.douban.com/chart'
req = request.Request(rooturl)
res = request.urlopen(req)
html = res.read().decode('utf-8')
# print (html)
# movie_title_regex = re.compile('<a[^>]+class="nbg"[^>]+href="https://movie.douban.com/subject/[0-9]+/"[^>]title="(.*?)">', re.IGNORECASE)
movie_title_regex = re.compile('title="(.*?)">', re.IGNORECASE)
movie_rating_nums_regex = re.compile('class="rating_nums">(.*?)</span>')
movie_poster_regex = re.compile('<img[^>]+src="(.*?)"[^>]+width="75"[^>]+alt=')
 
movie_titles = movie_title_regex.findall(html)
movie_rating_nums = movie_rating_nums_regex.findall(html)
movie_poster_urls = movie_poster_regex.findall(html)
movie_posters = []
# for posterurl in movie_posters:
# 	postername = posterurl.split('/')[-1]
# 	posterreq = request.Request(posterurl)
# 	posterres = request.urlopen(posterreq)
# 	poster = posterres.read()
# 	with open(postername, 'wb') as f:
# 		f.write(poster)
for i in range(topN):
	posterurl = movie_poster_urls[i]
	postername = movie_titles[i] + '.' + posterurl.split('.')[-1]
	movie_posters.append(postername)
	# posterpath = os.path.join('imgs', postername)
	posterreq = request.Request(posterurl)
	posterres = request.urlopen(posterreq)
	poster = posterres.read()
	with open(postername, 'wb') as posterfile:
		posterfile.write(poster)

# print (movie_titles)
# for title in movie_titles:
# 	print (title)