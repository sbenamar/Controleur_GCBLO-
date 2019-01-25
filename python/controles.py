#Pour l'explication des contrôles, se réferer au fichier Controlleur.xlsx dans le dossier Documentation

try:
    from fonctions import *
except Exception as e:
    log(e,33)

#Contrôle 2 / Contrôle 3: possibilité de selection du/des contrôle(s) à réaliser
def corresp_cable_infra_c3a(msg_rapport="",parcours_infra=True,parcours_c3a=True):
    if not parcours_infra and not parcours_c3a:
        return msg_rapport
    
    #Récupération des C3A sous plusieurs formats
    ##C3A pour le contrôle 3
    commandes_groupe = get_commandes_groupe()
    
    #C3A pour le contrôle 2
    commandes_joint = get_commandes_joint(commandes_groupe)

    #Récupération du tableau de cable infra
    cable_infra = ouvrir_cable_infra(cable_infra_csv_path)

    #Comparaison des C3A et cable infra
    
    #Table infra reformaté pour avoir les points A et B séparés et sélectionner les données utiles
    #On filtre selon le typ_imp, défini dans le fichier de définition
    liaisons_infra_filtre=[
        (i,cable["cm_id"].replace("_","/").split("=>")) for (i,cable) in enumerate(cable_infra)
        if cable["cm_typ_imp"] in type_imp
    ]
    
    #Simplification de la liste des commandes pour la comparaison
    liaisons_commandes=liaisons_commande(commandes_joint)
    
    cable_infra_fichier=chemin_fichier_application(cable_infra_csv_path)

    #Début du contrôle 2, s'il est sélectionné
    if parcours_infra:
        num_controle=2
        pre_erreur=[num_controle]+pre_entete_2
        
        erreurs_infra=[
            pre_erreur
            +[cable_infra_fichier,c3a_list_libelle,(cable[0]+"=>"+cable[1]).replace("/","_")]
            +post_entete_controle2
            for (i,cable) in liaisons_infra_filtre
            if cable not in liaisons_commandes and cable not in sorted(liaisons_commandes)
            ]        
        
        alim_rapport_csv(erreurs_infra)
    
    #Début du contrôle 3, s'il est sélectionné
    if parcours_c3a:
        num_controle=3
        pre_erreur=[num_controle]+pre_entete_2
        
        #On reprend la liste des cables, filtrée,
        ##en retirant l'identifiant pour n'avoir que l'information à comparer
        cables = [cable[1] for cable in liaisons_infra_filtre]
        
        #Création du tableau d'erreurs à afficher sous Excel selon l'entête
        erreurs_c3a=[]
        for c3a,commandes in commandes_groupe:
            erreurs_c3a+=[
                pre_erreur
                +[
                    chemin_fichier_application(c3a),
                    cable_infra_list_libelle,
                    prestation[3].value+" - "+prestation[5].value
                ]
                +post_entete_controle3
                for (num_prestation,prestation) in enumerate(commandes)
                if prestation not in cables and prestation not in sorted(cables)
            ]
            
        alim_rapport_csv(erreurs_c3a)
        
    return msg_rapport

#Contrôle 1
def version_c3a(msg_rapport="",selectionne=True):
    num_controle=1
    
    if not selectionne:
        return msg_rapport
    
    erreurs=[]
    
    for f in get_c3a_list():
        c3a=get_feuille_commande(f)
        version=c3a.cell_value(rowx=6, colx=3).strip(' ')
        
        #Récupération du nom de fichier seulement, sans le chemin
        chemin=chemin_fichier_application(f)
        
        if version != version_c3a_en_cours:
            erreurs+=[[num_controle]+pre_entete_1+[chemin,chemin,""]+post_entete_controle1]
    
    alim_rapport_csv(erreurs)
    
    return msg_rapport

