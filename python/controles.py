try:
    from fonctions import *
except Exception as e:
    log(e,4)

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
        msg="Vérification des correspondances de liaisons entre la table attributaire 'cable_infra' et les C3A pour les liaisons de type '"+"' ou '".join(type_imp)+"'..."
        msg_rapport+=msg+"\n\n"
        print(msg)

        #i+2 car l'indice commence à 0 au lieu de 1, et qu'on ne compte pas le header
        erreurs_infra=[
            ["","","",i+2,cable_infra[i]["cb_id"],cable[0],cable[1],cable_infra[i]["Ordre"]]
            for (i,cable) in liaisons_infra_filtre
            if cable not in liaisons_commandes and cable not in sorted(liaisons_commandes)
            ]
            
        entete_infra=["","","","ligne","cb_id","cm_id (A)", "cm_id (B)","Ordre"]
        resultat_infra=["Nombre d'erreurs",str(len(erreurs_infra))]
        
        nom_fichier=resultat_fichier(prefixe_resultat_controle2_1,resultat_infra,entete_infra,erreurs_infra)     
        
        print()
        msg=msg_erreur_fichier(erreurs_infra,nom_fichier)
        msg_rapport+=msg+"\n\n"
        
    if parcours_c3a:
        if parcours_infra:
            print()
            
        #### commandes -> infra ####
        msg="Vérification des correspondances de liaisons entre les C3A et la table attributaire 'cable_infra' pour les liaisons de type '"+"' ou '".join(type_imp)+"'..."
        print(msg)
        msg_rapport+=msg+"\n\n"
        
        cables = [cable[1] for cable in liaisons_infra_filtre]
        
        erreurs_c3a=[]
        for c3a,commandes in commandes_groupe:
            erreurs_c3a+=[
                ["","","",c3a.replace(commande_orange_path,""),num_prestation+ind_premiere_ligne_c3a+1,prestation[3].value,prestation[5].value]
                for (num_prestation,prestation) in enumerate(commandes)
                if prestation not in cables and prestation not in sorted(cables)
            ]
            
        entete_c3a=["","","","Fichier","Numéro de prestation","Numéro point A","Numéro point B"]
        resultat_c3a=["Nombre d'erreurs",str(len(erreurs_c3a))]
        
        nom_fichier=resultat_fichier(prefixe_resultat_controle2_2,resultat_c3a,entete_c3a,erreurs_c3a)     
        
        print()
        msg=msg_erreur_fichier(erreurs_c3a,nom_fichier)
        msg_rapport+=msg+"\n\n"
    
    print()    
    return msg_rapport

def version_c3a(msg_rapport=""):
    msg="Vérification de la version des C3A..."
    
    for f in get_c3a_list():
        c3a=get_feuille_commande(f)
        version=c3a.cell_value(rowx=6, colx=3).strip(' ')
    
        msg+=f.replace(commande_orange_path,"")+" :\n"
        if version == version_c3a_en_cours:
            msg+="La version du C3A est à jour."
        else:
            msg+="Version obsolète de la C3A. Veuillez mettre à jour à la version :"+version_c3a_en_cours
            
        msg+="\n\n"
    
    print(msg)
    msg_rapport+=msg+"\n"
    
    return msg_rapport

def corresp_poteau_c3a(msg_rapport=""):
    msg="Vérification de la correspondance entre les poteaux présents dans les C3A et les fiches poteaux..."
    print(msg)
    msg_rapport+=msg+"\n\n"
    
    poteaux = get_poteaux_fiche()
    commandes_groupe = get_commandes_groupe()
    commandes_joint = get_commandes_joint(commandes_groupe)
    liaisons_commandes = list(set(sum(liaisons_commande(commandes_joint),[])))
    
    erreurs=[]
    c3a_poteaux=[]
    
    for c3a,commandes in commandes_groupe:
        for (num_prestation,prestation) in enumerate(commandes):
            point_a=prestation[3].value.replace("/","_")
            point_b=prestation[5].value.replace("/","_")
            if point_a not in poteaux and point_a not in c3a_poteaux:
                erreurs.append([
                    "","","",
                    c3a.replace(commande_orange_path,""),
                    num_prestation+ind_premiere_ligne_c3a+1,
                    "A",
                    prestation[3].value
                ])
                c3a_poteaux.append(point_a)
                
            elif point_b not in poteaux and point_b not in c3a_poteaux:
                erreurs.append([
                    "","","",
                    c3a.replace(commande_orange_path,""),
                    num_prestation+ind_premiere_ligne_c3a+1,
                    "B",
                    prestation[5].value
                ])
                c3a_poteaux.append(point_b)
            else:
                pass
    
    entete=["","","","Fichier","Numéro de prestation","Identification A/B","Numéro de chambre / Appui aérien"]
    resultat=["Nombre d'erreurs",str(len(erreurs))]
    nom_fichier=resultat_fichier(prefixe_resultat_controle3,resultat,entete,erreurs)     
    
    print()
    msg=msg_erreur_fichier(erreurs,nom_fichier)
    msg_rapport+=msg+"\n\n"
    
    return msg_rapport