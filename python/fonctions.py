from definitions import *

try:
    import xlrd
except Exception as e:
    log(e,22)

#Fenêtre de message d'erreur avec un code d'identification
#Possibilité d'intégrer un message spécifique en renseignant le message
def msg_erreur(code,message=False):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setText("Une erreur est survenue")
    msg.setWindowTitle("Erreur")
    if not message:
        msg.setDetailedText("Code d'erreur: {}".format(str(code)))
    else:
        msg.setDetailedText(str(message))
    msg.setStandardButtons(QMessageBox.Close)
    msg.exec_()

#Message d'avertissement, indiquant la fin des contrôles en n'ayant pas executé la totalité car un contrôle est bloquant
def msg_alerte(num_controle):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    msg.setText("Une ou plusieurs erreures doivent être corrigées afin d'effectuer la totalité des contrôles")
    msg.setWindowTitle("Contrôles terminés")
    msg.setDetailedText("Dernier contrôle effectué: {}".format(str(num_controle)))
    msg.setStandardButtons(QMessageBox.Close)
    msg.exec_()

#Message de réussite à la fin du programme
def msg_succes():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText("Tous les contrôles ont été effectués.")
    msg.setWindowTitle("Contrôles terminés")
    msg.setDetailedText('Le rapport des contrôles a été généré dans le dossier "rapports"')
    msg.setStandardButtons(QMessageBox.Close)
    msg.exec_()

#Retourne le nombre de controles effectués dans une fonction de contrôle
def get_nb_controles(args):
    keys=args.keys()
    
    if "controle" in keys:
        return 1
    elif "controles" in keys:
        return list(args["controles"].values()).count(True)
    else:
        return list(args.values()).count(True)

#Vérifie si la combinaison type de livrable et réference livrable est existante
def check_combi_menu(type_lrvb,zone):
    return type_lrvb in col_param[zone]

#Mise à jour de la barre d'avancement selon le numéro de contrôle et le nombre de contrôles
def pbar_chargement(pbar,num,total):
    pbar.setValue(float(num)/total*100)

def init_pbar(widget):
    pbar = QProgressBar(widget)
    pbar.setMinimum(0)
    pbar.setMaximum(100)
    pbar.setAlignment(Qt.AlignHCenter)
    pbar.move(72,159)
    pbar.show()
    return pbar

#Mise à jour du dictionnaire de configuration avec le nouveaux généré après sélection du département
def update_conf_fct(config,type_lvrb,zone):
    exec(update_conf_exec)

#Retourne l'indice d'une colonne csv selon la lettre donnée
def pos_xl(lettre):
    return ord(lettre.lower()) - 96 - 1

#Supprimer le contenu d'un rapport s'il y a une exception
def vider_rapport_csv():
    with open(os.path.join(chemin_rapport,libelle_rapport_csv), 'w') as fichier:
        fichier.write("")

#Fonction permettant d'alimenter le log et avoir des informations sur une erreur / exception
def log(err,code=0):
    if err is not None:
        vider_rapport_csv()
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
    
    try:
        msg_erreur(str(code))
    except Exception as e:
        print(e)
        print("Une erreur est survenue (code: {})".format(str(code)))
        exit(code)

#Récupérer la liste des appuis contenus dans la C7
def appui_from_c7(c3a):
    (nom_c7,feuille) = get_feuille_c7(c3a)
    cmd_c7 = ouvrir_c7(feuille)
    return (nom_c7,[str(appui[0].value).replace("_","/").split(".")[0] for appui in cmd_c7])

#Récupération de la liste des appuis comme pour appui_from_c7 en récupérant que le nom
def appui_from_c7_nom(c3a):
    (nom_c7,appuis) = appui_from_c7(c3a)
    return (nom_c7,[appui.split("_")[-1] for appui in appuis])

#Création du code type sous la forme présente dans les C3A avec le type et le propriétaire
def code_type_point(type_point,prop):
    return "{}{}".format(
        corr_point_lib_code[type_point if type_point in type_point_liste else 'ND'],
        'T' if prop != prop_orange and type_point in point_tiers_liste else ''
        )

#Retourne tous les chemins menants vers des fichier C3A pour le projet
def get_c3a_list():
    liste=[f for f in glob.iglob(conf["chemin_c3a"], recursive=True) if "~$" not in f]
    if liste:
        return liste
    else:
        raise FileNotFoundError("fichiers C3A manquants")

