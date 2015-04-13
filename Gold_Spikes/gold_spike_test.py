__author__ = 'Darren'
import re,collections
import os,fnmatch,sys
from data_point import Market_Entry as m
from market_data import Market_Formatter, CalculateSpike, ProfitCalculation
import datetime

BLOCK_SIZE = 8000
input_file = sys.argv[1]
data_format = collections.namedtuple("data_format","date time price orders")
MarketResults = Market_Formatter()

try:
    line_num = 0
    with open(input_file,'rU') as files_to_open:
        file_list = files_to_open.read().splitlines()

        for file in file_list:
            with open(file,'rU') as filename:
                document = filename.readlines()
                for line in document:
                    line = re.sub('\r\n$','',line)
                    line = re.sub("\"[^]]*\"",lambda x:x.group(0).replace(',',''),line)
                    line = line.replace(';',' ').split(' ')
                    entry = data_format(*line)
                    MarketResults.Store_entry(m(line_num,entry))
                    line_num += 1

except IOError as err:
    print "{0} : cannot open {1}".format(err,input_file)


MarketResults.SortPrices()

# Adjust these time ranges
time_range = [20] # In seconds
trigger_range = [1.5, 2.0] # Buy / Sell trigger ranges

def CalculateTotalProfit(results):

    losses = sum(results['losing'])
    wins = sum(results['winning'])
    return wins + losses


market_report = open("Boys_Market_Data.txt", 'w')
results_str = ""

for dead_time in time_range:
    for trigger in trigger_range:

        # Need to calculate for each entry the max spike up or down vs opening price
        # If larger than trigger then execute trade
        # Don't look at data time has passed
        # Record profit/loss value
        for key in sorted(MarketResults._market_list):
            wait_on_trade = None
            trade_in_progress = None
            spike_counter = 0
            Profit_Tracker = {"winning":[],"losing":[],"neutral":[]}

            for entry in sorted(MarketResults._market_list[key]):

                try:
                    current_time = datetime.datetime.strptime(str(entry), "%H%M%S")
                except ValueError as err:
                    print err

                if not wait_on_trade:
                    wait_on_trade = current_time

                if current_time.time() > wait_on_trade.time():
                    if trade_in_progress:
                        total_profit_from_trade = ProfitCalculation(MarketResults._market_list[key][entry], entry, trade_in_progress)
                        trade_in_progress = None
                        if total_profit_from_trade > 0:
                            Profit_Tracker['winning'].append(float(total_profit_from_trade))
                        elif total_profit_from_trade < 0:
                            Profit_Tracker['losing'].append(float(total_profit_from_trade))
                        else:
                            Profit_Tracker['neutral'].append(float(total_profit_from_trade))


                    wait_on_trade = current_time
                    spike, buyprice = CalculateSpike(MarketResults._market_list[key][entry], trigger)
                    if round(abs(spike),1) > round(trigger,1):
                        spike_counter += 1
                        wait_on_trade = datetime.datetime.strptime(str(entry), "%H%M%S") +  datetime.timedelta(0,dead_time)
                        trade_in_progress = (spike, entry, round(buyprice,1))
                else:
                    pass

            print("BOY TODAY YOUR TOTAL PROFIT LOSS ON {}".format(key))
            print("PARAMETERS TRIGGER={}, DEAD_TIME={}s".format(trigger, dead_time))
            print("=====================================")
            print("Total losses {} :  Total wins {} : Total neutral {}".format(len(Profit_Tracker['losing']), len(Profit_Tracker['winning']), len(Profit_Tracker['neutral'])))
            print("Total sum lost {} : Total sum won {}".format(sum(Profit_Tracker['losing']), sum(Profit_Tracker['winning'])))
            print("Total Profit/Loss : {}".format(CalculateTotalProfit(Profit_Tracker)))
            print("=====================================")
            results_str += "{} {} {} \n".format(trigger, dead_time, CalculateTotalProfit(Profit_Tracker))


market_report.write(results_str)


