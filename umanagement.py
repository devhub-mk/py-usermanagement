import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import(
    QApplication,
    QMainWindow,
    QTableWidget,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
    QTableWidgetItem,
)


class Umanagement(QMainWindow):

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("User Management")
        self.setFixedWidth(600)
        self.generalLayout = QVBoxLayout()
        centralWidget = QWidget(self)
        centralWidget.setLayout(self.generalLayout)
        self.setCentralWidget(centralWidget)
        self._createFrom()
        self._createSearchForm()
        self.allRecords = self.readDataFromFile()
        self.createTable()
        self.displayRecords(self.allRecords)
        
        self.action = Action(view=self)

    def _createFrom(self):
        formLayout = QHBoxLayout()

        formLayout.addWidget(QLabel("Name"))
        self.inputName = QLineEdit()
        self.inputName.setFixedWidth(130)
        self.inputName.setPlaceholderText("Name")
        formLayout.addWidget(self.inputName)

        formLayout.addWidget(QLabel("Email"))
        self.inputEmail = QLineEdit()
        self.inputEmail.setFixedWidth(130)
        self.inputEmail.setPlaceholderText("Email")
        formLayout.addWidget(self.inputEmail)
        
        formLayout.addWidget(QLabel("Age"))
        self.inputAge = QLineEdit()
        self.inputAge.setFixedWidth(130)
        self.inputAge.setPlaceholderText("Age")
        formLayout.addWidget(self.inputAge,)

        self.submitButton = QPushButton("Submit")
        self.submitButton.setFixedWidth(80)
        formLayout.addWidget(self.submitButton)

        self.generalLayout.addLayout(formLayout)

    def _createSearchForm(self):
        searchLayout = QHBoxLayout()
        searchLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.searchInput = QLineEdit()
        self.searchInput.setFixedWidth(130)
        self.searchInput.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.searchInput.setPlaceholderText("Search")
        searchLayout.addWidget(self.searchInput)

        self.searchButton = QPushButton("Search")
        self.searchButton.setFixedWidth(80)
        searchLayout.addWidget(self.searchButton)

        self.generalLayout.addLayout(searchLayout)

    def createTable(self):
        self.tableLayout = QTableWidget(self)
        self.tableLayout.setColumnCount(3)
        self.tableLayout.setHorizontalHeaderLabels(["Name", "Email", "Age"])
        self.generalLayout.addWidget(self.tableLayout)

    def displayRecords(self, records):
        self.tableLayout.setRowCount(len(records))
        row = 0
        for record in records:
            self.tableLayout.setItem(row, 0, QTableWidgetItem(record["Name"]))
            self.tableLayout.setItem(row, 1, QTableWidgetItem(record["Email"]))
            self.tableLayout.setItem(row, 2, QTableWidgetItem(str(record["Age"]).strip("\n")))
            row += 1

        self.tableLayout.setColumnWidth(0,180)
        self.tableLayout.setColumnWidth(1,250)
        self.tableLayout.setColumnWidth(2,80)
        
    def readDataFromFile(self):
        data = []
        records = open('data.txt', 'r')
        for  record in records:
            listdata = list(record.split(","))
            data.append({"Name": listdata[0], "Email": listdata[1], "Age": listdata[2]})
        return data

    def clearFormInputs(self):
        self.inputName.setText("")
        self.inputEmail.setText("")
        self.inputAge.setText("")

    def readSearchInput(self):
        search = self.searchInput.text()
        return search
    
    def clearSearchInput(self):
        self.searchInput.setText("")

    def getFormData(self):
        name = self.inputName.text()
        email = self.inputEmail.text()
        age = self.inputAge.text()
        return name, email, age


class Action():

    def __init__(self, view):
        self._view = view
        self._connectSignalsAndSlots()

    def createNewRecord(self):
        name, email, age = self._view.getFormData()
        records = open("data.txt", "a")
        records.write("{},{},{}\n".format(name,email, age))
        records.close()
        self._view.allRecords.append({"Name": name, "Email": email, "Age": age})
        self._view.clearFormInputs()
        self._view.displayRecords(self._view.allRecords)
    
    def searchRecord(self):
        name = self._view.readSearchInput()
        if not name:
            self._view.displayRecords(self._view.allRecords)
        else:
            searchResult = filterRecords(self._view.allRecords,name=name)
            self._view.displayRecords(searchResult)
        self._view.clearSearchInput()

    def _connectSignalsAndSlots(self):
        self._view.submitButton.clicked.connect(self.createNewRecord)
        self._view.searchButton.clicked.connect(self.searchRecord)

def filterRecords(records, name=None):
    if name is None:
        return records

    filtered_records = []
    for record in records:
        if name.lower() in record["Name"].lower():
            filtered_records.append(record)
    return filtered_records

def main():
    umanagementApp = QApplication([])
    managementWindow = Umanagement()
    managementWindow.show()
    Action(view=managementWindow)
    sys.exit(umanagementApp.exec())


if __name__ == "__main__":
    main()