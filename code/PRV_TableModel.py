from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class TableModel(QAbstractTableModel):
    def __init__(self, data, header, from_date, to_date):
        super(TableModel, self).__init__()
        self._data = data
        self._header = header
        self.from_date = from_date
        self.to_date = to_date
        self.checkList = []
        for row in self._data:
            self.checkList.append('Unchecked')
        #self.checkList = ['Checked', 'Unchecked']
        #print(self._data)
        #print(self.checkList)

    def data(self, index, role):
        #print(self.checkList)
        row = index.row()
        col = index.column()
        if role == Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            if index.column() >0:
                return self._data[row][col-1]
        elif role == Qt.CheckStateRole:
            if index.column() == 0:
                return Qt.Checked if self.checkList[row] == 'Checked' else Qt.Unchecked

    def setData(self, index, value, role):
        row = index.row()
        col = index.column()
        if role == Qt.CheckStateRole and col == 0:
            self.checkList[row] = 'Checked' if value == Qt.Checked else 'Unchecked'
        return True

    def flags(self, index):
        if index.column() == 0:
            return Qt.ItemIsEnabled | Qt.ItemIsUserCheckable
        return Qt.ItemIsEnabled

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0])+1

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._header[section])

    def getCL(self):
        print(self.checkList)

    def getCheckedData(self):
        #print(self.checkList)
        #print(self._data)
        arr = []
        notAvail = False
        for x in range(len(self.checkList)):
            if self.checkList[x] == 'Checked':
                arr.append(self._data[x])

        if any('No' in subl for subl in arr):
            notAvail = True
        #print('k')
        #print(arr)
        return arr, notAvail

    def update(self, data, from_date, to_date):
        self._data = data
        self.checkList = []
        for row in self._data:
            self.checkList.append('Unchecked')
        self.layoutChanged.emit()
        self.from_date = from_date
        self.to_date = to_date

    def checkChecked(self):
        return ('Checked' in self.checkList)

