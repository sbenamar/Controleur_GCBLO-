try:
    from fonctions import *
except Exception as e:
    log(e,33)

def corresp_cable_infra_c3a(msg_rapport="",parcours_infra=True,parcours_c3a=True):
    if not parcours_c3a and not parcours_c3a:
        return 0
    
    ##### Partie XLS #####
    commandes_groupe = get_commandes_groupe()
    commandes_joint = get_commandes_joint(commandes_groupe)

    ##### Partie CSV #####
    cable_infra = ouvrir_cable_infra(cable_infra_csv_path)
    
    ##### Comparaison des 2 fichiers #####
    
    if parcours_infra or parcours_c3a:
        liaisons_infra_filtre=[
            (i,cable["cm_id"].replace("_","/").split("=>")) for (i,cable) in enumerate(cable_infra)
            if cable["cm_typ_imp"] in type_imp
            ]
        
        liaisons_commandes=liaisons_commande(commandes_joint)
    
    if parcours_infra:
        #### infra -> commandes ####
        msg=msg_debut_controle2.format("' ou '".join(type_imp))
        msg_rapport+=msg+"\n\n"
        print(msg)

        #i+2 car l'indice commence à 0 au lieu de 1, et qu'on ne compte pas le header
        erreurs_infra=[
            ["","","",i+2,cable_infra[i]["cb_id"],cable[0],cable[1],cable_infra[i]["Ordre"]]
            for (i,cable) in liaisons_infra_filtre
            if cable not in liaisons_commandes and cable not in sorted(liaisons_commandes)
            ]

        resultat_infra=[lib_nb_erreurs,str(len(erreurs_infra))]
        
        nom_fichier=resultat_fichier(prefixe_resultat_controle3,resultat_infra,entete_controle3,erreurs_infra)     
        
        print()
        msg=msg_erreur_fichier(erreurs_infra,nom_fichier)
        msg_rapport+=msg+"\n\n"
        
    if parcours_c3a:
        if parcours_infra:
            print()
            
        #### commandes -> infra ####
        msg=msg_debut_controle3.format("' ou '".join(type_imp))
        msg_rapport+=msg+"\n\n"
        print(msg)
        
        cables = [cable[1] for cable in liaisons_infra_filtre]
        
        erreurs_c3a=[]
        for c3a,commandes in commandes_groupe:
            erreurs_c3a+=[
                ["","","",c3a.replace(commande_orange_path,""),num_prestation+ind_premiere_ligne_c3a+1,prestation[3].value,prestation[5].value]
                for (num_prestation,prestation) in enumerate(commandes)
                if prestation not in cables and prestation not in sorted(cables)
            ]
            
        resultat_c3a=[lib_nb_erreurs,str(len(erreurs_c3a))]
        
        nom_fichier=resultat_fichier(prefixe_resultat_controle2,resultat_c3a,entete_controle2,erreurs_c3a)     
        
        print()
        msg=msg_erreur_fichier(erreurs_c3a,nom_fichier)
        msg_rapport+=msg+"\n\n"
    
    print()    
    return msg_rapport

def version_c3a(msg_rapport=""):
    msg=msg_debut_controle1+"\n"
    for f in get_c3a_list():
        c3a=get_feuille_commande(f)
        version=c3a.cell_value(rowx=6, colx=3).strip(' ')
    
        msg+=f.replace(commande_orange_path,"")+" :\n"
        if version == version_c3a_en_cours:
            msg+=msg_fin_controle1_1
        else:
            msg+=msg_fin_controle1_2
            
        msg+="\n\n"
    
    print(msg)
    msg_rapport+=msg+"\n"
    
    return msg_rapport

