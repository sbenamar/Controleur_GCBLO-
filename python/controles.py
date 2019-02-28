#Pour l'explication des contrôles, se réferer au fichier Controlleur.xlsx dans le dossier Documentation
from fonctions import *

def update_conf_ctrl(config,type_lvrb,zone):
    exec(update_conf_exec)

#Contrôle 2 / Contrôle 3: possibilité de selection du/des contrôle(s) à réaliser
def corresp_cable_infra_c3a(parcours_infra=True,parcours_c3a=True):
    if not parcours_infra and not parcours_c3a:
        return 
    
    #Récupération des C3A sous plusieurs formats
    ##C3A pour le contrôle 3
    commandes_groupe = get_commandes_groupe()
    
    #C3A pour le contrôle 2
    liaisons_commandes = [[prestation[3],prestation[5]] for c3a,num,prestation in get_commande_groupe_ligne()]

    #Récupération du tableau de cable infra
    cable_infra = ouvrir_cable_infra(conf["cable_infra_csv_path"])

    #Table infra reformaté pour avoir les points A et B séparés et sélectionner les données utiles
    #On filtre selon le typ_imp, défini dans le fichier de définition
    liaisons_infra_filtre=[
        (i,cable["cm_id"].replace("_","/").split("=>")) for (i,cable) in enumerate(cable_infra)
        if cable["cm_typ_imp"] in type_imp
    ]

    cable_infra_fichier=chemin_fichier_application(conf["cable_infra_csv_path"])

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
        alim_rapport_csv(erreurs_c3a)

#Contrôle 1
def version_c3a(controle=True):
    num_controle=1
    
    if not controle:
        return 
    
    erreurs=[]
    #Parcours des c3a
    for f in get_c3a_list():
        c3a=get_feuille_commande(f)
        version=c3a.cell_value(rowx=5, colx=2).strip(' ')
        
        #Récupération du nom de fichier seulement, sans le chemin
        chemin=chemin_fichier_application(f)
        
        if version != version_c3a_en_cours:
            erreurs+=[modele_erreur(num_controle,[chemin,"",""])]
            
    alim_rapport_csv(erreurs)
    return len(erreurs)

def check_format_fiches_poteau(controle=True):
    if not controle:
        return 
    
    num_controle=25
    
    poteaux = get_poteaux_fiche()
    pattern = re.compile("^\d{5}_\w+")
    
    erreurs=[
            modele_erreur(
                num_controle,
                [poteau_list_libelle,"",poteau]
            )
            for poteau in poteaux if not pattern.match(poteau)
        ]
        
    alim_rapport_csv(erreurs)

#Contrôle 4
def corresp_poteau_c3a(controle=True):
    if not controle:
        return 
    
    num_controle=4
    
    poteaux = get_poteaux_nom()
    noms_poteaux =""
    
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
    return 

#Contrôle 7 / Contrôle 8 / Contrôle 12: possibilité de selection du/des contrôle(s) à réaliser
def regles_gcblo_c3a_majeurs(controle7=True,controle8=True,controle12=True):
    if not controle7 and not controle8 and not controle12:
        return 
    
    erreurs = []
    
    #Pour un algorithme plus lisible plus bas, les conditions d'erreur sont stockés ici en texte
    #Ils seront évalués par une fonction python
    condition7_1 = '("/" in prestation[3].value and prestation[3].value.split("/")[0].isdigit()'
    condition7_2 = ' and len(prestation[3].value.split("/")[0]) == 5)'
    condition7_3 = '("/" in prestation[5].value and prestation[5].value.split("/")[0].isdigit()'
    condition7_4 = ' and len(prestation[5].value.split("/")[0]) == 5)'

    condition8_1 = '(isinstance(prestation[6].value, (int, float)) or str(prestation[6].value).isdigit())'
    condition8_2 = ' and int(prestation[6].value) >= 1'
    
    condition12= 'prestation[2].value+prestation[4].value in combinaisons_types'

    commandes_groupe = get_commandes_groupe()
    
    for c3a,commandes in commandes_groupe:
        if controle7:
            num_controle=7
            for (num_prestation,prestation) in enumerate(commandes):
                if prestation[3].ctype and not(eval(condition7_1+condition7_2)):
                    erreurs+=[
                        modele_erreur_c3a(
                            num_controle,
                            chemin_fichier_application(c3a),
                            prestation[3].value,
                            prestation[5].value
                        )
                    ]
                elif prestation[5].ctype and not(eval(condition7_3+condition7_4)):
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

