import os,sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from controleur_param import *

locale = QLocale.system().name()

def main(args) :
    app = QApplication(args)
    widget = QWidget(None)
    widget.setWindowTitle("Contrôleur v4")
    widget.resize(250,150)
    button = QPushButton("Lancer les contrôles", widget)
    button.resize(120,60)
    button.move(60,45)
    widget.setFixedSize(widget.size())
    button.clicked.connect(lambda: test(widget))
    widget.show()
    app.exec_()

def test(widget):
    dpt, ok = QInputDialog.getItem(widget,"Sélection du département", "Liste des départements", dpts, 0, False)
    
    if not(ok and dpt):
        return log(None,411)

    dpt="testv1"
    
    try:
        update_conf(conf_dpt[dpt])
    except Exception as e:
        return log(e,412)
        
    lancer_controles(widget)

def update_conf(conf_dpt):
    update_conf_param(conf_dpt)
    update_conf_ctrl(conf_dpt)
    update_conf_fct(conf_dpt)
    update_conf_def(conf_dpt)

if __name__ == "__main__":
    main(sys.argv)
