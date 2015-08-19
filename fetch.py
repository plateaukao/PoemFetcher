#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
from BeautifulSoup import BeautifulSoup
import sqlite3 as lite
import sys

URL_PREFIX = "http://cls.hs.yzu.edu.tw/300/all/"

class Poem:
    def __init__(self, name, author, url):
        self.name=name
        self.author=author
        self.url=url
        self.content=""
        self.poem_type=''

    def __repr__(self):
        return self.name + "(" + self.author + "):" + self.content

html = urllib.urlopen(URL_PREFIX + "ALL_TITLE.ASP").read()
soup = BeautifulSoup(html)

count=0
poemList = []
for tr in soup.body.findAll('tr'):
    if count == 0:
        count +=1
        continue
    tds = tr.findAll('td')
    author = unicode(tds[1].a.string).replace(" ","")
    #print tds[2]
    name = unicode(tds[2].a.string).replace(" ","")
    url = URL_PREFIX + tds[2].a['href']
    poem = Poem(name, author, url)

    if poem:
        poemList.append(poem)
    count += 1

# database handlings
con = lite.connect('poems.db')
with con:
    cur = con.cursor()
    count = 1

    for p in poemList:
        print p.name,p.author

        html = urllib.urlopen(p.url).read()
        soup = BeautifulSoup(html)
        raw_content = soup.body.find('a')['href']
        p.poem_type = soup.body.text[soup.body.text.find(u'詩體')+3:soup.body.text.find(u'詩文:')].replace(" ","")
        print p.poem_type

        p.content = raw_content[raw_content.find('=')+1:].replace(" ","")
        print p.content

        command = 'INSERT INTO Poems VALUES(%d,"%s", "%s", "%s", "%s", "%s")' % (count, p.name, p.author, p.url, p.content, p.poem_type)
        print command
        cur.execute(command)
        count += 1
