try:
    from controles import *
except Exception as e:
    log(e,4)

#warning d'un module pour une bibliothèque bientôt obsolète
warnings.simplefilter("ignore")

rapport=""

try:
    rapport=version_c3a(rapport)
except Exception as e:
    log(e,5)

try:
    rapport=corresp_cable_infra_c3a(rapport,True,True)
    print()
except Exception as e:
    log(e,6)

try:
    fin_programme(rapport)
except Exception as e:
    log(e,7)
