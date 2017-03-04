import requests
import re
import json
import html2text

URL = 'https://en.wikipedia.org/wiki/Zero_Escape:_Virtue%27s_Last_Reward'

s = requests.session()
s.headers= {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:53.0) Gecko/20100101 Firefox/53.0'}

response = s.get(URL)

rawtext = response.text

omitted = html2text.html2text( rawtext).encode('utf-8')
words = re.findall("[a-zA-Z]+", omitted)
worddict = {}

for word in words:
	if len(word) >= 2:
		word = word.lower()
		if word in worddict:
			worddict[word] += 1
		else:
			worddict[word] = 1

wordlist = []

for key, value in worddict.iteritems():
    temp = [key,value]
    wordlist.append(temp)

wordlist = sorted( wordlist, key=lambda tup: tup[1], reverse = True)

print wordlist

finalwordlist = []
maxcount = wordlist[0][1]

for item in wordlist:
	finalwordlist.append( ( item[0], { "count": item[1], "tf": 0.5 + 0.5 * item[1]/maxcount }))

print finalwordlist