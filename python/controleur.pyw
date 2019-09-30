from controleur_param import *

locale = QLocale.system().name()

def main(args) :
    app = QApplication(args)
    widget = QWidget(None)
    widget.setWindowTitle("Contrôleur v1")
    widget.resize(250,185)
    widget.setFixedSize(widget.size())
    pal=widget.palette()
    pal.setColor(widget.backgroundRole(), Qt.white)
    widget.setPalette(pal)
    
    formGroupBox = QGroupBox("Paramètres",widget)
    formGroupBox.move(20,0)
    
    dpt = QComboBox()
    for item in dpts:
        dpt.addItem(item)
    
    type_lvrb = QComboBox()
    for item in types_lvrb:
        type_lvrb.addItem(item)
    
    zone = QComboBox()
    for item in zones:
        zone.addItem(item)

    dpt.setCurrentIndex(3)
    type_lvrb.setCurrentIndex(3)
    zone.setCurrentIndex(3)

    comm = QCheckBox()
    comm.setChecked(True)

    layout = QFormLayout()
    layout.addRow(QLabel("Département:"), dpt)
    layout.addRow(QLabel("Référence de livrable:"), zone)
    layout.addRow(QLabel("Type de livrable:"),type_lvrb)
    layout.addRow(QLabel("Commande d'accès:"),comm)
    formGroupBox.setLayout(layout)
    formGroupBox.setEnabled(False)
    
    button = QPushButton("Lancer les contrôles", widget)
    button.resize(120,40)
    button.move(65,124)
    button.clicked.connect(lambda: controle_dpt(widget,dpt,type_lvrb,zone))
    
    widget.show()
    app.exec_()

def extract_livrable(widget,dpt,type_lrvb,zone):
    try:
        manager = Manager()
        return_conf = manager.dict()
        widget.hide()
        
        widget2 = QWidget(None)
        widget2.setWindowTitle("Extraction du livrable...")
        layout = QGridLayout()
        widget2.setLayout(layout)
        label = QLabel("Extraction de l'archive du livrable en cours... Veuillez patienter...")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label,0,0)
        widget2.show()
        
        p1 = Process(target=get_conf_xml, args=(conf_dpt[dpt]["app_path"],xml_livrables_path,type_lrvb,zone,return_conf))
        p1.start()
        p1.join()
        conf=return_conf[0][dpt]
        p1.terminate()
        widget2.hide()
        widget.show()
        return conf
    except Exception as e:
        return log(e,54)    

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
        dpt,type_lrvb,zone=dpt.currentText(),type_lrvb.currentText(),zone.currentText()
        dossiers=glob.glob(os.path.join(conf_dpt[dpt]["livrable_path"],"*/"))
        fzip=glob.glob(os.path.join(conf_dpt[dpt]["livrable_path"],"*.zip"))
        if (dpt,type_lrvb,zone)==("CD21","EXE","Distribution") and not len(dossiers) and len(fzip):
            conf=extract_livrable(widget,dpt,type_lrvb,zone)
        else:
            conf=get_conf_xml(conf_dpt[dpt]["app_path"],xml_livrables_path,type_lrvb,zone)[dpt]
    
        update_conf(conf,type_lrvb,zone)

    except Exception as e:
        return log(e,52)
    
    lancer_controles(widget)
    
#Met à jour le dictionnaire de configuration dans chaque fichier selon le choix du menu de sélection
def update_conf(conf_dpt,type_lrvb,zone):
    update_conf_param(conf_dpt,type_lrvb,zone)
    update_conf_ctrl(conf_dpt,type_lrvb,zone)
    update_conf_ctrl_fct(conf_dpt,type_lrvb,zone)
    update_conf_fct(conf_dpt,type_lrvb,zone)
    update_conf_def(conf_dpt,type_lrvb,zone)

if __name__ == "__main__":
    main(sys.argv)
