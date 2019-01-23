import qgis.utils,warnings,os,sys,traceback
from qgis.core import *
from qgis.core import QgsProject,QgsVectorLayer
from PyQt5.QtCore import QFileInfo
from datetime import datetime

try:
    chemin_courant=os.getcwd()
    log_path=os.path.join(*[chemin_courant,"python","log"])
    nom_log="log.txt"
    
    def log(err,code=0):
        exc_type, exc_obj, exc_tb = sys.exc_info()
        with open(os.path.join(log_path,nom_log), "a") as f:
            f.write(
                "{}: [ligne {} / code {} / erreur {}] - {}\n{}\n\n".format(
                str(datetime.now()),
                str(exc_tb.tb_lineno),
                str(code),
                str(exc_type),
                str(exc_obj),
                traceback.format_exc()
            ))

        print("Une erreur est survenue (code: "+str(code)+")")
        exit(code)
except Exception as e:
    print ("Erreur lors de l'initialisation (code 1)")
    exit(11)

try:
    qgis_installation_path=r"C:\Program Files\QGIS 3.4"
    chemin_exe=os.path.join(chemin_courant,"exe")
    exe_projet_racine=os.path.join(chemin_exe,"04 - Projet")
    
    try:
        nom_projet=os.listdir(exe_projet_racine)[0]
    except Exception as e:
        print("Un exe est nécessaire pour lancer les contrôles.")
        log(e,12)
        
    exe_projet=os.path.join(exe_projet_racine,nom_projet)
    commande_orange_path=os.path.join(chemin_exe,"11 - Commande_Orange")
    exe_projet_carto=os.path.join(exe_projet,"APD"+nom_projet+".qgs")
    chemin_layers=os.path.join(exe_projet,exe_projet,"LAYERS")
    layer_prises = os.path.join(chemin_layers+"PRISES.shp")
    cable_infra_csv_path=os.path.join(chemin_layers,"CABLE_INFRA.csv")
    appui_orange_path=os.path.join(chemin_exe,"09 - Appui Orange - CAPFT")
        
    ind_premiere_ligne_c3a=31-1
    type_imp=["CONDUITE FT","AERIEN FT"]
    version_c3a_en_cours='C3A BLO5'
    combinaisons_types=["CTCT","CCT","CTC","CTP","CTA","ACT","PCT"]
    
    chemin_rapport=os.path.join(chemin_courant,"rapports")
    prefixe_resultat_controle2_2="rapport_verif_c3a_cable_infra"
    prefixe_resultat_controle2_1="rapport_verif_cable_infra_c3a"
    prefixe_resultat_controle3="rapport_verif_c3a_poteaux"
    prefixe_resultat_controle4_1="rapport_verif_norme_numero"
    prefixe_resultat_controle4_2="rapport_verif_longueur_troncon"
    prefixe_resultat_controle4_3="rapport_verif_combinaison_types"
    nom_rapport="rapport.txt"
    
    msg_erreur=""
    msg=""
    rapport=""
except Exception as e:
    log(e,13)
