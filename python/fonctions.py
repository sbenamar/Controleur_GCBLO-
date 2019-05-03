from definitions import *

#Mise à jour du dictionnaire de configuration avec le nouveaux généré après sélection du département
def update_conf_fct(config,type_lvrb,zone):
    exec(update_conf_exec)

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

#Création du code type sous la forme présente dans les C3A avec le type et le propriétaire
def code_type_point(type_point,prop):
    return "{}{}".format(
        corr_point_lib_code[type_point if type_point in type_point_liste else 'ND'],
        prop_tiers_code if prop != prop_orange and type_point in point_tiers_liste else prop_orange_code
        )

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
    return fichier.replace(conf["dossier_path"],"").replace("\\.","") or "/"

#Crée ou alimente le rapport csv contenant les erreurs. S'il est créé, on ajoute le header
def alim_rapport_csv(erreurs=False):
    if type(erreurs) is not bool and len(erreurs) == 0:
        return
    
    with open(os.path.join(chemin_rapport,libelle_rapport_csv), 'a', newline='') as fichier:
        fwrite = csv.writer(fichier, delimiter=';',
            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        if erreurs:
            erreurs = [y.split("#!") for y in set(["#!".join(list(map(str,x))) for x in erreurs])]
            for erreur in erreurs:
                fwrite.writerow(erreur)
        else:
            fwrite.writerow(entete_rapport_csv)

def number_to_inline_list(nb):
    return ','.join(map(str,range(1,nb+1)) or "-1")

#Annonce la fin du programme
def fin_programme():
    print(msg_fin_programme_1)