#Pour l'explication des contrôles, se réferer au fichier Controlleur.xlsx dans le dossier Documentation
from controles_fct import *

#Mise à jour du dictionnaire de configuration avec le nouveaux généré après sélection du département
def update_conf_ctrl(config,type_lvrb,zone):
    exec(update_conf_exec)

#Contrôle 2 / Contrôle 3: possibilité de selection du/des contrôle(s) à réaliser
def corresp_cable_infra_c3a(parcours_infra=True,parcours_c3a=True):
    #On arrête la fonction si aucun contrôle n'est sélectionné
    if not parcours_infra and not parcours_c3a:
        return 0
    else:
        nb_controles=get_nb_controles(locals())

        
    #Récupération des C3A sous plusieurs formats
    ##C3A pour le contrôle 3
    commandes_groupe = get_commandes_groupe()
    
    #C3A pour le contrôle 2
    liaisons_commandes = [[prestation[3],prestation[5]] for c3a,num,prestation in get_commande_groupe_ligne()]

    #Récupération du tableau de cable infra
    cable_infra = ouvrir_cable_infra(conf["shape_cable_infra_path"])

    #Table infra reformaté pour avoir les points A et B séparés et sélectionner les données utiles
    #On filtre selon le typ_imp, défini dans le fichier de définition
    liaisons_infra_filtre=[
        (i,cable["cm_id"].replace("_","/").split("=>")) for (i,cable) in enumerate(cable_infra)
        if cable["cm_typ_imp"] in type_imp
    ]

    cable_infra_fichier=chemin_fichier_application(conf["shape_cable_infra_path"])

    #Début du contrôle 2, s'il est sélectionné
    if parcours_infra:
        #Initialisation du message d'erreur
        num_controle=2
        
        #Alimentation des lignes d'erreurs selon les conditions de contrôle,
        #complété par les variables préféfinies
        #On test la combinaison existe ou si la combinaison inverse existe
        erreurs_infra=[
            modele_erreur(
                num_controle,
                [cable_infra_fichier,c3a_list_libelle,(cable[0]+"=>"+cable[1]).replace("/","_")]
            )
            for (i,cable) in liaisons_infra_filtre
            if cable not in liaisons_commandes and cable[::-1] not in liaisons_commandes
        ]        

        #Ajout des lignes d'erreur dans le rapport csv
        alim_rapport_csv(erreurs_infra)
    
    #Début du contrôle 3, s'il est sélectionné
    if parcours_c3a:
        num_controle=3
        
        #On reprend la liste des cables, filtrée,
        ##en retirant l'identifiant pour n'avoir que l'information à comparer
        cables = [cable[1] for cable in liaisons_infra_filtre]
        
        #Création du tableau d'erreurs à afficher sous Excel selon l'entête
        erreurs_c3a=[]
        for c3a,commandes in commandes_groupe:
            erreurs_c3a+=[
                        modele_erreur_c3a(
                            num_controle,
                            c3a,
                            prestation[3].value,
                            prestation[5].value,
                            cable_infra_list_libelle
                        )
                for (num_prestation,prestation) in enumerate(commandes)
                if prestation not in cables and prestation not in sorted(cables)
            ]
            
        #Le rapport csv est mis à jour avec les eventuelles erreurs
        alim_rapport_csv(erreurs_c3a)
        
    return nb_controles
#Contrôle 1
def version_c3a(controle=True):
    num_controle=1
    
    if not controle:
        return 0
    else:
        nb_controles=get_nb_controles(locals())

    
    erreurs=[]
    #Parcours des c3a
    for f in get_c3a_list():
        c3a=get_feuille_commande(f)
        version=c3a.cell_value(rowx=5, colx=2).strip(' ')
        
        #Récupération du nom de fichier seulement, sans le chemin
        chemin=chemin_fichier_application(f)
        
        #Si la version n'est pas celle en cours, on génère une erreur
        if version != version_c3a_en_cours:
            erreurs+=[modele_erreur(num_controle,[chemin,"",""])]
            
    alim_rapport_csv(erreurs)
    return len(erreurs)

#Contrôle 25,57
def check_format_fiches_poteau(controle25=True,controle57=True):
    if not controle25 and not controle57:
        return 0
    else:
        nb_controles=get_nb_controles(locals())
    
    #Récupération du contenu du dossier poteau et des fiches poteau valides
    poteaux_tot = get_poteaux_fiche(True)
    poteaux = get_poteaux_fiche()
    
    if controle25:
        num_controle=25
        erreurs=[
                modele_erreur(
                    num_controle,
                    [poteau_list_libelle,"",poteau]
                )
                for poteau in poteaux_tot if not pattern_nom_point_souple.match(poteau)
            ]
            
        alim_rapport_csv(erreurs)
    
    if controle57:
        num_controle=57
        erreurs=[
                modele_erreur(
                    num_controle,
                    [poteau_list_libelle,"",poteau]
                )
                for poteau in poteaux_tot if poteau not in poteaux
            ]
            
        alim_rapport_csv(erreurs)
    return nb_controles

