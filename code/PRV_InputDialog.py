from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class InputDialog(QDialog):
    def __init__(self, parent):
        super(InputDialog,self).__init__(parent)

        self.first = QLineEdit(self)
        self.second = QLineEdit(self)
        self.second.setText('50')
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self);

        layout = QFormLayout(self)
        layout.addRow("Paticipant Name:", self.first)
        layout.addRow("Score:", self.second)
        layout.addWidget(buttonBox)

        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

    def getInputs(self):
        #print('bb')
        return (self.first.text(), self.second.text())