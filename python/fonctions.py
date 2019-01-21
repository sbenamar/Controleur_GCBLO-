import csv,xlrd,glob
from datetime import datetime
from definitions import *

def get_c3a_list():
    return [
                f for f in glob.iglob(os.path.join(
                    commande_orange_path,"**/**/*C3A*.xls"), recursive=True
                )
            ]
def resultat_fichier(libelle,tab_resultat,tab_entete,tab_erreur):
    nom_fichier=libelle+'_'+str(datetime.now()).split('.')[0].replace(' ','_').replace(':','-')+'.csv'
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

def get_feuille_commande(chemin):
    c3a_xls = xlrd.open_workbook(chemin)
    return c3a_xls.sheet_by_index(1)

def ouvrir_c3a(feuille_commandes,ind_premiere_ligne_c3a):
    commandes = [
        feuille_commandes.row(i)[:-1] for i in range(ind_premiere_ligne_c3a,feuille_commandes.nrows)
        if feuille_commandes.row(i)[1].ctype
        ]
    
    return commandes

def ouvrir_cable_infra(chemin):
    with open(chemin) as cable_infra_csv:
        cable_infra = [
            {k:v for k, v in row.items()}
            for row in csv.DictReader(cable_infra_csv, delimiter=';')
        ]

    return cable_infra

def msg_erreur(erreurs):
    msg_erreur=""
    if len(erreurs) > 1:
        msg_erreur="Le controlleur a détecté "+str(len(erreurs))+" erreurs:\n"+"\n".join(erreurs)
    elif len(erreurs) == 1:
        msg_erreur="Le controlleur a détecté 1 erreur ("+erreurs[0]+")."
    else:
        msg_erreur="Aucune erreur n'a été détectée par le controlleur."
    
    print(msg_erreur)    
    return msg_erreur

def msg_erreur_fichier(erreurs,nom_fichier):
    if len(erreurs) == 0:
        msg_erreur="Aucune erreur n'a été détectée par le controlleur."
    elif len(erreurs) == 1:
        msg_erreur="1 erreur a été détectée par le controlleur. Les détails sont dans le fichier "+nom_fichier
    else:
        msg_erreur=str(len(erreurs))+" erreurs ont été détectées par le controlleur. Les détails sont dans le fichier "+nom_fichier
    
    print(msg_erreur)
    return msg_erreur

def gen_rapport_txt(nom,rapport):
    with open(os.path.join(chemin_rapport,nom), "w") as f:
        f.write(rapport)

def fin_programme(msg_rapport=""):
    print("Programme terminé")
    gen_rapport_txt(nom_rapport,msg_rapport)
    input("Appuyez sur une touche pour quitter le programme...")