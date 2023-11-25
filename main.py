import webbrowser
from pathlib import Path
from requests import exceptions as requestsExceptions

from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt

import apiRequests


class MainWindow(QScrollArea):
    TARGET_WIDTH = 150  # width of images in grid
    IMDB_LINK = 'https://www.imdb.com/title/'

    moviesIds = []
    lists = []

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Movies')

        # SEARCH BAR
        searchBarBox = QHBoxLayout()
        searchInput = QLineEdit()
        searchButton = QPushButton('Search')
        searchButton.clicked.connect(lambda: self.search(searchInput.text()))

        searchBarBox.addStretch()
        searchBarBox.addWidget(searchInput)
        searchBarBox.addWidget(searchButton)
        searchBarBox.addStretch()

        # RANDOM MOVIES BAR
        randomBox = QHBoxLayout()
        comboBox = QComboBox()
        showRandomButton = QPushButton('Show Random Movies')
        showRandomButton.clicked.connect(lambda: self.showMovies(apiRequests.getRandomMovies(self.lists[comboBox.currentIndex()])))

        self.setLists(comboBox)

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

        # DESCRIPTION BOX
        self.descriptionBox = QVBoxLayout()

        miTitleLabel = QLabel()
        miTitleLabel.setObjectName('miTitleLabel')
        miPlotLabel = QLabel()
        miPlotLabel.setWordWrap(True)
        miRelease = QLabel()
        miGoToWebButton = QPushButton('Go to IMDB')
        miGoToWebButton.setObjectName('miGoToWebButton')
        miGoToWebButton.setVisible(False)

        self.descriptionBox.addWidget(miTitleLabel)
        self.descriptionBox.addWidget(miPlotLabel)
        self.descriptionBox.addWidget(miRelease)
        self.descriptionBox.addWidget(miGoToWebButton)

        # MAIN BOX
        mainBox = QVBoxLayout()
        mainBox.addLayout(navBarBox)
        mainBox.addLayout(self.gridBox)
        mainBox.addLayout(self.descriptionBox)
        mainBox.addStretch()

        mainWidget = QWidget()
        mainWidget.setLayout(mainBox)

        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)
        self.setMinimumSize(900, 800)
        self.setWidget(mainWidget)

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

                cellWidget = QWidget()
                cellWidget.setObjectName('cellWidget')
                cellWidget.setLayout(cellLayout)

                self.gridBox.addWidget(cellWidget, i, j)

        try:
            # TODO randomMovies = apiRequests.getRandomMovies(self.lists[0])
            randomMovies = apiRequests.getRandomMovies(self.lists[1])
            self.showMovies(randomMovies)
        except Exception as e:
            print('Random Movies Error: ', e)
            self.showErrorDialog()

        self.show()

    def calculateImageScale(self, width) -> float:
        return self.TARGET_WIDTH / width

    def openMovieWebPage(self, movieId: str):
        webbrowser.open(self.IMDB_LINK + movieId)

    def clearDescription(self):
        self.descriptionBox.itemAt(0).widget().clear()
        self.descriptionBox.itemAt(1).widget().clear()
        self.descriptionBox.itemAt(2).widget().clear()
        self.descriptionBox.itemAt(3).widget().setVisible(False)

    def getMoreMovieInfo(self, cell, grid):
        movieId = self.moviesIds[grid.indexOf(cell)]

        try:
            movieInfo = apiRequests.getInfo(movieId)
        except Exception as e:
            print('Get Movie Info Error: ', e)
            self.showErrorDialog()
            return

        self.clearDescription()
        self.descriptionBox.itemAt(3).widget().setVisible(True)
        self.descriptionBox.itemAt(3).widget().mousePressEvent = lambda event: self.openMovieWebPage(movieId)

        try:
            self.descriptionBox.itemAt(0).widget().setText(movieInfo['results']['originalTitleText']['text'])
        except Exception as e:
            print(e, ': originalTitleText')

        try:
            self.descriptionBox.itemAt(1).widget().setText(movieInfo['results']['plot']['plotText']['plainText'])
        except Exception as e:
            print(e, ': plotText')

        try:
            date = movieInfo['results']['releaseDate']
            dateString = ''

            if date['day'] is not None:
                dateString = 'Release date: ' + str(date['day']) + '.' + str(date['month']) + '.' + str(date['year'])
            elif date['month'] is not None:
                dateString = 'Release date: ' + str(date['month']) + '.' + str(date['year'])
            elif date['year'] is not None:
                dateString = 'Release date: ' + str(date['year'])

            self.descriptionBox.itemAt(2).widget().setText(dateString)
        except Exception as e:
            print(e, ': releaseDate')

    def setLists(self, cbox: QComboBox):
        try:
            listsResult = apiRequests.getLists()

            for listName in listsResult['results']:
                self.lists.append(listName)

            for listName in self.lists:
                cbox.addItem(' '.join(listName.split('_')))

        except Exception as e:
            print('Get Lists Error: ', e)
            self.showErrorDialog()
            return

    def search(self, title: str):
        self.clearDescription()

        try:
            movies = apiRequests.searchTitle(title)
            self.showMovies(movies)
        except requestsExceptions.HTTPError as e:
            print('Search Error - Incorrect Data: ', e)
            self.showErrorDialog(1)
        except Exception as e:
            print('Search Error: ', e)
            self.showErrorDialog(0)

    def showMovies(self, moviesJSON):
        self.clearDescription()

        try:
            moviesCount = len(moviesJSON['results'])
        except TypeError:  # if moviesJSON is empty
            for i in range(10):
                cell = self.gridBox.findChildren(QWidget)[i]

                cell.itemAt(0).widget().clear()
                cell.itemAt(2).widget().clear()
                cell.itemAt(3).widget().clear()

            return

        self.moviesIds.clear()

        for i in range(moviesCount):
            cellParent = self.gridBox.itemAt(i)
            cell = cellParent.widget().layout()

            try:
                self.moviesIds.append(moviesJSON['results'][i]['id'])

                # set title
                title = moviesJSON['results'][i]['originalTitleText']['text']
                cell.itemAt(3).widget().setText(title)

                # set rating
                rating = moviesJSON['results'][i]['ratingsSummary']['aggregateRating']

                if rating is None:
                    rating = '?'

                cell.itemAt(2).widget().setText('\u2605 ' + str(rating))

                # set image
                scaleValue = self.calculateImageScale(moviesJSON['results'][i]['primaryImage']['width'])
                scale = QTransform().scale(scaleValue, scaleValue)

                posterImage = QImage()
                posterImage.loadFromData(apiRequests.getImage(moviesJSON['results'][i]['primaryImage']['url']))

                cell.itemAt(0).widget().setPixmap(QPixmap(posterImage).transformed(scale))
            except Exception as e:
                print('ShowMovies Error: ', e)

                scaleValue = self.calculateImageScale(150)
                scale = QTransform().scale(scaleValue, scaleValue)
                cell.itemAt(0).widget().setPixmap(QPixmap('images/noImage.png').transformed(scale))

            cell.itemAt(0).widget().mousePressEvent = lambda event, c=cellParent: self.getMoreMovieInfo(c,
                                                                                                        self.gridBox)
            cell.itemAt(3).widget().mousePressEvent = lambda event, c=cellParent: self.getMoreMovieInfo(c,
                                                                                                        self.gridBox)

        for i in range(moviesCount, 10):
            cell = self.gridBox.itemAt(i).widget().layout()

            cell.itemAt(0).widget().clear()
            cell.itemAt(2).widget().clear()
            cell.itemAt(3).widget().clear()

    def showErrorDialog(self, error=0):
        msgDialog = QMessageBox()

        if error == 1:
            msgDialog.setText('Incorrect data was entered in the search field')
            msgDialog.setIcon(QMessageBox.Icon.Warning)
        else:
            msgDialog.setText('Connection Error. Please try again')
            msgDialog.setIcon(QMessageBox.Icon.Critical)

        msgDialog.setWindowTitle('Movies | Error')
        msgDialog.exec()


if __name__ == '__main__':
    app = QApplication([])
    app.setStyleSheet(Path('style.qss').read_text())
    window = MainWindow()
    app.exec()
