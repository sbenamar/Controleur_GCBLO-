import csv,xlrd,glob
from functools import reduce

try:
    from definitions import *
except Exception as e:
    log(e,21)
    
def get_c3a_list():
    return [
                f for f in glob.iglob(os.path.join(
                    commande_orange_path,"**/**/*C3A*.xls"), recursive=True
                )
            ]
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

def get_commandes_joint(commandes_groupe):
    return reduce(lambda acc_l, sl: acc_l.extend(sl) or acc_l, [commandes for c3a,commandes in commandes_groupe])

def liaisons_commande(commandes_joint):
    return [[prestation[3].value,prestation[5].value] for prestation in commandes_joint]

def get_poteaux_fiche():
    return list(set(sum(
        [os.path.splitext(os.path.basename(f))[0].split('_')
         for f in glob.iglob(os.path.join(appui_orange_path,"*.xls"))
         ],
        []
    )))

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

def msg_erreur_fichier(erreurs,nom_fichier):
    if len(erreurs) == 0:
        msg_erreur=msg_erreur_fichier1
    elif len(erreurs) == 1:
        msg_erreur=msg_erreur_fichier2.format(nom_fichier)
    else:
        msg_erreur=msg_erreur_fichier3.format(str(len(erreurs)),nom_fichier)
    
    print(msg_erreur)
    return msg_erreur

def gen_rapport_txt(nom,rapport):
    with open(os.path.join(chemin_rapport,nom), "w") as f:
        f.write(rapport)

def fin_programme(msg_rapport=""):
    print(msg_fin_programme_1)
    gen_rapport_txt(nom_rapport,msg_rapport)
    input(msg_fin_programme_2)