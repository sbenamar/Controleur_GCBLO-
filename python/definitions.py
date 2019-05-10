import warnings,os,sys,traceback,csv,glob,re
from InternalException import InternalException
from conf_xml import *
from datetime import datetime
from functools import reduce
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from qgis.core import *

#chemin_courant permettra de servir de base pour la création des autres chemins
chemin_courant=os.getcwd()

if "python" in chemin_courant:
    qgis_prefix_path=os.path.join(chemin_courant,*["lib","qgis"])
    xml_livrables_path=os.path.join("conf","livrables.xml")
else:
    qgis_prefix_path=os.path.join(chemin_courant,*["python","lib","qgis"])
    xml_livrables_path="python/conf/livrables.xml"
                                  
prefixe_rapport_csv="rapport_erreurs"
libelle_rapport_csv=prefixe_rapport_csv+'.csv'
chemin_rapport=os.path.join(chemin_courant,"rapports")
chemin_doc_controleur=os.path.join(chemin_courant,*["Documentation","controleur.xlsx"])

#Variable contenant les configurations (chemin, libelle,etc...) à utiliser
conf={}
#Variable contenant ces configurations par département. conf prendra la valeur d'un conf_dpt lorsqu'on change de département
conf_dpt={}

conf_dpt=get_conf_xml(chemin_courant,xml_livrables_path)

#conf_dpt["CD21"]=conf_dpt["CDXX"].copy()
#conf_dpt["CD21"]["dpt"]="CD21"

format_arbo_c7="*{}*C7*.xls*"
arbo_c7="*C7*.xls*"
arbo_c3a="*C3A*.xls*"

#Fenêtre de message d'erreur avec un code d'identification
#Possibilité d'intégrer un message spécifique en renseignant le message
def msg_erreur(code,message=False):
    QApplication(args)
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setText("Une erreur est survenue")
    msg.setWindowTitle("Erreur")
    if not message:
        msg.setDetailedText("Code d'erreur: {}".format(str(code)))
    else:
        msg.setDetailedText(str(message))
    msg.setStandardButtons(QMessageBox.Close)
    msg.exec_()

#Gestion de l'exception lors de la création de la fonction de log, qui permettra de généraliser
##la gestion des erreurs
try:
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

liste_couches=["point_technique","prises","sro","infra","boitier","racco_client","cable","zpbo","zsro","zpec","znro","nro","route","bati","cadastre","commune"]

