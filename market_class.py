from datetime import datetime

class DataDescriptor(object):

   def __init__(self,label):
  	self.label = label

   def __get__(self, instance, owner): 
	return instance.__dict__[self.label]

   def __set__(self, instance, value): 

	try :
	   if float(value) < 0 :  
		print "Invalue value: {0} entered, Cannot be less than 0".format(value)
		return
	except ValueError as err :
	   print "Entered Value : {0} , cannot be converted to float".format(value)
	   return

	if not hasattr(instance,self.label):
	     instance.__dict__[self.label] = float(value)
	else : 
	     print "Not Allowed to reset value of : {0}".format(self.label)

class Market_Entry(object):

   _open = DataDescriptor("_open")
   _close = DataDescriptor("_close")
   _high = DataDescriptor("_high")
   _low = DataDescriptor("_low")
   _trading_vol = DataDescriptor("_trading_vol")

   def __init__(self,identifier,data):

 	self.identity = identifier
	self._date = datetime.strptime(data.date, '%d/%m/%Y')
	self._open = data.open
	self._close = data.closing
	self._high = data.high
	self._low = data.low
	self._trading_vol = data.trading_vol
        
        self._high_vs_zero = None
	self._low_vs_zero = None
	self._profit = None
	self._open_was_lowest = None
	self.DoCalculation() 
	
   def SanityCheck(self): 
 
	if self._high_vs_zero < 0 or self._low_vs_zero > 0:
	    print "Some shit ain't right here, market opening value : {0}, falls outside low : {1} and high : {2} parameters".format(self._open,self._low,self._high)
	    sys.exit()

   def DoCalculation(self): 

	self._high_vs_zero = self._high - self._open
	self._low_vs_zero = self._low - self._open
	self._profit = self._close - self._open
	self.SanityCheck()
	self.CheckOutcome()

   def CheckOutcome(self):

	self._open_was_lowest = True if self._low_vs_zero == 0 else False

   def PrintResults(self):
	print  " Date : {date} | Trade Volume : {trade:<13}   |  Open Value : {open:<8}  | Close Value : {close:<8}  |   Profit was :  {prof:<7} | Opening == Low : {isopen} ".format(date = self._date.strftime("%d %b %Y"),trade = self._trading_vol, open = self._open, close = self._close, prof=self._profit,isopen=self._open_was_lowest)

     
