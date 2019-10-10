from fonctions import *

#Mise à jour du dictionnaire de configuration avec le nouveaux généré après sélection du département
def update_conf_ctrl_fct(config,type_lvrb,zone):
    exec(update_conf_exec)

#Récupérer la liste des appuis contenus dans la C7
def appui_from_c7(c3a=False):
    if c3a:
        (nom_c7,feuille) = get_feuille_c7(c3a)
        cmd_c7 = ouvrir_c7(feuille)
        return (nom_c7,[str(appui[0].value).replace("_","/").split(".")[0] for appui in cmd_c7])
    else:
        return [
                    (
                        nom_c7,
                        str(appui[0].value).replace("_","/").split(".")[0]
                    )
                    for (nom_c7,num,appui) in get_appuis_c7_groupe_ligne()
                ]

#Récupération de la liste des appuis comme pour appui_from_c7 en récupérant que le nom
def appui_from_c7_nom(c3a=False):
    if c3a:
        (nom_c7,appuis) = appui_from_c7(c3a)
        return (nom_c7,[appui.split("_")[-1].split("/")[-1] for appui in appuis])
    else:
        return [(nom_c7,appui.split("_")[-1].split("/")[-1]) for (nom_c7,appui) in appui_from_c7()]

#Retourne tous les chemins menants vers des fichier C3A pour le projet
def get_c3a_list():
    liste=[f for f in glob.iglob(os.path.join(conf["listeC3A_C3A_path"],arbo_c3a), recursive=True) if "~$" not in f]
    if liste:
        return liste
    else:
        raise FileNotFoundError("fichiers C3A manquants")

#Retourne tous les chemins menants vers des fichier C7 pour le projet
def get_c7_list():
    liste=[f for f in glob.iglob(os.path.join(conf["listeC7_C7_path"],arbo_c7), recursive=True) if "~$" not in f]
    if liste:
        return liste
    else:
        raise FileNotFoundError("fichiers C7 manquants")

#Retourne la liste des tableaux de C7 et le nom du fichier C7, groupé par nom de fichier C7
def get_appuis_c7_groupe():
    return [
        (
            c7,
            ouvrir_c7(
                get_feuille_c7(
                    False,
                    os.path.join(conf["commande_path"],c7)
                )
            )
        )
            for c7 in get_c7_list()
    ]

#Récupère les lignes de la C7 avec le numéro de ligne et le nom du fichier, tout sur une même ligne
def get_appuis_c7_groupe_ligne():
    return [[c7,num_appui,appui]
            for c7,appuis in get_appuis_c7_groupe()
            for (num_appui,appui) in enumerate(appuis)
            ]  

#Récupérer, ouvrir et lister les ligne d'une shape
def get_shape(chemin,nom_shape,check_exist=False):
    layer = QgsVectorLayer(chemin, nom_shape , "ogr")
    
    if not layer.isValid():
        if check_exist:
            return False
        else:
            raise Exception(format_shape_invalide.format(chemin))
    
    return layer,layer.getFeatures()

#Vérification de la présence des champs nécessaires dans une shape
def verif_champs_shape(num_controle,chemin_shape,nom_shape,champs,controle40=False):
    erreurs_struct=[]
    erreurs_attr=[]
    try:
        shape,list_points = get_shape(chemin_shape,nom_shape)
        champs_key=[k for k in champs if param_format.format(conf["zone"],conf["type_lvrb"]) in champs[k]]
        
        res_champs={key:(key.upper() in map(str.upper,shape.fields().names())) for key in champs_key}
        if not all(res_champs.values()):
            ctrl=40

            erreurs_attr=[
                modele_erreur(
                    ctrl,
                    [chemin_fichier_application(chemin_shape),"",champ]
                )
                for champ in res_champs if not res_champs[champ]
            ]
            
            erreurs_struct = [
                modele_erreur(
                    num_controle,
                    [chemin_fichier_application(chemin_shape),"",""]
                )
            ]
            
            alim_rapport_csv(erreurs_struct)
            alim_rapport_csv(erreurs_attr)
            
    except:
        pass

#Récupération de la première feuille du fichier C7
def get_feuille_c7(c3a=False,chemin=False):
    if c3a:
        nom = [f for f in glob.glob(os.path.join(conf["listeC7_C7_path"],format_arbo_c7).format(nom_fichier(c3a).split("C3")[0])) if "~$" not in f][0]
        c7_xls = xlrd.open_workbook(nom)
        return chemin_fichier_application(nom),c7_xls.sheet_by_index(0)
    if chemin:
        c7_xls = xlrd.open_workbook(chemin)
        return c7_xls.sheet_by_name("Commande")
    return False

