qgis_installation_path=r"C:\Program Files\QGIS 3.4"
exe_projet=r"C:\Users\PTPC9452\Documents\EXE test\04 - Projet\SRO21024SEM_1_Projet"
exe_projet_carto=exe_projet+"\APD_SRO21024SEM_1.qgs"
#exe_projet_carto=exe_projet+"\test2.qgs"

from qgis.core import *
#QgsApplication.setPrefixPath("C:/Program Files/QGIS 3.4/apps/qgis", True)

import qgis.utils
from qgis.core import QgsProject,QgsVectorLayer
from PyQt5.QtCore import QFileInfo

qgs = QgsApplication([], False)
qgs.initQgis()

#layer_prises ="C:/Users/PTPC9452/Documents/EXE test/04 - Projet/SRO21024SEM_1_Projet/LAYERS/PRISES.shp"
layer_prises = exe_projet+"\LAYERS\PRISES.shp"

layer = QgsVectorLayer(layer_prises, "PRISES" , "ogr")
if not layer.isValid():
  print("Erreur de chargement de la couche")
  input("Appuyez sur une touche pour quitter le programme...")
  exit(1)

qgs.exitQgis()
