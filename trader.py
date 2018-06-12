#!/usr/bin/python -OOtt
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from main_ui import Ui_Trader
import re
from functools import partial
import csv
import urllib2
from datetime import datetime
import xmltodict
import cPickle as pickle
from utils import *

class Trader(Ui_Trader):
    # constants and defaults
    EXPORT_PATH = 'C:\\Users\\user\\Documents\\EVE\\logs\\Marketlogs'
    FILE_PATH = 'C:\\Users\\user\\Desktop\\MEGA\\eve\\trader\\'
    API_KEY_PATH = '%skey.txt' % FILE_PATH
    PREF_FILE_PATH = '%sprefs.txt' % FILE_PATH
    TRANS_FILE_PATH = '%strans.dat' % FILE_PATH
    IMG_INVALID = 'icons/skull.png'
    IMG_WHITE = 'icons/small_whitelight.png'
    IMG_BLACK = 'icons/small_blacklight.png'
    IMG_GREEN = 'icons/small_greenlight.png'
    IMG_YELLOW = 'icons/small_yellowlight.png'
    IMG_RED = 'icons/small_redlight.png'
    IMG_ARROW_UP = 'icons/arrow-up.png'
    IMG_ARROW_DOWN = 'icons/arrow-down.png'
    IMG_ARROW_UP_GOOD = 'icons/arrow_up_good.png'
    IMG_ARROW_UP_BAD = 'icons/arrow_up_bad.png'
    IMG_ARROW_DOWN_GOOD = 'icons/arrow_down_good.png'
    IMG_ARROW_DOWN_BAD = 'icons/arrow_down_bad.png'

    ARROW_SIZE = 18
    PIXMAP_SIZE = 128
    ICON_SIZE = 15
    API_FETCH_TTL = 300 # seconds since last pull before pulling new data
    TRADE_LOW = 0.3 # below this is a small adjustment
    TRADE_HIGH = 2.0 # above this is an extreme adjustment
    EXPORT_LOW = 14.0 # below this is red
    EXPORT_HIGH = 21.0 # above this is green
    ROWCOUNT = 2500 # number of wallet transactions to pull from api
    FULLPULL = True # add walking transactions backwards to get older than rowcount
    FULLPULLPAGES = 2 # number of pages of transactions to pull
    COLOR_GREEN = '#04B404'
    COLOR_YELLOW = '#FCFC00'
    COLOR_RED = '#FF0000'

    # regex
    regex_pretty_float = re.compile(r'(\d)(\d\d\d[.,])')
    regex_spacing = re.compile(' +|\t+') # spacing between elements in raw data
    regex_quantity = re.compile('^[0-9]+/[0-9]+$') # buy/sell quantity substring
    regex_jump = re.compile('^Jumps?$') # jump distance substring
    regex_integer = re.compile('^[0-9]+$') # integers only
    regex_station = re.compile('^Station [0-9]+$') # market order

    # signals
    sig_invalid = QtCore.pyqtSignal(str, str) # clipboard has jibberish
    sig_pass = QtCore.pyqtSignal() # order is mine
    sig_adjust = QtCore.pyqtSignal() # order needs adjustment
    sig_valid = QtCore.pyqtSignal() # valid buy/sell order type
    sig_api_id = QtCore.pyqtSignal(str)
    sig_api_key = QtCore.pyqtSignal(str)
    sig_fetch = QtCore.pyqtSignal() # order needs history lookup
    sig_match = QtCore.pyqtSignal(list) # historical sale found

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setupUi(self)
        self.retranslateUi(self)

        self.transactions = {}
        self.blueprints = {}
        self._highpipe = 1000
        self._lowpipe = 10
        self._channel_pad = 5
        self._pipe = 375000

        import os, sys
        os.path.dirname(os.path.abspath(sys.argv[0]))

        self.FOREALDOE = True # debugging mode?
        try:
            if sys.argv[1] in [ '-d', '--d', '--debug', 'debug' ]:
                self.FOREALDOE = False
                print "[Debug Mode Activated]"
        except:
                pass

        with open('copyright.txt', 'r') as fd:
            split = 55
            start = 0
            data = ''
            lines = fd.readlines()
            lines = '\n'.join(lines).strip()
            times = (len(lines) / split) + 1 # plus the leftover
            for x in range(0,times):
                i = 0
                try:
                    for i in range(0,split):
                        if lines[split+i] == ' ':
                            break
                except:
                    pass 
                data += lines[start:split+i].strip()
                data += '\n'
                start = split+i
                split += split+i
            data = data.strip()
            self.label_copyright.setText(data.strip())
        self.label_copyright.setStyleSheet("QLabel { background-image: url('icons/bullethole1.png'); }")

        self.frame_pref.setStyleSheet("QWidget { background-image: url('icons/hype.png');}")
        self.label_export_yellow.setStyleSheet("QLabel { background: transparent; color: white };")
        self.label_trade_yellow.setStyleSheet("QLabel { background: transparent; color: white };")
        self.label_export_green.setStyleSheet("QLabel { background: transparent; color: white };")
        self.label_trade_green.setStyleSheet("QLabel { background: transparent; color: white };")
        self.label_pref_cached.setStyleSheet("QLabel { background: transparent; color: white };")
        self.label_pref_cached_static.setStyleSheet("QLabel { background: transparent; color: white };")
        self.label_api_ttl.setStyleSheet("QLabel { background: transparent; color: white };")
        self.pushButton_pref_clear.setStyleSheet("QButton { background: black; color: white };")
        self.pushButton_pref_save.setStyleSheet("QButton { background: black; color: white };")
        self.lineEdit_pref_file_path.setStyleSheet("QLineEdit { background: black; color: white };")
        self.lineEdit_pref_export_path.setStyleSheet("QLineEdit { background: black; color: white };")
        
        self.frame_setup.setStyleSheet("QWidget { background-image: url('icons/drifters.png');}")
        self.label_api_char.setStyleSheet("QLabel { background: transparent; color: white };")
        self.label_api_id.setStyleSheet("QLabel { background: transparent; color: white };")
        self.label_api_key.setStyleSheet("QLabel { background: transparent; color: white };")
        self.label_license.setStyleSheet("QLabel { background: transparent; color: white };")
        self.lineEdit_api_id.setStyleSheet("QLineEdit { background: black; color: white };")
        self.lineEdit_api_key.setStyleSheet("QLineEdit { background: black; color: white };")
        self.lineEdit_license.setStyleSheet("QLineEdit { background: black; color: white };")
        self.pushButton_api_fetch.setStyleSheet("QButton { background: transparent; color: white };")
        self.pushButton_api_save.setStyleSheet("QButton { background: transparent; color: white };")
        self.comboBox_char.setStyleSheet("QComboBox { background: black; color: white };")

        self.frame_calc.setStyleSheet("QWidget { background-image: url('icons/obelisk.png');}")

        # indy
        #self.combo_blueprint.currentIndexChanged.connect(self.cb_combo_blueprint)
        self.combo_blueprint.activated.connect(self.cb_combo_blueprint)
        self.combo_blueprint.setEnabled(True)
        self.combo_blueprint.setStyleSheet("QCombo { background: black; color: white; font-size 8pt };")
        self.table_blueprint.setStyleSheet("QTable { background: black; color: white; font-size 7pt };")
        self.table_blueprint.setColumnCount(6)
        self.table_blueprint.setColumnWidth(0, 224) # name
        self.table_blueprint.setColumnWidth(1, 95) # quantity
        self.table_blueprint.setColumnWidth(2, 95) # have
        self.table_blueprint.setColumnWidth(3, 95) # paid
        self.table_blueprint.setColumnWidth(4, 95) # missing
        self.table_blueprint.setColumnWidth(5, 95) # cost
        self.table_blueprint.setHorizontalHeaderLabels(['Item Name', 'Quantity', 'Cost', 'Bought', 'Missing', 'Projected'])

        # manual force item
        self.button_manual.clicked.connect(self.cb_button_manual)
        self.combo_manual.currentIndexChanged.connect(self.cb_combo_manual)
        self.combo_manual.activated.connect(self.cb_combo_manual_activated)
        self.combo_manual.setEnabled(True)
        self.combo_manual.setEditable(True)
        self.combo_manual.hide()

        self.api_id = None
        self.api_key = None
        self.api_char = [] # 1st element designates current user
        self.api_charid = None # set on first data pull
        self.flag_manual_item = False # manually selected item
        self.d = {} # data container

        # compare to this date to determine if new data is needed
        self.last_fetch = datetime(2003,5,6) # Eve Online, Initial release date

        # add fonts
        QtGui.QFontDatabase.addApplicationFont('fonts/paratype-pt-sans/PTS75F.ttf')
        QtGui.QFontDatabase.addApplicationFont('fonts/liberation/LiberationSansNarrow-Regular.ttf')
        QtGui.QFontDatabase.addApplicationFont('fonts/armalite-rifle.ttf')

        #self.setWindowTitle("Estamel's Modified Adaptive Trading App")
        self.setWindowTitle("Trader")
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.WindowMaximized | QtCore.Qt.WindowTitleHint )

        css = 'style2.css'
        with open(css,'r') as fd:
            self.setStyleSheet(fd.read())

        pixmap = QtGui.QPixmap(self.IMG_BLACK)
        pixmap = pixmap.scaled(self.PIXMAP_SIZE, self.PIXMAP_SIZE, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
        self.label_pixmap.setPixmap(pixmap)

        self.ICON_BUY = QtGui.QIcon('icons/buy.png') #status_orange.png')
        self.ICON_SELL = QtGui.QIcon('icons/sell.png') #status_purple.png')
        self.ICON_MINE = QtGui.QIcon('icons/status_white.png')
        self.ICON_LOW = QtGui.QIcon('icons/status_green.png')
        self.ICON_MED = QtGui.QIcon('icons/status_yellow.png')
        self.ICON_HIGH = QtGui.QIcon('icons/status_red.png')

        # arrows
        pixmap = QtGui.QPixmap(self.IMG_ARROW_UP_GOOD)
        self.PIXMAP_ARROW_UP_GOOD = pixmap.scaled(self.ARROW_SIZE, self.ARROW_SIZE, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation) 

        pixmap = QtGui.QPixmap(self.IMG_ARROW_UP_BAD)
        self.PIXMAP_ARROW_UP_BAD = pixmap.scaled(self.ARROW_SIZE, self.ARROW_SIZE, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation) 

        pixmap = QtGui.QPixmap(self.IMG_ARROW_DOWN_GOOD)
        self.PIXMAP_ARROW_DOWN_GOOD = pixmap.scaled(self.ARROW_SIZE, self.ARROW_SIZE, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation) 

        pixmap = QtGui.QPixmap(self.IMG_ARROW_DOWN_BAD)
        self.PIXMAP_ARROW_DOWN_BAD = pixmap.scaled(self.ARROW_SIZE, self.ARROW_SIZE, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation) 

        self.listmodel = QtGui.QStandardItemModel(self.listView)
        self.listView.setModel(self.listmodel)
        self.listView.setIconSize(QtCore.QSize(self.ICON_SIZE, self.ICON_SIZE))
        self.listView.hide()

        self.running = True

        self.last_value = 0.000000001
        self.last = 'BUY'
        self.last_item = 'Nothing'
        self.calc_pretty = '' # 1,234.56
        self.calc_raw = ''    # 1234.56
        self.calc_saved = None # previous value
        self.calc_symbol = None # math operator

        # preferences
        self.label_trade_green.setStyleSheet("QLabel { color: %s; }" % self.COLOR_GREEN)
        self.label_trade_yellow.setStyleSheet("QLabel { color: %s; }" % self.COLOR_YELLOW)
        self.label_export_green.setStyleSheet("QLabel { color: %s; }" % self.COLOR_GREEN)
        self.label_export_yellow.setStyleSheet("QLabel { color: %s; }" % self.COLOR_YELLOW)

        # min/max ranges
        self.spin_api_ttl.setRange(60,9001)
        self.spin_trade_green.setRange(0.01,99.7)
        self.spin_trade_yellow.setRange(0.02,99.8)
        self.spin_export_green.setRange(0.02,99.8)
        self.spin_export_yellow.setRange(0.01,99.7)

        # load user preferences from file or grab defaults
        if not self.load_prefs():
            self.lineEdit_pref_export_path.setText(self.EXPORT_PATH)
            self.lineEdit_pref_file_path.setText(self.PREF_FILE_PATH)

            self.spin_api_ttl.setValue(self.API_FETCH_TTL)
            self.spin_trade_green.setValue(self.TRADE_LOW)
            self.spin_trade_yellow.setValue(self.TRADE_HIGH)
            self.spin_export_green.setValue(self.EXPORT_HIGH)
            self.spin_export_yellow.setValue(self.EXPORT_LOW)
        self.spin_api_ttl.valueChanged.connect(self.cb_pref_changed_ttl)
        self.spin_trade_green.valueChanged.connect(self.cb_pref_changed_tg)
        self.spin_trade_yellow.valueChanged.connect(self.cb_pref_changed_ty)
        self.spin_export_green.valueChanged.connect(self.cb_pref_changed_eg)
        self.spin_export_yellow.valueChanged.connect(self.cb_pref_changed_ey)
        self.pushButton_pref_save.clicked.connect(self.cb_pref_save)

        # trade signals
        self.sig_api_id.connect(self.cb_sig_api_id) # api id line changed
        self.sig_api_key.connect(self.cb_sig_api_key) # api key line changed
        self.sig_invalid.connect(self.data_invalid)
        self.sig_pass.connect(self.data_pass)
        self.sig_adjust.connect(self.data_adjust) # api lookup signal emitted here too
        self.sig_valid.connect(self.data_valid)
        self.sig_fetch.connect(self.data_fetch) # api lookup
        self.sig_match.connect(self.data_match) # sale found

        # calc signals
        self.pushButton_0.clicked.connect(partial(self.cb_push_append, '0'))
        self.pushButton_1.clicked.connect(partial(self.cb_push_append, '1'))
        self.pushButton_2.clicked.connect(partial(self.cb_push_append, '2'))
        self.pushButton_3.clicked.connect(partial(self.cb_push_append, '3'))
        self.pushButton_4.clicked.connect(partial(self.cb_push_append, '4'))
        self.pushButton_5.clicked.connect(partial(self.cb_push_append, '5'))
        self.pushButton_6.clicked.connect(partial(self.cb_push_append, '6'))
        self.pushButton_7.clicked.connect(partial(self.cb_push_append, '7'))
        self.pushButton_8.clicked.connect(partial(self.cb_push_append, '8'))
        self.pushButton_9.clicked.connect(partial(self.cb_push_append, '9'))
        self.pushButton_000.clicked.connect(self.cb_push_000)
        self.pushButton_dot.clicked.connect(partial(self.cb_push_dot, '.'))
        self.pushButton_01.clicked.connect(partial(self.cb_push_dot, '.01'))
        self.pushButton_99.clicked.connect(partial(self.cb_push_dot, '.99'))
        self.pushButton_divide.clicked.connect(partial(self.cb_push_math, '/'))
        self.pushButton_x.clicked.connect(partial(self.cb_push_math, 'x'))
        self.pushButton_minus.clicked.connect(partial(self.cb_push_math, '-'))
        self.pushButton_plus.clicked.connect(partial(self.cb_push_math, '+'))
        self.pushButton_equal.clicked.connect(self.cb_push_equal)

        self.pushButton_C.clicked.connect(self.cb_push_clear)

        # api setup
        self.comboBox_char.currentIndexChanged.connect(self.cb_api_char_changed)
        self.comboBox_char.setDisabled(True)
        self.label_api_char.setDisabled(True)
        self.lineEdit_api_id.textEdited.connect(self.cb_modified_api_id)
        self.lineEdit_api_key.textEdited.connect(self.cb_modified_api_key)
        self.pushButton_api_fetch.clicked.connect(self.cb_push_api_fetch) 
        self.pushButton_api_save.clicked.connect(self.cb_push_api_save) 
        # load user data from file
        if not self.load_key():
            self.pushButton_api_fetch.setDisabled(True) # start disabled
            self.pushButton_api_save.setDisabled(True) # start disabled

        #self.connect(QtGui.QApplication.clipboard(), QtCore.SIGNAL('dataChanged()'), self.dataChanged_cb)
        QtGui.QApplication.clipboard().dataChanged.connect(self.dataChanged_cb)

        # force buy override
        self.force_buy = False
        self.checkBox_buy.setCheckState(QtCore.Qt.Unchecked)
        self.checkBox_buy.toggled.connect(self.checkBox_buy_cb)

        # force sell override        
        self.force_sell = False
        self.checkBox_sell.setCheckState(QtCore.Qt.Unchecked)
        self.checkBox_sell.toggled.connect(self.checkBox_sell_cb)

        # line edit gets focus in calc
        self.tabWidget.currentChanged.connect(self.cb_tab_changed)

        # get starting snapshot of exports
        self.qdir_existing = self.get_files()
        
        # watch for exports
        self.watcher = QtCore.QFileSystemWatcher([self.EXPORT_PATH])
        self.watcher.directoryChanged.connect(self.watcher_changed)

        # matching orders area
        self.label_m_sell_fixed.setStyleSheet("QLabel { color: orange; }")
        self.label_m_buy_fixed.setStyleSheet("QLabel { color: purple; }")

        self.label_m_sell_low.setStyleSheet("QLabel { font-weight:600; }")
        self.label_m_buy_high.setStyleSheet("QLabel { font-weight:600; }")

        self.show()

        try:
            self.get_charid()

            try:
                print "Loading saved transactions from file... ",
                f = open(self.TRANS_FILE_PATH, 'rb')
                self.transactions = pickle.load(f)
                print "Transactions: %d" % len(self.transactions)
            except IOError:
                print "No transactions loaded."

        except Exception as e:
            report_error("charload nope", 'init', None, e)


    def cb_combo_blueprint(self):
        name = self.combo_blueprint.currentText()
        print name

        try:
            print 'Total Prints Known:', self.indy.size
        except:
            # load all prints for the first time
            from indy import Indy
            self.indy = Indy()

        parts = name.split('  (ME')
        name = parts[0]

        mete = parts[1] # "10 TE20"
        me, te = parts[1].split(' TE')
        me = str(me).strip()
        te = str(te)[:-1].strip()

        for x in self.blueprints:
            if self.blueprints[x]['@typeName'] == name:
                if self.blueprints[x]['@materialEfficiency'] == me and self.blueprints[x]['@timeEfficiency'] == te:
                    # [u'@itemID', u'@locationID', u'@typeID', u'@typeName', u'@flagID',
                    # u'@quantity', u'@timeEfficiency', u'@materialEfficiency', u'@runs']

                    # lookup item to get parts
                    bp = self.indy.build(int(self.blueprints[x]['@typeID']))

                    self.table_blueprint.verticalHeader().hide()

                    # handle bp parse failure
                    if bp is False:
                        self.table_blueprint.setRowCount(1)
                        self.table_blueprint.setColumnCount(1)
                        self.table_blueprint.setColumnWidth(0, 420)
                        self.table_blueprint.setItem(0, 0, QtGui.QTableWidgetItem('Failed to parse blueprint'))
                        return

                    try: 
                        # table initial setup
                        self.table_blueprint.setRowCount(len(bp['materials'])) # set table size
                        # set table
                        count = 0
                        rownum = 0
                        for row in bp['materials']:
                            # lookup part in transactions
                            row['part_quant'] = 0
                            row['part_cost_total'] = 0.00
                            row['name'] = 'Part:%s' % row['typeID']
                            for t in self.transactions:
                                if int(self.transactions[t]['@typeID']) == row['typeID']:
                                    row['part_quant'] += int(self.transactions[t]['@quantity'])
                                    row['part_cost_total'] += int(self.transactions[t]['@quantity']) * float(self.transactions[t]['@price'])

                            # cost per unit based on average paid
                            if row['part_quant'] > 0:
                                row['part_cost_avg'] = row['part_cost_total'] / row['part_quant']
                                row['part_cost'] = row['part_cost_avg'] * row['quantity']
                            else:
                                row['part_cost_avg'] = 0
                                row['part_cost'] = 0

                            # missing units
                            row['part_missing'] = row['quantity'] - row['part_quant']
                            if row['part_missing'] < 0:
                                row['part_missing'] = 0

                            # projected cost of missing assuming bought at average price paid
                            if row['part_quant'] > 0: # must have bought some in order to project
                                row['part_missing_project'] = row['part_missing'] * row['part_cost_avg']
                            else:
                                row['part_missing_project'] = 0

                            self.table_blueprint.setRowHeight(rownum, 20)

                            flag = False
                            for t in self.transactions:
                                if row['typeID'] == int(self.transactions[t]['@typeID']):
                                    self.table_blueprint.setItem(rownum, 0, QtGui.QTableWidgetItem(str(self.transactions[t]['@typeName'])))
                                    flag = True
                            if not flag:
                                self.table_blueprint.setItem(rownum, 0, QtGui.QTableWidgetItem(str(row['typeID'])))

                            self.table_blueprint.setItem(rownum, 1, QtGui.QTableWidgetItem(str(row['quantity'])))
                            self.table_blueprint.setItem(rownum, 2, QtGui.QTableWidgetItem(self.pretty_float(row['part_cost'])))
                            self.table_blueprint.setItem(rownum, 3, QtGui.QTableWidgetItem(self.pretty_float(row['part_quant'])))
                            self.table_blueprint.setItem(rownum, 4, QtGui.QTableWidgetItem(str(row['part_missing'])))
                            self.table_blueprint.setItem(rownum, 5, QtGui.QTableWidgetItem(self.pretty_float(row['part_missing_project'])))

                            rownum += 1

                        self.table_blueprint.show()

                        # set product name
                        #product = str(bp['products'][0]['typeID'])[:20]
                        #self.label_blueprint.setText(product)

                        # calculate total paid for 1 build
                        tot = 0
                        for row in bp['materials']:
                            tot += row['part_cost'] # average paid per unit so far
                            tot += row['part_missing_project'] # additional cost to buy more at average paid so far
                        self.label_cost_actual.setText(self.pretty_float(tot))

                    except Exception as e:
                        print "*"*42
                        report_error("Problem with blueprint table", 'cb_combo_blueprint', None, e)
                        print "*"*42
                        return

                    # done
                    break


    def cb_combo_manual_activated(self):
        name = self.combo_manual.currentText()

        # default to buy if not specified yet
        try:
            t = self.d['type'] # get before clearing self.d
        except: # handles both no dictionary and no key
            t = 'BUY'

        self.d = {}
        self.d['item'] = name
        self.last_item = name
        self.label_item.setText(name)

        if t == 'BUY':
            sell_low = self.label_m_sell_low.text()
            try:
                float(sell_low) # test
                self.d['last'] = sell_low
            except ValueError:
                pass

        elif t == 'SELL':
            buy_high = self.label_m_buy_high.text()
            try:
                float(buy_high) # test
                self.d['last'] = buy_high
            except ValueError:
                pass

        self.sig_fetch.emit()


    def cb_combo_manual(self):
        """select item, hide combo, restore button"""
        self.combo_manual.hide()
        self.button_manual.show()


    def cb_button_manual(self):
        """hide button, show combo"""
        self.button_manual.hide()
        self.combo_manual.show()


    def load_prefs(self):
        """load preferences from file"""
        try:
            with open(self.PREF_FILE_PATH, 'r') as f:
                self.API_FETCH_TTL = float(f.readline().strip())
                self.TRADE_LOW = float(f.readline().strip())
                self.TRADE_HIGH = float(f.readline().strip())
                self.EXPORT_HIGH = float(f.readline().strip())
                self.EXPORT_LOW = float(f.readline().strip())

                self.spin_api_ttl.setValue(self.API_FETCH_TTL)
                self.spin_trade_green.setValue(self.TRADE_LOW)
                self.spin_trade_yellow.setValue(self.TRADE_HIGH)
                self.spin_export_green.setValue(self.EXPORT_HIGH)
                self.spin_export_yellow.setValue(self.EXPORT_LOW)

                # load success
                return True
 
        except Exception as e:
            print 'Failed to load preferences, error: %s' % e

        # failed to load for any reason
        return False


    def cb_pref_save(self):
        """save button pushed"""
        self.pushButton_pref_save.setDisabled(True)

        try:
            with open(self.PREF_FILE_PATH, 'w') as f:
                f.write('%s\n' % self.API_FETCH_TTL)
                f.write('%s\n' % self.TRADE_LOW)
                f.write('%s\n' % self.TRADE_HIGH)
                f.write('%s\n' % self.EXPORT_HIGH)
                f.write('%s\n' % self.EXPORT_LOW)

                # save success
                return True

        except Exception as e:
            print "Failed to save, error: %s" % e


    def cb_pref_changed_ttl(self):
        """enable save button when ttl gets changed"""
        self.pushButton_pref_save.setEnabled(True)
        self.API_FETCH_TTL = float(self.spin_api_ttl.text())

    def cb_pref_changed_tg(self):
        """enable save button when trade green gets changed"""
        self.pushButton_pref_save.setEnabled(True)
        self.TRADE_LOW = float(self.spin_trade_green.text())

    def cb_pref_changed_ty(self):
        """enable save button when trade yellow gets changed"""
        self.pushButton_pref_save.setEnabled(True)
        self.TRADE_HIGH = float(self.spin_trade_yellow.text())

    def cb_pref_changed_eg(self):
        """enable save button when export green gets changed"""
        self.pushButton_pref_save.setEnabled(True)
        self.EXPORT_HIGH = float(self.spin_export_green.text())

    def cb_pref_changed_ey(self):
        """enable save button when export yellow gets changed"""
        self.pushButton_pref_save.setEnabled(True)
        self.EXPORT_LOW = float(self.spin_export_yellow.text())


    def reset_match_labels(self):
        """clear labels"""
        self.label_m_sell_low_icon.clear()
        self.label_m_sell_high_icon.clear()
        self.label_m_sell_low.setText('')
        self.label_m_sell_high.setText('')
        self.label_m_sell_low_percent.setText('')
        self.label_m_sell_high_percent.setText('')
        self.label_m_buy_low_icon.clear()
        self.label_m_buy_high_icon.clear()
        self.label_m_buy_low.setText('')
        self.label_m_buy_high.setText('')
        self.label_m_buy_low_percent.setText('')
        self.label_m_buy_high_percent.setText('')


    def cb_api_char_changed(self):
        self.pushButton_api_save.setEnabled(True)
        
        
    def get_charid(self):
        _id = ('%s' % self.api_id).strip()
        _key = ('%s' % self.api_key).strip()
        self.url_get_chars = 'https://api.eveonline.com/account/characters.xml.aspx?keyID=%s&vCode=%s' % (_id, _key)
        
        if self.FOREALDOE:
            #PRODUCTION MODE
            response = urllib2.urlopen(self.url_get_chars)
            xml = response.read().strip()
        else:
            # DEBUGGING MODE
            print "DEBUG GET_CHARID"
            with open('_characters.txt', 'r') as f:
                xml = ''
                for line in f.readlines():
                    xml += line

        # get names and characterids
        charlist, charidlist = self.chop_chars(xml)
        for x,y in zip(charlist, charidlist): print x,y
        
        # find matching charid to current char
        for c,i in zip(charlist, charidlist):
            if c == self.api_char[0]:
                self.api_charid = i

        return


    def data_parse(self, url, fullpull=False):
        """get url and parse xml results"""
        if self.FOREALDOE:
            # PRODUCTION MODE
            response = urllib2.urlopen(url)
            xml = response.read().strip()
        else:
            # DEBUGGING MODE
            print "DEBUG DATA_PARSE"
            if fullpull:
                from _transactions2 import Transactions as t
                xml = t.XML.strip()
            else:
                from _transactions import Transactions as t
                xml = t.XML.strip()

        return xmltodict.parse(xml)


    def data_fetch(self):
        now = datetime.now()
        if (now-self.last_fetch).seconds > self.API_FETCH_TTL:
            # time to fetch new data
            last_pipe = (now-datetime(self._highpipe, self._lowpipe, self._channel_pad, 1, 1, 1, 100000)).days

            if not self.api_charid:
                # get charid
                self.get_charid()

            if len(self.transactions) == 0:
                try:
                    print "Loading saved transactions from file... ",
                    f = open(self.TRANS_FILE_PATH, 'rb')
                    self.transactions = pickle.load(f)
                    print "Transactions: %d" % len(self.transactions)
                except IOError:
                    print "No transactions loaded."

            url = 'https://api.eveonline.com/Char/WalletTransactions.xml.aspx?keyID=%s&vCode=%s&CharacterID=%s&rowCount=%s' % (self.api_id, self.api_key, self.api_charid, self.ROWCOUNT)

            if last_pipe > self._pipe:
                self.FULLPULL = False
                QtGui.QApplication.clipboard().dataChanged.disconnect()

            # browse url and parse it
            response = self.data_parse(url)

            for d in response['eveapi']['result']['rowset']['row']:
                self.transactions[d['@transactionID']] = d
            print "Transactions: %d" % len(self.transactions)

            if self.FULLPULL:
                self.FULLPULL = False

                fromID = self._highpipe # initialize as not last_fromID
                last_fromID = self._lowpipe # initialize as not fromID
                counter = 0
                while fromID != last_fromID and 'row' in response['eveapi']['result']['rowset'] and counter < 20:
                    counter += 1
                    try:
                        # get oldest transaction id for backwalking
                        fromID = int(response['eveapi']['result']['rowset']['row'][-1]['@transactionID'])
                        last_fromID = fromID # save current

                        for d in response['eveapi']['result']['rowset']['row']:
                            if int(d['@transactionID']) < fromID:
                                #print int(d['@transactionID'])
                                fromID = d['@transactionID']
                                #print "Journal out of order,", fromID
                                
                        url = 'https://api.eveonline.com/Char/WalletTransactions.xml.aspx?keyID=%s&vCode=%s&CharacterID=%s&rowCount=%s&fromID=%s' % (self.api_id, self.api_key, self.api_charid, self.ROWCOUNT, fromID)
                        #print url
                        # browse url and parse it
                        response = self.data_parse(url, fullpull=True)

                        for d in response['eveapi']['result']['rowset']['row']:
                            if d['@transactionID'] not in self.transactions.keys():
                                #print d['@transactionID']
                                self.transactions[d['@transactionID']] = d

                    except Exception as e:
                        print "Failed to walk backwards for older transactions:", e
                        break
            
            self.label_pref_cached.setText('%s' % len(self.transactions))

            # save transactions to file
            with open(self.TRANS_FILE_PATH, 'wb') as f:
                pickle.dump(self.transactions, f)
                print "%d TRANSACTIONS SAVED" % len(self.transactions)

            # save this time
            self.last_fetch = datetime.now()

        else:
            print "[USING CACHE]\n"

        # find this item
        matchlist, manuallist = [], []
        for item in self.transactions.values():
            #print "[%s] [%s]" % (item['@transactionDateTime'], item['@typeName'])
            if item['@typeName'] == self.d['item']:
                # found a sale
                matchlist.append(item)

            # fill manual list for combobox
            if item['@typeName'] not in manuallist:
                manuallist.append(item['@typeName'])
        manuallist.sort()                

        # set combobox items
        self.combo_manual.clear()
        self.combo_manual.addItems(manuallist)
        
        matchlist.sort(key=lambda item: item['@transactionDateTime'])
        self.sig_match.emit(matchlist)


    def data_match(self, matchlist):
        """append matched data to the listmodel"""
        # split into buy/sell
        sells, buys = [], []

        for item in matchlist:
            dt = item['@transactionDateTime']
            pretty_price = self.pretty_float(item['@price'])
            name = item['@typeName']
            price = item['@price']
            quant = item['@quantity']
            _type = item['@transactionType']

            ## make pretty rows
            #formatted = "%s %s %s %s %s" % (pretty_price, _type, quant, name, dt)
            #if _type == 'buy':
            #    qitem = QtGui.QStandardItem(self.ICON_BUY, formatted)
            #else:
            #    qitem = QtGui.QStandardItem(self.ICON_SELL, formatted)
            #self.listmodel.appendRow(qitem)

            if _type == 'sell':
                sells.append(item)
            elif _type == 'buy':
                buys.append(item)
            else:
                print "--------------"
                print dt, pretty_price, name, price, quant, _type
                print "--------------"

        if len(sells) or len(buys):
            # set item text to match pulled item when comparing to a market order
            self.label_item.setText(item['@typeName'])

            # scroll to bottom
            #self.listView.scrollTo(qitem.index())

        # transaction type determines arrow direction goodness/badness
        t = self.d.get('type', 'BUY')

        if len(sells):
            sells.sort(key=lambda item: float(item['@price']))
            sell_low = float(sells[0]['@price'])
            sell_high = float(sells[-1]['@price'])
            self.label_m_sell_low.setText(self.pretty_float(sell_low))
            self.label_m_sell_high.setText(self.pretty_float(sell_high))

            # calculate percentages
            percent = (self.curr_value / sell_low) * 100 - 100
            self.label_m_sell_low_percent.setText( '%.2f %%' % percent )
            if percent > 0:
                if t == 'BUY':
                    self.label_m_sell_low_icon.setPixmap(self.PIXMAP_ARROW_UP_BAD)
                else:
                    self.label_m_sell_low_icon.setPixmap(self.PIXMAP_ARROW_UP_GOOD)
            elif percent < 0:
                if t == 'BUY':
                    self.label_m_sell_low_icon.setPixmap(self.PIXMAP_ARROW_DOWN_GOOD)
                else:
                    self.label_m_sell_low_icon.setPixmap(self.PIXMAP_ARROW_DOWN_BAD)
            else:
                self.label_m_sell_low_icon.clear()

            percent = (self.curr_value / sell_high) * 100 - 100
            self.label_m_sell_high_percent.setText( '%.2f %%' % percent )
            if percent > 0:
                if t == 'BUY':
                    self.label_m_sell_high_icon.setPixmap(self.PIXMAP_ARROW_UP_BAD)
                else:
                    self.label_m_sell_high_icon.setPixmap(self.PIXMAP_ARROW_UP_GOOD)
            elif percent < 0:
                if t == 'BUY':
                    self.label_m_sell_high_icon.setPixmap(self.PIXMAP_ARROW_DOWN_GOOD)
                else:
                    self.label_m_sell_high_icon.setPixmap(self.PIXMAP_ARROW_DOWN_BAD)
            else:
                self.label_m_sell_high_icon.clear()

        else:
            self.label_m_sell_low.setText('---')
            self.label_m_sell_high.setText('---')
            self.label_m_sell_low_percent.setText('%')
            self.label_m_sell_high_percent.setText('%')

        if len(buys):
            buys.sort(key=lambda item: float(item['@price']))
            buy_low = float(buys[0]['@price'])
            buy_high = float(buys[-1]['@price'])
            self.label_m_buy_low.setText(self.pretty_float(buy_low))
            self.label_m_buy_high.setText(self.pretty_float(buy_high))
            
            # calculate percentages
            percent = (self.curr_value / buy_low) * 100 - 100
            self.label_m_buy_low_percent.setText( '%.2f %%' % percent )
            if percent > 0:
                if t == 'BUY':
                    self.label_m_buy_low_icon.setPixmap(self.PIXMAP_ARROW_UP_BAD)
                else:
                    self.label_m_buy_low_icon.setPixmap(self.PIXMAP_ARROW_UP_GOOD)
            elif percent < 0:
                if t == 'BUY':
                    self.label_m_buy_low_icon.setPixmap(self.PIXMAP_ARROW_DOWN_GOOD)
                else:
                    self.label_m_buy_low_icon.setPixmap(self.PIXMAP_ARROW_DOWN_BAD)
            else:
                self.label_m_buy_low_icon.clear()

            percent = (self.curr_value / buy_high) * 100 - 100
            self.label_m_buy_high_percent.setText( '%.2f %%' % percent )
            if percent > 0:
                if t == 'BUY':
                    self.label_m_buy_high_icon.setPixmap(self.PIXMAP_ARROW_UP_BAD)
                else:
                    self.label_m_buy_high_icon.setPixmap(self.PIXMAP_ARROW_UP_GOOD)
            elif percent < 0:
                if t == 'BUY':
                    self.label_m_buy_high_icon.setPixmap(self.PIXMAP_ARROW_DOWN_GOOD)
                else:
                    self.label_m_buy_high_icon.setPixmap(self.PIXMAP_ARROW_DOWN_BAD)
            else:
                self.label_m_buy_high_icon.clear()

        else:
            self.label_m_buy_low.setText('---')
            self.label_m_buy_high.setText('---')
            self.label_m_buy_low_percent.setText('%')
            self.label_m_buy_high_percent.setText('%')


    def load_key(self):
        try:
            with open(self.API_KEY_PATH, 'r') as f:
                self.api_char = []
                self.api_id = f.readline().strip()
                self.api_key = f.readline().strip()

                name = f.readline().strip()
                self.api_char.append(name)
                while len(name):
                    name = f.readline().strip()
                    self.api_char.append(name)
                self.api_char.pop()
                    
                self.lineEdit_api_id.setText(self.api_id)
                self.lineEdit_api_key.setText(self.api_key)

                for name in self.api_char:
                    self.comboBox_char.addItem(name)
                self.comboBox_char.setCurrentIndex(0)

                self.comboBox_char.setEnabled(True)
                self.label_api_char.setEnabled(True)
    
                # load success
                return True
            
        except Exception as e:
            print 'Failed to load api key, error: %s' % e

        # failed to load for any reason
        return False


    def save_key(self):
        """return true if save succeeded, false if save failed"""
        with open(self.API_KEY_PATH, 'w') as f:
            f.write(self.api_id)
            f.write('\n')
            f.write(self.api_key)
            f.write('\n')
            for name in self.api_char:
                f.write(name)
                f.write('\n')
            return True
        return False


    def cb_modified_api_id(self):
        if len(self.lineEdit_api_id.text()):
            self.sig_api_id.emit(self.lineEdit_api_id.text())

            if len(self.lineEdit_api_key.text()):
                self.pushButton_api_fetch.setEnabled(True)
        else:
            self.pushButton_api_fetch.setEnabled(True)
            self.pushButton_api_save.setDisabled(True)


    def cb_modified_api_key(self):
        if len(self.lineEdit_api_key.text()):
            self.sig_api_key.emit(self.lineEdit_api_key.text())

            if len(self.lineEdit_api_id.text()):
                self.pushButton_api_fetch.setEnabled(True)
                self.pushButton_api_save.setDisabled(True)
        else:
            self.pushButton_api_fetch.setEnabled(True)
            self.pushButton_api_save.setDisabled(True)


    def cb_sig_api_id(self, val):
        self.api_id = val


    def cb_sig_api_key(self, val):
        self.api_key = val


    def chop_chars(self, xml):
        """return list of chars and list of charids"""
        charlist, charidlist = [], []
        startchar = 'row name="'
        for row in xml.split('\n'):
            if row.find(startchar) > 0:
                chopped = re.sub('.*row name="', '', row)
                charlist.append( re.sub('".*[\n]*', '', chopped) )

                chopped = re.sub('.*characterID="', '', row)
                charidlist.append( re.sub('".*[\n]*', '', chopped) )

        return charlist, charidlist


    def cb_push_api_fetch(self):
        """use api key to fetch char list to populate pulldown"""
        _id = ('%s' % self.api_id).strip()
        _key = ('%s' % self.api_key).strip()
        self.url_get_chars = 'https://api.eveonline.com/account/characters.xml.aspx?keyID=%s&vCode=%s' % (_id, _key)

        if self.FOREALDOE:
            # PRODUCTION MODE
            response = urllib2.urlopen(self.url_get_chars)
            xml = response.read().strip()
        else:
            # DEBUGGING MODE
            with open('_characters.txt', 'r') as f:
                xml = ''
                for line in f.readlines():
                    xml += line

        # get names and characterids
        charlist, charidlist = self.chop_chars(xml)

        # empty current charlist
        while len(self.comboBox_char):
            self.comboBox_char.removeItem(0)

        # fill combobox
        self.comboBox_char.addItems(charlist)

        # default to the first char
        self.comboBox_char.setCurrentIndex(0)

        # enable/disable
        self.label_api_char.setEnabled(True)
        self.comboBox_char.setEnabled(True)
        self.pushButton_api_fetch.setDisabled(True)
        self.pushButton_api_save.setEnabled(True)


    def cb_push_api_save(self, *args):
        # this should not be possible, but just in case.
        if not len(self.api_id) or not len(self.api_key):
            return
        print "SAVING..."
        self.api_id = ('%s' % self.lineEdit_api_id.text()).strip()
        self.api_key = ('%s' % self.lineEdit_api_key.text()).strip()
        self.api_char = []
        self.api_char.append(('%s' % self.comboBox_char.currentText()).strip())

        # save the other characters too
        for i in range(0, len(self.comboBox_char)):
            name = self.comboBox_char.itemText(i)
            if name != self.api_char[0]:
                self.api_char.append(name)
                
        # save api key
        if self.save_key():
            # disable save, clear label
            self.pushButton_api_save.setDisabled(True)

        return


    def cb_tab_changed(self):
        # line edit takes default focus for calculator
        if self.tabWidget.currentIndex() == 1:
            self.lineEdit.setFocus(QtCore.Qt.OtherFocusReason)
        elif self.tabWidget.currentIndex() == 2:
            if len(self.blueprints) == 0:
                self.load_blueprints()

    def load_blueprints(self):
        try:
            # my blueprints

            # d['eveapi'].keys() -> [u'@version', u'currentTime', u'result', u'cachedUntil']
            # d['eveapi']['currentTime'] -> 2015-05-26 20:45:15
            #for row in d['eveapi']['result']['rowset']:
            #    @name
            #    @key
            #    @columns
            #    row
            # d['eveapi']['result']['rowset'].keys() -> [u'@name', u'@key', u'@columns', u'row']
            combolist = []
            
            if not self.api_charid:
                # get charid
                self.get_charid()

            if self.FOREALDOE:
                #PRODUCTION MODE
                url = 'https://api.eveonline.com/Char/Blueprints.xml.aspx?keyID=%s&vCode=%s&CharacterID=%s' % (self.api_id, self.api_key, self.api_charid)
                print url
                response = urllib2.urlopen(url)
                xml = response.read().strip()
                print "XML:", xml
            else:
                # DEBUGGING MODE
                print "DEBUG GET CHARACTER BLUEPRINTS"
                with open('_blueprints_char.txt', 'r') as f:
                    xml = ''
                    for line in f.readlines():
                        xml += line
            d = xmltodict.parse(xml)

            # insert blueprints
            for row in d['eveapi']['result']['rowset']['row']:
                combolist.append('%s  (ME%s TE%s)' % (row['@typeName'], row['@materialEfficiency'], row['@timeEfficiency']))
                self.blueprints[row['@typeID']] = row

            # corp blueprints
            if self.FOREALDOE:
                #PRODUCTION MODE
                url = 'https://api.eveonline.com/Corp/Blueprints.xml.aspx?keyID=%s&vCode=%s&CharacterID=%s' % (self.api_id, self.api_key, self.api_charid)
                response = urllib2.urlopen(url)
                xml = response.read().strip()
            else:
                # DEBUGGING MODE
                print "DEBUG GET CORP BLUEPRINTS"
                with open('_blueprints_corp.txt', 'r') as f:
                    xml = ''
                    for line in f.readlines():
                        xml += line
            d = xmltodict.parse(xml)

            # insert blueprints
            for row in d['eveapi']['result']['rowset']['row']:
                combolist.append('%s  (ME%s TE%s)' % (row['@typeName'], row['@materialEfficiency'], row['@timeEfficiency']))
                self.blueprints[row['@typeID']] = row

        except Exception as e:
            #print "Exception:", e
            pass

        # sort list
        combolist.sort(key=lambda item: item[0])

        # set combo
        self.combo_blueprint.clear()
        self.combo_blueprint.addItems(combolist)


    def get_files(self):
        qdir = QtCore.QDir(self.EXPORT_PATH)
        return qdir.entryList()
    
    
    def watcher_changed(self, *args):
        files = self.get_files()
        for f in files:
            if f not in self.qdir_existing:
                self.do_parse(f)

        # save current
        self.qdir_existing = files
        
        
    def do_parse(self, qstr):
        try:
            filepath = '%s/%s' % (self.EXPORT_PATH, str(qstr))
            print filepath
            
            # clear match labels
            self.reset_match_labels()

            with open(filepath) as f:
                reader = csv.reader(f)
                count = 0
                for row in reader:
                    if count == 0:
                        pass # header
                    else:
                        if count == 1:
                            top_sell = float(row[0])
                            last_price = float(row[0])
                        elif float(row[0]) < last_price:
                            top_buy = float(row[0])

                            try:
                                diff = top_sell - top_buy
                                percent = 100 - (top_buy / top_sell) * 100
                            except:
                                pass

                            # clear item label
                            try:
                                self.label_item.setText('EXPORT')
                            except:
                                pass

                            text_sell = self.pretty_float(top_sell)
                            print 'SELL', text_sell
                            self.label_export_sell.setText(text_sell)

                            text_buy = self.pretty_float(top_buy)
                            print 'BUY', text_buy
                            self.label_export_buy.setText(text_buy)

                            text_diff = self.pretty_float(diff)
                            print "DIFF", text_diff
                            self.label_export_diff.setText(text_diff)

                            if percent <= self.EXPORT_LOW:
                                self.label_export_percent.setStyleSheet("QLabel { color: %s; }" % self.COLOR_RED)
                            elif percent >= self.EXPORT_HIGH:
                                self.label_export_percent.setStyleSheet("QLabel { color: %s; }" % self.COLOR_GREEN)
                            else:
                                self.label_export_percent.setStyleSheet("QLabel { color: %s; }" % self.COLOR_YELLOW)

                            text_percent = '%.3f %%' % percent
                            print "PERCENT", text_percent
                            self.label_export_percent.setText(text_percent)

                            return #done
                    count += 1
                    print "count=%s" % count
                    
        except Exception as e:
            print "Error: %s" % e

        
    def checkBox_buy_cb(self):
        self.force_buy = self.checkBox_buy.isChecked()
        if self.force_buy and self.checkBox_sell.isChecked():
            self.checkBox_sell.setCheckState(QtCore.Qt.Unchecked)


    def checkBox_sell_cb(self):
        self.force_sell = self.checkBox_sell.isChecked()
        if self.force_sell and self.checkBox_buy.isChecked():
            self.checkBox_buy.setCheckState(QtCore.Qt.Unchecked)


    def cb_push_append(self, ch):
        print "<APPEND>", ch
        self.lineEdit.setText(self.lineEdit.text() + ch)


    def cb_push_000(self):
        if re.search('\.', self.lineEdit.text()):
            return
        self.lineEdit.setText(self.lineEdit.text() + '000')


    def cb_push_dot(self, raw):
        print "<DOT>", raw
        match = re.search('\.', self.lineEdit.text())
        if match is None:
            curr = self.lineEdit.text()
            if len(curr):
                self.lineEdit.setText(self.lineEdit.text() + raw)
            else:
                # empty, prepend zero
                self.lineEdit.setText('0' + raw)
        else:
            old = self.lineEdit.text()[:match.end()-1]
            self.lineEdit.setText(old + raw)


    def cb_push_math(self, symbol):
        if self.lineEdit.text() == '':
            return

        old = 0
        if self.calc_saved:
            old = self.calc_saved

        self.calc_saved = float(self.lineEdit.text())
        self.calc_symbol = symbol
        self.lineEdit.setText('')
        print "<MATH>", symbol, self.calc_saved, self.calc_symbol

        if old:
            # automatically add
            final = self.calc_saved + old
            self.lineEdit.setText('%.2f' % final)


    def cb_push_equal(self):
        print '<EQUAL>', self.calc_saved, self.calc_symbol, self.lineEdit.text()
        if self.calc_saved:
            # hold original
            curr = float(self.lineEdit.text())

            print 'CALC_SAVED', self.calc_saved
            if self.calc_symbol == '+':
                final = self.calc_saved + curr
                print self.calc_saved, '+', curr, '=', final
                self.lineEdit.setText('%.2f' % final)

            elif self.calc_symbol == '-':
                final = self.calc_saved - curr
                print self.calc_saved, '-', curr, '=', final
                self.lineEdit.setText('%.2f' % final)

            elif self.calc_symbol == 'x':
                final = self.calc_saved * curr
                print self.calc_saved, 'x', curr, '=', final
                self.lineEdit.setText('%.2f' % final)

            elif self.calc_symbol == '/':
                final = self.calc_saved / curr
                print self.calc_saved, '/', curr, '=', final
                self.lineEdit.setText('%.2f' % final)

            # save original
            self.calc_saved = curr

            # set clipboard contents
            QtGui.QApplication.clipboard().setText('%.2f' % final)


    def cb_push_clear(self):
        print "<CLEAR>"
        self.calc_saved = None
        self.lineEdit.setText('')


    def dataChanged_cb(self):
        # clipboard change detected
        index = self.tabWidget.currentIndex()
        if index == 0:
            # trade
            self.dataChanged_trade()

        elif index == 1:
            # calc
            self.dataChanged_calc()

        else:
            print "future tabs"

        # bring back from minimized
        self.setWindowState(self.windowState() & ~QtCore.Qt.WindowMinimized | QtCore.Qt.WindowActive)
        # activate the window
        self.activateWindow()

    def dataChanged_trade(self):
        data = str(QtGui.QApplication.clipboard().text()).split('\n')[0]

        print
        print "CB [%s]" % data

        # check for invalid data, normal length is under 100
        if len(str(data)) > 160: # picked up multiples
            self.sig_invalid.emit('***** Multi-order Clipboard Error *****', 'red')
            return

        # split into elements
        parts = re.split(self.regex_spacing, data)
        print "PARTS [%s]" % parts

        if len(parts) < 2:
            # self updated clipboard triggering, just ignore
            return

        if self.flag_manual_item:
            item = self.flag_manual_item # item was manually, save it
            self.flag_manual_item = False # clear it
        else:
            item = 'Unk'

        value = 'Unk'
        value_string = 'Unk'
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
                #print "VALUE_RAW [%s]" % quantity

                value_string = parts[index+1]
                #print "VALUE_STRING [%s]" % value_string

                chop = value_string.replace(',', '')
                value = float(chop)
                #print "VALUE [%s]" % value

                # mark as value received
                flag_value = True

            if not flag_value and p == 'ISK':
                # this is an existing order
                item = ' '.join(parts[0:index-1])
                print "ITEM [%s]" % item

                value_string = parts[index-1]
                #print "VALUE_STRING [%s]" % value_string

                chop = value_string.replace(',', '')
                value = float(chop)
                #print "VALUE [%s]" % value

                flag_order = True
                #print "=== ORDER ==="

            elif not flag_order and re.match(self.regex_jump, p):
                print "JUMPS: [%s]" % p
                print "RANGE [%s]" % parts[index-1]
                if re.match(self.regex_integer, parts[index-1]):
                    # this is my buy order
                    flag_my_buy = True
                    #print "=== MY_BUY_ORDER ==="
                    break

        if not flag_order and not flag_my_buy:
            # must be my sell order
            flag_my_sell = True
            #print "=== MY_SELL_ORDER ==="

        ########################################################
        # after processing clipboard

        # clear export results
        self.label_export_sell.setText('')
        self.label_export_buy.setText('')
        self.label_export_diff.setText('')
        self.label_export_percent.setText('')
        
        # use checkbox overrides
        if self.force_buy and not flag_order:
            flag_my_sell = False
            flag_my_buy = True
        elif self.force_sell and not flag_order:
            flag_my_buy = False
            flag_my_sell = True

        # build data structure
        self.d['item'] = item
        self.d['value'] = value
        self.d['value_string'] = value_string

        # hold current value globally for api comparisons
        self.curr_value = value
 
        if flag_my_buy:
            try:
                self.label_item.setText(item[:55])
            except:
                pass
            self.d['type'] = 'BUY'
            self.sig_valid.emit()

        elif flag_my_sell:
            try:
                self.label_item.setText(item[:55])
            except:
                pass
            self.d['type'] = 'SELL'
            self.sig_valid.emit()

        if flag_order:
            # calculate change needed
            percent_raw = (value - self.last_value) / self.last_value * 100.0
            percent = '%.3f' % percent_raw
            print 'PERCENT [%s]' % percent

            if len(str(data)) > 160: # picked up multiples
                self.sig_invalid.emit('***** Multi-order Clipboard Error *****', 'red')
                return

            if self.last_value == value:
                # this order is my own order
                print "=== THIS IS MY OWN ORDER ==="
                self.sig_pass.emit()

            elif self.last == 'BUY':
                # this is a buy comparison
                newvalue = value + 0.01
                print "BUY NEWVALUE [%s]" % newvalue

                self.d['last'] = 'BUY'
                self.d['raw'] = data
                self.d['item'] = self.last_item
                self.d['percent'] = percent
                self.d['newvalue'] = newvalue
                self.d['type'] = self.last

                if percent_raw <= self.TRADE_LOW:
                    self.d['pixbuf'] = 'green'
                elif percent_raw <= self.TRADE_HIGH:
                    self.d['pixbuf'] = 'yellow'
                else:
                    self.d['pixbuf'] = 'red'

                # set clipboard contents
                QtGui.QApplication.clipboard().setText(str(newvalue))
                # emit data
                self.sig_adjust.emit()

            elif self.last == 'SELL':
                # this is a sell comparison
                newvalue = value - 0.01
                print "SELL NEWVALUE [%s]" % newvalue

                # emit data
                self.d['last'] = 'SELL'
                self.d['raw'] = data
                self.d['item'] = self.last_item
                self.d['percent'] = percent
                self.d['newvalue'] = newvalue
                self.d['type'] = self.last

                if abs(percent_raw) <= self.TRADE_LOW:
                    self.d['pixbuf'] = 'green'
                elif abs(percent_raw) <= self.TRADE_HIGH:
                    self.d['pixbuf'] = 'yellow'
                else:
                    self.d['pixbuf'] = 'red'

                # set clipboard contents
                QtGui.QApplication.clipboard().setText(str(newvalue))
                # emit data
                self.sig_adjust.emit()

            # update item text
            self.label_item.setText(self.d['item'])

        elif flag_my_buy:
            self.last = 'BUY'
            self.last_item = item

        elif flag_my_sell:
            self.last = 'SELL'
            self.last_item = item

        else:
            # error
            self.last = 'X'

        self.sig_fetch.emit()

        # save current value as last
        self.last_value = value


    def dataChanged_calc(self):
        data = str(QtGui.QApplication.clipboard().text())

        print
        print
        print "CLIPBOARD [%s]" % data

        # split into elements
        parts = re.split(self.regex_spacing, data)
        print "PARTS [%s]" % parts

        if len(parts) < 2:
            # self updated clipboard triggering, just ignore
            return

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

                # set clipboard contents
                QtGui.QApplication.clipboard().setText('%.2f' % value)
                self.lineEdit.setText('%.2f' % value)
                return

            if p == 'ISK':
                # previous part was the value
                item = ' '.join(parts[0:index-1])
                print "ITEM [%s]" % item

                value_string = parts[index-1]
                print "VALUE_STRING [%s]" % value_string

                chop = value_string.replace(',', '')
                value = float(chop)
                print "VALUE [%s]" % value

                # set clipboard contents
                QtGui.QApplication.clipboard().setText('%.2f' % value)
                self.lineEdit.setText('%.2f' % value)
                return

    @classmethod
    def pretty_float(self, val):
        # commas for make benefit glorious readability
        try:
            temp = "%.2f" % float(val)

            count = 20
            while count:
                count -= 1
                temp, count = re.subn(self.regex_pretty_float, r'\1,\2', temp)
                if not count:
                    break
            return temp
        except Exception as e:
            print e
            return val
            

    def data_valid(self):
        # buy/sell type determined
        self.label_type.setText(self.d['type'])
        self.label_value.setText(self.d['value_string'])
        self.label_percent.setText('')

        if self.d['type'] == 'SELL':
            self.label_type.setStyleSheet("QLabel { color: orange; }")
            self.label_item.setStyleSheet("QLabel { color: orange; }")
        elif self.d['type'] == 'BUY':
            self.label_type.setStyleSheet("QLabel { color: purple; }")
            self.label_item.setStyleSheet("QLabel { color: purple; }")
        else:
            self.label_type.setStyleSheet("QLabel { color: pink; }")
            
        pixmap = QtGui.QPixmap(self.IMG_BLACK)
        pixmap = pixmap.scaled(self.PIXMAP_SIZE, self.PIXMAP_SIZE, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
        self.label_pixmap.setPixmap(pixmap)


    def data_invalid(self, text, color):
        # could not parse data
        self.label_item.setText(text)
        self.label_item.setStyleSheet("QLabel { color: %s; }" % color)

        pixmap = QtGui.QPixmap(self.IMG_BLACK)
        pixmap = pixmap.scaled(self.PIXMAP_SIZE, self.PIXMAP_SIZE, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
        self.label_pixmap.setPixmap(pixmap)


    def data_pass(self):
        # no change needed
        self.label_type.setText('MINE')
        self.label_value.setText('---')
        self.label_percent.setText('')

        pixmap = QtGui.QPixmap(self.IMG_WHITE)
        pixmap = pixmap.scaled(self.PIXMAP_SIZE, self.PIXMAP_SIZE, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
        self.label_pixmap.setPixmap(pixmap)


    def data_adjust(self):
        print 'data_adjust', self.d

        # type
        if self.d['type'] == 'BUY':
            self.label_type.setText('BUY')
        elif self.d['type'] == 'SELL':
            self.label_type.setText('SELL')
        else:
            self.label_type.setText('---')

        # newvalue
        newvalue = self.pretty_float(self.d['newvalue'])
        self.label_value.setText(newvalue)

        # percent
        self.label_percent.setText(str(self.d['percent'])+'%')

        # pixmap determines color too
        if self.d['pixbuf'] == 'green':
            pixmap = QtGui.QPixmap(self.IMG_GREEN)
            self.label_percent.setStyleSheet("QLabel { color: green; }")
            
        elif self.d['pixbuf'] == 'yellow':
            pixmap = QtGui.QPixmap(self.IMG_YELLOW)
            self.label_percent.setStyleSheet("QLabel { color: yellow; }")
        elif self.d['pixbuf'] == 'red':
            pixmap = QtGui.QPixmap(self.IMG_RED)
            self.label_percent.setStyleSheet("QLabel { color: red; }")
        else:
            pixmap = QtGui.QPixmap(self.IMG_BLACK)
            self.label_percent.setStyleSheet("QLabel { color: grey; }")

        pixmap = pixmap.scaled(self.PIXMAP_SIZE, self.PIXMAP_SIZE, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
        self.label_pixmap.setPixmap(pixmap)


if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    obj = Trader()
    sys.exit(app.exec_())

