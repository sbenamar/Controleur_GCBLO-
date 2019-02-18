from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import os,sys
from PyQt5.QtCore import QFileInfo
from qgis.core import *
from importlib import reload

init=False

#QgsApplication.setPrefixPath(qgis_prefix_path,True)
qgs = QgsApplication([], False)
qgs.initQgis()

try:
    from controles import *
except Exception as e:
    log(e,41)

#warning d'un module pour une bibliothèque bientôt obsolète
warnings.simplefilter("ignore")

rapport=""

#Ce dictionnaire liste les identifiants de contrôle avec l'autorisation ou non de les lancer
#Ce dictionnaire sera généré depuis un fichier Excel, selon si une case est cochée ou non
list_controle_exe={
    1:True,
    2:False,
    3:False,
    4:True,
    5:False,
    6:True,
    7:True,
    8:True,
    9:True,
    10:True,
    11:True,
    12:True,
    13:True,
    15:True,
    16:True,
    17:True,
    18:True,
    19:True,
    20:True,
    21:True,
    22:True,
    23:True,
    24:True
}

def update_conf_param(config):
    exec("global conf,libelle_rapport_csv;conf=config;libelle_rapport_csv=set_libelle_rapport_csv()")

def lancer_controles(widget):  
    pbar = QProgressBar(widget)
    pbar.setMinimum(0)
    pbar.setMaximum(100)
    pbar.setAlignment(Qt.AlignHCenter)
    pbar.move(66,104)
    pbar.show()
    
    #list_controle_exe=get_liste_controle_dpt(conf["dpt"])
    
    #Création du rapport, initialisé avec l'entête
    alim_rapport_csv()
    
    #Chaque contrôle est lancé à la suite, avec une gestion des exception pour chacun
    #list_controle_exe est passé en paramètre avec l'identifiant de contrôle correspondant
    #Le contrôle sera lancé si pour cet identifiant la valeur est True, sinon ignoré
    try:
        res=version_c3a(list_controle_exe[1])
        #if res:
            #pbar.setValue(100)
            #msg_succes()
            #return
        
        pbar.setValue(float(1)/len(list_controle_exe)*100)
    except Exception as e:
        return log(e,42)
    
    try:
        corresp_cable_infra_c3a(list_controle_exe[2],list_controle_exe[3])
        pbar.setValue(float(3)/len(list_controle_exe)*100)
    except Exception as e:
        return log(e,43)
    
    try:
        corresp_poteau_c3a(list_controle_exe[4])
        pbar.setValue(float(4)/len(list_controle_exe)*100)
    except Exception as e:
        return log(e,44)
    
    try:
        verif_point_technique_c3a(list_controle_exe[5])
        pbar.setValue(float(5)/len(list_controle_exe)*100)
    except Exception as e:
        return log(e,410)
    
    try:
        info_sous_tubage(list_controle_exe[6])
        pbar.setValue(float(6)/len(list_controle_exe)*100)
    except Exception as e:
        return log(e,45)
    
    try:
        regles_gcblo_c3a_majeurs(
            list_controle_exe[7],
            list_controle_exe[8],
            list_controle_exe[12]
        )
        pbar.setValue(float(7)/len(list_controle_exe)*100)
    except Exception as e:
        return log(e,46)
    
    try:
        verif_liste_colonnes(list_controle_exe[9])
        pbar.setValue(float(9)/len(list_controle_exe)*100)
    except Exception as e:
        return log(e,47)
    
    try:
        verif_c7_travaux_existe(list_controle_exe[10],list_controle_exe[11])
        pbar.setValue(float(10)/len(list_controle_exe)*100)
    except Exception as e:
        return log(e,48)
        
    try:
        #Pour les contrôles 13,15,16,...24
        valeurs_selon_liaisons({k: v for k, v in list_controle_exe.items() if 13 <= k <= 25 and k != 14})
        pbar.setValue(100)
    except Exception as e:
        return log(e,49)
    
    msg_succes()