#Récupération des lignes de la feuille de la C7
def ouvrir_c7(feuille):
    cmd_c7 = [
        feuille.row(i)[:-1] for i in range(ind_premiere_ligne_c7,feuille.nrows)
        if feuille.row(i)[1].ctype or feuille.row(i)[2].ctype
        ]
    return cmd_c7

#A partir d'un chemin de C3A, retourne la 2ème feuille, contenant les informations nécessaires
def get_feuille_commande(chemin):
    c3a_xls = xlrd.open_workbook(chemin)
    return c3a_xls.sheet_by_index(1)

#Récupération des lignes de la feuille de la C3A
def ouvrir_c3a(feuille_commandes):
    commandes = [
        feuille_commandes.row(i)[:-1] for i in range(ind_premiere_ligne_c3a,feuille_commandes.nrows)
        if feuille_commandes.row(i)[1].ctype or feuille_commandes.row(i)[2].ctype
        ]
    return commandes

def find_fichier_format(conf_chemin,conf_format,ext,variables,code_zasro_alt):
    variables_alt=variables.copy()
    variables_alt["code_zasro"]=code_zasro_alt
    
    return len([f
            for f in glob.iglob(os.path.join(conf_chemin,"*.{}*".format(ext)))
            if os.path.splitext(os.path.basename(f))[0].upper().replace(" ","-") in ([
                    str(format_inline(f_format,variables)).upper().replace(" ","-")
                    for f_format in conf_format
                ]
                +[
                    str(format_inline(f_format,variables_alt)).upper().replace(" ","-")
                    for f_format in conf_format
                ])
            ])

def find_synthese_etude():
    return find_fichier_format(
        conf["syntheseEtude_path"],
        conf["syntheseEtude_format"],
        "xls",
        {"code_zasro":conf["code_zasro"]},
        conf["code_zasro_alt"]
        )   

def find_synoptique_fichier(type_syn="cable"):
    if type_syn not in ["cable","fibre"]:
        raise Exception("Le fichier synoptique doit avoir qu'un seul type")
    
    return find_fichier_format(
        conf["optique_path"],
        conf["optique_synoptique_{}_format".format(type_syn)],
        "xls",
        {"code_zasro":conf["code_zasro"]},
        conf["code_zasro_alt"]
        ) 

def find_bpu():
    return find_fichier_format(
        conf["financier_path"],
        conf["financier_BPU_format"],
        "xls",
        {"code_zasro":conf["code_zasro"]},
        conf["code_zasro_alt"]
        )

def find_recap_conventions():
    return find_fichier_format(
        conf["conventions_path"],
        conf["conventions_recap_format"],
        "xls",
        {"code_zasro":conf["code_zasro"]},
        conf["code_zasro_alt"]
        )   

def get_noms_planboite():
    return [nom_fichier(f) for f in glob.iglob(os.path.join(conf["optique_plansBoite_path"],"*.xls*"))]

def find_pmv_souterrain(nom_commune):
    return find_fichier_format(
        conf["administratif_PMV_path"],
        conf["PMV_souterrain_format"],
        "pdf",
        {"code_zasro":conf["code_zasro"],"commune":nom_commune},
        conf["code_zasro_alt"]
        )    

def find_pmv_poteau(nom_commune):
    return find_fichier_format(
        conf["administratif_PMV_path"],
        conf["PMV_poteau_format"],
        "pdf",
        {"code_zasro":conf["code_zasro"],"commune":nom_commune},
        conf["code_zasro_alt"]
        )

def get_d15_from_fichier():
    chemins = [
        f for f in glob.glob(os.path.join(conf["FOA_annexeD15_path"],"*.xls*"))
        if get_valeurs_variables_conf(os.path.splitext(os.path.basename(f))[0],conf["FOA_annexeD15_format"])
    ]
    
    liste_dt=[]
    for chemin in chemins:
        feuille = xlrd.open_workbook(chemin).sheet_by_index(0)
        liste_dt.append({
            "pt1":feuille.row(22)[1],
            "pt2":feuille.row(22)[11],
            "fichier":chemin_fichier_application(chemin)
        })
    return liste_dt  

def pts_from_d15():
    return [[d15["pt1"].value,d15["pt2"].value] for d15 in get_d15_from_fichier()]

