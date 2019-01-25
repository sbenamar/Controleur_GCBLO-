import warnings,os,sys,traceback
from datetime import datetime
#import qgis.utils
#from qgis.core import *
#from qgis.core import QgsProject,QgsVectorLayer
#from PyQt5.QtCore import QFileInfo


#Gestion de l'exception lors de la création de la fonction de log, qui permettra de généraliser
##la gestion des erreurs
try:
    #chemin_courant permettra de servir de base pour la création des autres chemins
    chemin_courant=os.getcwd()
    
    #Préparation des variables utilisées par la fonction log dont un format d'affichage
    log_path=os.path.join(*[chemin_courant,"python","log"])
    nom_log="log.txt"
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
            
        print("Une erreur est survenue (code: {})".format(str(code)))
        exit(code)
except Exception as e:
    print ("Erreur lors de l'initialisation (code 1)")
    exit(11)

#Centralisation de tous les chemins, libéllés, variables, ... avec gestion d'une exception
try:
    qgis_installation_path=r"C:\Program Files\QGIS 3.4"
    chemin_exe=os.path.join(chemin_courant,"exe")
    exe_projet_racine=os.path.join(chemin_exe,"04 - Projet")
    
    #Avant de récupérer le chemin du projet de l'exe, vérifier que l'exe est présent
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
    chemin_rapport=os.path.join(chemin_courant,"rapports")
    
    ind_premiere_ligne_c3a=31-1
    type_imp=["CONDUITE FT","AERIEN FT"]
    version_c3a_en_cours='C3A BLO5'
    combinaisons_types=["CTCT","CCT","CTC","CTP","CTA","ACT","PCT"]
    
    prefixe_resultat_controle2="rapport_verif_cable_infra_c3a"
    prefixe_resultat_controle3="rapport_verif_c3a_cable_infra"
    prefixe_resultat_controle4="rapport_verif_c3a_poteaux"
    prefixe_resultat_controle7="rapport_verif_norme_numero"
    prefixe_resultat_controle8="rapport_verif_longueur_troncon"
    prefixe_resultat_controle12="rapport_verif_combinaison_types"
    prefixe_rapport_csv="rapport_erreurs"
    nom_rapport="rapport.txt"
    
    libelle_rapport_csv=prefixe_rapport_csv+'_'+str(datetime.now()).split('.')[0].replace(' ','_').replace(':','-')+'.csv'
    
    msg_debut_controle1="Vérification de la version des C3A..."
    msg_debut_controle2="Vérification des correspondances de liaisons entre la table attributaire 'cable_infra' et les C3A pour les liaisons de type {} ..."
    msg_debut_controle3="Vérification des correspondances de liaisons entre les C3A et la table attributaire 'cable_infra' pour les liaisons de type {} ..."
    msg_debut_controle4="Vérification de la correspondance entre les poteaux présents dans les C3A et les fiches poteaux..."
    msg_debut_controle7="Vérification de la conformité de la forme de l'identifiant des chambres / appuis aériens..."
    msg_debut_controle8="Vérification de la longueur du tronçon ou de la portée en domaine public..."
    msg_debut_controle12="Vérification de la bonne combinaison des points A et B..."
    
    msg_fin_controle1_1="La version du C3A est à jour."
    msg_fin_controle1_2="Version obsolète de la C3A. Veuillez mettre à jour à la version : {}".format(
        version_c3a_en_cours
    )
    msg_fin_programme_1="Programme terminé"
    msg_fin_programme_2="Appuyez sur une touche pour quitter le programme..."
    
    msg_detecte_erreur1="Le controlleur a détecté {} erreurs:\n{}"
    msg_detecte_erreur2="Le controlleur a détecté 1 erreur ({})."
    msg_detecte_erreur3="Aucune erreur n'a été détectée par le controlleur."
    
    msg_erreur_fichier1="Aucune erreur n'a été détectée par le controlleur."
    msg_erreur_fichier2="1 erreur a été détectée par le controlleur. Les détails sont dans le fichier {}"
    msg_erreur_fichier3="{} erreurs ont été détectées par le controlleur. Les détails sont dans le fichier {}"
    
    entete_controle2 = ["","","","ligne","cb_id","cm_id (A)", "cm_id (B)","Ordre"]
    entete_controle3 = ["","","","Fichier","Identifiant","Numéro point A","Numéro point B"]
    entete_controle4 = ["","","","Fichier","Identifiant","Identification A/B","Numéro de chambre / Appui aérien"]
    entete_controle7 = ["","","","Fichier","Identifiant","Numéro point A","Numéro point B"]
    entete_controle8 = ["","","","Fichier","Identifiant","Numéro point A","Numéro point B", "Longueur troncon / portée"]
    entete_controle12 = ["","","","Fichier","Identifiant","Numéro point A","Numéro point B","Combinaison de types"]
    
    entete_rapport_csv = [
        "Référence de contrôle",
        "Famille",
        "Sous-famille",
        "Source A",
        "Source B",
        "Contrôle effectué",
        "Erreur générée",
        "Criticité générée"
    ]
    
    csv_famille = {
        "commande_acces":"Commande d'accès"
    }
    
    csv_ss_famille = {
        "version":"Version",
        "completude":"Complétude",
        "coherence":"Cohérence",
        "regle_gcblo":"Règle GCBLO"
    }
    
    criticite={
        "mineure":"Mineure",
        "majeure":"Majeure",
        "bloquant":"Bloquant"
    }

    detail_controle1='Vérifier que la colonne C6 contient "C3A BLO5"'
    detail_controle2="Parcourir la table cable_infra. Pour chaque objet de la table de type infra_orange, vérifier qu'il existe une correspondance dans la C3A"
    detail_controle3="Parcourir la C3A. Pour chaque ligne, vérifier qu'il existe une correspondance dans la table_infra"
    detail_controle4="Vérifier qu'il existe une fiche poteaux pour chaque poteaux de la C3A"
    detail_controle7=""
    detail_controle8=""
    detail_controle12=""
    
    erreur_format_controle1="Mauvaise version de la C3A"
    erreur_format_controle2="Liaison {} manquant dans la C3A"
    erreur_format_controle3="Tronçon {}-{} présent dans la C3A mais absent de QGIS"
    erreur_format_controle4="Fiche poteaux {} manquante"
    erreur_format_controle7="Mauvaise con"
    erreur_format_controle8=""
    erreur_format_controle12="Combinaison interdite"
    
    lib_nb_erreurs="Nombre d'erreurs"
    lib_a="A"
    lib_b="B"
    msg_erreur=""
    msg=""
    rapport=""
    
    combinaison_type="{} - {}"
    num_ligne="Ligne {}"
except Exception as e:
    log(e,13)