#Contrôle 4
def corresp_poteau_c3a(msg_rapport="",selectionne=True):
    if not selectionne:
        return msg_rapport
    
    num_controle=4
    pre_erreur=[num_controle]+pre_entete_3
    
    poteaux = get_poteaux_fiche()
    commandes_groupe = get_commandes_groupe()
    
    erreurs=[]
    
    #Ce tableau sert à éviter d'ajouter des lignes doublons dans les erreurs
    #Dés qu'un poteau est manquant, on l'ajoute dans ce tableau et ce poteaux ne sera plus ajouté
    c3a_poteaux=[]
    
    for c3a,commandes in commandes_groupe:
        for (num_prestation,prestation) in enumerate(commandes):
            
            #Permet d'avoir le même format pour comparer
            point_a=prestation[3].value.replace("/","_")
            point_b=prestation[5].value.replace("/","_")
            
            if point_a not in poteaux and point_a not in c3a_poteaux and len(point_a):
                erreurs.append(
                    pre_erreur
                    +[
                        chemin_fichier_application(c3a),
                        cable_infra_list_libelle,
                        prestation[3].value
                    ]
                    +post_entete_controle4
                )
                c3a_poteaux.append(point_a)
                
            elif point_b not in poteaux and point_b not in c3a_poteaux and len(point_b):
                erreurs.append(
                    pre_erreur
                    +[
                        chemin_fichier_application(c3a),
                        cable_infra_list_libelle,
                        prestation[5].value
                    ]
                    +post_entete_controle4
                )
                c3a_poteaux.append(point_b)
            else:
                pass
            
    alim_rapport_csv(erreurs)
    return msg_rapport

#Contrôle 7 / Contrôle 8 / Contrôle 12: possibilité de selection du/des contrôle(s) à réaliser
def regles_gcblo_c3a_majeurs(msg_rapport="",controle7=True,controle8=True,controle12=True):
    if not controle7 and not controle8 and not controle12:
        return msg_rapport
    
    erreurs = []
    
    #Pour un algorithme plus lisible plus bas, les conditions d'erreur sont stockés ici en texte
    #Ils seront évalués par une fonction python
    condition7_1 = '("/" in prestation[3].value and prestation[3].value.split("/")[0].isdigit()'
    condition7_2 = ' and len(prestation[3].value.split("/")[0]) == 5)'
    condition7_3 = '("/" in prestation[5].value and prestation[5].value.split("/")[0].isdigit()'
    condition7_4 = ' and len(prestation[5].value.split("/")[0]) == 5)'

    condition8 = '(isinstance(prestation[6].value, (int, float)) or str(prestation[6].value).isdigit()) and int(prestation[6].value) >= 1'
    
    condition12= 'not(prestation[2].value+prestation[4].value in combinaisons_types)'

    commandes_groupe = get_commandes_groupe()
    msg=""
    
    for c3a,commandes in commandes_groupe:
        if controle7:
            num_controle=7
            pre_erreur=[num_controle]+pre_entete_3
            
            for (num_prestation,prestation) in enumerate(commandes):
                if not(eval(condition7_1+condition7_2)):
                    erreurs+=[
                        pre_erreur
                        +[
                            chemin_fichier_application(c3a),
                            chemin_fichier_application(c3a),
                            prestation[3].value
                        ]
                        +post_entete_controle7
                    ]
                    
                if not(eval(condition7_3+condition7_4)):
                    erreurs+=[
                        pre_erreur
                        +[
                            chemin_fichier_application(c3a),
                            chemin_fichier_application(c3a),
                            prestation[5].value
                        ]
                        +post_entete_controle7
                    ]

        if controle8:
            num_controle=8
            pre_erreur=[num_controle]+pre_entete_3
            
            erreurs+=[
                pre_erreur
                +[
                    chemin_fichier_application(c3a),
                    chemin_fichier_application(c3a),
                    prestation[3].value+" - "+prestation[5].value
                ]
                +post_entete_controle8
                for (num_prestation,prestation) in enumerate(commandes)
                if not(eval(condition8))
            ]

        if controle12:
            num_controle=8
            pre_erreur=[num_controle]+pre_entete_3
            
            erreurs+=[
                pre_erreur
                +[
                    chemin_fichier_application(c3a),
                    chemin_fichier_application(c3a),
                    prestation[3].value+" - "+prestation[5].value
                ]
                +post_entete_controle12
                for (num_prestation,prestation) in enumerate(commandes)
                if not(eval(condition12))
            ]

    alim_rapport_csv(erreurs)
    return msg_rapport