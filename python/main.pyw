import os,sys
from controleur import lancer_controles

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
locale = QLocale.system().name()

def main(args) :
    app = QApplication(args)
    widget = QWidget(None)
    widget.setWindowTitle("Contrôleur v3")
    widget.resize(250,150)
    button = QPushButton("Lancer les contrôles", widget)
    button.resize(120,60)
    button.move(60,45)
    button.clicked.connect(lambda: lancer_controles(widget))
    widget.show()
    app.exec_()
if __name__ == "__main__":
    main(sys.argv)