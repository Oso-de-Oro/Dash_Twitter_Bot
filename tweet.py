#!/usr/bin/env python

'''Post a message to twitter'''

__author__ = 'dewitt@google.com'

import configparser
import getopt
import os
import sys
import schedule
import time
import krakenex
import networkx as nx
import newspaper
from datetime import date
#import urllib2
import twitter

x = 0

def tweet():
  global x
  k = krakenex.API(key='VKF3XuOWoPFWb5Q8IddE5E6ZVFGk4976P3RJUMfmdzn29r2alC6F7vbL', secret='NR0rXUvh5f7heTNs85j64e/8itxL5CX31nYq5kyD1Y5+4u82waq3NQfeBNCLuDQnJYth2Jp5l7BAvJ2zGRzoOQ==')
  #c = krakenex.Connection(uri='https://api.kraken.com/0/public/Spread?pair=DASHUSD', timeout=30)
  price = k.query_public('Ticker',{'pair': 'DASHUSD'})
  print(price['result']['DASHUSD']['a'][0])
  if 1 - x/float(price['result']['DASHUSD']['a'][0]) < 0:
       pop = (1 - x/float(price['result']['DASHUSD']['a'][0])) * 100
       message = 'DASH price: %.2f (%.2f%%)\n\n%s' % (float(price['result']['DASHUSD']['a'][0]), pop, time.ctime())
  elif 1 - x/float(price['result']['DASHUSD']['a'][0]) >= 0:
       pop = (1 - x/float(price['result']['DASHUSD']['a'][0])) * 100
       message = 'DASH price: %.2f (+%.2f%%)\n\n%s' % (float(price['result']['DASHUSD']['a'][0]), pop, time.ctime())
  x = float(price['result']['DASHUSD']['a'][0])
  api = twitter.Api(consumer_key='Ftv26M5zL6vDQAuzxRF2EBnnm',
                        consumer_secret='yiQJcB1iicL28qE4utx4fuUhaBEGgF9n33J88lDfHz0b5bpk06',
                        access_token_key='878690810409222145-vAvH0BEWRgYRcEBIOUrjTxrx11e1TEo',
                        access_token_secret='dnoFxSJ113k4STzptxyQTvBtdyvwWJqlhsW8e6cPEUlsa')
  try:
    status = api.PostUpdate(message)
  except UnicodeDecodeError:
    print("Your message could not be encoded.  Perhaps it contains non-ASCII characters? ")
    print("Try explicitly specifying the encoding with the --encoding flag")
    sys.exit(2)
  print("%s just posted: %s" % (status.user.name, status.text))

def news():
    paper = newspaper.build('http://www.coindesk.com', memoize_articles=False)
    print(paper.size())
    #print(paper.articles[0].decode())
    for article in paper.articles:
        try:
            article.download()
            article.parse()
            print(str(article.text, 'utf-8'))
            if "bitcoin" in article.text.decode().lower() or "ethereum" in article.text.decode().lower() or "blockchain" in article.text.decode().lower():
                print("Okay")
                if 2 > 1:#"Digital Cash" in article.text.decode() or "Digital cash" in article.text.decode() or "digital cash" in article.text.decode():
                    api = twitter.Api(consumer_key='Ftv26M5zL6vDQAuzxRF2EBnnm',
                                     consumer_secret='yiQJcB1iicL28qE4utx4fuUhaBEGgF9n33J88lDfHz0b5bpk06',
                                     access_token_key='878690810409222145-vAvH0BEWRgYRcEBIOUrjTxrx11e1TEo',
                                     access_token_secret='dnoFxSJ113k4STzptxyQTvBtdyvwWJqlhsW8e6cPEUlsa')
                    try:
                        status = api.PostUpdate(article.title + "\n\n" + article.url)
                    except UnicodeDecodeError:
                        print("Your message could not be encoded.  Perhaps it contains non-ASCII characters? ")
                        print("Try explicitly specifying the encoding with the --encoding flag")
                        sys.exit(2)
                    print("%s just posted: %s" % (status.user.name, status.text))
                else:
                    pass
            else:
               pass
        except:
            pass

schedule.every().hours.do(tweet)
schedule.every().minutes.do(news)
#tweet()
while True:
    schedule.run_pending()
    time.sleep(60) # wait one minute

#if __name__ == "__main__":
#  main()
