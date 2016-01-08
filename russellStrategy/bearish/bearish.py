import csv, os
from tqdm import tqdm

def two_loss( clos, op, low, high, ticker, dat):
	with open('log2stop.txt','a') as f:
			f.write('it was a bearish in %s in company %s\n__________________\n'%(dat, ticker))
			min_elem = low[0]
			max_elem = high[0]
			my_list = [0,0,0]
			i = 1
			for line, row in zip(low, high):
				if line < min_elem:
					min_elem = line
				if row > max_elem:
					max_elem = row
				if (min_elem/op)-1 <= -0.02:
					f.write('%d-day VERY BAD return: -0.02\n'%(i))
					my_list[i-1]-=0.02
					break
				elif (max_elem) >= clos[0]:
					f.write('%d-day  return: %f\n'%(i, abs((op/clos[0])-1)))
					my_list[i-1] += abs((op/clos[0])-1)
				else: 
					f.write('%d-day  return: %f\n'%(i, clos[i-1]/op-1))	
					my_list[i-1] += clos[i]/op-1
				i=i+1			
			f.write('\n')
			f.close()
			outfile = open('tmp.csv', 'a')
			writer = csv.writer(outfile)
			writer.writerow(my_list)
			outfile.close()

def main(ticker):
	closing_price = []
	open_price= []
	low_price = []
	data_of_trade= []
	high_price= []
	with open('../../history/csv/'+ticker+'.csv','r') as csvfile:
		spamreader = csv.reader(csvfile)
		for row in spamreader:
			closing_price.append(row[4])
			open_price.append(row[1])
			low_price.append(row[3])
			data_of_trade.append(row[0])
			high_price.append(row[2])
			
	del closing_price[0]
	del open_price[0]
	del low_price[0]
	del data_of_trade[0]
	del high_price[0]
	closing_price = list(reversed(list(map(float, closing_price))))
	open_price = list(reversed( list(map(float, open_price))))
	low_price = list(reversed(list(map(float, low_price))))
	high_price = list(reversed(list(map(float, high_price))))
	data_of_trade = list(reversed( data_of_trade))
	f = open('tmp.csv','w')
	f.close()
	list_my = [0,0,0,'s',0,0]
	j=0
	
	#print closing_price
	for i,enum in enumerate(closing_price[:-4]):
		if open_price[i+1] < closing_price[i]:
			j= j+1
			if (abs((open_price[i+1])/closing_price[i]-1)) <= 0.04 and (abs((open_price[i+1])/closing_price[i]-1)) >= 0.02:
				#clos, op, low, high, ticker, dat
				two_loss(closing_price[i:i+4], open_price[i+1], low_price[i+1:i+4], high_price[i+1:i+4], ticker, data_of_trade[i])
				
	outfile = open('tmp.csv', 'r')
	writer = csv.reader(outfile)
	kostyl=0
	for x in writer:
		kostyl= kostyl+1
		list_my[0]+=float(x[0])
		list_my[1]+=float(x[1])
		list_my[2]+=float(x[2])
	list_my[0] = list_my[0]/kostyl
	list_my[1] = list_my[1]/kostyl
	list_my[2] = list_my[2]/kostyl
	outfile.close()
	list_my[3] = ticker
	list_my[4] = j
	list_my[5] = kostyl
	with open('olymp.csv','a') as f:
		writer = csv.writer(f)
		writer.writerow(list_my)
	f.close()
	os.system('rm tmp.csv')
			
with open('../../russell2000.txt','r') as w:
	for symbol in tqdm(w.readlines()):
		string = symbol[:-1]
		main(string)

	
	
