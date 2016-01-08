# -*- coding: utf-8 -*-
import json, time, csv
from datetime import datetime
try:
    from urllib.request import Request, urlopen
except ImportError:  # python 2
    from urllib2 import Request, urlopen
from tqdm import tqdm

def replaceKeys(quotes):
    global googleFinanceKeyToFullName
    quotesWithReadableKey = []
    for q in quotes:
        qReadableKey = {}
        for k in googleFinanceKeyToFullName:
            if k in q:
                qReadableKey[googleFinanceKeyToFullName[k]] = q[k]
        quotesWithReadableKey.append(qReadableKey)
    return quotesWithReadableKey

googleFinanceKeyToFullName = {
    u'id'     : u'ID',
    u't'      : u'StockSymbol',
    u'e'      : u'Index',
    u'l'      : u'LastTradePrice',
    u'l_cur'  : u'LastTradeWithCurrency',
    u'ltt'    : u'LastTradeTime',
    u'lt_dts' : u'LastTradeDateTime',
    u'lt'     : u'LastTradeDateTimeLong',
    u'div'    : u'Dividend',
    u'yld'    : u'Yield'
}

def buildUrl(symbols):
    symbol_list = ','.join([symbol for symbol in symbols])
    # a deprecated but still active & correct api
    return 'http://finance.google.com/finance/info?client=ig&q=' \
        + symbol_list

def request(symbols):
    url = buildUrl(symbols)
    req = Request(url)
    resp = urlopen(req)
    # remove special symbols such as the pound symbol
    content = resp.read().decode('ascii', 'ignore').strip()
    content = content[3:]
    return content

def getQuotes(symbols):
    if type(symbols) == type('str'):
        symbols = [symbols]
    content = json.loads(request(symbols))
    converted = replaceKeys(content)
    for some in converted:
		f = csv.writer(open('today/csv/'+some['StockSymbol']+'.csv','a'))
		#f.writerow(some.keys())
		f.writerow(some.values())
    return converted

def main():
	my_time = time.time()
	my_list = []
	f = open('sp500.txt', 'r')
	log = open('today/log.txt','w')
	i = 1
	for line in tqdm(f):
		my_list.append(line[:-1])
		if i%72==0:
			for it in getQuotes(my_list):
				d = datetime.today()
				log.write("%s updated in "%(it['StockSymbol']) + d.strftime('%A, %d. %B %Y %I:%M%p') + "\n")
			del my_list[:]
		i = i + 1
	for it in getQuotes(my_list):
		d = datetime.today()
		log.write("%s updated in "%(it['StockSymbol']) + d.strftime('%A, %d. %B %Y %I:%M%p') + "\n")
	f.close()
	log.close()
	print "Time for refreshing S&P500 is %f"%(time.time() - my_time)

main()
