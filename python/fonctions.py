import csv,glob
from functools import reduce

try:
    from definitions import *
except Exception as e:
    log(e,21)

try:
    import xlrd
except Exception as e:
    log(e,22)

def vider_rapport_csv():
    with open(os.path.join(chemin_rapport,libelle_rapport_csv), 'w') as fichier:
        fichier.write("")

def log(err,code=0):
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
        
    print("Une erreur est survenue (code: {})".format(str(code)))
    input()
    exit(code)
  
#Le tableau ne commence pas à la première ligne
##donc on récupère le numéro de la première ligne pour avoir le vrai numéro de ligne
def num_ligne_c3a(num_prestation):
    return num_prestation+ind_premiere_ligne_c3a+1

#Retourne tous les chemins menants vers des fichier C3A pour le projet
def get_c3a_list():
    return [
                f for f in glob.iglob(os.path.join(
                    commande_orange_path,arbo_c3a), recursive=True
                ) if "~$" not in f
            ]

def nom_fichier(chemin,extension=False):
    nom=os.path.basename(chemin)
    return os.path.splitext(nom)[0] if not extension else nom

def chemin_fichier_application(fichier):
    return fichier.replace(chemin_exe,"")

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

#Créé un reporting csv contenant la liste de anomalies et retourne le nom du fichier créé
def resultat_fichier(libelle,tab_resultat,tab_entete,tab_erreur):
    date=str(datetime.now())
    nom_fichier=libelle+'_'+date.split('.')[0].replace(' ','_').replace(':','-')+'.csv'
    with open(
        os.path.join(chemin_rapport,nom_fichier), 'w', newline=''
        ) as fichier:
        
        fwrite = csv.writer(fichier, delimiter=';',
            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        
        fwrite.writerow(tab_resultat)
        fwrite.writerow([])
        fwrite.writerow(tab_entete)
        for ligne in tab_erreur:
            fwrite.writerow(ligne)
            
    return nom_fichier

#A partir d'un chemin de C3A, retourne la 2ème feuille, contenant les informations nécessaires
def get_feuille_commande(chemin):
    c3a_xls = xlrd.open_workbook(chemin)
    return c3a_xls.sheet_by_index(1)

#A partir de la feuille de C3A, retourne toutes les lignes en tableau
def ouvrir_c3a(feuille_commandes,ind_premiere_ligne_c3a):
    commandes = [
        feuille_commandes.row(i)[:-1] for i in range(ind_premiere_ligne_c3a,feuille_commandes.nrows)
        if feuille_commandes.row(i)[1].ctype or feuille_commandes.row(i)[2].ctype
        ]
    return commandes

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
                    os.path.join(commande_orange_path,c3a)
                ),
                ind_premiere_ligne_c3a
            )
        )
            for c3a in get_c3a_list()
    ]

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
            for f in glob.iglob(os.path.join(appui_orange_path,"*.xls*"))
    ]

def modele_erreur(num_controle,erreur):
    pre_erreur=[num_controle]+pre_entete_lien[num_controle]
    return pre_erreur+erreur+eval("post_entete_controle"+str(num_controle))

def modele_erreur_c3a(num_controle,c3a,point_a,point_b):
    pre_erreur=[num_controle]+pre_entete_lien[num_controle]
    erreur=[
        chemin_fichier_application(c3a),
         "",
         troncon_format.format(point_a,point_b)
    ]
    return pre_erreur+erreur+eval("post_entete_controle"+str(num_controle))
    
#Créé le fichier rapport d'erreur en csv
##et affiche les informations de logs sur le terminal et fichier rapport
def contenu_rapport(msg_debut_controle,entete,erreurs,prefixe_fichier):
    msg=""
    print(msg_debut_controle)
    msg+=msg_debut_controle+"\n\n"
    resultat=[lib_nb_erreurs,str(len(erreurs))]
    
    nom_fichier=resultat_fichier(prefixe_fichier,resultat,entete,erreurs)     
    
    print()
    msg+=msg_erreur_fichier(erreurs,nom_fichier)
    msg+="\n\n"
    
    print()
    return msg

#Retourne et affiche le message d'erreur à écire selon le nombre d'erreurs dans le contrôle
def msg_erreur(erreurs):
    msg_erreur=""
    if len(erreurs) > 1:
        msg_erreur=msg_detecte_erreur1.format(str(len(erreurs)),"\n".join(erreurs))
    elif len(erreurs) == 1:
        msg_erreur=msg_detecte_erreur2.format(erreurs[0])
    else:
        msg_erreur=msg_detecte_erreur3
    
    print(msg_erreur)    
    return msg_erreur

#Retourne et affiche le message d'erreur à écire selon le nombre d'erreurs dans le contrôle
##en précisant le lien du fichier csv auquel se réferer 
def msg_erreur_fichier(erreurs,nom_fichier):
    if len(erreurs) == 0:
        msg_erreur=msg_erreur_fichier1
    elif len(erreurs) == 1:
        msg_erreur=msg_erreur_fichier2.format(nom_fichier)
    else:
        msg_erreur=msg_erreur_fichier3.format(str(len(erreurs)),nom_fichier)
    
    print(msg_erreur)
    return msg_erreur

#Génère le fichier rapport texte afin d'avoir une vue stynthétique sur le résultat des contrôles
def gen_rapport_txt(nom,rapport):
    with open(os.path.join(chemin_rapport,nom), "w") as f:
        f.write(rapport)

#Annonce la fin du programme et lance la génération du rapport texte
def fin_programme(msg_rapport=""):
    print(msg_fin_programme_1)
    input(msg_fin_programme_2)