try:
    dpts = ("CD21","CD39","CD58","CD70","CD71")
    col_dpt={
        "CD21":10,
        "CD39":12,
        "CD58":14,
        "CD70":16,
        "CD71":16,
        "testv1":10,
        "testv2":10,
        "CDXX":10
    }
    
    types_lvrb = ("AVP","RBAL","PRO","EXE")
    
    nro_lib="NRO"
    transport_lib="Transport"
    sro_lib="SRO"
    distribution_lib="Distribution"
    
    zones = (nro_lib,transport_lib,sro_lib,distribution_lib)
    
    col_param={
        nro_lib:{
            "AVP":3,
            "PRO":4,
            "EXE":5
        },
        transport_lib:{
            "PRO":6,
            "EXE":7
        },
        sro_lib:{
            "PRO":8,
            "EXE":9
        },
        distribution_lib:{
            "RBAL":10,
            "PRO":11,
            "EXE":12
        }
    }
    
    param_format="{} {}"
    
    param_distri_pro=param_format.format(distribution_lib,"PRO")
    param_distri_exe=param_format.format(distribution_lib,"EXE")
    param_distri_rbal=param_format.format(distribution_lib,"RBAL")
    param_transport_exe=param_format.format(transport_lib,"EXE")
    
    champs_point_technique={
        'pt_code':[param_distri_exe,param_distri_pro,param_distri_rbal,param_transport_exe],
        'pt_codeext':[param_distri_exe,param_distri_pro,param_distri_rbal,param_transport_exe],
        'pt_etiquet':[param_distri_exe,param_distri_pro,param_distri_rbal,param_transport_exe],
        'pt_nd_code':[param_distri_exe,param_distri_pro,param_distri_rbal,param_transport_exe],
        'pt_prop':[param_distri_exe,param_distri_pro,param_distri_rbal,param_transport_exe],
        'pt_gest':[param_distri_exe,param_distri_pro,param_distri_rbal,param_transport_exe],
        'ETAT':[param_distri_exe,param_distri_rbal,param_transport_exe],
        'pt_avct':[param_distri_exe,param_distri_pro,param_distri_rbal,param_transport_exe],
        'pt_typephy':[param_distri_exe,param_distri_pro,param_distri_rbal,param_transport_exe],
        'pt_nature':[param_distri_exe,param_distri_pro,param_distri_rbal,param_transport_exe],
        'pt_secu':[param_distri_exe,param_distri_pro,param_distri_rbal,param_transport_exe],
        'nd_voie':[param_distri_exe,param_distri_pro,param_distri_rbal,param_transport_exe],
        'pt_statut':[param_distri_exe,param_distri_pro,param_distri_rbal,param_transport_exe],
        'nd_r1_code':[param_distri_exe,param_distri_pro,param_distri_rbal,param_transport_exe],
        'nd_r2_code':[param_distri_exe,param_distri_pro,param_distri_rbal,param_transport_exe],
        'nd_r3_code':[param_distri_exe,param_distri_pro,param_distri_rbal,param_transport_exe],
        'nd_r4_code':[param_distri_exe,param_distri_pro,param_distri_rbal,param_transport_exe],
        'pt_creadat':[param_distri_exe,param_distri_pro,param_distri_rbal,param_transport_exe]
    }
    
    champs_prises = {
        'ad_code':[param_distri_exe,param_distri_pro,param_distri_rbal],
        'nom_sro':[param_distri_exe,param_distri_pro,param_distri_rbal],
        'ad_numero':[param_distri_exe,param_distri_pro,param_distri_rbal],
        'ad_rep':[param_distri_exe,param_distri_pro,param_distri_rbal],
        'ad_nomvoie':[param_distri_exe,param_distri_pro,param_distri_rbal],
        'ad_insee':[param_distri_exe,param_distri_pro,param_distri_rbal],
        'ad_postal':[param_distri_exe,param_distri_pro,param_distri_rbal],
        'ad_commune':[param_distri_exe,param_distri_pro,param_distri_rbal],
        'ad_nom_ld':[param_distri_exe,param_distri_pro,param_distri_rbal],
        'ad_idpar':[param_distri_exe,param_distri_pro,param_distri_rbal],
        'ad_nombat':[param_distri_exe,param_distri_pro,param_distri_rbal],
        'ad_nbprhab':[param_distri_exe,param_distri_pro,param_distri_rbal],
        'ad_nbprpro':[param_distri_exe,param_distri_pro,param_distri_rbal],
        'nb_prises':[param_distri_exe,param_distri_pro,param_distri_rbal],
        'ad_distinf':[param_distri_exe,param_distri_pro,param_distri_rbal],
        'LGR_CARTO':[param_distri_exe,param_distri_pro,param_distri_rbal],
        'Racco_long':[param_distri_exe,param_distri_pro,param_distri_rbal],
        'ad_racc':[param_distri_exe,param_distri_pro,param_distri_rbal],
        'ad_ietat':[param_distri_exe,param_distri_pro,param_distri_rbal],
        'ad_itypeim':[param_distri_exe,param_distri_pro,param_distri_rbal],
        'Nom_Pro':[param_distri_exe,param_distri_pro,param_distri_rbal],
        'bp_code':[param_distri_exe,param_distri_pro,param_distri_rbal],
        'ad_creadat':[param_distri_exe,param_distri_pro,param_distri_rbal],
        'Statut':[param_distri_exe,param_distri_pro,param_distri_rbal]
    }
    
    champs_sro = {
        'ST_CODE':[param_distri_exe,param_distri_pro,param_transport_exe],
        'ST_ND_CODE':[param_distri_exe,param_distri_pro,param_transport_exe],
        'LT_CODE':[param_distri_exe,param_distri_pro,param_transport_exe],
        'LT_CODEEXT':[param_distri_exe,param_distri_pro,param_transport_exe],
        'ba_code_t':[param_distri_exe,param_distri_pro,param_transport_exe],
        'ba_code_d':[param_distri_exe,param_distri_pro,param_transport_exe],
        'ST_PROP':[param_distri_exe,param_distri_pro,param_transport_exe],
        'ST_GEST':[param_distri_exe,param_distri_pro,param_transport_exe],
        'ND_R1_CODE':[param_distri_exe,param_distri_pro,param_transport_exe],
        'ND_R2_CODE':[param_distri_exe,param_distri_pro,param_transport_exe],
        'ND_R3_CODE':[param_distri_exe,param_distri_pro,param_transport_exe],
        'ND_VOIE':[param_distri_exe,param_distri_pro,param_transport_exe],
        'ST_STATUT':[param_distri_exe,param_distri_pro,param_transport_exe],
        'ST_AVCT':[param_distri_exe,param_distri_pro,param_transport_exe],
        'ST_TYPEPHY':[param_distri_exe,param_distri_pro,param_transport_exe],
        'ST_TYPELOG':[param_distri_exe,param_distri_pro,param_transport_exe],
        'ba_type':[param_distri_exe,param_distri_pro,param_transport_exe],
        'TYPE':[param_distri_exe,param_distri_pro,param_transport_exe],
        'PRISES':[param_distri_exe,param_distri_pro,param_transport_exe],
        'RAL':[param_distri_exe,param_distri_pro,param_transport_exe],
        'revetement':[param_distri_exe,param_distri_pro,param_transport_exe],
        'POB_FTTE_T':[param_distri_exe,param_distri_pro,param_transport_exe],
        'POB_FTTH_T':[param_distri_exe,param_distri_pro,param_transport_exe],
        'POB_FTTE_D':[param_distri_exe,param_distri_pro,param_transport_exe],
        'MEB':[param_distri_exe,param_distri_pro,param_transport_exe],
        'POS':[param_distri_exe,param_distri_pro,param_transport_exe],
        'ST_CREADAT':[param_distri_exe,param_distri_pro,param_transport_exe]
    }
    
    champs_boitier = {
        'bp_code':[param_distri_exe,param_distri_pro,param_transport_exe],
        'bp_etiquet':[param_distri_exe,param_distri_pro,param_transport_exe],
        'bp_codeext':[param_distri_exe,param_distri_pro,param_transport_exe],
        'NB_PRISES':[param_distri_exe,param_distri_pro,param_transport_exe],
        'bp_pt_code':[param_distri_exe,param_distri_pro,param_transport_exe],
        'bp_statut':[param_distri_exe,param_distri_pro,param_transport_exe],
        'bp_avct':[param_distri_exe,param_distri_pro,param_transport_exe],
        'bp_typephy':[param_distri_exe,param_distri_pro,param_transport_exe],
        'bp_typelog':[param_distri_exe,param_distri_pro,param_transport_exe],
        'bp_creadat':[param_distri_exe,param_distri_pro,param_transport_exe]
    }
    
    champs_infra = {
        'PROPRIETAI':[param_distri_exe,param_distri_pro,param_transport_exe],
        'nb_conduite':[param_distri_exe,param_distri_pro,param_transport_exe],
        'cm_code':[param_distri_exe,param_distri_pro,param_transport_exe],
        'cm_ndcode1':[param_distri_exe,param_distri_pro,param_transport_exe],
        'cm_ndcode2':[param_distri_exe,param_distri_pro,param_transport_exe],
        'cm_typ_imp':[param_distri_exe,param_distri_pro,param_transport_exe],
        'cm_typelog':[param_distri_exe,param_distri_pro,param_transport_exe],
        'cm_long':[param_distri_exe,param_distri_pro,param_transport_exe],
        'Etat':[param_distri_exe,param_distri_pro,param_transport_exe],
        'cm_statut':[param_distri_exe,param_distri_pro,param_transport_exe],
        'cm_avct':[param_distri_exe,param_distri_pro,param_transport_exe],
        'cm_r1_code':[param_distri_exe,param_distri_pro,param_transport_exe],
        'cm_r2_code':[param_distri_exe,param_distri_pro,param_transport_exe],
        'cm_r3_code':[param_distri_exe,param_distri_pro,param_transport_exe],
        'cm_r4_code':[param_distri_exe,param_distri_pro,param_transport_exe],
        'coupe_type':[param_distri_exe,param_distri_pro,param_transport_exe],
        'cm_creadat':[param_distri_exe,param_distri_pro,param_transport_exe]
    }
    
    champs_racco_client = {
        'AD_code':[param_distri_exe,param_distri_pro,param_distri_rbal],
        'PBO':[param_distri_exe,param_distri_pro],
        'type_infra':[param_distri_exe,param_distri_pro,param_distri_rbal],
        'longueur':[param_distri_exe,param_distri_pro,param_distri_rbal]
    }
    
    champs_cable = {
        'cb_code':[param_distri_exe,param_distri_pro,param_transport_exe],
        'cb_etiquet':[param_distri_exe,param_distri_pro,param_transport_exe],
        'cb_nd1':[param_distri_exe,param_distri_pro,param_transport_exe],
        'cb_nd2':[param_distri_exe,param_distri_pro,param_transport_exe],
        'cb_bp1':[param_distri_exe,param_distri_pro,param_transport_exe],
        'cb_bp2':[param_distri_exe,param_distri_pro,param_transport_exe],
        'cb_r1_code':[param_distri_exe,param_distri_pro,param_transport_exe],
        'cb_r2_code':[param_distri_exe,param_distri_pro,param_transport_exe],
        'cb_r3_code':[param_distri_exe,param_distri_pro,param_transport_exe],
        'cb_r4_code':[param_distri_exe,param_distri_pro,param_transport_exe],
        'cb_prop':[param_distri_exe,param_distri_pro,param_transport_exe],
        'cb_gest':[param_distri_exe,param_distri_pro,param_transport_exe],
        'cb_statut':[param_distri_exe,param_distri_pro,param_transport_exe],
        'cb_avct':[param_distri_exe,param_distri_pro,param_transport_exe],
        'cb_typelog':[param_distri_exe,param_distri_pro,param_transport_exe],
        'cb_creadat':[param_distri_exe,param_distri_pro,param_transport_exe],
        'cb_lgreel':[param_distri_exe,param_distri_pro,param_transport_exe],
        'cb_capafo':[param_distri_exe,param_distri_pro,param_transport_exe]
    }
    
    champs_zpbo = {
        'zp_code':[param_distri_exe,param_distri_pro],
        'zp_nd_code':[param_distri_exe,param_distri_pro],
        'zp_zs_code':[param_distri_exe,param_distri_pro],
        'zp_r1_code':[param_distri_exe,param_distri_pro],
        'zp_r2_code':[param_distri_exe,param_distri_pro],
        'zp_r3_code':[param_distri_exe,param_distri_pro],
        'zp_r4_code':[param_distri_exe,param_distri_pro],
        'zp_bp_code':[param_distri_exe,param_distri_pro],
        'nb_prises':[param_distri_exe,param_distri_pro],
        'zp_creadat':[param_distri_exe,param_distri_pro]
    }
    
    champs_zpec = {
        'Bp_code':[param_distri_exe,param_distri_pro],
        'nb_prises':[param_distri_exe,param_distri_pro]
    }
    
    champs_zsro = {
        'zs_code':[param_distri_exe,param_distri_pro,param_distri_rbal],
        'zs_nd_code':[param_distri_exe,param_distri_pro,param_distri_rbal],
        'zs_zn_code':[param_distri_exe,param_distri_pro,param_distri_rbal],
        'zs_r1_code':[param_distri_exe,param_distri_pro,param_distri_rbal],
        'zs_r2_code':[param_distri_exe,param_distri_pro,param_distri_rbal],
        'zs_r3_code':[param_distri_exe,param_distri_pro,param_distri_rbal],
        'zs_refpm':[param_distri_exe,param_distri_pro,param_distri_rbal],
        'zs_etatpm':[param_distri_exe,param_distri_pro,param_distri_rbal],
        'zs_capamax':[param_distri_exe,param_distri_pro,param_distri_rbal],
        'zs_nblogmt':[param_distri_exe,param_distri_pro,param_distri_rbal],
        'zs_creadat':[param_distri_exe,param_distri_pro,param_distri_rbal]
    }
    
    champs_znro = {
        'zn_code':[param_distri_exe,param_transport_exe],
        'COMMUNE':[param_distri_exe,param_transport_exe],
        'zn_nd_code':[param_distri_exe,param_transport_exe],
        'zn_r1_code':[param_distri_exe,param_transport_exe],
        'zn_r2_code':[param_distri_exe,param_transport_exe],
        'zn_creadat':[param_distri_exe,param_transport_exe]
    }
    
    champs_nro = {
        'zn_code':[param_distri_exe,param_transport_exe],
        'st_code':[param_distri_exe,param_transport_exe],
        'st_nd_code':[param_distri_exe,param_transport_exe],
        'st_codeext':[param_distri_exe,param_transport_exe],
        'st_prop':[param_distri_exe,param_transport_exe],
        'st_gest':[param_distri_exe,param_transport_exe],
        'nd_r1_code':[param_distri_exe,param_transport_exe],
        'nd_r2_code':[param_distri_exe,param_transport_exe],
        'nd_voie':[param_distri_exe,param_transport_exe],
        'st_statut':[param_distri_exe,param_transport_exe],
        'st_avct':[param_distri_exe,param_transport_exe],
        'st_typephy':[param_distri_exe,param_transport_exe],
        'st_typelog':[param_distri_exe,param_transport_exe],
        'st_creadat':[param_distri_exe,param_transport_exe],
        'lt_code':[param_distri_exe,param_transport_exe],
        'lt_code_ext':[param_distri_exe,param_transport_exe]
    }
    
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
    
    format_shape_invalide="Shape non valide: {}"
    
    criticite={
        "mineure":"Mineure",
        "majeure":"Majeure",
        "bloquant":"Bloquant",
        "avertissement":"Avertissement"
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
    
    erreur_controle={}
    erreur_controle[1]="Mauvaise version de la C3A"
    erreur_controle[2]="Liaison manquante dans la C3A"
    erreur_controle[3]="Tronçon présent dans la C3A mais absent de QGIS"
    erreur_controle[4]="Fiche poteaux manquante"
    erreur_controle[5]="Incohérence du type de point technique entre la C3A et QGIS"
    erreur_controle[6]="Information de sous tubage incomplète pour le tronçon. La colonne I doit être renseigné"
    erreur_controle[7]="Format de nommage incorrect"
    erreur_controle[8]="Longueur de tronçon / portée incorrect"
    erreur_controle[9]="Les valeurs ne respectent pas les listes déroulantes"
    erreur_controle[10]="Fichier C7 manquant"
    erreur_controle[11]="Appui manquant dans la C7"
    erreur_controle[12]="Combinaison interdite"
    erreur_controle[13]="Information de diamètre de l'alvéole mal renseigné"
    erreur_controle[14]="La colonne F doit être vide"
    erreur_controle[15]='La colonne H doit contenir la valeur "adduction"'
    erreur_controle[16]="La colonne F doit être vide"
    erreur_controle[17]='La colonne G doit contenir la valeur "7"'
    erreur_controle[18]="La colonne F doit être vide"
    erreur_controle[19]='La colonne H doit contenir la valeur "transition"'
    erreur_controle[20]='La colonne G doit contenir la valeur "7"'
    erreur_controle[21]='La colonne H doit contenir la valeur "transition"'
    erreur_controle[22]='La colonne F doit être vide'
    erreur_controle[23]='Les colonne B et D doivent être vide'
    erreur_controle[24]='La colonne H doit contenir la valeur "transition"'
    erreur_controle[25]='Nom de fiche poteau incorrect'
    erreur_controle[26]="La structuration des champs de la couche point technique est incorrecte"
    erreur_controle[27]="La structuration des champs de la couche prises est incorrecte"
    erreur_controle[28]="La structuration des champs de la couche SRO est incorrecte"
    erreur_controle[29]="La structuration des champs de la couche boitier est incorrecte"
    erreur_controle[30]="La structuration des champs de la couche infrastructure est incorrecte"
    erreur_controle[31]="La structuration des champs de la couche racco_client est incorrecte"
    erreur_controle[32]="La structuration des champs de la couche cable est incorrecte"
    erreur_controle[33]="La structuration des champs de la couche ZPBO est incorrecte"
    erreur_controle[34]="La structuration des champs de la couche ZSRO est incorrecte"
    erreur_controle[35]="La structuration des champs de la couche ZPEC est incorrecte"
    erreur_controle[36]="La structuration des champs de la couche ZNRO est incorrecte"
    erreur_controle[37]="La structuration des champs de la couche NRO est incorrecte"
    erreur_controle[38]="Le format du numéro d'appui dans la C7 est incorrect"
    erreur_controle[39]="La couche est manquante"
    erreur_controle[40]="L'attribut est manquant"
    erreur_controle[41]="DT manquants pour la commune"
    erreur_controle[42]="Des fichiers sont manquants dans le dossier L49"
    erreur_controle[43]="Le fichier PMV aérien est manquant pour la commune"
    erreur_controle[44]="Le fichier PMV conduite est manquant pour la commune"
    erreur_controle[45]="Le récapitulatif de convention est introuvable dans le dossier de conventions"
    erreur_controle[46]="Le fichier BPU est introuvable"
    erreur_controle[47]="Le répertoire LAYERS ou le fichier .qgs est introuvable dans le répertoire PROJET_QGIS"
    erreur_controle[48]="Le fichier de plan de tirage est introuvable dans le répertoire PROJET_QGIS"
    erreur_controle[49]="Le fichier synoptique cable est introuvable"
    erreur_controle[50]="Le fichier synoptique fibre est introuvable"
    erreur_controle[51]="Le boitier est introuvable dans le dossier Plan de boîte"
    erreur_controle[52]="Il existe des points techniques Enedis mais le dossier Enedic est vide"
    erreur_controle[53]="Le fichier appui est manquant pour ce point technique"
    erreur_controle[54]="Le fichier chambre est manquant pour ce point technique"
    erreur_controle[55]="L'annexe est manquante pour cette élement"
    erreur_controle[56]="Le fichier de synthèse d'étude est introuvable"
    erreur_controle[57]="Nom de fiche poteau incorrect"
    erreur_controle[58]="Fiche chambre manquante"
    
    pre_entete = {}
    pre_entete[1] = ["Commande d'accès","Version"]
    pre_entete[2] = ["Commande d'accès","Complétude"]
    pre_entete[3] = ["Commande d'accès","Règle GCBLO"]
    pre_entete[4] = ["Commande d'accès","Cohérence"]
    pre_entete[5] = ["Commande d'accès","Structuration des couches"]
    pre_entete[6] = ["Complétude","Plan de tirage"]
    pre_entete[7] = ["Complétude","Projet QGIS"]
    pre_entete[8] = ["Complétude","QGIS"]
    pre_entete[9] = ["Complétude","Etude CAPFT"]
    pre_entete[10] = ["Complétude","FOA"]
    pre_entete[11] = ["Complétude","Etude Comac"]
    pre_entete[12] = ["Complétude","Synthèse étude"]
    pre_entete[13] = ["Complétude","Synoptique cable"]
    pre_entete[14] = ["Complétude","Synoptique fibre à fibre"]
    pre_entete[15] = ["Complétude","Financier"]
    pre_entete[16] = ["Complétude","Convention"]
    pre_entete[17] = ["Complétude","Plan de boite"]
    pre_entete[18] = ["Complétude","PMV conduite"]
    pre_entete[19] = ["Complétude","DT"]
    pre_entete[20] = ["Complétude","L49"]
    pre_entete[21] = ["Complétude","PMV aérien"]
    pre_entete[22] = ["Complétude","Annexe D15"]
    
    pre_entete_lien={}
    pre_entete_lien.update(dict.fromkeys([1],1))
    pre_entete_lien.update(dict.fromkeys([2,3,58],2))
    pre_entete_lien.update(dict.fromkeys([4,6,7,8,9,10,11,12,13,15,16,17,18,19,20,21,22,23,24,25,38,57],3))
    pre_entete_lien.update(dict.fromkeys([5],4))
    pre_entete_lien.update(dict.fromkeys([26,27,28,29,30,31,32,33,34,35,36,37],5))
    pre_entete_lien.update(dict.fromkeys([48],6))
    pre_entete_lien.update(dict.fromkeys([47],7))
    pre_entete_lien.update(dict.fromkeys([39],8))
    pre_entete_lien.update(dict.fromkeys([53],9))
    pre_entete_lien.update(dict.fromkeys([54],10))
    pre_entete_lien.update(dict.fromkeys([52],11))
    pre_entete_lien.update(dict.fromkeys([56],12))
    pre_entete_lien.update(dict.fromkeys([49],13))
    pre_entete_lien.update(dict.fromkeys([50],14))
    pre_entete_lien.update(dict.fromkeys([46],15))
    pre_entete_lien.update(dict.fromkeys([45],16))
    pre_entete_lien.update(dict.fromkeys([51],17))
    pre_entete_lien.update(dict.fromkeys([44],18))
    pre_entete_lien.update(dict.fromkeys([41],19))
    pre_entete_lien.update(dict.fromkeys([42],20))
    pre_entete_lien.update(dict.fromkeys([43],21))
    pre_entete_lien.update(dict.fromkeys([55],22))
    
    post_criticite_lien={}
    post_criticite_lien.update(dict.fromkeys([1,2,4,58],criticite['bloquant']))
    post_criticite_lien.update(dict.fromkeys([6,9,13,14,15,16,17,18,19,20,21,22,23,24,56,57],criticite['mineure']))
    post_criticite_lien.update(dict.fromkeys([25,38],criticite['avertissement']))
    post_criticite_lien.update(dict.fromkeys([3,5,7,8,10,11,12,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55],criticite['majeure']))
    
    lib_nb_erreurs="Nombre d'erreurs"
    c3a_list_libelle="Ensemble des C3A"
    c7_list_libelle="Ensemble des C7"
    poteau_list_libelle="Ensemble des fiches poteaux"
    chambre_list_libelle="Ensemble des fiches chambres"
    cable_infra_list_libelle="Ensemble des cables infra"
    projet_dossier_libelle="Dossier PROJET QGIS"
    dossier_comac_libelle="Dossier Comac"
    lib_a="A"
    lib_b="B"
    msg_erreur=""
    msg=""
    rapport=""
    
    shape_point_technique_nom="POINT TECHNIQUE"
    shape_prises_nom="PRISES"
    shape_sro_nom="SRO"
    shape_boitier_nom="BOITIER"
    shape_infra_nom="INFRASTRUCTURE"
    shape_racco_client_nom="RACCO_CLIENT"
    shape_cable_nom="CABLE"
    shape_zpbo_nom="ZPBO"
    shape_zpec_nom="ZPEC"
    shape_zsro_nom="ZSRO"
    shape_znro_nom="ZNRO"
    shape_nro_nom="NRO"
    shape_bati_nom="BATI"
    shape_cadastre_nom="CADASTRE"
    shape_route_nom="ROUTE"
    shape_commune_nom="COMMUNE"
    
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
    prop_orange_code=''
    prop_tiers_code='T'
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
    codes_gc_prevu=("C","A CREER")
    codes_poteau_chng_rplc=("CHANGEMENT","RENFORT")
    codes_pt_problematique=("PROBLEMATIQUE","DECROUTAGE","REHAUSSE","INTROUVABLE")
    codes_infra_problematique=("PROBLEMATIQUE","DECROUTAGE","REHAUSSE","INTROUVABLE")
    
    #Types de liaisons
    liaison_c_c="C - C"
    liaison_c_imb="C - IMB"
    liaison_c_f="C - F"
    liaison_c_p="C - P"
    laison_c_pt="C - PT"
    laison_ct_p="CT - P"
    
    #Format attendu du nom des points et fiches poteaux
    pattern_nom_point_souple = re.compile("^\d{5}[_/]\w+")
    pattern_nom_point = re.compile("^\d{5}/\w+")
    
    pattern_plan_tirage=re.compile("^(.)*plan_tirage(.)*.pdf")
        
except Exception as e:
    log(e,11)

def set_libelle_rapport_csv():
    return prefixe_rapport_csv+'_'+str(datetime.now()).split('.')[0].replace(' ','_').replace(':','-')+'.csv'

#La fonction update_conf contient le même code dans chaque fichier donc pour éviter les doublons,
#on a le code en chaîne de caracère afin

update_conf_exec="""
global conf,libelle_rapport_csv;
conf=config;
conf['type_lvrb']=type_lvrb;
conf['zone']=zone;
libelle_rapport_csv=set_libelle_rapport_csv();
"""

#Mise à jour du dictionnaire de configuration avec le nouveaux généré après sélection du département
def update_conf_def(config,type_lvrb,zone):
    exec(update_conf_exec)