import os
import sys
from PyQt5.QtWidgets import QMainWindow, QPlainTextEdit, QWidget
from PyQt5.QtWidgets import QAction, QVBoxLayout
from PyQt5.QtGui import QFont

class TextEditorGUI(QMainWindow):

    def __init__(self, loaded_File, reenable_PLC, extract_Name):
        super().__init__()

        #creates a reenable_PLC function in the TextEditorGUI
        #so it can be used in the close function
        self.reenable_PLC = reenable_PLC
        self.extract_Name = extract_Name

        self.setGeometry(80, 560, 500, 400)

        #creates a text field editor and sets its font
        self.editor = QPlainTextEdit()
        self.editor.setFont(QFont('Times', 11))

        #matches the filepath in TextEditor to the filepath in the main TrackController
        self.path = loaded_File

        #creates and adds the layout and central widgets
        editor_Layout = QVBoxLayout()
        main_Widget = QWidget()

        editor_Layout.addWidget(self.editor)
        main_Widget.setLayout(editor_Layout)
        self.setCentralWidget(main_Widget)

        #creates file menu and adds save button
        file_Menu = self.menuBar().addMenu("&File")

        save_Option = QAction("Save", self)
        save_Option.triggered.connect(self.save_File)
        file_Menu.addAction(save_Option)

        #opens the file as the last step after GUI elements are setup
        self.open_File()


    #sets filepath
    def set_Filepath(self, fp):
        self.path = fp

    #opens the file
    def open_File(self):
        program_File = open(self.path, "r")
        text = program_File.read()
        program_File.close()

        self.editor.setPlainText(text)

        self.setWindowTitle("Editing " + self.extract_Name(self.path))

    #saves the file
    def save_File(self):
        text = self.editor.toPlainText()

        program_File = open(self.path, 'w')
        program_File.write(text)
        program_File.close()

    #default closeEvent behavior is overwritten to reenable PLC logic on exit
    def closeEvent(self, event):
        self.reenable_PLC()

        self.hide()