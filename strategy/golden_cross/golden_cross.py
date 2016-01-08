import csv, time, os
from tqdm import tqdm


def two_stop_loss(clos, op, ticker, dat, low):
	with open('logTwoStop.txt','a') as f:
		f.write('it was a golden cross in %s in company %s\n__________________\n'%(dat, ticker))
		min_elem = low[len(low)-1]
		myList = [0,0,0,0,0,0,0,0,0,0]
		i = len(low)-1
		for line in low[::-1]:
			if line < min_elem:
				min_elem = line
			if (min_elem/op)-1 <= -0.02:
				f.write('%d-day VERY BAD return: -0.02\n'%(10-i))
				myList[i]-=0.02
				break
			else:
				f.write('%d-day return: %f\n'%(10-i,(clos[i]/op)-1))
				myList[i]+=clos[i]/op-1
			i = i-1
		f.write('\n\n')
		f.close()
	outfile = open('tmp.csv', 'a')
	writer = csv.writer(outfile)
	writer.writerow(myList)
	outfile.close()
		

def no_stop_loss(clos, op, ticker, dat):
	with open('logNoStop.txt', 'a') as f:
		f.write('it was a golden cross in %s in company %s\n__________________\n'%(dat, ticker))
		f.write('1-day return: %f\n'%((clos[9]/op)-1))
		f.write('2-day return: %f\n'%((clos[8]/op)-1))
		f.write('3-day return: %f\n'%((clos[7]/op)-1))
		f.write('4-day return: %f\n'%((clos[6]/op)-1))
		f.write('5-day return: %f\n'%((clos[5]/op)-1))
		f.write('6-day return: %f\n'%((clos[4]/op)-1))
		f.write('7-day return: %f\n'%((clos[3]/op)-1))
		f.write('8-day return: %f\n'%((clos[2]/op)-1))
		f.write('9-day return: %f\n'%((clos[1]/op)-1))
		f.write('10-day return: %f\n\n\n'%((clos[0]/op)-1))
		f.close()

def fuck(l50, l200):
	first0 = reduce(lambda x, y: x + y, l50[:-1]) / (len(l50)-1)
	second0 = reduce(lambda x, y: x + y, l200[:-1]) / (len(l200)-1)
	first1 = reduce(lambda x, y: x + y, l50[1:]) / (len(l50)-1)
	second1 = reduce(lambda x, y: x + y, l200[1:]) / (len(l200)-1)
	if first1 > second1 and first0 < second0:
		return True
	else:
		return False

def open_me(ticker):
	# open data
	closing_price = []
	open_price= []
	low_price = []
	data_of_trade= []
	with open('../../history/csv/'+ticker+'.csv','r') as csvfile:
		spamreader = csv.reader(csvfile)
		for row in spamreader:
			closing_price.append(row[4])
			open_price.append(row[1])
			low_price.append(row[3])
			data_of_trade.append(row[0])
			
	# run over 50/200 days
	del closing_price[0]
	del open_price[0]
	del low_price[0]
	del data_of_trade[0]
	closing_price = list(map(float, closing_price))
	open_price = list(map(float, open_price))
	low_price = list(map(float, low_price))
	myList = []
	j = 0
	i = 0
	f = open('tmp.csv','w')
	f.close()
	# print reduce(lambda x, y: x + y, closing_price) / len(closing_price)
	for enum in closing_price[:-200]:
		if i >= 10:
			x = int(i) + 50
			y = int(i) + 200
			if fuck(list(reversed(closing_price[i:x])), list(reversed(closing_price[i:y]))) == True:
				j=j+1
				no_stop_loss(list(closing_price[i-10:i]), open_price[i-1], ticker, data_of_trade[i])
				two_stop_loss(list(closing_price[i-10:i]),open_price[i-1], ticker,data_of_trade[i], list(low_price[i-10:i]))
		i=i+1
			# print 'it was a golden cross in %s in company %s'%(data_of_trade[i], ticker)
	data=[0,0,0,0,0,0,0,0,0,0,'symbol',0]
	outfile = open('tmp.csv', 'r')
	writer = csv.reader(outfile)
	kostyl=0
	for x in writer:
		kostyl+=1
		data[0]+=float(x[0])
		data[1]+=float(x[1])
		data[2]+=float(x[2])
		data[3]+=float(x[3])
		data[4]+=float(x[4])
		data[5]+=float(x[5])
		data[6]+=float(x[6])
		data[7]+=float(x[7])
		data[8]+=float(x[8])
		data[9]+=float(x[9])
	outfile.close()
	data[0]=data[0]/kostyl
	data[1]=data[1]/kostyl
	data[2]=data[2]/kostyl
	data[3]=data[3]/kostyl
	data[4]=data[4]/kostyl
	data[5]=data[5]/kostyl
	data[6]=data[6]/kostyl
	data[7]=data[7]/kostyl
	data[8]=data[8]/kostyl
	data[9]=data[9]/kostyl
	data[10] = ticker
	data[11] = j
	with open('olymp.csv','a') as f:
		writer = csv.writer(f)
		writer.writerow(data)
	f.close()
	os.system('rm tmp.csv')
	

my_time = time.time()			
with open('../../sp500.txt','r') as w:
	for symbol in tqdm(w.readlines()):
		string = symbol[:-1]
		open_me(string)
print '______________________________\n%f sec'%(time.time()- my_time)

