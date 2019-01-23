try:
    from controles import *
except Exception as e:
    log(e,41)

#warning d'un module pour une bibliothèque bientôt obsolète
warnings.simplefilter("ignore")

rapport=""

try:
    rapport=version_c3a(rapport)
except Exception as e:
    log(e,42)

try:
    rapport=corresp_cable_infra_c3a(rapport,True,True)
    print()
except Exception as e:
    log(e,43)

try:
    rapport=corresp_poteau_c3a(rapport)
    print()
except Exception as e:
    log(e,44)

try:
    rapport=regles_gcblo_c3a_majeurs(rapport)
    print()
except Exception as e:
    log(e,45)   

try:
    fin_programme(rapport)
except Exception as e:
    log(e,46)
