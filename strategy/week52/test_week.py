# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import time, argparse, sys, os, csv
from math import *	
from tqdm import tqdm

def createParser():
	parser = argparse.ArgumentParser()
	parser.add_argument('-d','--days',type=int,default=0)
	return parser
	
def usage():
	os.system('clear')
	print 'week52 1.0.2 - (C) 2016 SAITAMA'
	print 'Released under the GNU GPL.'
	print
	print '\t\t█───█─███─███─█──█─████─████'
	print '\t\t█───█─█───█───█─█──█────█──█'
	print '\t\t█─█─█─███─███─██───████───██'
	print '\t\t█████─█───█───█─█─────█─██'
	print '\t\t─█─█──███─███─█──█─████─████'
	print '\t\t────────────────────────────'
	print '\tSome questions? twiggymonro@gmail.com'
	print "\tI don't mention your email? Skype: twiggymonro"
	print '\tAlso can find me vk.com/id26310944'
	print '\tor maybe facebook.com/maxim.vasiliev.1291'
	print
	print 'Example:'
	print '\tpython week52.py'
	print

def sharpCount(s):
	res =pd.DataFrame(s)
	res['STD']=np.std(res,axis=1,ddof=1)
	res['AVG']=res.mean(axis=1)
	res['Sharp']=1
	res['Sharp']=res['AVG']/res['STD']
	return res

def sharp(x):
	df=pd.DataFrame(x,columns=['d1','d2','d3','scen','flag'])
	scenarios=[0,1,2,3,4,5,6,7,8,9]
	table=[]
	little_table1=[]
	little_table2=[]
	little_table3=[]
	for x in scenarios:
		if len(df[df.scen==x]) != 0:
			little_table=[]
			little_table1.append((df['d1'][df.scen == x].values))
			little_table2.append((df['d2'][df.scen == x].values))
			little_table3.append((df['d3'][df.scen == x].values))
		
			table.append(x)

			
	
	final_table=pd.DataFrame(np.nan, index=[0,1,2,3,4,5,6,7,8,9],columns=['d1 AVG','d1 Sharpe','d2 AVG','d2 Sharpe','d3 AVG','d3 Sharpe'])
	little_table1 = sharpCount(little_table1)
	little_table2 = sharpCount(little_table2)
	little_table3 = sharpCount(little_table3)
	i=0

	for some in table:
		final_table['d1 AVG'].ix[some] = little_table1['AVG'].ix[i]
		final_table['d1 Sharpe'].ix[some] = little_table1['Sharp'].ix[i]
		final_table['d2 AVG'].ix[some] = little_table2['AVG'].ix[i]
		final_table['d2 Sharpe'].ix[some] = little_table2['Sharp'].ix[i]
		final_table['d3 AVG'].ix[some] = little_table3['AVG'].ix[i]
		final_table['d3 Sharpe'].ix[some] = little_table3['Sharp'].ix[i]
		i+=1
	
	return final_table

def gain(df,i,flag):
	days = []
	i+=1
	op = df.Open.ix[i]
	if flag == True:
		days.append(df.Close.ix[i]/op-1)
		days.append(df.Close.ix[i+1]/op-1)
		days.append(df.Close.ix[i+2]/op-1)
		days.append(df.Scenario.ix[i-1])
		days.append(flag)
	elif flag == False:
		days.append(op/df.Close.ix[i]-1)
		days.append(op/df.Close.ix[i+1]-1)
		days.append(op/df.Close.ix[i+2]-1)
		days.append(df.Scenario.ix[i-1])
		days.append(flag)
	
	return days

def my_min(values):
	return min(values)

def my_max(values):
	return max(values)
	
def checker(ticker):
	table = pd.read_csv('../sp500/csv/'+ticker+'.csv')
	table['Max'] = pd.rolling_apply(table['High'],260,my_max)
	table['Min'] = pd.rolling_apply(table['Low'],260,my_min)
	
	table['MoveUp'] = 0
	table['MoveUp'][table.Low ==  table.Min] = 1
	table['MoveUp'][table.High ==  table.Max] = 2

	
	is_today=False
	my_iterator = len(table)-1
	flag = False
	boolka = True
	
	if table.MoveUp.ix[my_iterator] > 0:
		is_today = True
		return ticker
	
	if is_today == True:

		my_counter=0
		#flag = table.MoveUp.ix[0]
		up_gain=[]
		down_gain=[]
		for i,row in table.iterrows():
		
			if i == len(table)-4:
				break
	
			if table.MoveUp.ix[i] > 0:
				
				if table.MoveUp.ix[i] == 1:
					flag = False
				elif table.MoveUp.ix[i] == 2:
					flag = True
				
				my_gain = []
				my_gain = gain(table.ix[i:i+3],i,flag)
				if flag == True:
					up_gain.append(my_gain)
				elif flag == False:
					down_gain.append(my_gain)
			
		
		if len(down_gain) == 0:
			return None
		else:
			down=sharp(down_gain)
			
		if len(up_gain) == 0:
			return None
		else:
			up=sharp(up_gain)
		
		'''
		if today_trend == True:
			t = table.ix[len(table)-1:len(table)-1]
			t['Ticker'] = ticker
			t['Days'] = d
			t['Go up?'] = today_trend
			t['d1 AVG'] = up['d1 AVG'].ix[today_scen:today_scen].values
			t['d2 AVG'] = up['d2 AVG'].ix[today_scen:today_scen].values
			t['d3 AVG'] = up['d3 AVG'].ix[today_scen:today_scen].values
			t['d1 Sharpe'] = up['d1 Sharpe'].ix[today_scen:today_scen].values
			t['d2 Sharpe'] = up['d2 Sharpe'].ix[today_scen:today_scen].values
			t['d3 Sharpe'] = up['d3 Sharpe'].ix[today_scen:today_scen].values
			return t
		else:
			t = table.ix[len(table)-1:len(table)-1]
			t['Ticker'] = ticker
			t['Days'] = d
			t['Go up?'] = today_trend
			t['d1 AVG'] = down['d1 AVG'].ix[today_scen:today_scen].values
			t['d2 AVG'] = down['d2 AVG'].ix[today_scen:today_scen].values
			t['d3 AVG'] = down['d3 AVG'].ix[today_scen:today_scen].values
			t['d1 Sharpe'] = down['d1 Sharpe'].ix[today_scen:today_scen].values
			t['d2 Sharpe'] = down['d2 Sharpe'].ix[today_scen:today_scen].values
			t['d3 Sharpe'] = down['d3 Sharpe'].ix[today_scen:today_scen].values
			return t
		'''
		return ticker
		

if __name__ == '__main__':
	parser = createParser()
	namespace = parser.parse_args(sys.argv[1:])
	os.system('rm result.csv')
	os.system('touch result.csv')
	d = namespace.days
	if True:
		usage()
		with open('../sp500.txt') as f:
			for word in tqdm(f.readlines()):
				try:
					word = word[:-1]
					try:
						with open('result1.csv', 'a') as x:
							some = checker(word)
							if len(some) != 0:
								a = csv.writer(x)
								a.writerow([some])
					except TypeError:
						continue
				except IOError:
					continue

