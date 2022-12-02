import sys
from PyQt5 import QtWidgets
from PyQt5 import uic

#from Signals import signals

#this is how you import ui directly
#if changes need to be made to ui, go to QtDesigner -> redesign -> simply save
form_mainWindow = uic.loadUiType("ctc_main.ui")[0]

class CTCWindowClass(QtWidgets.QMainWindow, form_mainWindow):
    def __init__(self,ctc):
        super().__init__()
        self.ctc = ctc
        self.setupUi(self)
        self.init_ui()
        self.show()

    #some temporarily function.
    def init_ui(self):
        self.train_entries = []
        self.block_entries = []

        self.schedule_trains = 0
        self.manual_trains = 0

        self.dispatch_button.clicked.connect(lambda: self.dispatch_pressed())
        self.throughput_button.clicked.connect(lambda:self.output_throughput())
        self.schedule_button.clicked.connect(lambda:self.add_schedule())

    def dispatch_pressed(self):
        self.manual_trains += 1
        arrival_time = (self.hour_selection.value(),self.minute_selection.value(),self.second_selection.value())
        destinations = self.destination_selection.toPlainText()
        self.train_entries, travel_time = self.ctc.schedule.manual_dispatch_train(arrival_time,self.train_selection.value(),self.line_train_selection.currentText(),destinations)

        #sends dispatch signal
        """"
        line = str(self.train_entries[5])
        line.upper()
        signals.send_tm_dispatch.emit(line)
        """

        self.train_table_display.addItem("MANUAL TRAIN DISPATCHED!!!!!!!!!")
        self.train_table_display.addItem("Train #: " + str(self.train_entries[0]))
        self.train_table_display.addItem("Position: " + str(self.train_entries[1]))
        self.train_table_display.addItem("Destinations: " + str(self.train_entries[3]))
        self.train_table_display.addItem("Authority: " + str(self.train_entries[4]))
        self.train_table_display.addItem("Line: " + str(self.train_entries[5]))
        self.train_table_display.addItem("Arrival Time: " + str(self.train_entries[6]))
    
    def schedule_output(self,train):
        print("SCHEDULE TRAIN: " + str(train))
        self.schedule_trains += 1
        self.schedule_list.addItem("SCHEDULE TRAIN DISPATCHED!!!!!!!!!")
        self.schedule_list.addItem("Train #: " + str(train[0]))
        self.schedule_list.addItem("Position: " + str(train[1]))
        self.schedule_list.addItem("Destinations: " + str(train[3]))
        self.schedule_list.addItem("Authority: " + str(train[4]))
        self.schedule_list.addItem("Line: " + str(train[5]))
        self.schedule_list.addItem("Arrival Time: " + str(train[6]))
        
        
    #TODO GET TICKET SALES FROM TRACKMODEL
    def output_throughput(self):
        line = self.line_throughput_selection.currentText()
        #TODO: GET TICKET SALES FROM THE TRACKMODEL
        throughput = self.ctc.schedule.calc_throughput(line=line,ticket_sales=10,hours=self.current_hour.value())
        self.throughput_output.setText(str(throughput))
    
    def add_schedule(self):
        file_name = QtWidgets.QFileDialog.getOpenFileName(self,"Open File", "", "All Files (*);;Xlsx Files(*.xlsx)")
        print("file_name: " + str(file_name[0]))
        self.ctc.schedule.upload_schedule(file_name[0])
    
    def update_current_time(self):
        #self.ctc.clock.update_time()
        self.ctc.clock.get_time()
        self.current_hour.setValue(self.ctc.clock.get_hours())
        self.current_minute.setValue(self.ctc.clock.get_minutes())
        self.current_second.setValue(self.ctc.clock.get_seconds())
        for i in range(self.manual_trains):
            if self.ctc.schedule.train_table.get_authority(i) == 0:
                authority = self.ctc.schedule.calc_authority(self.ctc.schedule.train_table.get_train_id(i),self.ctc.schedule.train_table.get_line(i),self.ctc.schedule.train_table.get_next_destination(i),self.ctc.schedule.train_table.get_position(i))
                self.ctc.schedule.train_table.change_authority(i,authority)
                self.train_table_display.takeItem((i*6) + (i + 2))
                self.train_table_display.insertItem((i*6) + (i + 2),"Position: " + str(self.ctc.schedule.train_table.get_position(i)))
                self.train_table_display.takeItem((i*6) + (i + 4))
                self.train_table_display.insertItem((i*6) + (i + 4),"Authority: " + str(self.ctc.schedule.train_table.get_authority(i)))
            else:
                self.train_table_display.takeItem((i*6) + (i + 2))
                self.train_table_display.insertItem((i*6) + (i + 2),"Position: " + str(self.ctc.schedule.train_table.get_position(i)))
                self.train_table_display.takeItem((i*6) + (i + 4))
                self.train_table_display.insertItem((i*6) + (i + 4),"Authority: " + str(self.ctc.schedule.train_table.get_authority(i)))

        for i in range(self.schedule_trains):
            if self.ctc.schedule.train_table.get_authority(i) == 0:
                authority = self.ctc.schedule.calc_authority(self.ctc.schedule.train_table.get_train_id(i),self.ctc.schedule.train_table.get_line(i),self.ctc.schedule.train_table.get_next_destination(i),self.ctc.schedule.train_table.get_position(i))
                self.ctc.schedule.train_table.change_authority(i,authority)
                self.schedule_list.takeItem((i*6) + (i + 2))
                self.schedule_list.insertItem((i*6) + (i + 2),"Position: " + str(self.ctc.schedule.train_table.get_position(i)))
                self.schedule_list.takeItem((i*6) + (i + 4))
                self.schedule_list.insertItem((i*6) + (i + 4),"Authority: " + str(self.ctc.schedule.train_table.get_authority(i)))
            else:
                self.schedule_list.takeItem((i*6) + (i + 2))
                self.schedule_list.insertItem((i*6) + (i + 2),"Position: " + str(self.ctc.schedule.train_table.get_position(i)))
                self.schedule_list.takeItem((i*6) + (i + 4))
                self.schedule_list.insertItem((i*6) + (i + 4),"Authority: " + str(self.ctc.schedule.train_table.get_authority(i)))


        for i in range(self.ctc.schedule.block_table.get_table_length()):
            if self.block_table_display.count() == 0:
                self.block_table_display.addItem(str(self.ctc.schedule.block_table.get_entry(i)))
            else:
                contains = False
                string = str(self.ctc.schedule.block_table.get_entry(i-1))
                #print("string: " + string)
                for j in range(self.block_table_display.count()):
                    #print("entry: " + str(self.block_table_display.item(j).text()))
                    if string == self.block_table_display.item(j).text():
                        contains = True
                if contains == False:
                    self.block_table_display.addItem(str(self.ctc.schedule.block_table.get_entry(i)))
        

    


#to run this file as main
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ctc_window = CTCWindowClass()
    sys.exit(app.exec_())