#Contrôle 4
def corresp_poteau_c3a(controle=True):
    if not controle:
        return 0
    else:
        nb_controles=get_nb_controles(locals())

    num_controle=4
    
    #Récupération des poteaux en ne récupérant que le nom de poteau,
    #sans les autres eventuels caractères afin de faciliter la comparaison et la reconnaissance
    poteaux = get_poteaux_nom()
    noms_poteaux =""
    
    #Récupération des lignes de C3A
    commandes_groupe = get_commandes_groupe()
    
    erreurs=[]

    for c3a,commandes in commandes_groupe:
        #Ce tableau sert à éviter d'ajouter des lignes doublons dans les erreurs
        #Dés qu'un poteau est manquant, on l'ajoute dans ce tableau et ce poteaux ne sera plus ajouté
        c3a_poteaux=[]

        for (num_prestation,prestation) in enumerate(commandes):
            
            #Permet d'avoir le même format pour comparer
            point_a=prestation[3].value.split("/")[-1] if "/" in str(prestation[3].value) else prestation[3].value
            point_b=prestation[5].value.split("/")[-1] if "/" in str(prestation[5].value) else prestation[5].value
            
            if prestation[2].value == "A" and str(point_a) not in poteaux and point_a not in c3a_poteaux and len(point_a):
                erreurs.append(
                    modele_erreur_c3a(num_controle,c3a,prestation[3].value,"",poteau_list_libelle,1)
                )
                c3a_poteaux.append(point_a)
                
            elif prestation[4].value == "A" and str(point_b) not in poteaux and point_b not in c3a_poteaux and len(point_b):
                erreurs.append(
                    modele_erreur_c3a(num_controle,c3a,"",prestation[5].value,poteau_list_libelle,1)
                )
                c3a_poteaux.append(point_b)
            else:
                pass

    alim_rapport_csv(erreurs)
    return nb_controles 

#Contrôle 58
def corresp_chambre_c3a(controle=True):
    if not controle:
        return 0
    else:
        nb_controles=get_nb_controles(locals())

    num_controle=58
    
    #Récupération des chambres en ne récupérant que le nom de chambres,
    #sans les autres eventuels caractères afin de faciliter la comparaison et la reconnaissance
    chambres = get_chambres_nom()
    noms_chambres =""
    
    #Récupération des lignes de C3A
    commandes_groupe = get_commandes_groupe()
    
    erreurs=[]

    for c3a,commandes in commandes_groupe:
        #Ce tableau sert à éviter d'ajouter des lignes doublons dans les erreurs
        #Dés qu'une chambre est manquante, on l'ajoute dans ce tableau et cette chambre ne sera plus ajoutée
        c3a_chambres=[]

        for (num_prestation,prestation) in enumerate(commandes):
            
            #Permet d'avoir le même format pour comparer
            point_a=prestation[3].value.split("/")[-1] if "/" in str(prestation[3].value) else prestation[3].value
            point_b=prestation[5].value.split("/")[-1] if "/" in str(prestation[5].value) else prestation[5].value
            
            if prestation[2].value == "C" and str(point_a) not in chambres and point_a not in c3a_chambres and len(point_a):
                erreurs.append(
                    modele_erreur_c3a(num_controle,c3a,prestation[3].value,"",chambre_list_libelle,1)
                )
                c3a_chambres.append(point_a)
                
            elif prestation[4].value == "C" and str(point_b) not in chambres and point_b not in c3a_chambres and len(point_b):
                erreurs.append(
                    modele_erreur_c3a(num_controle,c3a,"",prestation[5].value,chambre_list_libelle,1)
                )
                c3a_chambres.append(point_b)
            else:
                pass

    alim_rapport_csv(erreurs)
    return nb_controles 

#Contrôle 7 / Contrôle 8 / Contrôle 12: possibilité de selection du/des contrôle(s) à réaliser
def regles_gcblo_c3a_majeurs(controle7=True,controle8=True,controle12=True):
    if not controle7 and not controle8 and not controle12:
        return 0
    else:
        nb_controles=get_nb_controles(locals())

    
    erreurs = []
    
    #Pour un algorithme plus lisible plus bas, les conditions d'erreur sont stockés ici en texte
    #Ils seront évalués par une fonction python
    condition7_1 = 'pattern_nom_point.match(str(prestation[3].value))'
    condition7_3 = 'pattern_nom_point.match(str(prestation[5].value))'

    condition8_1 = '(isinstance(prestation[6].value, (int, float)) or str(prestation[6].value).isdigit())'
    condition8_2 = ' and int(prestation[6].value) >= 1'
    
    condition12= 'prestation[2].value+prestation[4].value in combinaisons_types'

    commandes_groupe = get_commandes_groupe()
    
    for c3a,commandes in commandes_groupe:
        if controle7:
            num_controle=7
            for (num_prestation,prestation) in enumerate(commandes):
                if prestation[3].ctype and not(eval(condition7_1)):
                    erreurs+=[
                        modele_erreur_c3a(
                            num_controle,
                            chemin_fichier_application(c3a),
                            prestation[3].value,
                            prestation[5].value
                        )
                    ]
                elif prestation[5].ctype and not(eval(condition7_3)):
                    erreurs+=[
                        modele_erreur_c3a(
                            num_controle,
                            chemin_fichier_application(c3a),
                            prestation[3].value,
                            prestation[5].value
                        )
                    ]

        if controle8:
            num_controle=8
            erreurs+=[
                modele_erreur_c3a(
                            num_controle,
                            chemin_fichier_application(c3a),
                            prestation[3].value,
                            prestation[5].value
                        )
                for (num_prestation,prestation) in enumerate(commandes)
                if not(eval(condition8_1+condition8_2))
            ]

        if controle12:
            num_controle=12           
            erreurs+=[
                modele_erreur_c3a(
                            num_controle,
                            chemin_fichier_application(c3a),
                            prestation[2].value,
                            prestation[4].value
                        )
                for (num_prestation,prestation) in enumerate(commandes)
                if eval(condition12)
            ]

    alim_rapport_csv(erreurs)
    return nb_controles

