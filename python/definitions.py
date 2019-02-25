import os,sys
import warnings,os,sys,traceback,csv,glob
from datetime import datetime
from functools import reduce
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from qgis.core import *

#chemin_courant permettra de servir de base pour la création des autres chemins
chemin_courant=os.getcwd()

prefixe_rapport_csv="rapport_erreurs"
libelle_rapport_csv=prefixe_rapport_csv+'.csv'
chemin_rapport=os.path.join(chemin_courant,"rapports")
chemin_doc_controleur=os.path.join(chemin_courant,*["Documentation","controleur.xlsx"])

conf={}
conf_dpt={}

update_conf_exec="global conf,libelle_rapport_csv;conf=config;libelle_rapport_csv=set_libelle_rapport_csv()"

def msg_erreur(code):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setText("Une erreur est survenue")
    msg.setWindowTitle("Erreur")
    msg.setDetailedText("Code d'erreur: {}".format(str(code)))
    msg.setStandardButtons(QMessageBox.Close)
    msg.exec_()

def msg_succes():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText("Tous les contrôles ont été effectués.")
    msg.setWindowTitle("Contrôles terminés")
    msg.setDetailedText('Le rapport des contrôles a été généré dans le dossier "rapports"')
    msg.setStandardButtons(QMessageBox.Close)
    msg.exec_()

#Gestion de l'exception lors de la création de la fonction de log, qui permettra de généraliser
##la gestion des erreurs
try:
    #chemin_courant permettra de servir de base pour la création des autres chemins
    chemin_courant=os.getcwd()
    
    #Préparation des variables utilisées par la fonction log dont un format d'affichage
    log_path=os.path.join(*[chemin_courant,"python","log"])
    nom_log="log"
    format_log="{}: [ligne {} / code {} / erreur {}] - {}\n{}\n\n"

    #Lors d'une exception, permet d'afficher le message d'erreur dans le fichier log.txt.
    #Le message d'erreur initial est affiche, avec une entête permettant d'avoir une vue rapide.
    #Un code est inclus, permettant de rapidement identifier la source de l'erreur.
    def log(err,code=0):
        exc_type, exc_obj, exc_tb = sys.exc_info()
        with open(os.path.join(log_path,nom_log), "a") as f:
            f.write(
                format_log.format(
                str(datetime.now()),
                str(exc_tb.tb_lineno),
                str(code),
                str(exc_type),
                str(exc_obj),
                traceback.format_exc()
            ))
        try:
            msg_erreur(code)
        except Exception as e:
            print("Une erreur est survenue (code: {})".format(str(code)))
    
except Exception as e:
    print("Une erreur est survenue (code: 1)")


chemin_exe=os.path.join(chemin_courant,"exe")
exe_projet_racine=os.path.join(chemin_exe,"04 - Projet")

#Avant de récupérer le chemin du projet de l'exe, vérifier que l'exe est présent
try:
    nom_projet=os.listdir(exe_projet_racine)[0]
except:
    nom_projet=""
    
exe_projet=os.path.join(exe_projet_racine,nom_projet)
commande_orange_path=os.path.join(chemin_exe,"09 - Commande_Orange")
chemin_layers=os.path.join(exe_projet,"LAYERS")
cable_infra_csv_path=os.path.join(chemin_layers,"CABLE_INFRA.csv")
point_technique_path=os.path.join(chemin_layers,"POINT_TECHNIQUE.shp")
appui_orange_path=os.path.join(chemin_exe,"07 - Appui","Appui Orange - CAPFT","POTEAU")
arbo_c3a="**/**/*C3A*.xls*"
format_arbo_c7="*{}*C7*.xls*"
chemin_c3a=os.path.join(commande_orange_path,arbo_c3a)
format_chemin_c7=os.path.join(commande_orange_path,format_arbo_c7)

conf_dpt["EXE"]={
    "dpt":"EXE",
    "chemin_exe":chemin_exe,
    "exe_projet_racine":exe_projet_racine,
    "nom_projet":nom_projet,
    "exe_projet":exe_projet,
    "commande_orange_path":commande_orange_path,
    "chemin_layers":chemin_layers,
    "cable_infra_csv_path":cable_infra_csv_path,
    "point_technique_path":point_technique_path,
    "appui_orange_path":appui_orange_path,
    "arbo_c3a":arbo_c3a,
    "format_arbo_c7":format_arbo_c7,
    "chemin_c3a":chemin_c3a,
    "format_chemin_c7":format_chemin_c7
}