def find_d15(noms_pt):
    return find_fichier_format(
        conf["FOA_annexeD15_path"],
        conf["FOA_annexeD15_format"],
        "xls",
        {"code_zasro":conf["code_zasro"],"pt1":noms_pt[0],"pt2":noms_pt[1]}
        if type(noms_pt) is list
        else {"code_zasro":conf["code_zasro"],"pt1":noms_pt,"pt2":""},
        conf["code_zasro_alt"]
        )
    
def get_dt_pdf(nom_commune):
    return [f
            for f in glob.iglob(os.path.join(*[conf["administratif_DT_path"],nom_commune],"**/*.pdf"))
            ]

def get_l49_recepisse(nom_commune):
    return find_fichier_format(
        conf["administratif_L49_path"],
        conf["L49_recepisse_format"],
        ".",
        {"code_zasro":conf["code_zasro"],"commune":nom_commune},
        conf["code_zasro_alt"]
        )

def get_l49_dossier(nom_commune):
    return find_fichier_format(
        conf["administratif_L49_path"],
        conf["L49_dossier_format"],
        ".",
        {"code_zasro":conf["code_zasro"],"commune":nom_commune},
        conf["code_zasro_alt"]
        )

def get_l49_fichiers_complets(nom_commune):
    return get_l49_dossier(nom_commune) and get_l49_recepisse(nom_commune)

#Retourne le tableau de la table cable_infra
def ouvrir_cable_infra(chemin):
    with open(chemin) as cable_infra_csv:
        cable_infra = [
            {k:v for k, v in row.items()}
            for row in csv.DictReader(cable_infra_csv, delimiter=';')
        ]
    return cable_infra

#Retourne la liste des tableaux de C3A et le nom du fichier C3a, groupé par nom de fichier C3A
def get_commandes_groupe():
    return [
        (
            c3a,
            ouvrir_c3a(
                get_feuille_commande(
                    os.path.join(conf["commande_path"],c3a)
                )
            )
        )
            for c3a in get_c3a_list()
    ]

#Récupère les lignes de la C3A avec le numéro de ligne et le nom du fichier, tout sur une même ligne
def get_commande_groupe_ligne():
    return [[c3a,num_prestation,prestation]
            for c3a,commandes in get_commandes_groupe()
            for (num_prestation,prestation) in enumerate(commandes)
            ]          

#A partir de la liste groupée de C3A,
## retourne la concatenation de tous les tableaux de C3A en un seul tableau
def get_commandes_joint(commandes_groupe):
    return reduce(lambda acc_l, sl: acc_l.extend(sl) or acc_l, [commandes for c3a,commandes in commandes_groupe])

#Retourne un tableau simplifié des commandes des C3A en gardant que les points A et B
def liaisons_commande(commandes_joint):
    return [[prestation[3].value,prestation[5].value] for prestation in commandes_joint]

#Récupère la liste des poteaux en explorant la liste des fichiers de poteaux et en récupérant leur nom 
def get_poteaux_fiche(dossier_complet=False):
    return [os.path.splitext(os.path.basename(f))[0]
            for f in glob.iglob(os.path.join(conf["appuis_orange_poteau_path"],"*.xls*"))
            if dossier_complet
            or format_nommage_complt(os.path.splitext(os.path.basename(f))[0],conf["appuis_orange_poteau_format"])
            ]

#Récupère la liste des chambres en explorant la liste des fichiers de chambres et en récupérant leur nom 
def get_chambres_fiche(dossier_complet=False):
    return [os.path.splitext(os.path.basename(f))[0]
            for f in glob.iglob(os.path.join(conf["FOA_chambre_path"],"*.xls*"))
            if dossier_complet
            or format_nommage_complt(os.path.splitext(os.path.basename(f))[0],conf["FOA_chambre_format"])
            ]

def get_poteaux_nom():
    return [get_valeurs_variables_conf(poteau,conf["appuis_orange_poteau_format"])["conf"]["id"] for poteau in get_poteaux_fiche()]

def get_chambres_nom():
    return [get_valeurs_variables_conf(chambre,conf["FOA_chambre_format"])["conf"]["id"] for chambre in get_chambres_fiche()]

