# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from urllib2 import urlopen
import time, os

my_time = time.time()

html_doc = urlopen('http://www.barchart.com/stocks/russell2000.php?_dtp1=0')
soup = BeautifulSoup(html_doc)
soup.unicode
f = open('russell2000.txt', 'w')

table = soup.find('div', attrs ={'class','xscroll'})
tbody = table.find('tbody')
tr = tbody.find_all('tr')
td = ""
for some in tr:
	f.write("%s\n" % (some.find('td').text))

f.close()
print time.time() - my_time
os.system('python hipric.py -i sp500.txt')
os.system('python hipric.py -i russell2000.txt')
