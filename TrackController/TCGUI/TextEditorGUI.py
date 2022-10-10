import os
import sys
from PyQt5.QtWidgets import QMainWindow, QLayout, QPlainTextEdit, QWidget
from PyQt5.QtWidgets import QStatusBar, QToolBar, QAction
from PyQt5.QtGui import QFont

class TextEditorGUI(QMainWindow):

    def __init__(self, loadedFile, reenable_PLC):
        super().__init__()

        self.setGeometry(80, 480, 500, 400)

        self.editor = QPlainTextEdit()
        self.editor.setFont(QFont('Times', 12))


    #default closeEvent behavior is overwritten to reenable PLC logic on exit
    #this might work maybe
    def closeEvent(self, event):
        self.reenable_PLC()

        event.accept()