from controles import *

#Initialisation du gestionnaire de QGIS
qgs = QgsApplication([], False)
qgs.initQgis()

#warning d'un module pour une bibliothèque bientôt obsolète
warnings.simplefilter("ignore")

#Mise à jour du dictionnaire de configuration avec le nouveaux généré après sélection du département
def update_conf_param(config,type_lvrb,zone):
    exec(update_conf_exec)

#Lancement des contrôles à la suite avec gestion des exceptions et de la sélection des controles
def lancer_controles(widget):
    #Initialisation de la barre de progression
    pbar=init_pbar(widget)
    
    #Récupération de la liste des contrôles à effectuer
    try:
        list_controle_exe=get_liste_controle_dpt(conf["dpt"],conf["type_lvrb"],conf["zone"])
    except Exception as e:
        return log(e,411)
     
    #Création du rapport, initialisé avec l'entête
    alim_rapport_csv()
    
    #Nombre de tests à réaliser
    nb_ctrl=list(list_controle_exe.values()).count(True)
    
    #Nombre de contrôle déjà effectués
    step_ctrl=0
    
    #list_controle_exe est passé en paramètre avec l'identifiant de contrôle correspondant
    #Le contrôle sera lancé si pour cet identifiant la valeur est True, sinon ignoré
    #La barre de progression est mise à jour après chaque contrôle effectué
    try:
        res=version_c3a(list_controle_exe[1])
        #if res:
            #pbar.setValue(100)
            #msg_succes()
            #return
        
        #Mise à jour de la barre de progression
        step_ctrl+=1
        pbar_chargement(pbar,step_ctrl,nb_ctrl)
    except Exception as e:
        return log(e,42)
    
    try:
        #La progression se fait selon le nombre de contrôles effectués
        step_ctrl+=corresp_cable_infra_c3a(list_controle_exe[2],list_controle_exe[3])
        pbar_chargement(pbar,step_ctrl,nb_ctrl)
    except Exception as e:
        return log(e,43)
    
    try:
        step_ctrl+=check_format_fiches_poteau(list_controle_exe[25])
        pbar_chargement(pbar,step_ctrl,nb_ctrl)
    except Exception as e:
        return log(e,412)
    
    try:
        step_ctrl+=corresp_poteau_c3a(list_controle_exe[4])
        pbar_chargement(pbar,step_ctrl,nb_ctrl)
    except Exception as e:
        return log(e,44)
    
    try:
        step_ctrl+=verif_point_technique_c3a(list_controle_exe[5])
        pbar_chargement(pbar,step_ctrl,nb_ctrl)
    except Exception as e:
        return log(e,410)
    
    try:
        step_ctrl+=info_sous_tubage(list_controle_exe[6])
        pbar_chargement(pbar,step_ctrl,nb_ctrl)
    except Exception as e:
        return log(e,45)
    
    try:
        step_ctrl+=regles_gcblo_c3a_majeurs(
            list_controle_exe[7],
            list_controle_exe[8],
            list_controle_exe[12]
        )
        pbar_chargement(pbar,step_ctrl,nb_ctrl)
    except Exception as e:
        return log(e,46)
    
    try:
        step_ctrl+=verif_liste_colonnes(list_controle_exe[9])
        pbar_chargement(pbar,step_ctrl,nb_ctrl)
    except Exception as e:
        return log(e,47)
    
    try:
        step_ctrl+=verif_c7_travaux_existe(list_controle_exe[10],list_controle_exe[11])
        pbar_chargement(pbar,step_ctrl,nb_ctrl)
    except Exception as e:
        return log(e,48)
        
    try:
        #Pour les contrôles 13,15,16,...24
        step_ctrl+=valeurs_selon_liaisons({k: v for k, v in list_controle_exe.items() if 13 <= k <= 24 and k != 14})
        pbar_chargement(pbar,step_ctrl,nb_ctrl)
    except Exception as e:
        return log(e,49)
    
    try:
        step_ctrl+=verif_struct_shape(list_controle_exe[26],list_controle_exe[27])
        pbar_chargement(pbar,100,100)
    except Exception as e:
        return log(e,413)
    
    #Affichage du message de fin confirmant la réussite des controles
    msg_succes()