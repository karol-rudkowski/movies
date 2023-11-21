import apiRequests
import webbrowser
from pathlib import Path
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *


class MainWindow(QWidget):
    TARGET_WIDTH = 180  # width of images in grid
    IMDB_LINK = "https://www.imdb.com/title/"

    moviesIds = []
    lists = []

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Movies")

        # SEARCH BAR
        searchBarBox = QHBoxLayout()
        searchInput = QLineEdit()
        searchButton = QPushButton("Search")
        searchButton.clicked.connect(lambda: self.search(searchInput.text()))

        searchBarBox.addStretch()
        searchBarBox.addWidget(searchInput)
        searchBarBox.addWidget(searchButton)
        searchBarBox.addStretch()

        # RANDOM MOVIES BAR
        randomBox = QHBoxLayout()
        comboBox = QComboBox()
        showRandomButton = QPushButton("Show Random Movies")
        showRandomButton.clicked.connect(
            lambda: self.showMovies(apiRequests.getRandomMovies(self.lists[comboBox.currentIndex()])))

        self.getLists()

        for listName in self.lists:
            comboBox.addItem(' '.join(listName.split('_')))

        randomBox.addStretch()
        randomBox.addWidget(comboBox)
        randomBox.addWidget(showRandomButton)
        randomBox.addStretch()

        # NAV BAR
        navBarBox = QVBoxLayout()
        navBarBox.addLayout(searchBarBox)
        navBarBox.addLayout(randomBox)

        # GRID BOX
        self.gridBox = QGridLayout()

        # MAIN BOX
        mainBox = QVBoxLayout()
        mainBox.addLayout(navBarBox)
        mainBox.addLayout(self.gridBox)
        mainBox.addStretch()

        self.setLayout(mainBox)

        for i in range(0, 2):
            for j in range(0, 5):
                cellLayout = QVBoxLayout()
                imageLabel = QLabel()
                cellLayout.addWidget(imageLabel)
                cellLayout.addStretch()

                ratingLabel = QLabel()
                cellLayout.addWidget(ratingLabel)

                titleLabel = QLabel()
                titleLabel.setWordWrap(True)
                titleLabel.setMaximumWidth(self.TARGET_WIDTH)
                cellLayout.addWidget(titleLabel)

                self.gridBox.addLayout(cellLayout, i, j)

        try:
            # TODO randomMovies = apiRequests.getRandomMovies(self.lists[0])
            randomMovies = apiRequests.getRandomMovies(self.lists[1])
            self.showMovies(randomMovies)
        except Exception as e:
            print("Random Movies Error: ", e)
            self.showErrorDialog()

        self.show()

    def calculateImageScale(self, width) -> float:
        return self.TARGET_WIDTH / width

    def getMovieIdAndOpenWebBrowser(self, cell, grid):
        movieId = self.moviesIds[grid.indexOf(cell)]
        webbrowser.open(self.IMDB_LINK + movieId)

    def getLists(self):
        try:
            listsResult = apiRequests.getLists()
        except Exception as e:
            print("Get Lists Error: ", e)
            self.showErrorDialog()
            return

        for listName in listsResult['results']:
            self.lists.append(listName)

    def search(self, title: str):
        try:
            movies = apiRequests.searchTitle(title)
            self.showMovies(movies)
        except Exception as e:
            print("Search Error: ", e)
            self.showErrorDialog()

    def showMovies(self, moviesJSON):
        try:
            moviesCount = len(moviesJSON['results'])
        except TypeError:  # if moviesJSON is empty
            for i in range(10):
                cell = self.gridBox.findChildren(QVBoxLayout)[i]
                cell.itemAt(0).widget().clear()
                cell.itemAt(2).widget().clear()
                cell.itemAt(3).widget().clear()

            return

        self.moviesIds.clear()

        for i in range(moviesCount):
            cell = self.gridBox.findChildren(QVBoxLayout)[i]

            try:
                self.moviesIds.append(moviesJSON['results'][i]['id'])

                # set title
                title = moviesJSON['results'][i]['originalTitleText']['text']
                cell.itemAt(3).widget().setText(title)

                # set rating
                rating = moviesJSON['results'][i]['ratingsSummary']['aggregateRating']

                if rating is None:
                    rating = "?"

                cell.itemAt(2).widget().setText('\u2605 ' + str(rating))

                # set image
                scaleValue = self.calculateImageScale(moviesJSON['results'][i]['primaryImage']['width'])
                scale = QTransform().scale(scaleValue, scaleValue)

                posterImage = QImage()
                posterImage.loadFromData(apiRequests.getImage(moviesJSON['results'][i]['primaryImage']['url']))

                cell.itemAt(0).widget().setPixmap(QPixmap(posterImage).transformed(scale))
            except Exception as e:
                print("ShowMovies Error: ", e)

                scaleValue = self.calculateImageScale(102)
                scale = QTransform().scale(scaleValue, scaleValue)
                cell.itemAt(0).widget().setPixmap(QPixmap("images/noImage.png").transformed(scale))

            cell.itemAt(0).widget().mousePressEvent = lambda event, c=cell: self.getMovieIdAndOpenWebBrowser(c,
                                                                                                             self.gridBox)
            cell.itemAt(3).widget().mousePressEvent = lambda event, c=cell: self.getMovieIdAndOpenWebBrowser(c,
                                                                                                             self.gridBox)

        for i in range(moviesCount, 10):
            cell = self.gridBox.findChildren(QVBoxLayout)[i]
            cell.itemAt(0).widget().clear()
            cell.itemAt(2).widget().clear()
            cell.itemAt(3).widget().clear()

    def showErrorDialog(self):
        msgDialog = QMessageBox()
        msgDialog.setIcon(QMessageBox.Icon.Critical)
        msgDialog.setText("Connection Error. Please try again")
        msgDialog.setWindowTitle("Movies | Error")
        msgDialog.exec()


if __name__ == '__main__':
    app = QApplication([])
    app.setStyleSheet(Path('style.qss').read_text())
    window = MainWindow()
    app.exec()