#controle 6
def info_sous_tubage(controle=True):
    if not controle:
        return 0
    else:
        nb_controles=get_nb_controles(locals())

    
    num_controle=6
    
    commandes = get_commande_groupe_ligne()
    
    erreurs=[
        modele_erreur_c3a(
            num_controle,
            chemin_fichier_application(c3a),
            prestation[3].value,
            prestation[5].value
        )
        for c3a,num,prestation in commandes
        if not(prestation[8].ctype or len(prestation[8].value))
        and (prestation[9].ctype or len(prestation[9].value))
    ]
    
    alim_rapport_csv(erreurs)
    return nb_controles

#controle 13,15,16,17,18,19,20,21,22,23,24
def valeurs_selon_liaisons(controles={}):
    
    #valeurs possibles des paramètres
    valeurs=[[False],[True],[False,True]]
    
    #Vérifier que le paramètre passé est conforme (liste entière et valeurs attendues)
    if list(set(controles.values())) not in valeurs or list(controles.keys()) != [13]+list(range(15,25)):
        try:
            raise ValueError(str(controles))
        except Exception as e:
            log(e,34)
    
    #On stoppe si aucun contrôle n'est sélectionné       
    if not any(controles.values()):
        return 0
    else:
        nb_controles=get_nb_controles(locals())

    
    #Initialisation du tableau d'erreur organisé par numéro de contrôle, afin de tout afficher à la suite
    erreurs={k:[] for k in controles.keys()}
    
    commandes = get_commande_groupe_ligne()
    
    for c3a,num,prestation in commandes:
        liaison=combinaison_type.format(prestation[2].value,prestation[4].value)
 
        if liaison == liaison_c_c:
            #contrôle 13
            num_controle=13
            
            diametre=prestation[7].value
            condition1=diametre in diametre_alveole_liste_c_c
            condition2_1=isnumber(diametre)
            condition2=condition2_1 and str(int(diametre)) in diametre_alveole_liste_c_c

            if controles[num_controle] and not(condition1 or (condition2)):
                erreurs[num_controle].append(
                                        modele_erreur_c3a(
                                            num_controle,
                                            c3a,
                                            prestation[3].value,
                                            prestation[5].value
                                            )
                                        )
        if liaison == liaison_c_imb:
            #contrôle 15
            num_controle=15
            if controles[num_controle] and prestation[pos_xl("H")].value != "adduction":
                erreurs[num_controle].append(
                                        modele_erreur_c3a(
                                            num_controle,
                                            c3a,
                                            prestation[3].value,
                                            prestation[5].value
                                            )
                                        )
            #contrôle 16
            num_controle=16
            if controles[num_controle] and prestation[pos_xl("F")].ctype:
                erreurs[num_controle].append(
                                        modele_erreur_c3a(
                                            num_controle,
                                            c3a,
                                            prestation[3].value,
                                            prestation[5].value
                                            )
                                        )
            #contrôle 17
            num_controle=17
            condition=controles[num_controle] and isnumber(prestation[pos_xl("G")])
            if condition and int(prestation[pos_xl("G")].value) != 7:
                erreurs[num_controle].append(
                                        modele_erreur_c3a(
                                            num_controle,
                                            c3a,
                                            prestation[3].value,
                                            prestation[5].value
                                            )
                                        )
                
        if liaison == liaison_c_f:    
            #contrôle 18
            num_controle=18
            if controles[num_controle] and prestation[pos_xl("F")].ctype:
                erreurs[num_controle].append(
                                        modele_erreur_c3a(
                                            num_controle,
                                            c3a,
                                            prestation[3].value,
                                            prestation[5].value
                                            )
                                        )  
            #contrôle 19
            num_controle=19
            if controles[num_controle] and prestation[pos_xl("H")].value != "transition":
                erreurs[num_controle].append(
                                        modele_erreur_c3a(
                                            num_controle,
                                            c3a,
                                            prestation[3].value,
                                            prestation[5].value
                                            )
                                        )
            
            #contrôle 20
            num_controle=20
            condition=controles[num_controle] and isnumber(prestation[pos_xl("G")])
            if condition and int(prestation[pos_xl("G")].value) != 7:
                erreurs[num_controle].append(
                                        modele_erreur_c3a(
                                            num_controle,
                                            c3a,
                                            prestation[3].value,
                                            prestation[5].value
                                            )
                                        )
                
        if liaison in (liaison_c_p,laison_c_pt):
            #contrôle 21
            num_controle=21
            if controles[num_controle] and prestation[pos_xl("H")].value != "transition":
                erreurs[num_controle].append(
                                        modele_erreur_c3a(
                                            num_controle,
                                            c3a,
                                            prestation[3].value,
                                            prestation[5].value
                                            )
                                        )
                
        if liaison == laison_c_pt:
            #contrôle 22
            num_controle=22
            if controles[num_controle] and prestation[pos_xl("F")].ctype:
                erreurs[num_controle].append(
                                        modele_erreur_c3a(
                                            num_controle,
                                            c3a,
                                            prestation[3].value,
                                            prestation[5].value
                                            )
                                        )
        if liaison == laison_ct_p:
            #contrôle 23
            num_controle=23
            if controles[num_controle] and (prestation[pos_xl("B")].ctype or prestation[pos_xl("D")].ctype):
                erreurs[num_controle].append(
                                        modele_erreur_c3a(
                                            num_controle,
                                            c3a,
                                            prestation[3].value,
                                            prestation[5].value
                                            )
                                        )
            #contrôle 24
            num_controle=24
            if controles[num_controle] and prestation[pos_xl("H")].value != "transition":
                erreurs[num_controle].append(
                                        modele_erreur_c3a(
                                            num_controle,
                                            c3a,
                                            prestation[3].value,
                                            prestation[5].value
                                            )
                                        )
    
    #Ecriture des erreurs pour chaque contrôle selectionné
    for ctrl in set(erreurs.keys()):
        alim_rapport_csv(erreurs[ctrl])
    
    return nb_controles