chemin_exe=os.path.join(chemin_courant,"Commande")
commande_orange_path=chemin_exe
cable_infra_csv_path=os.path.join(chemin_exe,"CABLE_INFRA.csv")
appui_orange_path=os.path.join(chemin_exe,"Appui aérien")
arbo_c3a="*C3A*.xls*"
format_arbo_c7="*{}*C7*.xls*"
chemin_c3a=os.path.join(commande_orange_path,arbo_c3a)
format_chemin_c7=os.path.join(commande_orange_path,format_arbo_c7)

conf_dpt["testv1"]={
    "dpt":"testv1",
    "chemin_exe":chemin_exe,
    "commande_orange_path":commande_orange_path,
    "cable_infra_csv_path":cable_infra_csv_path,
    "appui_orange_path":appui_orange_path,
    "arbo_c3a":arbo_c3a,
    "format_arbo_c7":format_arbo_c7,
    "chemin_c3a":chemin_c3a,
    "format_chemin_c7":format_chemin_c7
}

chemin_exe=os.path.join(chemin_courant,"Commande")
commande_orange_path=chemin_exe
cable_infra_csv_path=os.path.join(chemin_exe,"CABLE_INFRA.csv")
appui_orange_path=os.path.join(chemin_exe,"Appui aérien")
arbo_c3a="*C3A*.xls*"
format_arbo_c7="*{}*C7*.xls*"
chemin_c3a=os.path.join(commande_orange_path,arbo_c3a)
format_chemin_c7=os.path.join(commande_orange_path,format_arbo_c7)
point_technique_path=os.path.join(chemin_exe,"POINT_TECHNIQUE.shp")

conf_dpt["testv2"]={
    "dpt":"testv2",
    "chemin_exe":chemin_exe,
    "commande_orange_path":commande_orange_path,
    "cable_infra_csv_path":cable_infra_csv_path,
    "appui_orange_path":appui_orange_path,
    "arbo_c3a":arbo_c3a,
    "format_arbo_c7":format_arbo_c7,
    "chemin_c3a":chemin_c3a,
    "format_chemin_c7":format_chemin_c7,
    "point_technique_path":point_technique_path
}

#if "testv2" in environnement:
#chemin_exe=os.path.join(chemin_courant,"Commande d'accès")
#commande_orange_path=chemin_exe
#cable_infra_csv_path=os.path.join(chemin_exe,"CABLE_INFRA.csv")
#appui_orange_path=os.path.join(chemin_exe,"Appui aérien")
#chemin_rapport=os.path.join(chemin_courant,"rapports")
#arbo_c3a="*C3A*.xls*"
#format_arbo_c7="*{}*C7*.xls*"
#chemin_c3a=os.path.join(commande_orange_path,arbo_c3a)
#format_chemin_c7=os.path.join(commande_orange_path,format_arbo_c7)
#exe_projet=r"C:\Users\PTPC9452\Documents\EXE test\04 - Projet\SRO21024SEM_1_Projet"
    
