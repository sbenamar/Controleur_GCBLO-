try:
    from controles import *
except Exception as e:
    log(e,41)

#warning d'un module pour une bibliothèque bientôt obsolète
warnings.simplefilter("ignore")

rapport=""

#Ce dictionnaire liste les identifiants de contrôle avec l'autorisation ou non de les lancer
#Ce dictionnaire sera généré depuis un fichier Excel, selon si une case est cochée ou non
list_controle_exe={
    1:True,
    2:False,
    3:False,
    4:True,
    5:False,
    6:True,
    7:True,
    8:True,
    9:False,
    10:False,
    11:False,
    12:True,
    13:True,
    14:True,
    15:True,
    16:True,
    17:True,
    18:True,
    19:True,
    20:True,
    21:True,
    22:True,
    23:True,
    24:True
}

print("Contrôles en cours...")

#Création du rapport, initialisé avec l'entête
alim_rapport_csv()

#Chaque contrôle est lancé à la suite, avec une gestion des exception pour chacun
#list_controle_exe est passé en paramètre avec l'identifiant de contrôle correspondant
#Le contrôle sera lancé si pour cet identifiant la valeur est True, sinon ignoré
try:
    #Pour chaque fonction,
    ##on passe le rapport texte en paramètre, puis on le récupère pour réutiliser dans la suivante
    #Ainsi il est enrichi petit à petit par chaque fonction
    rapport=version_c3a(rapport,list_controle_exe[1])
except Exception as e:
    log(e,42)

try:
    rapport=corresp_cable_infra_c3a(rapport,list_controle_exe[2],list_controle_exe[3])
except Exception as e:
    log(e,43)

try:
    rapport=corresp_poteau_c3a(rapport,list_controle_exe[4])
except Exception as e:
    log(e,44)

try:
    info_sous_tubage(list_controle_exe[6])
except Exception as e:
    log(e,45)

try:
    rapport=regles_gcblo_c3a_majeurs(
        rapport,
        list_controle_exe[7],
        list_controle_exe[8],
        list_controle_exe[12]
    )
except Exception as e:
    log(e,46)

try:
    valeurs_selon_liaisons({k: v for k, v in list_controle_exe.items() if 13 <= k <= 25})
except Exception as e:
    log(e,47)
    
"""
try:
    fin_programme(rapport)
except Exception as e:
    log(e,46)
"""