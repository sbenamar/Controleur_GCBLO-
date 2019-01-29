import warnings,os,sys,traceback
from datetime import datetime
#import qgis.utils
#from qgis.core import *
#from qgis.core import QgsProject,QgsVectorLayer
#from PyQt5.QtCore import QFileInfo

environnement = ["testv1"]

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
        input()
        exit(code)
except Exception as e:
    print ("Erreur lors de l'initialisation (code 1)")
    exit(11)

#Centralisation de tous les chemins, libéllés, variables, ... avec gestion d'une exception
try:
    if "EXE" in environnement:
        qgis_installation_path=r"C:\Program Files\QGIS 3.4"
        chemin_exe=os.path.join(chemin_courant,"exe")
        exe_projet_racine=os.path.join(chemin_exe,"04 - Projet")
        
        #Avant de récupérer le chemin du projet de l'exe, vérifier que l'exe est présent
        try:
            nom_projet=os.listdir(exe_projet_racine)[0]
        except Exception as e:
            print("Un projet est nécessaire pour lancer les contrôles.")
            log(e,12)
            
        exe_projet=os.path.join(exe_projet_racine,nom_projet)
        commande_orange_path=os.path.join(chemin_exe,"11 - Commande_Orange")
        exe_projet_carto=os.path.join(exe_projet,"APD"+nom_projet+".qgs")
        chemin_layers=os.path.join(exe_projet,exe_projet,"LAYERS")
        layer_prises = os.path.join(chemin_layers+"PRISES.shp")
        cable_infra_csv_path=os.path.join(chemin_layers,"CABLE_INFRA.csv")
        appui_orange_path=os.path.join(chemin_exe,"09 - Appui Orange - CAPFT")
        chemin_rapport=os.path.join(chemin_courant,"rapports")
        arbo_c3a="**/**/*C3A*.xls*"
        
    if "testv1" in environnement:
        qgis_installation_path=r"C:\Program Files\QGIS 3.4"
        chemin_exe=os.path.join(chemin_courant,"Commande d'accès")
        commande_orange_path=chemin_exe
        cable_infra_csv_path=os.path.join(chemin_exe,"CABLE_INFRA.csv")
        appui_orange_path=os.path.join(chemin_exe,"Appui aérien")
        chemin_rapport=os.path.join(chemin_courant,"rapports")
        arbo_c3a="*C3A*.xls*"
    
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
    erreur_controle6="Information de sous tubage incomplète pour le tronçon. La colonne I doit être renseigné"
    erreur_controle7="Mauvaise con"
    erreur_controle8="à remplir"
    erreur_controle12="Combinaison interdite"
    
    '''
    entete_controle2 = ["","","","ligne","cb_id","cm_id (A)", "cm_id (B)","Ordre"]
    entete_controle3 = ["","","","Fichier","Identifiant","Numéro point A","Numéro point B"]
    entete_controle4 = ["","","","Fichier","Identifiant","Identification A/B","Numéro de chambre / Appui aérien"]
    entete_controle6 = ["","","","Fichier","Identifiant","Identification A/B","Information de sous tubage incomplète pour le tronçon. La colonne I doit être renseigné"]
    entete_controle7 = ["","","","Fichier","Identifiant","Numéro point A","Numéro point B"]
    entete_controle8 = ["","","","Fichier","Identifiant","Numéro point A","Numéro point B", "Longueur troncon / portée"]
    entete_controle12 = ["","","","Fichier","Identifiant","Numéro point A","Numéro point B","Combinaison de types"]
    '''
    
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
    
    pre_entete_lien={
        1:pre_entete_1,
        2:pre_entete_2,
        3:pre_entete_2,
        4:pre_entete_3,
        5:pre_entete_3,
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
    }
    
    post_entete_controle1=[erreur_controle1,criticite['bloquant']]
    post_entete_controle2=[erreur_controle2,criticite['bloquant']]
    post_entete_controle3=[erreur_controle3,criticite['majeure']]
    post_entete_controle4=[erreur_controle4,criticite['bloquant']]
    post_entete_controle6=[erreur_controle6,criticite['mineure']]
    post_entete_controle7=[erreur_controle7,criticite['majeure']]
    post_entete_controle8=[erreur_controle8,criticite['majeure']]
    post_entete_controle12=[erreur_controle12,criticite['majeure']]
    
    """
    csv_famille = {
        "commande_acces":"Commande d'accès"
    }
    
    csv_ss_famille = {
        "version":"Version",
        "completude":"Complétude",
        "coherence":"Cohérence",
        "regle_gcblo":"Règle GCBLO"
    }
    """
    
    lib_nb_erreurs="Nombre d'erreurs"
    c3a_list_libelle="Ensemble des C3A"
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
except Exception as e:
    log(e,13)