try:
    dpts = ("CD21","CD39","CD58","CD70","CD71","testv1","testv2","EXE")
    col_dpt={
        "CD21":10,
        "CD39":12,
        "CD58":14,
        "CD70":16,
        "CD71":16,
        "testv1":10,
        "testv2":10,
        "EXE":10
    }
    
    qgis_prefix_path=r".\lib\qgis"
    
    ind_premiere_ligne_c3a=12-1
    ind_premiere_ligne_c7=20-1
    type_imp=["CONDUITE FT","AERIEN FT"]
    version_c3a_en_cours='C3A BLO5'
    combinaisons_types=["CTCT","CCT","CTC","CTP","CTA","ACT","PCT"]
    
    msg_fin_programme_1="Programme terminé"
    
    erreur_format_controle1="Mauvaise version de la C3A"
    erreur_format_controle2="Liaison {} manquant dans la C3A"
    erreur_format_controle3="Tronçon {}-{} présent dans la C3A mais absent de QGIS"
    erreur_format_controle4="Fiche poteaux {} manquante"
    erreur_format_controle7="Format de nommage incorrect"
    erreur_format_controle8=""
    erreur_format_controle12="Combinaison interdite"
    
    erreur_controle1="Mauvaise version de la C3A"
    erreur_controle2="Liaison manquante dans la C3A"
    erreur_controle3="Tronçon présent dans la C3A mais absent de QGIS"
    erreur_controle4="Fiche poteaux manquante"
    erreur_controle5="Incohérence du type de point technique entre la C3A et QGIS"
    erreur_controle6="Information de sous tubage incomplète pour le tronçon. La colonne I doit être renseigné"
    erreur_controle7="Format de nommage incorrect"
    erreur_controle8="Longueur de tronçon / portée incorrect"
    erreur_controle9="Les valeurs ne respectent pas les listes déroulantes"
    erreur_controle10="Fichier C7 manquant"
    erreur_controle11="Appui manquant dans la C7"
    erreur_controle12="Combinaison interdite"
    erreur_controle13="Information de diamètre de l'alvéole mal renseigné"
    erreur_controle14="La colonne F doit être vide"
    erreur_controle15='La colonne H doit contenir la valeur "adduction"'
    erreur_controle16="La colonne F doit être vide"
    erreur_controle17='La colonne G doit contenir la valeur "7"'
    erreur_controle18="La colonne F doit être vide"
    erreur_controle19='La colonne H doit contenir la valeur "transition"'
    erreur_controle20='La colonne G doit contenir la valeur "7"'
    erreur_controle21='La colonne H doit contenir la valeur "transition"'
    erreur_controle22='La colonne F doit être vide'
    erreur_controle23='Les colonne B et D doivent être vide'
    erreur_controle24='La colonne H doit contenir la valeur "transition"'
    
    criticite={
        "mineure":"Mineure",
        "majeure":"Majeure",
        "bloquant":"Bloquant"
    }
    
    entete_rapport_csv = [
        "Numéro de contrôle",
        "Famille",
        "Sous-famille",
        "Source A",
        "Source B",
        "Champ concerné",
        "Erreur générée",
        "Criticité"
    ]
    
    pre_entete_1= ["Commande d'accès","Version"]
    pre_entete_2= ["Commande d'accès","Complétude"]
    pre_entete_3= ["Commande d'accès","Règle GCBLO"]
    pre_entete_4= ["Commande d'accès","Cohérence"]
    
    pre_entete_lien={
        1:pre_entete_1,
        2:pre_entete_2,
        3:pre_entete_2,
        4:pre_entete_3,
        5:pre_entete_4,
        6:pre_entete_3,
        7:pre_entete_3,
        8:pre_entete_3,
        9:pre_entete_3,
        10:pre_entete_3,
        11:pre_entete_3,
        12:pre_entete_3,
        13:pre_entete_3,
        14:pre_entete_3,
        15:pre_entete_3,
        16:pre_entete_3,
        17:pre_entete_3,
        18:pre_entete_3,
        19:pre_entete_3,
        20:pre_entete_3,
        21:pre_entete_3,
        22:pre_entete_3,
        23:pre_entete_3,
        24:pre_entete_3,
        25:pre_entete_3
    }
    
    post_entete_controle1=[erreur_controle1,criticite['bloquant']]
    post_entete_controle2=[erreur_controle2,criticite['bloquant']]
    post_entete_controle3=[erreur_controle3,criticite['majeure']]
    post_entete_controle4=[erreur_controle4,criticite['bloquant']]
    post_entete_controle5=[erreur_controle5,criticite['majeure']]
    post_entete_controle6=[erreur_controle6,criticite['mineure']]
    post_entete_controle7=[erreur_controle7,criticite['majeure']]
    post_entete_controle8=[erreur_controle8,criticite['majeure']]
    post_entete_controle9=[erreur_controle9,criticite['mineure']]
    post_entete_controle10=[erreur_controle10,criticite['majeure']]
    post_entete_controle11=[erreur_controle11,criticite['majeure']]
    post_entete_controle12=[erreur_controle12,criticite['majeure']]
    post_entete_controle13=[erreur_controle13,criticite['mineure']]
    post_entete_controle14=[erreur_controle14,criticite['mineure']]
    post_entete_controle15=[erreur_controle15,criticite['mineure']]
    post_entete_controle16=[erreur_controle16,criticite['mineure']]
    post_entete_controle17=[erreur_controle17,criticite['mineure']]
    post_entete_controle18=[erreur_controle18,criticite['mineure']]
    post_entete_controle19=[erreur_controle19,criticite['mineure']]
    post_entete_controle20=[erreur_controle20,criticite['mineure']]
    post_entete_controle21=[erreur_controle21,criticite['mineure']]
    post_entete_controle22=[erreur_controle22,criticite['mineure']]
    post_entete_controle23=[erreur_controle23,criticite['mineure']]
    post_entete_controle24=[erreur_controle24,criticite['mineure']]
    
    lib_nb_erreurs="Nombre d'erreurs"
    c3a_list_libelle="Ensemble des C3A"
    c7_list_libelle="Ensemble des C7"
    poteau_list_libelle="Ensemble des fiches poteaux"
    cable_infra_list_libelle="Ensemble des cables infra"
    lib_a="A"
    lib_b="B"
    msg_erreur=""
    msg=""
    rapport=""
    
    combinaison_type="{} - {}"
    num_ligne="Ligne {}"
    troncon_format="{} - {}"
    
    type_chambre_appui=["C","A","P","IMB","F","CT","AT","PT"]
    diametre_alveole_liste=["28","32","45","60","80","100","150",
                            "Sous-tubage existant","caniveau","galerie","transition","adduction","aérien"
                            ]
    diametre_alveole_liste_c_c=["28","32","45","60","80","100","150",
                                "Sous-tubage existant","caniveau","galerie"
                                ]
    tubage_rigide_liste=["Oui"]
    diametre_tube_liste=["6/8mm","8/10mm","11/14mm","13/16mm","15/18mm","16/20mm","21/25mm","27/32mm"]
    diametre_cable_liste=[nb/2 for nb in range(0,43)]
    travaux_liste=["oui percement grand pied droit","oui percement petit pied droit",
            "oui percement avec plus de 4 alvéoles","oui remplacement appui",
            "oui renforcement appui sans commande d'appui",
            "oui renforcement appui avec commande d'appui",
            "oui transition égout petit pied droit",
            "oui transition égout grand pied droit"]
    
    installation_liste=["A Manchon > 2dm3",
                "A Micro Manchon < 2dm3",
                "B Manchon > 2dm3",
                "B Micro Manchon < 2dm3",
                "A PEO",
                "B PEO",
                "A PMSB",
                "B PMSB",
                "A PB Chambre",
                "B PB Chambre",
                "A PB Appui",
                "B PB Appui"
                ]
    
    refus_res_liste=["X"]
    
    condition_travaux_c7=["oui remplacement appui","oui renforcement appui avec commande d'appui"]
    
    prop_orange='ORANGE'
    proprietaire_point_liste=['AUTRE', 'CLIENT', 'ENEDIS', prop_orange]
    type_point_liste=['APPUI', 'CHAMBRE', 'POTELET']
    
    corr_point_lib_code={
        'APPUI':'A',
        'CHAMBRE':'C',
        'POTELET':'P',
        'IMMEUBLRE':'IMB',
        'FACADE':'F',
        'ND':'ND'
    }
    
    point_tiers_liste=['APPUI','CHAMBRE','POTELET']
    
    liaison_c_c="C - C"
    liaison_c_imb="C - IMB"
    liaison_c_f="C - F"
    liaison_c_p="C - P"
    laison_c_pt="C - PT"
    laison_ct_p="CT - P"
        
except Exception as e:
    log(e,11)

def set_libelle_rapport_csv():
    return prefixe_rapport_csv+'_'+str(datetime.now()).split('.')[0].replace(' ','_').replace(':','-')+'.csv'

def update_conf_def(config):
    exec("global conf,libelle_rapport_csv;conf=config;libelle_rapport_csv=set_libelle_rapport_csv()")