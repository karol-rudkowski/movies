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
            cellLayout = QVBoxLayout()
            cellLabel = QLabel()
            cellLabel.setPixmap(QPixmap("images/noImage.png"))
            cellLayout.addWidget(cellLabel)
            cellLayout.addWidget(QLabel("label"))
            cellLayout.addStretch()

            gridBox.addLayout(cellLayout, i, j)

    try:
        random = apiRequests.getRandomMovies()
    except ConnectionError as e:
        print(e)
        return

    scale = QTransform().scale(0.1, 0.1)

    for i in range(0, 10):
        # set title
        title = random['results'][i]['originalTitleText']['text']
        cell = gridBox.findChildren(QVBoxLayout)[i]
        cell.itemAt(1).widget().setText(title)

        # set image
        poster = QImage()

        try:
            poster.loadFromData(apiRequests.getImage(random['results'][i]['primaryImage']['url']))
            cell.itemAt(0).widget().setPixmap(QPixmap(poster).transformed(scale))
        except:
            cell.itemAt(0).widget().setPixmap(QPixmap("images/noImage.png"))

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
