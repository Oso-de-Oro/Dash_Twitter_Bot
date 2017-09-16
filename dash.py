#!/usr/bin/env python

#import configparser
import getopt
import os
import sys
import schedule
import time
import krakenex
from datetime import date
import twitter

x = 0

def tweet():
  global x
  k = krakenex.API(key='API_Key', secret='Secret_Key')
  price = k.query_public('Ticker',{'pair': 'DASHUSD'})
  print(price['result']['DASHUSD']['a'][0])
  if 1 - x/float(price['result']['DASHUSD']['a'][0]) < 0:
       pop = (1 - x/float(price['result']['DASHUSD']['a'][0])) * 100
       message = 'DASH price: %.2f (%.2f%%)\n\n%s' % (float(price['result']['DASHUSD']['a'][0]), pop, time.ctime())
  elif 1 - x/float(price['result']['DASHUSD']['a'][0]) >= 0:
       pop = (1 - x/float(price['result']['DASHUSD']['a'][0])) * 100
       message = 'DASH price: %.2f (+%.2f%%)\n\n%s' % (float(price['result']['DASHUSD']['a'][0]), pop, time.ctime())
  x = float(price['result']['DASHUSD']['a'][0])
  api = twitter.Api(consumer_key='C_Key',
                        consumer_secret='C_Secret',
                        access_token_key='Token_Key',
                        access_token_secret='Token_Secret')
  try:
    status = api.PostUpdate(message)
  except UnicodeDecodeError:
    print("Your message could not be encoded.  Perhaps it contains non-ASCII characters? ")
    print("Try explicitly specifying the encoding with the --encoding flag")
    sys.exit(2)
  print("%s just posted: %s" % (status.user.name, status.text))

schedule.every().minutes.do(tweet)

while True:
    schedule.run_pending()
    time.sleep(60)