#Contrôle 9
def verif_liste_colonnes(controle=True):
    if not controle:
        return 0
    else:
        nb_controles=get_nb_controles(locals())

    
    num_controle=9
    commandes = get_commande_groupe_ligne()
    
    erreurs=[
        modele_erreur_c3a(
                        num_controle,
                        c3a,
                        prestation[3].value,
                        prestation[5].value
        )
        for c3a,num,prestation in commandes
        if (prestation[pos_xl("C")].ctype
            and not prestation[pos_xl("C")].value in type_chambre_appui
            )
        or (prestation[pos_xl("E")].ctype
            and not prestation[pos_xl("E")].value in type_chambre_appui
            )
        or (prestation[pos_xl("H")].ctype
            and not(prestation[pos_xl("H")].value in diametre_alveole_liste
                 or (
                    isnumber(prestation[pos_xl("H")].value)
                    and str(int(prestation[pos_xl("H")].value)) in diametre_alveole_liste
                    )
                )
           )
        or (prestation[pos_xl("I")].ctype
            and not prestation[pos_xl("I")].value in tubage_rigide_liste
            )
        or (prestation[pos_xl("J")].ctype
            and not prestation[pos_xl("J")].value in diametre_tube_liste
            )
        or (prestation[pos_xl("K")].ctype
            and (
                isnumber(prestation[pos_xl("K")].value)
                and not float(prestation[pos_xl("K")].value) in diametre_cable_liste
                )
            or not isnumber(prestation[pos_xl("K")].value)
           )
        or (prestation[pos_xl("M")].ctype
            and not prestation[pos_xl("M")].value in travaux_liste
            )
        or (prestation[pos_xl("N")].ctype
            and not prestation[pos_xl("N")].value in travaux_liste
            )
        or (prestation[pos_xl("O")].ctype
            and not prestation[pos_xl("O")].value in installation_liste
            )
        or (prestation[pos_xl("P")].ctype
            and not prestation[pos_xl("P")].value in refus_res_liste
            )
    ]

    alim_rapport_csv(erreurs)
    return nb_controles

#Contrôle 10 et 11 et 38 
def verif_c7_travaux_existe(controle10=True,controle11=True,controle38=True):
    if not(controle10 or controle11 or controle38):
        return 0
    else:
        nb_controles=get_nb_controles(locals())

    erreurs=[[],[],[]]
    commandes = get_commande_groupe_ligne()
    
    for c3a,num,prestation in commandes:
        condition_a=prestation[pos_xl("M")].value in condition_travaux_c7
        condition_b=prestation[pos_xl("N")].value in condition_travaux_c7
        appuis=[]
        
        #Si l'ouverture de la C7 échoue, on attrape l'exception et ça signie donc que la C7 n'existe pas
        #et donc que le contrôle 10 est en erreur
        if condition_a:
            #Contrôle 11 et 38 pour colonne M
            num_controle=38
            try:
                appuis=appui_from_c7_nom()
                if not appuis:
                    raise IndexError("La liste des c7 est vide")
                
                erreurs[2].extend([
                        modele_erreur(num_controle,[chemin_fichier_application(nom_c7),"",appui])
                        for (nom_c7,appui) in appui_from_c7()
                        if not pattern_nom_point_souple.match(str(appui))
                ])
                
                num_controle=11
                if prestation[3].ctype and str(prestation[3].value).split("/")[-1] not in list(zip(*appuis))[1]:
                    erreurs[1].append(
                                    modele_erreur_c3a(
                                        num_controle,
                                        c3a,
                                        prestation[3].value,
                                        "",
                                        c7_list_libelle,
                                        1
                                    )
                                )
            except (IndexError,FileNotFoundError) as e:
                #Contrôle 10 pour colonne M
                num_controle=10
                erreurs[0].append(
                                    modele_erreur_c3a(
                                        num_controle,
                                        c3a,
                                        prestation[3].value,
                                        "",
                                        c7_list_libelle,
                                        1
                                    )
                                )
                     
        if condition_b:
            #Contrôle 11 et 38 pour colonne N
            num_controle=38
            try:
                if not appuis:
                    appuis=appui_from_c7_nom()
                    if not appuis:
                        raise IndexError("La liste des c7 est vide")
                
                    erreurs[2].extend([
                        modele_erreur(num_controle,[chemin_fichier_application(nom_c7),"",appui])
                        for (nom_c7,appui) in appui_from_c7()
                        if not pattern_nom_point_souple.match(str(appui))
                    ])
                
                num_controle=11
                if prestation[5].ctype and str(prestation[5].value).split("/")[-1] not in list(zip(*appuis))[1]:
                    erreurs[1].append(
                                    modele_erreur_c3a(
                                        num_controle,
                                        c3a,
                                        "",
                                        prestation[5].value,
                                        nom_c7,
                                        1
                                    )
                                )
            except (IndexError,FileNotFoundError) as e:
                #Contrôle 10 pour colonne N
                num_controle=10
                erreurs[0].append(
                                    modele_erreur_c3a(
                                        num_controle,
                                        c3a,
                                        "",
                                        prestation[5].value,
                                        c7_list_libelle,
                                        1
                                    )
                                )
                
    alim_rapport_csv(erreurs[0])
    alim_rapport_csv(erreurs[1])
    alim_rapport_csv(erreurs[2])
    return nb_controles

