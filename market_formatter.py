from market_class import Market_Entry
from datetime import datetime
import sys


class Market_Formatter(object):
    def __init__(self, market_list=[]):
        self._market_list = market_list

    def Helper(self):
        if len(self._market_list) != 0:
            print "Available Fields to search and slice are :"
            for key in self._market_list[0].__dict__:
                if key.startswith('_'): print key.lstrip('_')
        else:
            print "No Data in list to parse"

    def Store_entry(self, market_object):
        self._market_list.append(market_object)

    def Print(self, value=100):
        for item in self._market_list[:value]: item.PrintResults()

    def FieldStrip(self, field='data', low_val=None, high_val=None):
        """
	return a list of a filtered field
	"""
        print "=============="
        print "Attempting to Strip by {0} in range {1} - {2}".format(field, low_val, high_val)
        print "=============="

        field = "_" + field

        if not hasattr(self._market_list[0], field):
            print "Field |  {0} |  not available, Cannot be filtered".format(field.lstrip('_'))
            sys.exit()
        else:
            if field == "_date":
                low_val = datetime.strptime(low_val, '%d/%m/%Y')
                high_val = datetime.strptime(high_val, '%d/%m/%Y')
            if field == "_open_was_lowest":
                low_val = bool(low_val)
                high_val = low_val
            if type(getattr(self._market_list[0], field)) != type(low_val) or type(
                    getattr(self._market_list[0], field)) != type(high_val):
                raise Exception, " Wrong Types entered to sort field {0}  : Type low  {1}  Type high {2}".format(
                    type(getattr(self._market_list[0], field)), type(low_val), type(high_val))
            print isinstance(low_val, bool)
            if not isinstance(low_val, bool):
                assert high_val > low_val, "Data range entered incorrectly, low value must be smaller than high value"

        newlist = filter(lambda x: getattr(x, field) >= low_val and getattr(x, field) <= high_val, self._market_list)
        assert len(newlist) > 0, "Sliced field length is 0 , change your search parameters!"
        temp = Market_Formatter(newlist)
        return temp.FieldSort(field.lstrip('_'))

    def FieldSort(self, field='date', reverse=True):
        """
	 sort by a field within the market class category
	 """
        print "=============="
        print "Attempting to Sort by {0}".format(field)
        print "=============="

        field = "_" + field
        if not hasattr(self._market_list[0], field):
            print "Field |  {0} |  not available, Cannot be sorted".format(field.lstrip('_'))
            sys.exit()

        newlist = sorted(self._market_list, key=lambda x: getattr(x, field), reverse=reverse)
        return Market_Formatter(newlist)
