from matplotlib import pyplot as plt
import numpy as np

import sys
import re
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PySide2.QtWidgets import QApplication, QWidget, QLineEdit, QLabel, QGridLayout, QPushButton, QMessageBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Plotter")
        self.setMinimumHeight(700)
        self.setMinimumWidth(700)
        self.widget = QWidget(self)
        self.error = QMessageBox
        self.showUILayout()

    def makeFunctionInput(self):
        self.functionInput = QLineEdit(self)
        self.functionInput.setPlaceholderText("Enter the function")
        self.functionLabel = QLabel("f(x)")

    def showError(self, errorMessage):
        if errorMessage != "":
            self.error.warning(self, "Error", errorMessage)

    def makeRangeInput(self):
        self.minLabel = QLabel("Minimum X")
        self.minimumInput = QLineEdit(self)
        self.minimumInput.setPlaceholderText("Enter minimum value")
        self.maxLabel = QLabel("Maximum X")
        self.maximumInput = QLineEdit(self)
        self.maximumInput.setPlaceholderText("Enter maximum value")

    def makeButtonShow(self):
        self.showButton = QPushButton("Plot", self)
        self.showButton.clicked.connect(self.draw)

    def makeGraphCanvas(self):
        self.graph = plt.figure()
        self.axes = self.graph.add_subplot(111)
        self.canvas = FigureCanvas(self.graph)
        self.toolbar = NavigationToolbar(self.canvas, self)


    def setUI(self):
        self.makeFunctionInput()
        self.makeRangeInput()
        self.makeButtonShow()
        self.makeGraphCanvas()

    def showUILayout(self):
        self.setUI()
        self.layout = QGridLayout(self.widget)
        self.layout.addWidget(self.functionLabel, 0, 0)
        self.layout.addWidget(self.functionInput, 0, 1)
        self.layout.addWidget(self.minLabel, 1, 0)
        self.layout.addWidget(self.minimumInput, 1, 1)
        self.layout.addWidget(self.maxLabel, 1, 2)
        self.layout.addWidget(self.maximumInput, 1, 3)
        self.layout.addWidget(self.showButton, 2, 0)
        self.layout.addWidget(self.toolbar, 4, 0, 1, 4)
        self.layout.addWidget(self.canvas, 5, 0, 1, 4)

    def validate(self, function, minX, maxX):
        if(function == ""):
            self.showError("Empty Function body")
            return False

        if(minX == ""):
            self.showError("Empty Min x")
            return False

        if(maxX == ""):
            self.showError("Empty Max x")
            return False

        regex = "(?:[0-9-+ * / ^ () x])+"
        if not bool(re.search(regex, function)):
            self.showError("Wrong Function f(x)")
            return False

        return True

    def set_app_logic(self):
        function = self.functionInput.text().lower()
        function = function.replace("^", "**")
        minimumX = self.minimumInput.text()
        maximumX = self.maximumInput.text()

        x = []
        y = []

        if not (self.validate(function, minimumX, maximumX)):
            return x, y

        try:
            minimumX = float(minimumX)
            maximumX = float(maximumX)
        except:
            self.showError("Wrong x values, try again please")
            return x, y

        if(maximumX <= minimumX):
            self.showError("Maximum must be greater than minimum")


        try:
            x = np.linspace(minimumX, maximumX, 100)
            y = eval(function)
        except:
            self.showError("Wrong function, try again please")
            return x, y, False

        return x, y

    def draw(self):
        x, y = self.set_app_logic()
        self.axes.clear()
        self.axes.plot(x, y)
        self.canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec_()
