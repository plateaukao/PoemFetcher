#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
from BeautifulSoup import BeautifulSoup

URL_PREFIX = "http://cls.hs.yzu.edu.tw/300/all/"

class Poem:
    def __init__(self, name, author, url):
        self.name=name
        self.author=author
        self.url=url

    def __repr__(self):
        return self.name + self.author + self.url

html = urllib.urlopen(URL_PREFIX + "ALL_TITLE.ASP").read()
soup = BeautifulSoup(html)

count=0
for tr in soup.body.findAll('tr'):
    if count == 0:
        count +=1
        continue
    tds = tr.findAll('td')
    author = unicode(tds[1].a.string)
    #print tds[2]
    name = unicode(tds[2].a.string)
    url = URL_PREFIX + tds[2].a['href']
    poem = Poem(name, author, url)

    if poem:
        print poem.name, poem.author, poem.url
    print count
    count += 1

