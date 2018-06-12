#!/usr/bin/python -OOtt
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from stats_ui import Ui_Stats
from trader import Trader
import cPickle as pickle
import os, sys

# d['3841231553'].items()
#   @transactionDateTime  2015-04-11 01:01:42
#   @transactionID        3812367383
#   @quantity             5
#   @typeName             Small Focused Pulse Laser II
#   @typeID               3041
#   @price                539898.72
#   @clientID             1126586337
#   @clientName           triplleboy
#   @stationID            60003760
#   @stationName          Jita IV - Moon 4 - Caldari Navy Assembly Plant
#   @transactionType      sell
#   @transactionFor       personal
#   @journalTransactionID 11343438629
#   @clientTypeID         1383

class TraderStatistics(Ui_Stats):

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setupUi(self)
        self.retranslateUi(self)
        os.path.dirname(os.path.abspath(sys.argv[0]))

        self.setWindowTitle("Trader")
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.WindowMaximized | QtCore.Qt.WindowTitleHint )

        css = 'style2.css'
        with open(css,'r') as fd:
            self.setStyleSheet(fd.read())

        sales = self.load_transactions()

        self.table.setRowCount(len(sales))
        self.table.setColumnCount(4)
        self.table.setColumnWidth(0, 325)
        self.table.setColumnWidth(1, 135)
        self.table.setColumnWidth(2, 135)
        self.table.setColumnWidth(3, 135)

        total = 0
        rownum = 0
        for name in sales:
            profit = float(sales[name]['buy']) + float(sales[name]['sell'])

            total += profit
            #print '============= %22.2f %s %s' % (profit, name, total)

            self.table.setItem(rownum, 0, QtGui.QTableWidgetItem(name))
            self.table.setItem(rownum, 1, QtGui.QTableWidgetItem(Trader.pretty_float(sales[name]['buy'])))
            self.table.setItem(rownum, 2, QtGui.QTableWidgetItem(Trader.pretty_float(sales[name]['sell'])))
            self.table.setItem(rownum, 3, QtGui.QTableWidgetItem(Trader.pretty_float(profit)))
            rownum += 1

        print Trader.pretty_float(total)
        self.show()


    def load_transactions(self):
        try:
            f = open(Trader.TRANS_FILE_PATH, 'rb')
            transactions = pickle.load(f)
        except Exception as e:
            print "Failed to parse saved transactions file: %s" % Trader.TRANS_FILE_PATH
            import sys
            sys.exit(1)

        return self.calc_totals(transactions)


    def calc_totals(self, d):
        x = {}
        for trans in d: # for each transaction look for buys
            transactionType = d[trans]['@transactionType'] # buy/sell?

            if True: #d[trans]['@typeName'].startswith('Dread Guristas Medium'):
                price = float(d[trans]['@price'])
                quant = int(d[trans]['@quantity'])
                name = d[trans]['@typeName']
                subtotal = price * quant

                if name not in x:
                    x[name] = {}
                    x[name]['buy'] = 0
                    x[name]['sell'] = 0

                if transactionType == 'buy':
                    #print "+++buy"
                    x[name]['buy'] -= subtotal
                else:
                    #print "---sell"
                    x[name]['sell'] += subtotal

                #print '%s: (%sx%s) %s B%s S%s' % (name, price,quant, transactionType, x[name]['buy'], x[name]['sell'])

        return x

                    
############################################################
############################################################

if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    obj = TraderStatistics()
    sys.exit(app.exec_())



