from controles import *

#warning d'un module pour une bibliothèque bientôt obsolète
warnings.simplefilter("ignore")

rapport=""
rapport=corresp_cable_infra_c3a(rapport,True,True)
print()
rapport=version_c3a(rapport)
print()
fin_programme(rapport)
