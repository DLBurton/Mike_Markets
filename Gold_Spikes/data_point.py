__author__ = 'Darren'

import datetime


class DataDescriptor(object):
    def __init__(self, label):
        self.label = label

    def __get__(self, instance, owner):
        return instance.__dict__[self.label]

    def __set__(self, instance, value):

        try:
            if float(value) < 0:
                print "Invalue value: {0} entered, Cannot be less than 0".format(value)
                return
        except ValueError as err:
            print "Entered Value : {0} , cannot be converted to float".format(value)
            return

        if not hasattr(instance, self.label):
            instance.__dict__[self.label] = float(value)
        else:
            print "Not Allowed to reset value of : {0}".format(self.label)


class Market_Entry(object):

    _price = DataDescriptor("_price")
    _orders = DataDescriptor("_orders")


    def __init__(self, identifier, data):
        self.identity = identifier
        self._date = datetime.datetime.strptime(data.date, "%Y%m%d")
        self._time = str(data.time)
        self._price = data.price
        self._orders = data.orders



