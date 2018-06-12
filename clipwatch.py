#!/usr/bin/python -OOtt

from PyQt4 import QtCore, QtGui
import re
from utils import *
import ctypes
from time import sleep

class ClipWatch(QtCore.QThread):

    # signals
    sig_invalid = QtCore.pyqtSignal() # clipboard has jibberish
    sig_pass = QtCore.pyqtSignal() # order is mine
    sig_adjust = QtCore.pyqtSignal(dict) # order needs adjustment

    # thresholds
    LOW = 0.5 # below this is a small adjustment
    HIGH = 3.0 # above this is an extreme adjustment

    def __init__(self):
        QtCore.QThread.__init__(self)

        self.regex_spacing = re.compile(' +|\t+') # spacing between elements in raw data
        self.regex_quantity = re.compile('^[0-9]+/[0-9]+$') # buy/sell quantity substring
        self.regex_jump = re.compile('^Jumps?$') # jump distance substring
        self.regex_integer = re.compile('^[0-9]+$') # integers only
        self.regex_station = re.compile('^Station [0-9]+$') # market order

        #if os.environ.get('OS','') == 'Windows_NT':
        #    def get_cb(self):
        #        ctypes.windll.user32.OpenClipboard(None)
        #        pcontents = ctypes.windll.user32.GetClipboardData(1)
        #        data = ctypes.c_char_p(pcontents).value
        #        ctypes.windll.user32.CloseClipboard()
        #        return data

    def start(self):
        try:
            self.running = True

            cb = QtGui.QApplication.clipboard()
            self.contents = str(cb.text())

            while self.running:
                data = str(cb.text())

                if data and self.contents != data:
                    # clipboard change detected
                    self.contents = data
                    print
                    print
                    print "CLIPBOARD [%s]" % self.contents

                    # split into elements
                    parts = re.split(self.regex_spacing, data)
                    print "PARTS [%s]" % parts

                    flag_my_buy = False
                    flag_my_sell = False
                    flag_order = False
                    flag_value = False

                    index = -1
                    for p in parts:
                        index += 1
                        if re.search(self.regex_quantity, p):
                            # everything up to here is the item
                            item = ' '.join(parts[0:index])
                            print "ITEM [%s]" % item

                            # this part is the quantity
                            quantity = p
                            print "VALUE_RAW [%s]" % quantity

                            value_string = parts[index+1]
                            print "VALUE_STRING [%s]" % value_string

                            chop = value_string.replace(',', '')
                            value = float(chop)
                            print "VALUE [%s]" % value

                            # mark as value received
                            flag_value = True

                        if not flag_value and p == 'ISK':
                            # this is an existing order
                            item = ' '.join(parts[0:index-1])
                            print "ITEM [%s]" % item

                            value_string = parts[index-1]
                            print "VALUE_STRING [%s]" % value_string

                            chop = value_string.replace(',', '')
                            value = float(chop)
                            print "VALUE [%s]" % value

                            flag_order = True
                            print "=== ORDER ==="

                        elif not flag_order and re.match(self.regex_jump, p):
                            print "JUMPS: [%s]" % p
                            print "RANGE [%s]" % parts[index-1]
                            if re.match(self.regex_integer, parts[index-1]):
                                # this is my buy order
                                flag_my_buy = True
                                print "=== MY_BUY_ORDER ==="
                                break

                    if not flag_order and not flag_my_buy:
                        # must be my sell order
                        flag_my_sell = True
                        print "=== MY_SELL_ORDER ==="

                    ########################################################
                    # after processing clipboard
                    if flag_order:

                        # calculate change needed
                        percent_raw = (value - self.last_value) / self.last_value * 100.0
                        percent = '%.5f' % percent_raw
                        print 'PERCENT [%s]' % percent

                        if self.last_value == value:
                            # this order is my own order
                            print "=== THIS IS MY OWN ORDER ==="
                            self.sig_pass.emit()

                        elif self.last == 'B':
                            # this is a buy comparison
                            newvalue = value + 0.01
                            print "BUY NEWVALUE [%s]" % newvalue

                            d = {}
                            d['raw'] = self.contents 
                            d['item'] = self.last_item
                            d['percent'] = percent
                            d['newvalue'] = newvalue
                            d['type'] = self.last

                            if percent_raw <= self.LOW:
                                d['pixbuf'] = 'green'
                            elif percent_raw <= self.HIGH:
                                d['pixbuf'] = 'yellow'
                            else:
                                d['pixbuf'] = 'red'

                            # set clipboard contents
                            cb.setText(str(newvalue))

                            # emit data
                            self.sig_adjust.emit(d)


                        elif self.last == 'S':
                            # this is a sell comparison
                            newvalue = value - 0.01
                            print "SELL NEWVALUE [%s]" % newvalue

                            # emit data
                            d = {}
                            d['raw'] = self.contents 
                            d['item'] = self.last_item
                            d['percent'] = percent
                            d['newvalue'] = newvalue
                            d['type'] = self.last

                            if percent_raw <= self.LOW:
                                d['pixbuf'] = 'green'
                            elif percent_raw <= self.HIGH:
                                d['pixbuf'] = 'yellow'
                            else:
                                d['pixbuf'] = 'red'

                            # set clipboard contents
                            cb.setText(str(newvalue))

                            # emit data
                            self.sig_adjust.emit(d)


                    elif flag_my_buy:
                        self.last = 'B'
                        self.last_item = item

                    elif flag_my_sell:
                        self.last = 'S'
                        self.last_item = item

                    else:
                        # error
                        self.last = 'X'
                    print 'LAST [%s]' % self.last

                    # save current value as last
                    self.last_value = value

                else:
                    # clipboard contents did not change
                    pass

            sleep(0.25)


        except Exception as e:
            report_error('ERROR: %s' % e, 'check', None, e)

            # emit
            self.sig_invalid.emit()


if __name__ == '__main__':
    class Test(QtGui.QWidget):
        def __init__(self, parent=None):
            QtGui.QWidget.__init__(self, parent)

            self.resize(600,250)

            self.label1 = QtGui.QLabel()
            font = QtGui.QFont()
            font.setBold(True)
            font.setWeight(20)
            self.label1.setFont(font)

            self.layout = QtGui.QGridLayout()
            self.layout.addWidget(self.label1)

            self.setLayout(self.layout)


        def start(self):
            thread = ClipWatch()
            print "Thread created..."
            thread.sig_invalid.connect(self.data_invalid)
            thread.sig_pass.connect(self.data_pass)
            thread.sig_adjust.connect(self.data_adjust)
            thread.start()
            print "Thread running..."


        def data_invalid(self):
            x = "data_invalid"
            print x
            self.label1.setText(x)
            self.label1.repaint()


        def data_pass(self):
            x = "data_pass"
            print x
            self.label1.setText(x)
            self.label1.repaint()


        def data_adjust(self, d):
            x = "data_adjust"
            print x, d
            self.label1.setText(x)
            self.label1.repaint()


    import sys
    app = QtGui.QApplication(sys.argv)
    test = Test()
    test.show()
    test.start()
    sys.exit(app.exec_())

