from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTime, Qt, QEvent, QTimer
from PyQt5.QtGui import QStandardItem
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import *
from PyQt5 import *
from CTC.Block_Table import Block_Table

#MAINTENANCE_SCREEN
class maintenance_screen(QWidget):
    def __init__(self):
        super(maintenance_screen,self).__init__()
        self.setupUi()
        self.show()
    def setupUi(self):
        self.main_button = QtWidgets.QPushButton(self)
        self.main_button.setGeometry(QtCore.QRect(1260, 560, 161, 221))
        self.main_button.setObjectName("main_button")
        self.maintenance_button = QtWidgets.QPushButton(self)
        self.maintenance_button.setGeometry(QtCore.QRect(390, 40, 491, 91))
        self.maintenance_button.setObjectName("maintenance_button")
        self.textEdit = QtWidgets.QTextEdit(self)
        self.textEdit.setGeometry(QtCore.QRect(390, 130, 491, 331))
        self.textEdit.setObjectName("textEdit")
        self.line_selection = QtWidgets.QComboBox(self)
        self.line_selection.setGeometry(QtCore.QRect(460, 200, 141, 26))
        self.line_selection.setObjectName("line_selection")
        self.status_selection = QtWidgets.QComboBox(self)
        self.status_selection.setGeometry(QtCore.QRect(550, 140, 141, 26))
        self.status_selection.setObjectName("status_selection")
        self.section_selection = QtWidgets.QComboBox(self)
        self.section_selection.setGeometry(QtCore.QRect(500, 260, 141, 26))
        self.section_selection.setObjectName("section_selection")
        self.block_selection = QtWidgets.QSpinBox(self)
        self.block_selection.setGeometry(QtCore.QRect(570, 310, 48, 31))
        self.block_selection.setObjectName("block_selection")
        self.maintenance_output = QtWidgets.QLineEdit(self)
        self.maintenance_output.setGeometry(QtCore.QRect(610, 370, 113, 21))
        self.maintenance_output.setObjectName("maintenance_output")

        self.block_table = Block_Table()

        self.retranslateUi(self)
        #QtCore.QMetaObject.connectSlotsByName()
        self.maintenance()
        self.maintenance_button.clicked.connect(lambda:self.pressed())
        self.main_button.clicked.connect(lambda:self.closescr())
    
    def closescr(self):
        self.hide()
        
    def maintenance(self):
        self.status_selection.addItems(["Open","Close"])
        self.line_selection.addItems(["Red","Green"])
        self.section_selection.addItems(["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"])
    """"
    def set_signal(self,Form):
        if self.status_selection.currentText() == "Open":
            self.maintenance_output.setText("False")
            maintenance_track = Track(id_n=self.block_selection.value(),sec=self.section_selection.currentText(),main_signal="False")
        else:
            self.maintenance_output.setText("True")
            maintenance_track = Track(id_n=self.block_selection.value(),sec=self.section_selection.currentText(),main_signal="True")
    """
    def pressed(self):
        if self.status_selection.currentText() == "Open":
            self.maintenance_output.setText("False")
        else:
            self.maintenance_output.setText("True")
        self.block_table.set_maintenance(self.block_selection.value(),self.section_selection.currentText(),self.line_selection.currentText())
    
    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.main_button.setText(_translate("Form", "Back to Main Window"))
        self.maintenance_button.setText(_translate("Form", "Maintenance"))
        self.textEdit.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'.SF NS Text\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:24pt;\">- Track Status: </span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:24pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:24pt;\">- Line:</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:24pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:24pt;\">- Section:</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:24pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:24pt;\">-Block Number:</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:24pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:24pt;\">Maintenance Signal: </span></p></body></html>"))

