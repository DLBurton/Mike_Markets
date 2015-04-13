#!/usr/bin/env python

import ROOT as r
import logging,itertools
import os,fnmatch,sys
from market_class import Market_Entry as m
from market_formatter import Market_Formatter
import re,collections
from datetime import datetime

BLOCK_SIZE = 8000
input_file = sys.argv[1]

MarketResults = Market_Formatter()
data_format = collections.namedtuple("data_format","date open high low closing trading_vol")

try:
  line_num = 0
  with open(input_file,'r') as filename:
    document = filename.readlines()
    for line in document[1:10]:
      line = re.sub('\r\n$','',line)
      line = re.sub("\"[^]]*\"",lambda x:x.group(0).replace(',',''),line)
      line = line.replace('"','').split(',')
      print line
      entry = data_format(*line[:6])
      MarketResults.Store_entry(m(line_num,entry))
      line_num += 1

except IOError as err:
  print "{0} : cannot open {1}".format(err,input_file)

MarketResults.Helper()
MarketResults_sorted = MarketResults.FieldSort("profit")
print "======================="
MarketResults_sorted.Print(50)

MarketResults_filtered = MarketResults.FieldStrip("open_was_lowest",True)
print "======================="
MarketResults_filtered.Print(20)

