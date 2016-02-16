# -*- coding: utf-8 -*-
# let's go
import urllib, time, sys, getopt, os
from tqdm import tqdm
import pandas as pd
import numpy as np

def ADX(df, n, n_ADX):  
    i = len(df)-2  
    UpI = []  
    DoI = [] 
    while i >= 0:  
        UpMove = df.get_value(i, 'High') - df.get_value(i+1, 'High')  
        DoMove = df.get_value(i+1, 'Low') - df.get_value(i, 'Low')  
        if 0 < UpMove > DoMove:  
            UpD = UpMove  
        else:
			UpD = 0  
        UpI.append(UpD)  
        if 0 < DoMove > UpMove:  
            DoD = DoMove  
        else:
			DoD = 0  
        DoI.append(DoD)

        i = i - 1   
    i = len(df)-2 
    TR_l = [0]  
    while i >= 0:    
        TR = max((df.get_value(i,'High') - df.get_value(i,'Low')),(abs(df.get_value(i,'High')-df.get_value(i+1,'Close'))),(abs(df.get_value(i,'Low')-df.get_value(i+1,'Close'))))
        TR_l.append(TR)  
        i = i - 1  
    TR_s = pd.Series(TR_l)
    ATR = pd.Series(pd.rolling_mean(TR_s, window = 14))
    UpI = pd.Series(UpI)
    DoI = pd.Series(DoI)
  
    smoothDXP = 0
    smoothDXN = 0
    i = 0
    while i <= 13:
		smoothDXP += UpI.get_value(i)
		smoothDXN += DoI.get_value(i)
		
		i+=1
		
    SMP=[0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    SMN=[0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    SMP.append(smoothDXP/14)
    SMN.append(smoothDXN/14)
    i = 14
    while i <= len(UpI)-1:
		someP = (SMP[-1]*13 + UpI.get_value(i))/14
		someN = (SMN[-1]*13 + DoI.get_value(i))/14
		
		SMN.append(someN)
		SMP.append(someP)
		
		i+=1
    
    pizda = pd.Series(SMP)
    hyi = pd.Series(SMN)
    pizda = pizda.multiply(100)
    hyi = hyi.multiply(100)
    PosDI = pizda / ATR
    NegDI = hyi / ATR

    DX = (abs(PosDI-NegDI)/(PosDI+NegDI)).multiply(100)
    adx = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    
    i = 14
    some = 0
    while i <= 27:
		some += DX.get_value(i)
		
		i+=1
    some = some / 14
    i = 28
    while i <= len(DX)-1:
		some = (adx[-1]*13 + DX.get_value(i))/14
		adx.append(some)
		
		i+=1
    adx= adx[::-1]
    ADX = pd.Series(adx, name='ADX_num')

    df = df.join(ADX)
    
    mypositiv = PosDI.tolist()
    mynegative = NegDI.tolist()
    
    mypositiv = mypositiv[::-1]
    mynegative = mynegative[::-1]
    
    P = pd.Series(mypositiv, name='+DI')
    N = pd.Series(mynegative, name='-DI')
    
    
    df = df.join(P)
    df = df.join(N)
    df[df == 0] = np.nan

    return df

    
def rsi(price, n=14):
    ''' rsi indicator '''
    gain = (price-price.shift(1)).fillna(0) # calculate price gain with previous day, first row nan is filled with 0

    def rsiCalc(p):
        # subfunction for calculating rsi for one lookback period
        avgGain = p[p>0].sum()/n
        avgLoss = -p[p<0].sum()/n 
        rs = avgGain/avgLoss
        return 100 - 100/(1+rs)

    # run for all periods with rolling_apply
    return pd.rolling_apply(gain,n,rsiCalc) 


base_url = "http://ichart.finance.yahoo.com/table.csv?s="
app_url = "&a=0&b=1&c=2010&d=0&e=1&f=2017&g=d"
def make_url(ticker_symbol):
	return "http://ichart.finance.yahoo.com/table.csv?s=%s&a=0&b=1&c=2010&d=0&e=1&f=2017&g=d" % (ticker_symbol)

def my_min(values):
	return min(values)

def my_max(values):
	return max(values)

def pull_historical_data(ticker_symbol,name):
    try:
        urllib.urlretrieve(make_url(ticker_symbol), ""+name[:-4]+"/csv/"+ ticker_symbol +".csv")
        try:
			df = pd.read_csv(""+name[:-4]+"/csv/"+ ticker_symbol +".csv")
			df = df.iloc[::-1]
			df['RSI_num'] = rsi(df['Close'])

			df = ADX(df,14,14)
        
			df['RSI'] = 'Neutral'
			df.ix[df.RSI_num >= 70,'RSI'] = 'Oversold'
			df.ix[df.RSI_num <= 30,'RSI'] = 'Overbought'
        
			df['ADX']='N/A'
			df.ix[df.ADX_num < 20,'ADX'] = 'Sideways'
			df.ix[(df.ADX_num > 25) & (df['+DI']>df['-DI']),'ADX'] = 'Bullish'
			df.ix[(df.ADX_num > 25) & (df['+DI']<df['-DI']),'ADX'] = 'Bearish'
        
			df['Scenario']='0'
			df.ix[(df.ADX_num < 20),'Scenario'] = '5'
			df.ix[(df.ADX_num > 25) & (df['+DI']>df['-DI']),'Scenario'] = '4'
			df.ix[(df.ADX_num > 25) & (df['+DI']<df['-DI']),'Scenario'] = '6'
        
			df.ix[(df.ADX_num < 20) & (df.RSI_num >= 70),'Scenario'] = '2'
			df.ix[(df.ADX_num > 25) & (df['+DI']>df['-DI']) & (df.RSI_num >= 70),'Scenario'] = '1'
			df.ix[(df.ADX_num > 25) & (df['+DI']<df['-DI']) & (df.RSI_num >= 70),'Scenario'] = '3'

			df.ix[(df.ADX_num < 20) & (df.RSI_num <= 30),'Scenario'] = '8'
			df.ix[(df.ADX_num > 25) & (df['+DI']>df['-DI']) & (df.RSI_num <= 30),'Scenario'] = '7'
			df.ix[(df.ADX_num > 25) & (df['+DI']<df['-DI']) & (df.RSI_num <= 30),'Scenario'] = '9'
			
			df['1D CHG%'] = (df.Close / df.Close.shift(1)) - 1
			df['5D CHG%'] = (df.Close / df.Close.shift(5)) - 1
			df['1M CHG%'] = (df.Close / df.Close.shift(22)) - 1
			#df['YTD CHG%'] = (df.Close / df['Close']) - 1
			df['52-week High-Low Range'] = (df.Close - pd.rolling_apply(df['Low'],260,my_min)) / (pd.rolling_apply(df['High'],260,my_max) - pd.rolling_apply(df['Low'],260,my_min))
			
			
			df.to_csv(""+name[:-4]+"/csv/"+ ticker_symbol +".csv")			
	except KeyError as p:
		os.system("rm "+name[:-4]+"/csv/"+ ticker_symbol +".csv")
	except pd.parser.CParserError as p:
		os.system("rm "+name[:-4]+"/csv/"+ ticker_symbol +".csv")
    except urllib.ContentTooShortError as e:
        outfile = open(""+name[:-4]+"/csv/"+ ticker_symbol +"___.csv", "w")
        outfile.write(e.content)
        outfile.close()
     
def cmon(symbol,name):
	pull_historical_data(symbol,name)
	

def usage():
	os.system('clear')
	print '────────────────────────────────────────────────'
	print '█──█──███──████──████──███──████─────████──██─██'
	print '█──█───█───█──█──█──█───█───█──█─────█──█───███'
	print '████───█───████──████───█───█────────████────█'
	print '█──█───█───█─────█─█────█───█──█─────█───────█'
	print '█──█──███──█─────█─█───███──████──█──█───────█'
	print '─────────────────────────────────────────────█'
	print 'Welcome to hipric, collector of historical prices from yahoo finance'
	print 'Have fun, have a good day, have hipric'
	print '__________________________________________________\n\t\tPowered by SAITAMA'
	print '\tSome questions? twiggymonro@gmail.com'
	print "\tI don't mention your email? Skype: twiggymonro"
	print '\tAlso can find me vk.com/id26310944'
	print '\tor maybe facebook.com/maxim.vasiliev.1291'
	print 'Hipric Tool'
	print 'hipric.py -h -i file_path'
	print '-h, --help - help menu'
	print '-i, --ifile - file where we can find all tickers(default is file "ticker.txt")'
	print
	print 'Examples:'
	print 'hipric.py -i /my_dir/tickers_dir/t.txt'

def main(argv):
   inputfile = ""
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile="])
   except getopt.GetoptError:
      usage()
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         usage()
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
   if not len(sys.argv[1:]):
        usage()
   else:
	   usage()
	   os.system('rm -r '+inputfile[:-4])
	   os.system('mkdir '+inputfile[:-4])
	   os.system('mkdir '+inputfile[:-4]+'/csv')
	   r = open(inputfile, "r")
	   end_sum=0
	   f = open(""+inputfile[:-4]+"/log.txt", "w")
	   print "Let's go!"
	   string_name = ""
	   for line in tqdm(r.readlines()):
		   my_time = time.time()
		   string_name = line[0:-1]
		   string_name = string_name.replace(".","-")
		   cmon(string_name,inputfile)
		   f.write("speed for %s is --------- %f\n" % (string_name, time.time()-my_time))
		   end_sum = end_sum + time.time()-my_time

	   f.write("__________________________\n\nTotal Time is %f\n" % (end_sum/60))
	   f.close()
	   r.close()
	   print "total time is %f" % (end_sum/60)
	   print "\n________________________________________________"
	   print "\t\t\tbe with SAITAMA"

main(sys.argv[1:])		
