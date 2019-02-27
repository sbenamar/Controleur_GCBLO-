from controles import *

#QgsApplication.setPrefixPath(qgis_prefix_path,True)
qgs = QgsApplication([], False)
qgs.initQgis()

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

def update_conf_param(config,type_lvrb,zone):
    exec(update_conf_exec)

def lancer_controles(widget):
    pbar=init_pbar(widget)
    
    try:
        list_controle_exe=get_liste_controle_dpt(conf["dpt"],conf["type_lvrb"],conf["zone"])
    except Exception as e:
        return log(e,411)
     
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
        
        pbar_chargement(pbar,1,len(list_controle_exe))
    except Exception as e:
        return log(e,42)
    
    try:
        corresp_cable_infra_c3a(list_controle_exe[2],list_controle_exe[3])
        pbar_chargement(pbar,3,len(list_controle_exe))
    except Exception as e:
        return log(e,43)
    
    try:
        check_format_fiches_poteau(list_controle_exe[25])
    except Exception as e:
        return log(e,412)
    
    try:
        corresp_poteau_c3a(list_controle_exe[4])
        pbar_chargement(pbar,4,len(list_controle_exe))
    except Exception as e:
        return log(e,44)
    
    try:
        verif_point_technique_c3a(list_controle_exe[5])
        pbar_chargement(pbar,5,len(list_controle_exe))
    except Exception as e:
        return log(e,410)
    
    try:
        info_sous_tubage(list_controle_exe[6])
        pbar_chargement(pbar,6,len(list_controle_exe))
    except Exception as e:
        return log(e,45)
    
    try:
        regles_gcblo_c3a_majeurs(
            list_controle_exe[7],
            list_controle_exe[8],
            list_controle_exe[12]
        )
        pbar_chargement(pbar,7,len(list_controle_exe))
    except Exception as e:
        return log(e,46)
    
    try:
        verif_liste_colonnes(list_controle_exe[9])
        pbar_chargement(pbar,9,len(list_controle_exe))
    except Exception as e:
        return log(e,47)
    
    try:
        verif_c7_travaux_existe(list_controle_exe[10],list_controle_exe[11])
        pbar_chargement(pbar,10,len(list_controle_exe))
    except Exception as e:
        return log(e,48)
        
    try:
        #Pour les contrôles 13,15,16,...24
        valeurs_selon_liaisons({k: v for k, v in list_controle_exe.items() if 13 <= k <= 24 and k != 14})
        pbar.setValue(100)
    except Exception as e:
        return log(e,49)
    
    msg_succes()