#Retourne le nom du fichier selon le chemin
def nom_fichier(chemin,extension=False):
    nom=os.path.basename(chemin)
    return os.path.splitext(nom)[0] if not extension else nom

#Vérifier que la variable est un nombre
def isnumber(variable):
    return str(variable).replace('.','',1).isdigit()

#Retourner l'identifiant d'un point selon la présence ou non de l'insee
def format_id_pt(id_pt,insee):
    return id_pt if "_" in id_pt or not insee else "{}_{}".format(insee,id_pt)

#Récupérer, ouvrir et lister les ligne d'une shape
def get_shape(chemin,nom_shape):
    layer = QgsVectorLayer(chemin, nom_shape , "ogr")
    
    if not layer.isValid():
        raise Exception(format_shape_invalide.format(chemin))
    
    return layer,layer.getFeatures()

#Vérification de la présence des champs nécessaires dans une shape
def verif_champs_shape(num_controle,chemin_shape,nom_shape,champs):
    erreur=[]
    shape,list_point_technique = get_shape(chemin_shape,nom_shape)
    champs_key=[k for k in champs if param_format.format(conf["zone"],conf["type_lvrb"]) in champs[k]]
    
    if not all(key in shape.fields().names() for key in champs_key):
        erreurs = [
            modele_erreur(
                num_controle,
                [chemin_fichier_application(chemin_shape),"",""]
            )
        ]
        alim_rapport_csv(erreurs)

#Récupération de la première feuille du fichier C7
def get_feuille_c7(c3a):
    nom = [f for f in glob.glob(conf["format_chemin_c7"].format(nom_fichier(c3a).split("C3")[0])) if "~$" not in f][0]
    c7_xls = xlrd.open_workbook(nom)
    return nom_fichier(nom,True),c7_xls.sheet_by_index(0)

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

def get_feuille_doc_controleur(dpt):
    c3a_xls = xlrd.open_workbook(chemin_doc_controleur)
    return c3a_xls.sheet_by_name(dpt)

#Récupération des lignes de la feuille de la C3A
def get_liste_controle_dpt(dpt,type_lvrb,zone):
    feuille=get_feuille_doc_controleur(dpt)
    controles_dpt=list(map(bool,feuille.col_values(col_param[zone][type_lvrb])[1:]))
    identifiants=map(int,feuille.col_values(0)[1:])
    return dict(zip(identifiants,controles_dpt))

#Chemin du fichier à partir du dossier de l'application
def chemin_fichier_application(fichier):
    return fichier.replace(conf["chemin_exe"],"")

#Crée ou alimente le rapport csv contenant les erreurs. S'il est créé, on ajoute le header
def alim_rapport_csv(erreurs=False):
    if type(erreurs) is not bool and len(erreurs) == 0:
        return

    with open(os.path.join(chemin_rapport,libelle_rapport_csv), 'a', newline='') as fichier:
        fwrite = csv.writer(fichier, delimiter=';',
            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        if erreurs:
            for erreur in erreurs:
                fwrite.writerow(erreur)
        else:
            fwrite.writerow(entete_rapport_csv)

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
                    os.path.join(conf["commande_orange_path"],c3a)
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
def get_poteaux_fiche():
    return [os.path.splitext(os.path.basename(f))[0]
            for f in glob.iglob(os.path.join(conf["appui_orange_path"],"*.xls*"))]

def get_poteaux_nom():
    #pattern=re.compile("^\W*\w*\d{5}\w*\W*$")
    #return [re.findall("[0-9]{5}",poteau)[-1] for poteau in get_poteaux_fiche()
    #        if pattern.match(poteau)]
    return [poteau.split("_")[-1].replace("FicheAppui","") for poteau in get_poteaux_fiche()]

#Modèle de ligne d'erreur dans le fichier rapport, contenant les informations de contrôle pré-enregistrés
#selon le numéro de contrôle.
def modele_erreur(num_controle,erreur):
    pre_erreur=[num_controle]+pre_entete_lien[num_controle]
    return pre_erreur+erreur+eval("post_entete_controle"+str(num_controle))

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

#Annonce la fin du programme
def fin_programme():
    print(msg_fin_programme_1)