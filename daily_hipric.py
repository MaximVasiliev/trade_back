# -*- coding: utf-8 -*-
import urllib2  # works fine with Python 2.7.9 (not 3.4.+)
import json, time, csv
 
def fetchPreMarket(symbol):
    link = "http://finance.google.com/finance/info?client=ig&q="
    url = link+"%s" % (symbol)
    u = urllib2.urlopen(url)
    content = u.read()
    data = json.loads(content[3:])
    output = csv.writer(open('/root/opt/PYTHON/borovykh/today/csv/' + symbol + '.csv','a'))
    print data
    for row in data:
		output.writerow(row.values())
    
    """t = str(info["elt"])    # time stamp
    l = float(info["l"])    # close price (previous trading day)
    p = float(info["el"])   # stock price in pre-market (after-hours)
    """
 
flag = True
while flag:
	my_time = time.time()
	fetchPreMarket("AAPL")
	flag = False
	print time.time() - my_time
    
    
    # time.sleep(60)
