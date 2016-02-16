# -*- coding: utf-8 -*-
import finsymbols, time, os

my_time = time.time()
sp500 = finsymbols.get_sp500_symbols()
f = open('sp500.txt', 'w')
for symbol in sp500:
	f.write("%s\n"%(symbol['symbol']))
f.close()
print time.time() - my_time


