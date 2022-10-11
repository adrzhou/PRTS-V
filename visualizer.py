from PySide6.QtWidgets import (QApplication, QWidget, QLabel, QMainWindow,
                               QHBoxLayout, QPushButton, QVBoxLayout)
from PySide6.QtCore import Qt, QPoint, QRect
from PySide6.QtGui import QPixmap, QPainter, QColor, QBrush, QImage, QPen
from utils.map import Map
import tomli

with open('NL-EX-8.toml', 'rb') as file:
    steps = tomli.load(file)


class Visualizer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Visualizer')
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setWindowFlag(Qt.WindowTransparentForInput)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.center = QLabel()
        self.canvas = QPixmap()
        self.setCentralWidget(self.center)

        self.cur = 0
        self.steps = steps
        self.map = None
        self.plot = None

    def load(self):
        width = self.center.width()
        height = self.center.height()
        self.canvas = QPixmap(width, height)
        self.canvas.fill(Qt.GlobalColor.transparent)

        map_ = Map(width, height)
        self.map = map_
        self.plot = self.map.plot('NL-EX-8')

        painter = QPainter(self.canvas)
        for row in self.plot:
            for tile in row:
                data, pos = tile
                brush = QBrush()
                brush.setColor(QColor(255 * data.heightType, 0, 255 * data.buildableType))
                brush.setStyle(Qt.BrushStyle.Dense1Pattern)
                painter.setBrush(brush)
                painter.drawEllipse(pos[0], pos[1], 15, 15)
        painter.end()
        self.center.setPixmap(self.canvas)

    def reload(self):
        self.canvas = QPixmap()
        self.center.setPixmap(self.canvas)
        self.cur = 0

    def prev(self):
        if self.cur == 1:
            return
        self.cur -= 1
        self.draw()

    def next(self):
        if self.cur == len(self.steps):
            return
        self.cur += 1
        self.draw()

    def draw(self):
        step = self.steps[str(self.cur)]
        x = step['x']
        y = step['y']
        action = step['Action']
        oprt = step['Operator']
        condition = step['Condition']

        tile_pos = self.plot[y][x][1]
        self.canvas.fill(Qt.GlobalColor.transparent)
        painter = QPainter(self.canvas)
        painter.setOpacity(0.4)
        painter.translate(-20, -30)
        point = QPoint(tile_pos[0], tile_pos[1])
        image = QImage(f'{action}.png')
        painter.drawImage(point, image)
        painter.resetTransform()
        painter.translate(30, 30)
        brush = QBrush()
        brush.setColor(Qt.black)
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        painter.setBrush(brush)

        textbox = QRect(tile_pos[0], tile_pos[1], 180, 120)
        painter.drawRect(textbox)

        pen = QPen()
        pen.setColor(Qt.white)
        pen.setWidth(20)
        painter.setPen(pen)
        text1 = f'Operator: {oprt}'
        text2 = f'Condition: {condition}'

        painter.drawText(tile_pos[0], tile_pos[1] + 10, text1)
        painter.drawText(tile_pos[0], tile_pos[1] + 24, text2)

        painter.end()

        self.center.setPixmap(self.canvas)


class Controller(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setWindowTitle('Controller')
        self.top = QWidget()
        self.top.setLayout(QHBoxLayout())
        self.top.layout().addWidget(QWidget())
        self.load = QPushButton('Load')
        self.load.clicked.connect(visualizer.load)
        self.top.layout().addWidget(self.load)
        self.top.layout().addWidget(QWidget())
        self.middle = QWidget()
        self.middle.setLayout(QHBoxLayout())
        self.prev = QPushButton('Prev')
        self.middle.layout().addWidget(self.prev)
        self.prev.clicked.connect(visualizer.prev)
        self.middle.layout().addWidget(QWidget())
        self.next = QPushButton('Next')
        self.middle.layout().addWidget(self.next)
        self.next.clicked.connect(visualizer.next)
        self.bottom = QWidget()
        self.bottom.setLayout(QHBoxLayout())
        self.bottom.layout().addWidget(QWidget())
        self.reload = QPushButton('Reload')
        self.bottom.layout().addWidget(self.reload)
        self.reload.clicked.connect(visualizer.reload)
        self.bottom.layout().addWidget(QWidget())
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.top)
        self.layout().addWidget(self.middle)
        self.layout().addWidget(self.bottom)


app = QApplication([])
visualizer = Visualizer()
controller = Controller()
visualizer.show()
controller.show()

if __name__ == '__main__':
    app.exec()
