import apiRequests
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QApplication, QLabel

if __name__ == '__main__':
    resp = apiRequests.searchTitle("Bodies")

    # print(resp['results'][1]['primaryImage']['url'])
    print(resp)

    app = QApplication([])

    image = QImage()
    image.loadFromData(apiRequests.getImage(resp['results'][0]['primaryImage']['url']))

    image_label = QLabel()
    image_label.setPixmap(QPixmap(image))
    image_label.show()

    app.exec()
