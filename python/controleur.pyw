from controleur_param import *

locale = QLocale.system().name()

def main(args) :
    app = QApplication(args)
    widget = QWidget(None)
    widget.setWindowTitle("Contrôleur v9")
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
    layout.addRow(QLabel("Référence de livrable:"), zone)
    layout.addRow(QLabel("Type de livrable:"),type_lvrb)
    formGroupBox.setLayout(layout)
    
    button = QPushButton("Lancer les contrôles", widget)
    button.resize(120,40)
    button.move(65,120)
    button.clicked.connect(lambda: controle_dpt(widget,dpt,type_lvrb,zone))
    
    widget.show()
    app.exec_()

#Lors du clic sur le bouton de contrôle, on récupère les informations sélectionnées, on paramètre en fonction et on lance les contrôles
def controle_dpt(widget,dpt,type_lrvb,zone):
    #Vérification de la validité des combinaisons de reference et type de livraison
    try:
        if not check_combi_menu(type_lrvb.currentText(),zone.currentText()):
            #raise KeyError("Ce type de livrable est inexistant pour cette référence de livrable")
            return msg_erreur(53,"Ce type de livrable est inexistant pour cette référence de livrable")
    except Exception as e:
        return log(e,53)
    
    #Mise à jour des variables de configuration spécifiques au département, avec les informations sélectionnées
    try:
        update_conf(conf_dpt[dpt.currentText()],type_lrvb.currentText(),zone.currentText())
    except Exception as e:
        return log(e,52)
        
    lancer_controles(widget)

#Met à jour le dictionnaire de configuration dans chaque fichier selon le choix du menu de sélection
def update_conf(conf_dpt,type_lrvb,zone):
    update_conf_param(conf_dpt,type_lrvb,zone)
    update_conf_ctrl(conf_dpt,type_lrvb,zone)
    update_conf_fct(conf_dpt,type_lrvb,zone)
    update_conf_def(conf_dpt,type_lrvb,zone)

if __name__ == "__main__":
    main(sys.argv)
