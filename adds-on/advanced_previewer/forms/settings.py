# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer/settings.ui'
#
# Created: Sat Aug  5 16:04:10 2017
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(450, 382)
        Dialog.setMaximumSize(QtCore.QSize(450, 429))
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(10, 345, 431, 31))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok|QtGui.QDialogButtonBox.RestoreDefaults)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.tabWidget = QtGui.QTabWidget(Dialog)
        self.tabWidget.setGeometry(QtCore.QRect(10, 10, 431, 321))
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.gridLayoutWidget_4 = QtGui.QWidget(self.tab)
        self.gridLayoutWidget_4.setGeometry(QtCore.QRect(10, 15, 404, 51))
        self.gridLayoutWidget_4.setObjectName(_fromUtf8("gridLayoutWidget_4"))
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget_4)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_5 = QtGui.QLabel(self.gridLayoutWidget_4)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 0, 0, 1, 1)
        self.cb_dpl_qa = QtGui.QCheckBox(self.gridLayoutWidget_4)
        self.cb_dpl_qa.setObjectName(_fromUtf8("cb_dpl_qa"))
        self.gridLayout.addWidget(self.cb_dpl_qa, 1, 0, 1, 1)
        self.gridLayoutWidget_5 = QtGui.QWidget(self.tab)
        self.gridLayoutWidget_5.setGeometry(QtCore.QRect(10, 75, 404, 141))
        self.gridLayoutWidget_5.setObjectName(_fromUtf8("gridLayoutWidget_5"))
        self.gridLayout_2 = QtGui.QGridLayout(self.gridLayoutWidget_5)
        self.gridLayout_2.setMargin(0)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.label_6 = QtGui.QLabel(self.gridLayoutWidget_5)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout_2.addWidget(self.label_6, 0, 0, 1, 1)
        self.cb_rev_main = QtGui.QCheckBox(self.gridLayoutWidget_5)
        self.cb_rev_main.setObjectName(_fromUtf8("cb_rev_main"))
        self.gridLayout_2.addWidget(self.cb_rev_main, 1, 0, 1, 1)
        self.cb_rev_ahd = QtGui.QCheckBox(self.gridLayoutWidget_5)
        self.cb_rev_ahd.setObjectName(_fromUtf8("cb_rev_ahd"))
        self.gridLayout_2.addWidget(self.cb_rev_ahd, 2, 0, 1, 1)
        self.cb_rev_nxt = QtGui.QCheckBox(self.gridLayoutWidget_5)
        self.cb_rev_nxt.setObjectName(_fromUtf8("cb_rev_nxt"))
        self.gridLayout_2.addWidget(self.cb_rev_nxt, 3, 0, 1, 1)
        self.cb_rev_ans = QtGui.QCheckBox(self.gridLayoutWidget_5)
        self.cb_rev_ans.setObjectName(_fromUtf8("cb_rev_ans"))
        self.gridLayout_2.addWidget(self.cb_rev_ans, 4, 0, 1, 1)
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.textBrowser = QtGui.QTextBrowser(self.tab_2)
        self.textBrowser.setGeometry(QtCore.QRect(-2, -2, 431, 351))
        self.textBrowser.setObjectName(_fromUtf8("textBrowser"))
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.tabWidget, self.cb_dpl_qa)
        Dialog.setTabOrder(self.cb_dpl_qa, self.cb_rev_main)
        Dialog.setTabOrder(self.cb_rev_main, self.cb_rev_ahd)
        Dialog.setTabOrder(self.cb_rev_ahd, self.buttonBox)
        Dialog.setTabOrder(self.buttonBox, self.textBrowser)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Advanced Previewer Options", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("Dialog", "<html><head/><body><p><span style=\" font-weight:600;\">Display Options</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.cb_dpl_qa.setToolTip(QtGui.QApplication.translate("Dialog", "Automatically reveals the answer when previewing cards", None, QtGui.QApplication.UnicodeUTF8))
        self.cb_dpl_qa.setText(QtGui.QApplication.translate("Dialog", "Show both question and answer by default", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("Dialog", "<html><head/><body><p><span style=\" font-weight:600;\">Reviewing Cards</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.cb_rev_main.setToolTip(QtGui.QApplication.translate("Dialog", "Adds answer buttons to the bottom left corner of the previewer", None, QtGui.QApplication.UnicodeUTF8))
        self.cb_rev_main.setText(QtGui.QApplication.translate("Dialog", "Allow studying cards from the preview window", None, QtGui.QApplication.UnicodeUTF8))
        self.cb_rev_ahd.setToolTip(QtGui.QApplication.translate("Dialog", "Allows you to review cards that aren\'t due, yet", None, QtGui.QApplication.UnicodeUTF8))
        self.cb_rev_ahd.setText(QtGui.QApplication.translate("Dialog", "Allow reviewing cards ahead of schedule", None, QtGui.QApplication.UnicodeUTF8))
        self.cb_rev_nxt.setToolTip(QtGui.QApplication.translate("Dialog", "Jump to the next card in line after rating a card", None, QtGui.QApplication.UnicodeUTF8))
        self.cb_rev_nxt.setText(QtGui.QApplication.translate("Dialog", "Automatically switch to the next card after rating", None, QtGui.QApplication.UnicodeUTF8))
        self.cb_rev_ans.setToolTip(QtGui.QApplication.translate("Dialog", "If active, the answer buttons will only be shown<br>after the answer is revealed", None, QtGui.QApplication.UnicodeUTF8))
        self.cb_rev_ans.setText(QtGui.QApplication.translate("Dialog", "Only show rating buttons when the answer is visible", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtGui.QApplication.translate("Dialog", "General", None, QtGui.QApplication.UnicodeUTF8))
        self.textBrowser.setHtml(QtGui.QApplication.translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:12px; margin-left:10px; margin-right:10px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Credits and License</span> </p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:10px; margin-right:10px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-style:italic;\">Advanced Previewer</span> is copyright © 2016-2017 <a href=\"https://github.com/Glutanimate\"><span style=\" text-decoration: underline; color:#0000ff;\">Aristotelis P.</span></a> </p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:10px; margin-right:10px; -qt-block-indent:0; text-indent:0px;\">Licensed under the GNU AGPLv3. </p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:10px; margin-right:10px; -qt-block-indent:0; text-indent:0px;\">This add-on was developed on a commission. If you\'d like to hire my services to work an add-on or new feature, feel free to reach out to me on <a href=\"https://twitter.com/glutanimate\"><span style=\" text-decoration: underline; color:#0000ff;\">Twitter</span></a> or at ankiglutanimate [αt] gmail . com.</p>\n"
"<p style=\" margin-top:14px; margin-bottom:12px; margin-left:10px; margin-right:10px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">More Information</span> </p>\n"
"<ul style=\"margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 0;\"><li style=\" margin-top:12px; margin-bottom:10px; margin-left:35px; margin-right:10px; -qt-block-indent:0; text-indent:0px;\"><a href=\"https://github.com/Glutanimate/advanced-previewer\"><span style=\" text-decoration: underline; color:#0000ff;\">Project page on GitHub</span></a></li>\n"
"<li style=\" margin-top:12px; margin-bottom:10px; margin-left:35px; margin-right:10px; -qt-block-indent:0; text-indent:0px;\"><a href=\"https://ankiweb.net/shared/info/544521385\"><span style=\" text-decoration: underline; color:#0000ff;\">Add-on description on AnkiWeb</span></a></li></ul></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QtGui.QApplication.translate("Dialog", "Help and Info", None, QtGui.QApplication.UnicodeUTF8))

