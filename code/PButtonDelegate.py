from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class PushButtonDelegate(QStyledItemDelegate):
    clicked = pyqtSignal(QModelIndex)
    text = []

    def paint(self, painter, option, index):
        if (
            isinstance(self.parent(), QAbstractItemView)
            and self.parent().model() is index.model()
        ):
            self.parent().openPersistentEditor(index)

    def createEditor(self, parent, option, index):
        button = QPushButton(parent)
        button.clicked.connect(lambda *args, ix=index: self.clicked.emit(ix))
        return button

    def setEditorData(self, editor, index):
        editor.setText(index.data(Qt.DisplayRole))
        self.text.append(index.data(Qt.DisplayRole))

    def setModelData(self, editor, model, index):
        pass

    def getTxt(self):
        return self.text