#Contrôle 5
def verif_point_technique_c3a(controle5=True):
    if not controle5:
        return 0
    else:
        nb_controles=get_nb_controles(locals())
    
    shape,list_point_technique = get_shape(conf["shape_point_technique_path"],shape_point_technique_nom)
        
    num_controle=5
    
    #Récupération des points techniques en uniformisant la forme du nom selon l'insee
    try:
        points_techniques=[
            (
                code_type_point(ligne['pt_typephy'],ligne['pt_prop']),
                format_id_pt(str(ligne['NOM']),str(ligne['CODE_INSEE'])) if ligne.fieldNameIndex('CODE_INSEE') != -1 else str(ligne['NOM'])
            ) for ligne in list_point_technique
        ]
    except Exception as e:
        log(e,36)
        
    #Liste des lignes de C3A en séparant en 2 lignes les points A et B
    commandes = reduce(
            lambda x,y:x+y,
            [
                (
                    (str(prestation[2].value),str(prestation[3].value).replace("/","_")),
                    (str(prestation[4].value),str(prestation[5].value).replace("/","_"))
                )
                for c3a,num,prestation in get_commande_groupe_ligne()
            ]
    )
    
    pt_ids = list(zip(*points_techniques))[1]
    
    erreurs5=[
        modele_erreur(
            num_controle,
            [chemin_fichier_application(conf["shape_point_technique_path"]),c3a_list_libelle,commande[1].replace("_","/")]
        )
        for commande in commandes
        if commande[1]
        and commande not in points_techniques
        and (commande[0],commande[1].split("_")[-1]) not in points_techniques
        and (commande[1] in pt_ids or commande[1].split("_")[-1] in pt_ids)
    ]
    
    alim_rapport_csv(erreurs5)
    return nb_controles

#Contrôles 26,27,28,29,30,31,32,33,34,35,36,37,40
def verif_struct_shape(controles={}):
    
    #valeurs possibles des paramètres
    valeurs=[[False],[True],[False,True]]
    
    #Vérifier que le paramètre passé est conforme (liste entière et valeurs attendues)
    if list(set(controles.values())) not in valeurs or list(controles.keys()) != list(range(26,38))+[40]:
        try:
            raise ValueError(str(controles))
        except Exception as e:
            log(e,35)
    
    #On stoppe si aucun contrôle n'est sélectionné       
    if not any(controles.values()):
        return 0
    else:
        nb_controles=get_nb_controles(locals())
    
    num_controle=26
    if controles[num_controle]:
        verif_champs_shape(num_controle,conf["shape_point_technique_path"],shape_point_technique_nom,champs_point_technique,controles[40])
        
    num_controle=27
    if controles[num_controle]:
        verif_champs_shape(num_controle,conf["shape_prises_path"],shape_prises_nom,champs_prises,controles[40])
    
    num_controle=28
    if controles[num_controle]:
        verif_champs_shape(num_controle,conf["shape_sro_path"],shape_sro_nom,champs_sro,controles[40])
    
    num_controle=29
    if controles[num_controle]:
        verif_champs_shape(num_controle,conf["shape_boitier_path"],shape_boitier_nom,champs_boitier,controles[40])
    
    num_controle=30
    if controles[num_controle]:
        verif_champs_shape(num_controle,conf["shape_infra_path"],shape_infra_nom,champs_infra,controles[40])
        
    num_controle=31
    if controles[num_controle]:
        verif_champs_shape(num_controle,conf["shape_racco_client_path"],shape_racco_client_nom,champs_racco_client,controles[40])
        
    num_controle=32
    if controles[num_controle]:
        verif_champs_shape(num_controle,conf["shape_cable_path"],shape_cable_nom,champs_cable,controles[40])
        
    num_controle=33
    if controles[num_controle]:
        verif_champs_shape(num_controle,conf["shape_zpbo_path"],shape_zpbo_nom,champs_zpbo,controles[40])
        
    num_controle=34
    if controles[num_controle]:
        verif_champs_shape(num_controle,conf["shape_zsro_path"],shape_zsro_nom,champs_zsro,controles[40])
        
    num_controle=35
    if controles[num_controle]:
        verif_champs_shape(num_controle,conf["shape_zpec_path"],shape_zpec_nom,champs_zpec,controles[40])
        
    num_controle=36
    if controles[num_controle]:
        verif_champs_shape(num_controle,conf["shape_znro_path"],shape_znro_nom,champs_znro,controles[40])
        
    num_controle=37
    if controles[num_controle]:
        verif_champs_shape(num_controle,conf["shape_nro_path"],shape_nro_nom,champs_nro,controles[40])
    
    return nb_controles

