import os
import sys

from PIL import Image
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt


class ListWidget(QtWidgets.QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()

            itemList = []

            for url in event.mimeData().urls():
                if url.isLocalFile():
                    itemList.append(str(url.toLocalFile()))
                else:
                    print("File is not local")

            self.addItems(itemList)

        else:
            event.ignore()


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(350, 250)
        MainWindow.setMinimumSize(QtCore.QSize(350, 250))
        MainWindow.setMaximumSize(QtCore.QSize(350, 250))
        # MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(10, 200, 240, 30))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setTextVisible(False)
        self.progressBar.setOrientation(QtCore.Qt.Horizontal)
        self.progressBar.setObjectName("progressBar")

        self.resizeButton = QtWidgets.QPushButton(self.centralwidget)
        self.resizeButton.setGeometry(QtCore.QRect(260, 200, 80, 30))
        self.resizeButton.setObjectName("resizeButton")
        self.resizeButton.clicked.connect(self.Resize_Images)

        self.imageList = ListWidget(self.centralwidget)
        self.imageList.setGeometry(QtCore.QRect(10, 10, 330, 180))
        self.imageList.setAcceptDrops(True)
        self.imageList.setAlternatingRowColors(True)
        self.imageList.setObjectName("imageList")

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Emote Resize Tool"))
        self.resizeButton.setText(_translate("MainWindow", "Resize"))

    def Resize_Images(self):
        itemList = [
            self.imageList.item(i).text() for i in range(self.imageList.count())
        ]

        for item in itemList:
            if os.path.exists(item):
                image = Image.open(item)
                image_size = image.size
                image_name = image.filename.split(".")[0]

                if image_size[0] % 28 == 0 and image_size[1] % 28 == 0:
                    image_28 = image.resize((28, 28))
                    image_28.save(image_name + "_28px.png")

                    image_56 = image.resize((56, 56))
                    image_56.save(image_name + "_56px.png")

                    image_112 = image.resize((112, 112))
                    image_112.save(image_name + "_112px.png")

                else:
                    print("Incorrect dimensions")
            else:
                print("Item does not exist")

        self.imageList.clear()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
