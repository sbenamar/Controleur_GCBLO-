set OSGEO4W_ROOT=C:\PROGRA~1\QGIS3~1.4
set PATH=%OSGEO4W_ROOT%\apps\qgis\bin;%PATH%;%OSGEO4W_ROOT%\apps\Python37;%OSGEO4W_ROOT%\apps\Python37\Scripts;%OSGEO4W_ROOT%\apps\qt5\bin;%OSGEO4W_ROOT%\bin;%PATH%

set QT_PLUGIN_PATH=%OSGEO4W_ROOT%\apps\Qt5\plugins

set O4W_QT_PREFIX=%OSGEO4W_ROOT:\=/%/apps/Qt5
set O4W_QT_BINARIES=%OSGEO4W_ROOT:\=/%/apps/Qt5/bin
set O4W_QT_PLUGINS=%OSGEO4W_ROOT:\=/%/apps/Qt5/plugins
set O4W_QT_LIBRARIES=%OSGEO4W_ROOT:\=/%/apps/Qt5/lib
set O4W_QT_TRANSLATIONS=%OSGEO4W_ROOT:\=/%/apps/Qt5/translations
set O4W_QT_HEADERS=%OSGEO4W_ROOT:\=/%/apps/Qt5/include
set O4W_QT_DOC=%OSGEO4W_ROOT:\=/%/apps/Qt5/doc

SET PYTHONPATH=
SET PYTHONHOME=%OSGEO4W_ROOT%\apps\Python37

set QGIS_PREFIX_PATH=%OSGEO4W_ROOT:\=/%/apps/qgis
set GDAL_FILENAME_IS_UTF8=YES
set VSI_CACHE=TRUE
set VSI_CACHE_SIZE=1000000
set QT_PLUGIN_PATH=%OSGEO4W_ROOT%\apps\qgis\qtplugins;%OSGEO4W_ROOT%\apps\qt5\plugins
set PYTHONPATH=%OSGEO4W_ROOT%\apps\qgis\python;%PYTHONPATH%

set GDAL_DATA=%OSGEO4W_ROOT%\share\gdal

start pythonw python/controleur.pyw

import os

os.environ["OSGEO4W_ROOT"] = "C:\PROGRA~1\QGIS3~1.4"
os.environ["PATH"] = os.environ["OSGEO4W_ROOT"]+r"\apps\qgis\bin;"+os.environ["PATH"]+r";"+os.environ["OSGEO4W_ROOT"]+r"\apps\Python37;"+os.environ["OSGEO4W_ROOT"]+r"\apps\Python37\Scripts;"+os.environ["OSGEO4W_ROOT"]+r"\apps\qt5\bin;"+os.environ["OSGEO4W_ROOT"]+r"\bin;"+os.environ["PATH"]
os.environ["QT_PLUGIN_PATH"] = os.environ["OSGEO4W_ROOT"]+r"\apps\Qt5\plugins"
os.environ["PYTHONHOME"]=os.environ["OSGEO4W_ROOT"]+r"\apps\Python37"
os.environ["PYTHONPATH"]=""
os.environ["PYTHONPATH"]=os.environ["OSGEO4W_ROOT"]+r"\apps\qgis\python;"+os.environ["PYTHONPATH"]