def get_cable_infra_shp(format_troncon=False):
    infras = [infra for infra in get_shape(conf["shape_infra_path"],shape_infra_nom)[1]]
    pts = [pt for pt in get_shape(conf["shape_point_technique_path"],shape_point_technique_nom)[1]]
    cables = [cable for cable in get_shape(conf["shape_cable_path"],shape_cable_nom)[1]]
    
    cbl_inf=[]
    for cable in cables:
        type_inf,prop,pt1,pt2 = [""]*4
        for infra in infras:
            if infra.geometry().contains(cable.geometry()):
                try:
                    type_inf,prop = infra["cm_typ_imp"],infra["PROPRIETAI"]
                except KeyError as e:
                    log(e,23)
                    raise InternalException()
                break
        for pt in pts:
            if pt["pt_nd_code"] == cable["cb_nd1"]:
                pt1=format_id_pt(str(pt['NOM']),str(pt['CODE_INSEE'])) if pt.fieldNameIndex('CODE_INSEE') != -1 else str(pt['NOM'])
            if pt["pt_nd_code"] == cable["cb_nd2"]:
                pt2=format_id_pt(str(pt['NOM']),str(pt['CODE_INSEE'])) if pt.fieldNameIndex('CODE_INSEE') != -1 else str(pt['NOM'])
        if "CONDUITE" in type_inf and prop == "ORANGE":
            cbl_inf.append([pt1,pt2] if not format_troncon else "{}=>{}".format(pt1,pt2))
    
    return cbl_inf

def get_valeurs_variables_conf(nom_fiche,f_formats):
    for f_format in (f_formats if type(f_formats) is list else [f_formats]):
        try:
            f_format_origine=f_format
            nb_var=f_format.count("{")
            srch = re.search(("{(.+)}."*nb_var)[:-1],f_format)
            variables_liste = eval('srch.group({})'.format(number_to_inline_list(nb_var)))

            for var in variables_liste:
                f_format=f_format.replace("{"+var+"}","(.+)")

            variables_valeurs=eval("re.search(f_format,nom_fiche).group({})".format(number_to_inline_list(f_format.count(".+"))))
            
            return {
                "format":f_format_origine,
                "conf":dict(zip(variables_liste,variables_valeurs))
            }
        except Exception as e:
            pass
    return False

def format_inline(f_format,params):
    inline = (str(params)
        .replace("{'","")
        .replace("': ","=")
        .replace(", '",", ")
        .replace("}","")
        .replace("}","")
        .replace("{","")
        )

    return eval("f_format.format({})".format(inline)) if f_format else ""

def format_nommage_complt(nom_fiche,f_formats):
    confs = get_valeurs_variables_conf(nom_fiche,f_formats)
    
    if confs:
        f_format,conf=confs.values()       
        return format_inline(f_format,conf)
    else:
        return False

#Récupère la liste des chambres en explorant la liste des fichiers de chambres et en récupérant leur nom 
def get_chambres_fiche():
    return [os.path.splitext(os.path.basename(f))[0]
            for f in glob.iglob(os.path.join(conf["FOA_chambre_path"],"*.xls*"))
            if format_nommage_complt(os.path.splitext(os.path.basename(f))[0],conf["FOA_chambre_format"])
            ]

def get_chambres_nom():
    return [get_valeurs_variables_conf(chambre,conf["FOA_chambre_format"])["conf"]["id"] for chambre in get_chambres_fiche()]

def get_contenu_comac():
    return [os.path.splitext(os.path.basename(f))[0]
            for f in glob.iglob(os.path.join(conf["appuis_enedis_dossier_path"],"*"))]

#Modèle de ligne d'erreur dans le fichier rapport, contenant les informations de contrôle pré-enregistrés
#selon le numéro de contrôle.
def modele_erreur(num_controle,erreur):
    pre_erreur=[num_controle]+pre_entete[pre_entete_lien[num_controle]]
    return pre_erreur+erreur+[erreur_controle[num_controle],post_criticite_lien[num_controle]]

#Utilisation de la fonction modele_erreur plus spécifiquement pour la C3A
#Le modèle affiche en "champ concerné" la concaténation des points, ou seulement l'un ou l'autre
def modele_erreur_c3a(num_controle,c3a,point_a,point_b,source_b="",nb_champs=2):
    if nb_champs == 2:
        erreur=[
            chemin_fichier_application(c3a),
             source_b,
             troncon_format.format(point_a,point_b)
        ]
    else:
        if point_a:
            erreur=[
                chemin_fichier_application(c3a),
                 source_b,
                 point_a
            ]
        else:
            erreur=[
                chemin_fichier_application(c3a),
                 source_b,
                 point_b
            ]
    
    return modele_erreur(num_controle,erreur)

#Vérifier l'existance du fichier plan_tirange 
def find_plan_tirage():
    return any([f
            for f in glob.iglob(os.path.join(conf["projet_path"],"*.pdf"))
            if format_nommage_complt(os.path.splitext(os.path.basename(f))[0],conf["projet_planTirage_format"])
            ])
