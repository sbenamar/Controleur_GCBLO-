from controles import *

#Initialisation du gestionnaire de QGIS
QgsApplication.setPrefixPath(qgis_prefix_path,True)
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
        step_ctrl+=check_format_fiches_poteau(list_controle_exe[25],list_controle_exe[57])
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
        step_ctrl+=verif_c7_travaux_existe(list_controle_exe[10],list_controle_exe[11],list_controle_exe[38])
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
        step_ctrl+=verif_struct_shape({k: v for k, v in list_controle_exe.items() if 26 <= k <= 37})
        pbar_chargement(pbar,step_ctrl,nb_ctrl)
    except Exception as e:
        return log(e,413)
    
    try:
        step_ctrl+=verif_couches_exist(list_controle_exe[39])
        pbar_chargement(pbar,step_ctrl,nb_ctrl)
    except Exception as e:
        return log(e,416)
    
    try:
        step_ctrl+=verif_dossier_qgis_exist(list_controle_exe[47])
        pbar_chargement(pbar,step_ctrl,nb_ctrl)
    except Exception as e:
        return log(e,414)
    
    try:
        step_ctrl+=verif_plan_tirage_exist(list_controle_exe[48])
        pbar_chargement(pbar,step_ctrl,nb_ctrl)
    except Exception as e:
        return log(e,415)

    try:
        step_ctrl+=verif_fichier_enedis_pt(list_controle_exe[52])
        pbar_chargement(pbar,step_ctrl,nb_ctrl)
    except Exception as e:
        return log(e,417)
    
    try:
        step_ctrl+=verif_fichier_appui_orange_pt(list_controle_exe[53])
        pbar_chargement(pbar,step_ctrl,nb_ctrl)
    except Exception as e:
        return log(e,418)
    
    try:
        step_ctrl+=verif_fichier_chambre_pt(list_controle_exe[54])
        pbar_chargement(pbar,step_ctrl,nb_ctrl)
    except Exception as e:
        return log(e,419)
    
    try:
        step_ctrl+=verif_synthese_etude(list_controle_exe[56])
        pbar_chargement(pbar,step_ctrl,nb_ctrl)
    except Exception as e:
        return log(e,421)
    
    try:
        step_ctrl+=verif_synoptique(list_controle_exe[49],list_controle_exe[50])
        pbar_chargement(pbar,step_ctrl,nb_ctrl)
    except Exception as e:
        return log(e,422)
    
    try:
        step_ctrl+=verif_bpu(list_controle_exe[46])
        pbar_chargement(pbar,step_ctrl,nb_ctrl)
    except Exception as e:
        return log(e,423)
    
    try:
        step_ctrl+=verif_convention(list_controle_exe[45])
        pbar_chargement(pbar,step_ctrl,nb_ctrl)
    except Exception as e:
        return log(e,424)
    
    try:
        step_ctrl+=verif_boitier_planboite(list_controle_exe[51])
        pbar_chargement(pbar,step_ctrl,nb_ctrl)
    except Exception as e:
        return log(e,425)
    
    try:
        step_ctrl+=verif_pmv_aerien_poteau_etat(list_controle_exe[43])
        pbar_chargement(pbar,step_ctrl,nb_ctrl)
    except Exception as e:
        return log(e,430)
    
    try:
        step_ctrl+=verif_pmv_conduite_gc(list_controle_exe[44])
        pbar_chargement(pbar,step_ctrl,nb_ctrl)
    except Exception as e:
        return log(e,426)
    
    try:
        step_ctrl+=corresp_chambre_c3a(list_controle_exe[58])
        pbar_chargement(pbar,step_ctrl,nb_ctrl)
    except Exception as e:
        return log(e,427)
    
    try:
        step_ctrl+=verif_dt_gc(list_controle_exe[41])
        pbar_chargement(pbar,step_ctrl,nb_ctrl)
    except Exception as e:
        return log(e,428)
    
    try:
        step_ctrl+=verif_l49_gc_1000(list_controle_exe[42])
        pbar_chargement(pbar,step_ctrl,nb_ctrl)
    except Exception as e:
        return log(e,429)
    
    #try:
    #    step_ctrl+=verif_d15_problematique(list_controle_exe[55])
    #    pbar_chargement(pbar,step_ctrl,nb_ctrl)
    #except Exception as e:
    #    return log(e,431)
    
    pbar_chargement(pbar,100,100)
    
    #Affichage du message de fin confirmant la réussite des controles
    msg_succes()