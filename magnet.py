#!/usr/bin/python3

# -*- coding: utf-8 -*-
import yaml
import sys
from os import environ
import importlib.util
from importlib.machinery import SourceFileLoader
import configparser
import subprocess
import shlex
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


def main():
    class Ui_Dialog(object):

        def load_static_inventory(self, i):
            self.aliases = self.yaml_obj['aliases']
            for k, v in self.yaml_obj['hosts'].items():
                i.append({'host': k, 'words': ' '.join(v)})

        def action_match_nodes(self):
            result = self.i.match_nodes(self.aliases.get(self.lineEdit.text())
                                        if self.aliases.get(self.lineEdit.text())
                                        else self.lineEdit.text())
            self.tableWidget.clear()
            self.tableWidget.setRowCount(len(result))
            self.tableWidget.setHorizontalHeaderLabels(["Hosts"])
            for index, iitem in enumerate(result):
                self.tableWidget.setItem(index, 0, QtGui.QTableWidgetItem(iitem['host']))

        def ok_action(self):
            ready_list = []
            for ssh in range(self.tableWidget.rowCount()):
                ready_list.append(self.tableWidget.item(ssh, 0).text())
            subprocess.Popen(shlex.split('%s %s' % (config['DEFAULT']['cmd'], ' '.join(ready_list))))
            Dialog.accept()

        def load_hosts(self):
            self.loading = QtGui.QLabel(Dialog)
            font = QtGui.QFont()
            font.setBold(True)
            font.setWeight(100)
            self.label.setFont(font)
            ui.i = plugin_sd.Inventory()
            self.load_static_inventory(self.i.nodes_list)
            self.tableWidget.setRowCount(len(self.i.nodes_list))
            for index, iitem in enumerate(self.i.nodes_list):
                self.tableWidget.setItem(index, 0, QtGui.QTableWidgetItem(iitem['host']))
            self.timer.stop()

        def setupUi(self, Dialog):
            self.timer = QtCore.QTimer(Dialog)
            QtCore.QObject.connect(self.timer, QtCore.SIGNAL("timeout()"), self.load_hosts)
            self.timer.start(500)
            Dialog.setObjectName(_fromUtf8("Dialog"))
            Dialog.setEnabled(True)
            Dialog.resize(580, 474)
            sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
            Dialog.setSizePolicy(sizePolicy)
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(_fromUtf8("%s/.magnet/Magnet-icon.png" % str(environ['HOME']))), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            Dialog.setWindowIcon(icon)
            Dialog.setToolTip(_fromUtf8(""))
            Dialog.setStatusTip(_fromUtf8(""))
            Dialog.setWhatsThis(_fromUtf8(""))
            Dialog.setAccessibleName(_fromUtf8(""))
            Dialog.setAutoFillBackground(False)
            font = QtGui.QFont()
            font.setBold(True)
            font.setWeight(75)
            self.gridLayout = QtGui.QGridLayout(Dialog)
            self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
            self.horizontalLayout = QtGui.QHBoxLayout()
            self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
            self.label = QtGui.QLabel(Dialog)
            self.label.setFont(font)
            self.label.setObjectName(_fromUtf8("label"))
            self.horizontalLayout.addWidget(self.label)
            self.lineEdit = QtGui.QLineEdit(Dialog)
            self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
            self.horizontalLayout.addWidget(self.lineEdit)
            self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
            self.verticalLayout = QtGui.QVBoxLayout()
            self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
            self.tableWidget = QtGui.QTableWidget(Dialog)
            self.tableWidget.setColumnCount(1)
            self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
            self.tableWidget.setRowCount(1)
            self.tableWidget.setHorizontalHeaderLabels(["Hosts"])
            self.tableWidget.horizontalHeader().setResizeMode(0, QtGui.QHeaderView.Stretch)
            self.tableWidget.selectRow(0)
            self.tableWidget.setItem(0, 0, QtGui.QTableWidgetItem("LOADING ....."))
            self.verticalLayout.addWidget(self.tableWidget)
            self.line = QtGui.QFrame(Dialog)
            self.line.setFrameShape(QtGui.QFrame.HLine)
            self.line.setFrameShadow(QtGui.QFrame.Sunken)
            self.line.setObjectName(_fromUtf8("line"))
            self.verticalLayout.addWidget(self.line)
            self.label_3 = QtGui.QLabel(Dialog)
            self.label_3.setFont(font)
            self.label_3.setObjectName(_fromUtf8("label_3"))
            self.verticalLayout.addWidget(self.label_3)
            self.line_2 = QtGui.QFrame(Dialog)
            self.line_2.setFrameShape(QtGui.QFrame.HLine)
            self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
            self.line_2.setObjectName(_fromUtf8("line_2"))
            self.verticalLayout.addWidget(self.line_2)
            self.buttonBox = QtGui.QDialogButtonBox(Dialog)
            self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
            self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel | QtGui.QDialogButtonBox.Ok)
            self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
            self.verticalLayout.addWidget(self.buttonBox)
            self.gridLayout.addLayout(self.verticalLayout, 1, 0, 1, 1)
            self.retranslateUi(Dialog)
            QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), self.ok_action)
            QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
            QtCore.QObject.connect(self.lineEdit, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")),
                                   self.action_match_nodes)
            QtCore.QMetaObject.connectSlotsByName(Dialog)

        def retranslateUi(self, Dialog):
            Dialog.setWindowTitle(_translate("Dialog", "Magnet", None))
            self.label.setText(_translate("Dialog", "Keywords", None))
            self.label_3.setText(_translate("Dialog", "Plugin: %s" % config['DEFAULT']['plugin'], None))

    plugin_sd = None
    config = configparser.ConfigParser()
    consumed_files = config.read('%s/.magnet/magnet.conf' % str(environ['HOME']))
    if consumed_files:
        try:
            absolute_plugin_path = '%s/.magnet/plugins/%s/%s.py' % (environ['HOME'],
                                                                config['DEFAULT']['plugin'],
                                                                config['DEFAULT']['plugin'])
            plugin_sd = SourceFileLoader(config['DEFAULT']['plugin'], absolute_plugin_path).load_module()
        except (ImportError, FileNotFoundError) as err:
            print("Plugin is missing.\nERROR: %s" % err)
            sys.exit(1)
        if plugin_sd:
            try:
                yobj = yaml.load(open('%s/.magnet/static_inventory.yaml' % str(environ['HOME'])))
                app = QtGui.QApplication(sys.argv)
                Dialog = QtGui.QDialog()
                ui = Ui_Dialog()
                ui.yaml_obj = yobj
                ui.setupUi(Dialog)
                Dialog.show()
                sys.exit(app.exec_())
            except plugin_sd.PluginConfigNotFound as pcm:
                print('ERROR: %s' % pcm.args)
                sys.exit(app.exec_())
            except yaml.YAMLError or yaml.scanner.ScannerError:
                print("ERROR: sytax error in %s/.magnet/static_inventory.yaml" % str(environ['HOME']))
                sys.exit(1)
        else:
            print('No such plugin.')
    else:
        print('ERROR: main config magnet.conf file is missing.')


if __name__ == "__main__":
    main()