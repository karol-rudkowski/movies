import apiRequests
import webbrowser
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

TARGET_WIDTH = 150.0  # width of images in grid
IMDB_LINK = "https://www.imdb.com/title/"

moviesIds = []


def findScale(width) -> float:
    return TARGET_WIDTH / width


def getMovieIdAndOpenWebBrowser(cell, grid):
    movieId = moviesIds[grid.indexOf(cell)]
    webbrowser.open(IMDB_LINK + movieId)


def window():
    app = QApplication([])

    def search(title: str):
        try:
            movies = apiRequests.searchTitle(title)
            showMovies(movies)
        except ConnectionError as e:
            print(e)
            return

    # SEARCH BAR
    searchBarBox = QHBoxLayout()
    searchInput = QLineEdit()
    searchButton = QPushButton("Search")
    searchButton.clicked.connect(lambda: search(searchInput.text()))

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
            cellLayout.addWidget(imageLabel)
            cellLayout.addStretch()

            titleLabel = QLabel()
            titleLabel.setWordWrap(True)
            titleLabel.setGeometry(QRect(0, 0, 150, 50))  # TODO check if it works
            cellLayout.addWidget(titleLabel)

            gridBox.addLayout(cellLayout, i, j)

    def showMovies(moviesJSON):
        moviesCount = len(moviesJSON['results'])
        moviesIds.clear()

        for i in range(moviesCount):
            # set title
            title = moviesJSON['results'][i]['originalTitleText']['text']
            cell = gridBox.findChildren(QVBoxLayout)[i]
            cell.itemAt(2).widget().setText(title)

            # set image
            try:
                moviesIds.append(moviesJSON['results'][i]['id'])

                scaleValue = findScale(moviesJSON['results'][i]['primaryImage']['width'])
                scale = QTransform().scale(scaleValue, scaleValue)

                poster = QImage()
                poster.loadFromData(apiRequests.getImage(moviesJSON['results'][i]['primaryImage']['url']))

                cell.itemAt(0).widget().setPixmap(QPixmap(poster).transformed(scale))
            except:
                scale = QTransform().scale(1.47, 1.47)
                cell.itemAt(0).widget().setPixmap(QPixmap("images/noImage.png").transformed(scale))

            cell.itemAt(0).widget().mousePressEvent = lambda event, c=cell: getMovieIdAndOpenWebBrowser(c, gridBox)
            cell.itemAt(2).widget().mousePressEvent = lambda event, c=cell: getMovieIdAndOpenWebBrowser(c, gridBox)

        for i in range(moviesCount, 10):
            cell = gridBox.findChildren(QVBoxLayout)[i]
            cell.itemAt(0).widget().clear()
            cell.itemAt(2).widget().clear()

    try:
        randomMovies = apiRequests.getRandomMovies()
        showMovies(randomMovies)
    except ConnectionError as e:
        print(e)
        return

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