def corresp_poteau_c3a(msg_rapport=""):
    print(msg_debut_controle4)
    msg=msg_debut_controle4+"\n\n"
    
    poteaux = get_poteaux_fiche()
    commandes_groupe = get_commandes_groupe()
    
    erreurs=[]
    c3a_poteaux=[]
    
    for c3a,commandes in commandes_groupe:
        for (num_prestation,prestation) in enumerate(commandes):
            point_a=prestation[3].value.replace("/","_")
            point_b=prestation[5].value.replace("/","_")
            if point_a not in poteaux and point_a not in c3a_poteaux and len(point_a):
                erreurs.append([
                    "","","",
                    c3a.replace(commande_orange_path,""),
                    num_prestation+ind_premiere_ligne_c3a+1,
                    lib_a,
                    prestation[3].value
                ])
                c3a_poteaux.append(point_a)
                
            elif point_b not in poteaux and point_b not in c3a_poteaux and len(point_b):
                erreurs.append([
                    "","","",
                    c3a.replace(commande_orange_path,""),
                    num_prestation+ind_premiere_ligne_c3a+1,
                    lib_b,
                    prestation[5].value
                ])
                c3a_poteaux.append(point_b)
            else:
                pass
    
    resultat=[lib_nb_erreurs,str(len(erreurs))]
    nom_fichier=resultat_fichier(prefixe_resultat_controle4,resultat,entete_controle4,erreurs)     
    
    print()
    msg+=msg_erreur_fichier(erreurs,nom_fichier)
    msg_rapport+=msg+"\n\n"
    
    return msg_rapport

def regles_gcblo_c3a_majeurs(msg_rapport="",controle7=True,controle8=True,controle12=True):
    erreurs7 = []
    erreurs8= []
    erreurs12 = []

    condition7_1 = '("/" in prestation[3].value and prestation[3].value.split("/")[0].isdigit()'
    condition7_2 = ' and len(prestation[3].value.split("/")[0]) == 5)'
    condition7_3 = ' and ("/" in prestation[5].value and prestation[5].value.split("/")[0].isdigit()'
    condition7_4 = ' and len(prestation[5].value.split("/")[0]) == 5)'

    condition8 = '(isinstance(prestation[6].value, (int, float)) or str(prestation[6].value).isdigit()) and int(prestation[6].value) >= 1'
    
    condition12= 'not(prestation[2].value+prestation[4].value in combinaisons_types)'

    commandes_groupe = get_commandes_groupe()
    msg=""
    
    for c3a,commandes in commandes_groupe:
        fnom = c3a.replace(commande_orange_path,"")
        
        if controle7:
            erreurs7+=[
                ["","","",
                    fnom,
                    num_prestation+ind_premiere_ligne_c3a+1,
                    prestation[3].value,
                    prestation[5].value
                 ]
                for (num_prestation,prestation) in enumerate(commandes)
                if not(eval(condition7_1+condition7_2+condition7_3+condition7_4))
            ]
        if controle8:
            erreurs8+=[
                ["","","",
                    fnom,
                    num_prestation+ind_premiere_ligne_c3a+1,
                    prestation[3].value,
                    prestation[5].value,
                    prestation[6].value
                ]
                for (num_prestation,prestation) in enumerate(commandes)
                if not(eval(condition8))
            ]

        if controle12:
            erreurs12+=[
                ["","","",
                    fnom,
                    num_prestation+ind_premiere_ligne_c3a+1,
                    prestation[3].value,
                    prestation[5].value,
                    combinaison_type_format.format(prestation[2].value,prestation[4].value)
                ]
                for (num_prestation,prestation) in enumerate(commandes)
                if not(eval(condition12))
            ]
    if controle7:        
        msg += contenu_rapport(
                    msg_debut_controle7,
                    entete_controle7,
                    erreurs7,
                    prefixe_resultat_controle7
                )
    if controle8:
        msg += contenu_rapport(
                    msg_debut_controle8,

                    entete_controle8,
                    erreurs8,
                    prefixe_resultat_controle8
                )
    if controle12:
        msg += contenu_rapport(
                    msg_debut_controle12,
                    entete_controle12,
                    erreurs12,
                    prefixe_resultat_controle12
                )
    msg_rapport+=msg
    return msg_rapport