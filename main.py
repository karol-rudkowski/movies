import apiRequests
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *


def window():
    app = QApplication([])

    # SEARCH BAR
    searchBarBox = QHBoxLayout()
    searchInput = QLineEdit()
    searchButton = QPushButton("Search")

    searchBarBox.addStretch()
    searchBarBox.addWidget(searchInput)
    searchBarBox.addWidget(searchButton)
    searchBarBox.addStretch()

    # GRID BOX
    gridBox = QGridLayout()

    for i in range(0, 2):
        for j in range(0, 5):
            tempLayout = QVBoxLayout()
            tempLabel = QLabel()
            tempLabel.setPixmap(QPixmap("images/noImage.png"))
            tempLayout.addWidget(tempLabel)
            tempLayout.addWidget(QLabel("label"))
            tempLayout.addStretch()

            gridBox.addLayout(tempLayout, i, j)

            # gridBox.addLayout(QVBoxLayout().addWidget(QLabel().setPixmap(QPixmap("images/noImage.png"))), i, j)
            # gridBox.addWidget(QPushButton("B" + str(i) + str(j)), i, j)

    # MAIN BOX
    mainBox = QVBoxLayout()
    mainBox.addLayout(searchBarBox)
    mainBox.addLayout(gridBox)
    mainBox.addStretch()

    # WINDOW
    window = QWidget()
    window.setLayout(mainBox)
    window.setWindowTitle("Movies")
    window.show()

    app.exec()


if __name__ == '__main__':
    window()

    # resp = apiRequests.searchTitle("Bodies")

    # print(resp['results'][1]['primaryImage']['url'])
    # print(resp)

    # image = QImage()
    # image.loadFromData(apiRequests.getImage(resp['results'][0]['primaryImage']['url']))
    #
    # image_label = QLabel()
    # image_label.setPixmap(QPixmap(image))
    # image_label.show()
