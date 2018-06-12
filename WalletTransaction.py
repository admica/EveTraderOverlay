#!/usr/bin/python

from datetime import datetime
import re

class WalletTransaction(object):

    regex_pretty_float = re.compile(r'(\d)(\d\d\d[.,])')

    def __init__(self, item):
        self.transactionDateTime = item['@transactionDateTime']
        self.transactionID = item['@transactionID']
        self.quantity = item['@quantity']
        self.typeName = item['@typeName']
        self.typeid = item['@typeID']
        self.price = item['@price']
        self.clientID = item['@clientID']
        self.clientName = item['@clientName']
        self.stationID = item['@stationID']
        self.stationName = item['@stationName']
        self.transactionType = item['@transactionType']
        self.transactionFor = item['@transactionFor']
        self.journalTransactionID = item['@journalTransactionID']
        self.clientTypeID = item['@clientTypeID']

        self.datetime = item['@transactionDateTime']
        self.pretty_price = item['@price']

    def __repr__(self):
        data = 'NAME: %s' % self.typeName
        data += '\n'
        data += 'PRICE: %s x%s' % (self.pretty_price, self.quantity)
        data += '\n'
        data += 'DATETIME: %s' % self.datetime
        return data


    @property
    def datetime(self):
        try:
            return self._datetime
        except:
            return None
    @datetime.setter
    def datetime(self, val):
        try:
            self._datetime = datetime.strptime(val, '%Y-%m-%d %H:%M:%S')
        except Exception as e:
            print e
            self._datetime = None


    @property
    def pretty_price(self):
        try:
            return self._pretty_price
        except:
            return None
    @pretty_price.setter
    def pretty_price(self, val):
        # commas for make benefit glorious readability
        try:
            temp = "%.2f" % float(val)

            count = 20
            while count:
                count -= 1
                temp, count = re.subn(self.regex_pretty_float, r'\1,\2', temp)
                if not count:
                    break
            self._pretty_price = temp
        except Exception as e:
            print e
            return val

if __name__ == '__main__':

    from _transactions import Transactions
    import xmltodict
    import re

    response = xmltodict.parse(Transactions.XML.strip())
    items = response['eveapi']['result']['rowset']['row']

    #for i in items:
    #    if int(i['@typeID']) < 50:
    #        print i['@typeID'], i['@typeName']
    #print

    w = WalletTransaction(items[0])
    for k,v in w.__dict__.items():
        print k, v

    print '---'
    print w