#controle 6
def info_sous_tubage(controle=True):
    if not controle:
        return
    
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

#controle 13,15,16,17,18,19,20,21,22,23,24
def valeurs_selon_liaisons(controles={}):
    
    #valeurs possibles des paramètres
    valeurs=[[False],[True],[False,True]]
    
    #Vérifier que le paramètre passé est conforme (liste entière et valeurs attendues)
    if list(set(controles.values())) not in valeurs or list(controles.keys()) != [13]+list(range(15,25)):
        try:
            raise ValueError(msg_erreur_controle14_25.format(str(controles)))
        except Exception as e:
            log(e,34)

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

#Contrôle 9
def verif_liste_colonnes(controle=True):
    if not controle:
        return
    
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

#Contrôles 10 et 11
def verif_c7_travaux_existe(controle10=True,controle11=True):
    if not controle10 and not controle11:
        return
    
    erreurs=[[],[]]
    commandes = get_commande_groupe_ligne()
    
    for c3a,num,prestation in commandes:
        condition_a=prestation[pos_xl("M")].value in condition_travaux_c7
        condition_b=prestation[pos_xl("N")].value in condition_travaux_c7
        
        #Si l'ouverture de la C7 échoue, on attrape l'exception et ça signie donc que la C7 n'existe pas
        #et donc que le contrôle 10 est en erreur
        if condition_a:
            #Contrôle 11 pour colonne M
            num_controle=11
            try:
                (nom_c7,appuis)=appui_from_c7_nom(c3a)
                if prestation[3].ctype and str(prestation[3].value).split("/")[-1] not in appuis:
                    erreurs[1].append(
                                    modele_erreur_c3a(
                                        num_controle,
                                        c3a,
                                        prestation[3].value,
                                        "",
                                        nom_c7,
                                        1
                                    )
                                )
            except IndexError as e:
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
            #Contrôle 11 pour colonne N
            num_controle=11
            try:
                (nom_c7,appuis)=appui_from_c7_nom(c3a)
                if prestation[5].ctype and str(prestation[5].value).split("/")[-1] not in appuis:
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
            except IndexError:
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

def verif_point_technique_c3a(controle=True):
    if not controle:
        return
    num_controle=5
    
    layer = QgsVectorLayer(conf["point_technique_path"], "POINT TECHNIQUE" , "ogr")
    
    if not layer.isValid():
        raise Exception("Shape non valide: {}".format(conf["point_technique_path"]))
    else:
        iter = layer.getFeatures()
        points_techniques=[
            (
                code_type_point(feature['pt_typephy'],feature['pt_prop']),
                format_id_pt(str(feature['NOM']),str(feature['CODE_INSEE'])) if 'CODE_INSEE' in feature else str(feature['NOM'])
            ) for feature in iter
        ]
            
        
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

        erreurs=[
            modele_erreur(
                num_controle,
                [chemin_fichier_application(conf["point_technique_path"]),c3a_list_libelle,commande[1].replace("_","/")]
            )
            for commande in commandes if commande[1] and (commande not in points_techniques and (commande[0],commande[1].split("_")[-1]) not in points_techniques)
        ]
        
        for commande in commandes:
            print(commande[1])
        
        alim_rapport_csv(erreurs)