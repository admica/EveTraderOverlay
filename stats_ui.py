#!/usr/bin/python -OOtt
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'stats.ui'
#
# Created: Thu May 21 17:05:39 2015
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Stats(QtGui.QWidget):
    def setupUi(self, Stats):
        Stats.setObjectName(_fromUtf8("Stats"))
        Stats.resize(811, 751)
        self.table = QtGui.QTableWidget(Stats)
        self.table.setGeometry(QtCore.QRect(10, 10, 791, 731))
        self.table.setObjectName(_fromUtf8("table"))
        self.table.setColumnCount(0)
        self.table.setRowCount(0)

        self.retranslateUi(Stats)
        QtCore.QMetaObject.connectSlotsByName(Stats)

    def retranslateUi(self, Stats):
        Stats.setWindowTitle(_translate("Stats", "Form", None))

if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    win = Ui_Stats()
    win.setupUi(win)
    win.retranslateUi(win)
    win.show()
    sys.exit(app.exec_())

