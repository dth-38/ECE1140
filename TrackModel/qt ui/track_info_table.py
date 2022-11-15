import sys
from PyQt5.QtWidgets import QApplication, QWidget, QTabWidget, QTableWidget, QTableWidgetItem, QPushButton, QHeaderView, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt
from track_info import *

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.window_width, self.window_height = 700, 500
        self.resize(self.window_width, self.window_height)
        self.setWindowTitle('Load Excel (or CSV) data to QTableWidget')

        self.info_tabs = QTabWidget()
        self.layout = QVBoxLayout()

    def add_table_tabs(self, sheets):
        # Initialize tab screen
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.info_tabs.resize(300,200)
        
        # Add tabs
        self.info_tabs.addTab(self.tab1, sheets[0])
        self.info_tabs.addTab(self.tab2, sheets[1])
        
        # Create first tab
        self.tab1.layout = QVBoxLayout(self)
        self.table1 = QTableWidget(self)
        self.tab1.layout.addWidget(self.table1)
        self.tab1.setLayout(self.tab1.layout)

        # Create second tab
        self.tab2.layout = QVBoxLayout(self)
        self.table2 = QTableWidget(self)
        self.tab2.layout.addWidget(self.table2)
        self.tab2.setLayout(self.tab2.layout)
        
        # Add tabs to widget
        self.layout.addWidget(self.info_tabs)
        self.setLayout(self.layout)
        
if __name__ == '__main__':
    # don't auto scale when drag app to a different monitor.
    # QGuiApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    
    file = TrackInfo(fp = 'track_layout.xlsx')
    worksheets = [file.get_sheet(0), file.get_sheet(1)]

    app = QApplication(sys.argv)
    app.setStyleSheet('''
        QWidget {
            font-size: 30px;
        }
    ''')
    
    myApp = MyApp()
    myApp.add_table_tabs(worksheets)

    myApp.table1 = file.load_excel_data(file.get_sheet(0))
    myApp.table2 = file.load_excel_data(file.get_sheet(1))

    #file.load_excel_data(file.get_sheet(0), myApp.table1)
    #file.load_excel_data(file.get_sheet(1), myApp.table2)

    myApp.show()

    try:
        sys.exit(app.exec())
    except SystemExit:
        print('Closing Window...')