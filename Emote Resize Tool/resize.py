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

            item_list = []

            for item in event.mimeData().urls():
                if item.isLocalFile():
                    item_list.append(item.toLocalFile())

            self.addItems(item_list)
        else:
            event.ignore()


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(350, 250)
        MainWindow.setMinimumSize(QtCore.QSize(350, 250))
        MainWindow.setMaximumSize(QtCore.QSize(350, 250))
        MainWindow.setWindowIcon(
            QtGui.QIcon(f"{os.path.dirname(os.path.realpath(__file__))}/icon.ico")
        )

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(10, 200, 240, 30))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setTextVisible(False)
        self.progressBar.setOrientation(QtCore.Qt.Horizontal)
        self.progressBar.setObjectName("progressBar")

        self.progressBarLabel = QtWidgets.QLabel(self.centralwidget)
        self.progressBarLabel.setGeometry(QtCore.QRect(10, 205, 240, 20))
        self.progressBarLabel.setText("")
        self.progressBarLabel.setAlignment(Qt.AlignCenter)
        self.progressBarLabel.setObjectName("progressBarLabel")

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

        number_of_items = len(itemList)
        skipped_items = 0

        for count, item in enumerate(itemList):
            if os.path.exists(item) and item.lower().endswith("png"):
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
                elif image_size[0] % 18 == 0 and image_size[1] % 18 == 0:
                    image_18 = image.resize((18, 18))
                    image_18.save(image_name + "_18px.png")

                    image_36 = image.resize((36, 36))
                    image_36.save(image_name + "_36px.png")

                    image_72 = image.resize((72, 72))
                    image_72.save(image_name + "_72px.png")
                else:
                    skipped_items += 1
            else:
                skipped_items += 1

            percentage = ((count + 1) * 100) / number_of_items
            self.progressBar.setValue(percentage)

        if skipped_items > 0:
            label_text = f"Resize complete! {skipped_items} items skipped"
        else:
            label_text = "Resize complete!"

        self.progressBarLabel.setText(label_text)
        self.imageList.clear()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
