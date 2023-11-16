import apiRequests
import webbrowser
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

TARGET_SIZE = 150.0
IMDB_LINK = "https://www.imdb.com/title/"
moviesIds = []
def findScale(size) -> float:
    return TARGET_SIZE / size

def labelClicked(cell, grid):
    id = moviesIds[grid.indexOf(cell)]
    webbrowser.open(IMDB_LINK + id)
    print(id)

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

            imageLabel = QLabel()
            imageLabel.setPixmap(QPixmap("images/noImage.png"))
            cellLayout.addWidget(imageLabel)

            cellLayout.addStretch()

            titleLabel = QLabel("title")
            titleLabel.setWordWrap(True)
            titleLabel.setGeometry(QRect(0, 0, 150, 50))
            cellLayout.addWidget(titleLabel)

            gridBox.addLayout(cellLayout, i, j)


    try:
        randomMovies = apiRequests.getRandomMovies()
    except ConnectionError as e:
        print(e)
        return

    for i in range(0, 10):
        # set title
        title = randomMovies['results'][i]['originalTitleText']['text']
        cell = gridBox.findChildren(QVBoxLayout)[i]
        cell.itemAt(2).widget().setText(title)

        # set image
        try:
            scaleValue = findScale(randomMovies['results'][i]['primaryImage']['width'])
            scale = QTransform().scale(scaleValue, scaleValue)

            poster = QImage()
            poster.loadFromData(apiRequests.getImage(randomMovies['results'][i]['primaryImage']['url']))

            moviesIds.append(randomMovies['results'][i]['id'])

            cell.itemAt(0).widget().setPixmap(QPixmap(poster))
            cell.itemAt(0).widget().setPixmap(QPixmap(poster).transformed(scale))

            cell.itemAt(0).widget().mousePressEvent = lambda event, c=cell: labelClicked(c, gridBox)
            cell.itemAt(2).widget().mousePressEvent = lambda event, c=cell: labelClicked(c, gridBox)
        except:
            scale = QTransform().scale(1.47, 1.47)

            cell.itemAt(0).widget().setPixmap(QPixmap("images/noImage.png").transformed(scale))

            cell.itemAt(0).widget().mousePressEvent = lambda event, c=cell: labelClicked(c, gridBox)
            cell.itemAt(2).widget().mousePressEvent = lambda event, c=cell: labelClicked(c, gridBox)

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
