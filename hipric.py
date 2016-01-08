# -*- coding: utf-8 -*-
# let's go
import urllib, time, sys, getopt, os
from tqdm import tqdm

base_url = "http://ichart.finance.yahoo.com/table.csv?s="
app_url = "&a=0&b=1&c=2010&d=0&e=1&f=2017&g=d"
def make_url(ticker_symbol):
	return "http://ichart.finance.yahoo.com/table.csv?s=%s&a=0&b=1&c=2010&d=0&e=1&f=2016&g=d" % (ticker_symbol)

def pull_historical_data(ticker_symbol):
    try:
        urllib.urlretrieve(make_url(ticker_symbol), "history/csv/"+ ticker_symbol +".csv")
    except urllib.ContentTooShortError as e:
        outfile = open("history/csv/"+ ticker_symbol +"___.csv", "w")
        outfile.write(e.content)
        outfile.close()
     
def cmon(symbol):
	pull_historical_data(symbol)

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
	   r = open(inputfile, "r")
	   end_sum=0
	   f = open("history/log.txt", "w")
	   print "Let's go!"
	   string_name = ""
	   for line in tqdm(r.readlines()):
		   my_time = time.time()
		   string_name = line[0:-1]
		   cmon(string_name)
		   f.write("speed for %s is --------- %f\n" % (string_name, time.time()-my_time))
		   end_sum = end_sum + time.time()-my_time

	   f.write("__________________________\n\nTotal Time is %f\n" % (end_sum/60))
	   f.close()
	   r.close()
	   print "total time is %f" % (end_sum/60)
	   print "\n________________________________________________"
	   print "\t\t\tbe with SAITAMA"

main(sys.argv[1:])		