#Contrôle 39
def verif_couches_exist(controle=True):
    if not controle:
        return 0
    else:
        nb_controles=get_nb_controles(locals())
    
    num_controle=39
    erreurs=[
        modele_erreur(
            num_controle,
            [chemin_fichier_application(conf["shape_{}_path".format(point)]),"",""]
        )
        for point in liste_couches if not get_shape(conf["shape_{}_path".format(point)],exec("shape_{}_nom".format(point)),True)
    ]
    
    alim_rapport_csv(erreurs)
    return nb_controles

#Contrôle 48
def verif_plan_tirage_exist(controle=True):
    if not controle:
        return 0
    else:
        nb_controles=get_nb_controles(locals())
    
    num_controle=48
    path=conf["projet_path"]
    fichier=chemin_fichier_application(path)
    erreurs=[
        modele_erreur(
            num_controle,
            [fichier if fichier else projet_dossier_libelle,"",""]
        )
    ] if not find_plan_tirage() else []
    
    alim_rapport_csv(erreurs)
    return nb_controles

#Contrôle 47
def verif_dossier_qgis_exist(controle=True):
    if not controle:
        return 0
    else:
        nb_controles=get_nb_controles(locals())
    
    num_controle=47
    path=conf["projet_projetQGIS_path"]
    fichier=chemin_fichier_application(path)
    erreurs=[
        modele_erreur(
            num_controle,
            [fichier if fichier else projet_dossier_libelle,"",""]
        )
    ] if not all([x in ''.join(glob.glob(os.path.join(path,"*"))) for x in ["LAYERS",".qgs"]]) else []
    
    alim_rapport_csv(erreurs)
    return nb_controles

#Contrôle 53
def verif_fichier_appui_orange_pt(controle=True):
    if not controle:
        return 0
    else:
        nb_controles=get_nb_controles(locals())
    
    num_controle=53
    
    shape,list_point_technique = get_shape(conf["shape_point_technique_path"],shape_point_technique_nom)
    
    #Récupération des points techniques en uniformisant la forme du nom selon l'insee
    #un poteau est trouvable mais avec le mauvais INSEE...
    points_techniques=[
        [
            format_id_pt(str(ligne['NOM']),str(ligne['CODE_INSEE'])) if ligne.fieldNameIndex('CODE_INSEE') != -1 else str(ligne['NOM']),
            str(ligne['NOM']).split("_")[-1]
        ]
        for ligne in list_point_technique
        if code_type_point(ligne['pt_typephy'],ligne['pt_prop']) == "A"
    ]
    
    appuis=get_poteaux_fiche()+get_poteaux_nom()
    
    erreurs=[
        modele_erreur(
            num_controle,
            [chemin_fichier_application(conf["shape_point_technique_path"]),poteau_list_libelle,appui[0]]
        )
        for appui in points_techniques if appui[0] not in appuis and (appui[1] not in appuis or True)
    ]
    
    alim_rapport_csv(erreurs)
    return nb_controles

#Contrôle 54
def verif_fichier_chambre_pt(controle=True):
    if not controle:
        return 0
    else:
        nb_controles=get_nb_controles(locals())
    
    num_controle=54
    
    shape,list_point_technique = get_shape(conf["shape_point_technique_path"],shape_point_technique_nom)
    
    #Récupération des points techniques en uniformisant la forme du nom selon l'insee
    #une chambre est trouvable mais avec le mauvais INSEE...
    points_techniques=[
        [
            format_id_pt(str(ligne['NOM']),str(ligne['CODE_INSEE'])) if ligne.fieldNameIndex('CODE_INSEE') != -1 else str(ligne['NOM']),
            str(ligne['NOM']).split("_")[-1]
        ]
        for ligne in list_point_technique
        if ligne['pt_typephy'] == "CHAMBRE"
    ]
    
    chambres=get_chambres_fiche()+get_chambres_nom()
    
    erreurs=[
        modele_erreur(
            num_controle,
            [chemin_fichier_application(conf["shape_point_technique_path"]),chambre_list_libelle,chambre[0]]
        )
        for chambre in points_techniques if chambre[0] not in chambres and (chambre[1] not in chambres or True)
    ]
     
    alim_rapport_csv(erreurs)
    return nb_controles

#Contrôle 52
def verif_fichier_enedis_pt(controle=True):
    if not controle:
        return 0
    else:
        nb_controles=get_nb_controles(locals())
    
    num_controle=52
    
    shape,list_point_technique = get_shape(conf["shape_point_technique_path"],shape_point_technique_nom)
    
    nb_points_techniques=len([
        ligne
        for ligne in list_point_technique
        if ligne['pt_prop'] == "ENEDIS"
    ])
    
    nb_fichiers=len(get_contenu_comac())
    
    erreurs=[
        modele_erreur(
            num_controle,
            [chemin_fichier_application(conf["shape_point_technique_path"]),dossier_comac_libelle,""]
        )
    ] if nb_points_techniques and not nb_fichiers else []
     
    alim_rapport_csv(erreurs)
    return nb_controles

#Contrôle 56
def verif_synthese_etude(controle=True):
    if not controle:
        return 0
    else:
        nb_controles=get_nb_controles(locals())
    
    num_controle=56
    
    erreurs=[
        modele_erreur(
            num_controle,
            [chemin_fichier_application(conf["syntheseEtude_path"]),"",""]
        )
    ] if not find_synthese_etude() else []
     
    alim_rapport_csv(erreurs)
    return nb_controles

