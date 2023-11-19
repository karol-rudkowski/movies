import apiRequests
import webbrowser
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

TARGET_WIDTH = 150  # width of images in grid
IMDB_LINK = "https://www.imdb.com/title/"

moviesIds = []
lists = []


def calculateImageScale(width) -> float:
    return TARGET_WIDTH / width


def getMovieIdAndOpenWebBrowser(cell, grid):
    movieId = moviesIds[grid.indexOf(cell)]
    webbrowser.open(IMDB_LINK + movieId)


def showErrorDialog():
    msgDialog = QMessageBox()
    msgDialog.setIcon(QMessageBox.Icon.Critical)
    msgDialog.setText("Connection Error. Please try again")
    msgDialog.setWindowTitle("Movies | Error")
    msgDialog.exec()


def getLists():
    try:
        listsResult = apiRequests.getLists()
    except Exception as e:
        print("Get Lists Error: ", e)
        showErrorDialog()
        return

    for listName in listsResult['results']:
        lists.append(listName)

    # lists.remove("titles")  # "titles" doesn't work


def window():
    app = QApplication([])

    def search(title: str):
        try:
            movies = apiRequests.searchTitle(title)
            showMovies(movies)
        except Exception as e:
            print("Search Error: ", e)
            showErrorDialog()

    # SEARCH BAR
    searchBarBox = QHBoxLayout()
    searchInput = QLineEdit()
    searchButton = QPushButton("Search")
    searchButton.clicked.connect(lambda: search(searchInput.text()))

    searchBarBox.addStretch()
    searchBarBox.addWidget(searchInput)
    searchBarBox.addWidget(searchButton)
    searchBarBox.addStretch()

    # RANDOM MOVIES BAR
    randomBox = QHBoxLayout()
    comboBox = QComboBox()
    drawButton = QPushButton("Show Random Movies")
    drawButton.clicked.connect(lambda: showMovies(apiRequests.getRandomMovies(lists[comboBox.currentIndex()])))

    getLists()

    for listName in lists:
        comboBox.addItem(' '.join(listName.split('_')))

    randomBox.addStretch()
    randomBox.addWidget(comboBox)
    randomBox.addWidget(drawButton)
    randomBox.addStretch()

    # NAV BAR
    navBarBox = QVBoxLayout()
    navBarBox.addLayout(searchBarBox)
    navBarBox.addLayout(randomBox)

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
            titleLabel.setMaximumWidth(TARGET_WIDTH)
            cellLayout.addWidget(titleLabel)

            gridBox.addLayout(cellLayout, i, j)

    def showMovies(moviesJSON):
        try:
            moviesCount = len(moviesJSON['results'])
        except TypeError:  # if moviesJSON is empty
            for i in range(10):
                cell = gridBox.findChildren(QVBoxLayout)[i]
                cell.itemAt(0).widget().clear()
                cell.itemAt(2).widget().clear()

            return

        moviesIds.clear()

        for i in range(moviesCount):
            cell = gridBox.findChildren(QVBoxLayout)[i]

            try:
                moviesIds.append(moviesJSON['results'][i]['id'])

                # set title
                title = moviesJSON['results'][i]['originalTitleText']['text']
                cell.itemAt(2).widget().setText(title)

                # set image
                scaleValue = calculateImageScale(moviesJSON['results'][i]['primaryImage']['width'])
                scale = QTransform().scale(scaleValue, scaleValue)

                poster = QImage()
                poster.loadFromData(apiRequests.getImage(moviesJSON['results'][i]['primaryImage']['url']))

                cell.itemAt(0).widget().setPixmap(QPixmap(poster).transformed(scale))
            except Exception as e:
                print("ShowMovies Error: ", e)
                scale = QTransform().scale(1.47, 1.47)
                cell.itemAt(0).widget().setPixmap(QPixmap("images/noImage.png").transformed(scale))

            cell.itemAt(0).widget().mousePressEvent = lambda event, c=cell: getMovieIdAndOpenWebBrowser(c, gridBox)
            cell.itemAt(2).widget().mousePressEvent = lambda event, c=cell: getMovieIdAndOpenWebBrowser(c, gridBox)

        for i in range(moviesCount, 10):
            cell = gridBox.findChildren(QVBoxLayout)[i]
            cell.itemAt(0).widget().clear()
            cell.itemAt(2).widget().clear()

    try:
        randomMovies = apiRequests.getRandomMovies("most_pop_movies")
        showMovies(randomMovies)
    except Exception as e:
        print("Random Movies Error: ", e)
        showErrorDialog()

    # MAIN BOX
    mainBox = QVBoxLayout()
    mainBox.addLayout(navBarBox)
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
