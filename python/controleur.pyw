from controleur_param import *

locale = QLocale.system().name()

def main(args) :
    app = QApplication(args)
    widget = QWidget(None)
    widget.setWindowTitle("Contrôleur v5")
    widget.resize(250,185)
    widget.setFixedSize(widget.size())
    pal=widget.palette()
    pal.setColor(widget.backgroundRole(), Qt.white)
    widget.setPalette(pal)
    
    formGroupBox = QGroupBox("Paramètres",widget)
    formGroupBox.move(20,5)
    
    dpt = QComboBox()
    for item in dpts:
        dpt.addItem(item)
    
    type_lvrb = QComboBox()
    for item in types_lvrb:
        type_lvrb.addItem(item)
    
    zone = QComboBox()
    for item in zones:
        zone.addItem(item)
        
    layout = QFormLayout()
    layout.addRow(QLabel("Département:"), dpt)
    layout.addRow(QLabel("Type de livrable:"),type_lvrb)
    layout.addRow(QLabel("Référence de livrable:"), zone)
    formGroupBox.setLayout(layout)
    
    button = QPushButton("Lancer les contrôles", widget)
    button.resize(120,40)
    button.move(65,120)
    button.clicked.connect(lambda: controle_dpt(widget,dpt,type_lvrb,zone))
    
    widget.show()
    app.exec_()

def controle_dpt(widget,dpt,type_lrvb,zone):
    try:
        update_conf(conf_dpt[dpt.currentText()],type_lrvb.currentText(),zone.currentText())
    except Exception as e:
        return log(e,52)
        
    lancer_controles(widget)

def update_conf(conf_dpt,type_lrvb,zone):
    update_conf_param(conf_dpt,type_lrvb,zone)
    update_conf_ctrl(conf_dpt,type_lrvb,zone)
    update_conf_fct(conf_dpt,type_lrvb,zone)
    update_conf_def(conf_dpt,type_lrvb,zone)

if __name__ == "__main__":
    main(sys.argv)
