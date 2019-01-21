from qgis.core import *
import qgis.utils
from qgis.core import QgsProject,QgsVectorLayer
from PyQt5.QtCore import QFileInfo
import warnings
import os

chemin_courant=os.getcwd()
qgis_installation_path=r"C:\Program Files\QGIS 3.4"
chemin_exe=os.path.join(chemin_courant,"exe")
exe_projet_racine=os.path.join(chemin_exe,"04 - Projet")
nom_projet=os.listdir(exe_projet_racine)[0]
exe_projet=os.path.join(exe_projet_racine,nom_projet)
commande_orange_path=os.path.join(chemin_exe,"11 - Commande_Orange")
exe_projet_carto=os.path.join(exe_projet,"APD"+nom_projet+".qgs")
chemin_layers=os.path.join(exe_projet,exe_projet,"LAYERS")
layer_prises = os.path.join(chemin_layers+"PRISES.shp")
cable_infra_csv_path=os.path.join(chemin_layers,"CABLE_INFRA.csv")
#c3a_xls_path=os.path.join(commande_orange_path,"F99999jjmmaa_21024_21100_21224_21271_21498_21528_21694_jjmmaa_C3A.xls")
ind_premiere_ligne_c3a=31-1
type_imp=["CONDUITE FT","AERIEN FT"]
version_c3a_en_cours='C3A BLO5'

chemin_rapport=os.path.join(chemin_courant,"rapports")
prefixe_resultat_controle1_2="rapport_verif_c3a_cable_infra"
prefixe_resultat_controle1_1="rapport_verif_cable_infra_c3a"
nom_rapport="rapport.txt"

msg_erreur=""
msg=""
rapport=""