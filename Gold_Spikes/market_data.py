from data_point import Market_Entry
from datetime import datetime
import sys


class Market_Formatter(object):
    def __init__(self, market_list={}):
        self._market_list = market_list

    def Store_entry(self, market_object):
        if self._market_list.has_key(str(market_object._date.date())):
            pass
        else :
            self._market_list[str(market_object._date.date())] = {}

        if self._market_list[str(market_object._date.date())].has_key(market_object._time):
            self._market_list[str(market_object._date.date())][market_object._time]["prices"].append(market_object._price)
        else:
            self._market_list[str(market_object._date.date())][market_object._time] = {"opening":market_object._price, "closing":market_object._price, "prices":[market_object._price]}


    def SortPrices(self):
        for key in sorted(self._market_list.iterkeys()):
            for market_entry in self._market_list[key].iterkeys():
                self._market_list[key][market_entry]['closing'] = self._market_list[key][market_entry]['prices'][-1]
                self._market_list[key][market_entry]['prices'] = sorted(self._market_list[key][market_entry]['prices'])


def CalculateSpike(data, trigger):

    opening = data['opening']
    lowest = data['prices'][0]
    highest = data['prices'][-1]

    if abs(lowest-opening) > highest-opening:
        return lowest-opening, opening-trigger

    return highest-opening, opening + trigger

def ProfitCalculation(data,entry, trade):

    opening = data['opening']
    if trade[0] > 0:
        #print opening, trade, round(trade[2] - opening,1)
        return round(trade[2] - opening,1)
    #print opening, trade, round(opening - trade[2],1)
    return round(opening - trade[2],1)


