import sys
import csv

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem


class Ui_MainWindow(QMainWindow):
    def setupUi(self, MainWindow):
        super(Ui_MainWindow, self).__init__()
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(682, 494)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.school_num = QtWidgets.QComboBox(self.centralwidget)
        self.school_num.setGeometry(QtCore.QRect(20, 30, 201, 31))
        self.school_num.setObjectName("school_num")
        self.class_num = QtWidgets.QComboBox(self.centralwidget)
        self.class_num.setGeometry(QtCore.QRect(240, 30, 201, 31))
        self.class_num.setObjectName("class_num")
        self.res = QtWidgets.QPushButton(self.centralwidget)
        self.res.setGeometry(QtCore.QRect(460, 30, 201, 31))
        self.res.setObjectName("res")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(20, 80, 641, 381))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.res.setText(_translate("MainWindow", "Узнать результаты"))


class Olimp(Ui_MainWindow):
    def __init__(self):
        super().setupUi(self)
        self.table_name = 'rez.csv'
        self.loadTable(self.table_name, 'Все', 'Все')
        with open(self.table_name, encoding="utf8") as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
            self.school_num.addItems(['Все'] + sorted(list(set([i['login'].split('-')[2] for i in reader]))))
            self.class_num.addItem('Все')
        self.school_num.currentTextChanged.connect(self.class_num_add)
        self.res.clicked.connect(self.get_result)
        self.setWindowTitle('Результат олимпиады: фильтрация')

    def get_result(self):
        self.loadTable(self.table_name, self.school_num.currentText(), self.class_num.currentText())

    def class_num_add(self):
        with open(self.table_name, encoding="utf8") as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
            curr = self.class_num.currentText()
            self.class_num.clear()
            self.class_num.addItems(['Все'] + sorted(list(set([i['login'].split('-')[3] for i in reader if
                                                               i['login'].split('-')[
                                                                   2] == self.school_num.currentText()]))))
            if curr in [self.class_num.itemText(i) for i in range(self.class_num.count())]:
                self.class_num.setCurrentText(curr)

    def loadTable(self, table_name, sch, cl):
        with open(table_name, encoding="utf8") as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
            title = ['Фамилия', 'Результат']
            self.tableWidget.clear()
            self.tableWidget.setColumnCount(len(title))
            self.tableWidget.setHorizontalHeaderLabels(title)
            self.tableWidget.setRowCount(0)
            count = 0
            for i, row in enumerate(reader):
                if (row['login'].split('-')[2] == (sch if sch != 'Все' else row['login'].split('-')[2]) and
                        row['login'].split('-')[3] == (cl if cl != 'Все' else row['login'].split('-')[3])):
                    self.tableWidget.setRowCount(
                        self.tableWidget.rowCount() + 1)

                    for j, elem in enumerate((row['user_name'], row['Score'])):
                        self.tableWidget.setItem(
                            count, j, (QTableWidgetItem(elem.split()[3]) if j == 0 else QTableWidgetItem(elem)))
                    count += 1
        self.tableWidget.resizeColumnsToContents()


if __name__ == '__main__':
    app = QApplication([])
    form = Olimp()
    form.show()
    sys.exit(app.exec())