#Contrôle 49,50
def verif_synoptique(controle49=True,controle50=True):
    if not controle49 and not controle50:
        return 0
    else:
        nb_controles=get_nb_controles(locals())
    
    if controle49:
        num_controle=49
        
        erreurs=[
            modele_erreur(
                num_controle,
                [chemin_fichier_application(conf["optique_path"]),"",""]
            )
        ] if not find_synoptique_fichier("cable") else []
        
        alim_rapport_csv(erreurs)
        
    if controle50:
        num_controle=50
        
        erreurs=[
            modele_erreur(
                num_controle,
                [chemin_fichier_application(conf["optique_path"]),"",""]
            )
        ] if not find_synoptique_fichier("fibre") else []
        
        alim_rapport_csv(erreurs)
        
    return nb_controles

#Contrôle 46
def verif_bpu(controle=True):
    if not controle:
        return 0
    else:
        nb_controles=get_nb_controles(locals())
    
    num_controle=46
    
    erreurs=[
        modele_erreur(
            num_controle,
            [chemin_fichier_application(conf["financier_path"]),"",""]
        )
    ] if find_bpu() != 1 else []
     
    alim_rapport_csv(erreurs)
    return nb_controles

#Contrôle 45
def verif_convention(controle=True):
    if not controle:
        return 0
    else:
        nb_controles=get_nb_controles(locals())
    
    num_controle=45
    erreurs=[
        modele_erreur(
            num_controle,
            [chemin_fichier_application(conf["conventions_path"]),"",""]
        )
    ] if find_recap_conventions() != 1 else []
     
    alim_rapport_csv(erreurs)
    return nb_controles

#Contrôle 51
def verif_boitier_planboite(controle=True):
    if not controle:
        return 0
    else:
        nb_controles=get_nb_controles(locals())
    
    shape,boitiers = get_shape(conf["shape_boitier_path"],shape_boitier_nom)
    plansboite=get_noms_planboite()
    
    num_controle=51   

    erreurs=[
        modele_erreur(
            num_controle,
            [chemin_fichier_application(conf["shape_boitier_path"]),chemin_fichier_application(conf["optique_plansBoite_path"]),boitier["bp_etiquet"] or "N/D"]
        )
        for boitier in boitiers if boitier["bp_etiquet"] not in plansboite
    ]
    
    alim_rapport_csv(erreurs)
    return nb_controles

#Contrôle 44
def verif_pmv_conduite_gc(controle=True):
    if not controle:
        return 0
    else:
        nb_controles=get_nb_controles(locals())
    
    num_controle=44
    
    infras = get_shape(conf["shape_infra_path"],shape_infra_nom)[1]
    communes = [commune for commune in get_shape(conf["shape_commune_path"],shape_commune_nom)[1]]
    communes_err = []
    erreurs = []
    
    for inf in infras:
        if inf["cm_avct"] in codes_gc_prevu:
            for comm in communes:
                if comm.geometry().contains(inf.geometry()) and comm["NOM"] not in communes_err and not find_pmv_souterrain(comm["NOM"].upper()):
                    erreurs+=[
                        modele_erreur(
                            num_controle,
                            [
                                chemin_fichier_application(conf["shape_infra_path"]),
                                chemin_fichier_application(conf["administratif_PMV_path"]),
                                "{} ({})".format(comm["NOM"],inf["cm_code"])
                             ]
                        ) 
                    ]
                    communes_err.append(comm["NOM"])
    
    alim_rapport_csv(erreurs)
    return nb_controles

#Contrôle 43
def verif_pmv_aerien_poteau_etat(controle=True):
    if not controle:
        return 0
    else:
        nb_controles=get_nb_controles(locals())
    
    num_controle=43
    
    pts = get_shape(conf["shape_point_technique_path"],shape_infra_nom)[1]
    communes = [commune for commune in get_shape(conf["shape_commune_path"],shape_commune_nom)[1]]
    communes_err = []
    erreurs = []
    
    for pt in pts:
        if pt["ETAT"] in codes_poteau_chng_rplc:
            for comm in communes:
                if comm.geometry().contains(pt.geometry()) and comm["NOM"] not in communes_err and not find_pmv_poteau(comm["NOM"].upper()):
                    erreurs+=[
                        modele_erreur(
                            num_controle,
                            [
                                chemin_fichier_application(conf["shape_point_technique_path"]),
                                chemin_fichier_application(conf["administratif_PMV_path"]),
                                "{} ({})".format(
                                    comm["NOM"],
                                    format_id_pt(str(pt['NOM']),str(pt['CODE_INSEE'])) if pt.fieldNameIndex('CODE_INSEE') != -1 else str(pt['NOM']))
                             ]
                        ) 
                    ]
                    communes_err.append(comm["NOM"])
    
    alim_rapport_csv(erreurs)
    return nb_controles

#Contrôle 41
def verif_dt_gc(controle=True):
    if not controle:
        return 0
    else:
        nb_controles=get_nb_controles(locals())
    
    num_controle=41

    infras = get_shape(conf["shape_infra_path"],shape_infra_nom)[1]
    communes = [commune for commune in get_shape(conf["shape_commune_path"],shape_commune_nom)[1]]
    communes_err = []
    erreurs = []
    
    for inf in infras:
        if inf["cm_avct"] in codes_gc_prevu:
            for comm in communes:
                nom_commune=comm["NOM"].upper().replace("-"," ")
                if comm.geometry().contains(inf.geometry()) and comm["NOM"] not in communes_err and not len(get_dt_pdf(nom_commune)):

                    erreurs+=[
                        modele_erreur(
                            num_controle,
                            [
                                chemin_fichier_application(conf["administratif_DT_path"]),
                                chemin_fichier_application(conf["shape_point_technique_path"]),
                                "{} ({})".format(comm["NOM"],inf["cm_code"])
                             ]
                        ) 
                    ]
                    communes_err.append(comm["NOM"])
    
    alim_rapport_csv(erreurs)
    return nb_controles

#Contrôle 55
def verif_d15_problematique(controle=True):
    if not controle:
        return 0
    else:
        nb_controles=get_nb_controles(locals())
    
    num_controle=55

    infras = [inf for inf in get_shape(conf["shape_infra_path"],shape_infra_nom)[1]]
    pts = [pt for pt in get_shape(conf["shape_point_technique_path"],shape_point_technique_nom)[1]]
    pts_pb = []
    infras_pb = []
    
    pts_d15 = pts_from_d15()
    
    for inf in infras:
        if inf["ETAT"] in codes_infra_problematique:
            troncon_pb = ["",""]
            for pt in pts:
                if pt["pt_nd_code"] == inf["cm_ndcode1"]:
                    troncon_pb[0]=pt["NOM"]
                elif pt["pt_nd_code"] == inf["cm_ndcode2"]:
                    troncon_pb[1]=pt["NOM"]
                if pt["ETAT"] in codes_infra_problematique and pt["NOM"] not in pts_pb and not([pt["NOM"],""] in pts_d15 or ["",pt["NOM"]] in pts_d15):
                    pts_pb.append(pt["NOM"])
            if [inf["cm_code"],troncon_pb] not in infras_pb and not(troncon_pb in pts_d15):
                infras_pb.append([inf["cm_code"],troncon_pb])
                
    erreurs_pt=[
                modele_erreur(
                    num_controle,
                    [
                        chemin_fichier_application(conf["shape_point_technique_path"]),
                        chemin_fichier_application(conf["FOA_annexeD15_path"]),
                        pt_nom
                    ]
                ) for pt_nom in pts_pb
            ]
    
    erreurs_inf=[
                modele_erreur(
                    num_controle,
                    [
                        chemin_fichier_application(conf["shape_infra_path"]),
                        chemin_fichier_application(conf["FOA_annexeD15_path"]),
                        "{} ({} => {})".format(code,pt1,pt2)
                    ]
                ) for (code,(pt1,pt2)) in infras_pb
            ]
    
    alim_rapport_csv(erreurs_pt)
    alim_rapport_csv(erreurs_inf)
    return nb_controles

#Contrôle 42
def verif_l49_gc_1000(controle=True):
    if not controle:
        return 0
    else:
        nb_controles=get_nb_controles(locals())
    
    num_controle=42

    infras = get_shape(conf["shape_infra_path"],shape_infra_nom)[1]
    communes = [commune for commune in get_shape(conf["shape_commune_path"],shape_commune_nom)[1]]
    communes_err = []
    erreurs = []
    
    for inf in infras:
        if float(inf["cm_long"]) > 1000:
            for comm in communes:
                nom_commune=comm["NOM"]
                if comm.geometry().contains(inf.geometry()) and comm["NOM"] not in communes_err and not get_l49_fichiers_complets(nom_commune):
                    erreurs+=[
                        modele_erreur(
                            num_controle,
                            [
                                chemin_fichier_application(conf["shape_point_technique_path"]),
                                chemin_fichier_application(conf["administratif_L49_path"]),
                                "{} ({})".format(comm["NOM"],inf["cm_code"])
                             ]
                        ) 
                    ]
                    communes_err.append(comm["NOM"])
    
    alim_rapport_csv(erreurs)
    return nb_controles

#Contrôle 2 et contrôle 3 [nouvelle version sans cable-infra]
def verif_cable_c3a(controle2=True,controle3=True):
    if not controle2 and not controle3:
        return 0
    else:
        nb_controles=get_nb_controles(locals())
    
    liaisons_commandes = ["{}=>{}".format(prestation[3].value.replace("/","_"),prestation[5].value.replace("/","_")) for c3a,num,prestation in get_commande_groupe_ligne()]
    
    cbl_inf = get_cable_infra_shp(True)
    
    num_controle=2
    
    erreurs_2 = [
        modele_erreur(
            num_controle,
            [
                chemin_fichier_application(conf["listeC3A_C3A_path"]),
                chemin_fichier_application(conf["shape_cable_path"]),
                troncon
             ]
        )
        for troncon in set(cbl_inf)-set(liaisons_commandes)
    ]
    
    num_controle=3
    
    erreurs_3 = [
        modele_erreur(
            num_controle,
            [
                chemin_fichier_application(conf["shape_cable_path"]),
                chemin_fichier_application(conf["listeC3A_C3A_path"]),
                troncon
             ]
        )
        for troncon in set(liaisons_commandes)-set(cbl_inf)
    ]
    
    if controle2:
        alim_rapport_csv(erreurs_2)
    if controle3:
        alim_rapport_csv(erreurs_3)
    return nb_controles