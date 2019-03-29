import xmltodict
from lxml import etree
import os

def format_fichier_xml(elem):
    format_pre=["pre_code_zasro","code_zasro","separateur_zasro_etr","code_etr","branche_optique"]
    format_post=["nom"]
    format_variables_complexes=["pt1_pt2","insee_id"]
    format_variables_simples=["commune","id","canton"]
    
    format_elem=""
    options=format_pre+format_post
    
    for attr in elem.attrib:
        for var in format_variables_complexes+format_variables_simples:
            if var in attr:
                if var in format_variables_complexes:
                    var1,var2=var.split("_")
                    format_elem="pre_{var}&&#{var1}&&separateur_{var}&&#{var2}&&post_{var}".format(var=var,var1=var1,var2=var2)
                else:
                    format_elem="pre_{var}&&#{var}&&post_{var}".format(var=var)
                break
        if format_elem:
            options=format_pre+format_elem.split("&&")+format_post
            break

    format_final=""
    for option in options:
        if "#" not in option:
            opt=str(elem.get(option)).replace("None","").replace("true","{"+option+"}")
        else:
            opt=option.replace("#","{")+"}"
        format_final+=opt
        
    return format_final

def prefixe_variable(elem,type_pre="nommage"):
    parent=elem.getparent() if type_pre=="nommage" else elem
    gparent=parent.getparent()

    if gparent.tag=="livrable":
        prefixe="{}".format(parent.tag)
    elif gparent.tag=="proprietaire":
        prefixe="{}_{}_{}".format(gparent.getparent().tag,gparent.get("nom"),parent.tag)
    elif "type" in parent.attrib:
        prefixe="{}_{}_{}".format(gparent.tag,parent.tag,parent.get("type"))
    else:
        prefixe="{}_{}".format(gparent.tag,parent.tag)
        
    return prefixe

def get_conf_xml(chemin_courant,xml_livrables_path="conf/livrables.xml"):
    parser = etree.XMLParser(dtd_validation=True)
    try:
        root = etree.parse(xml_livrables_path,parser)
    except etree.XMLSyntaxError as e:
        print("Mauvais schema XML: "+str(e))
        exit()
    
    conf_dpt={}
    
    #Gerer le cas ou il y a plusieurs fois un element pour mettre plusieurs chemins
    for livrable in root.xpath("//livrable"):
        conf={}
        chemin_livrable=os.path.join(chemin_courant,"Livrable" if livrable.get("dpt") == "CD21" else "Commande")
        conf["dossier_path"]=chemin_livrable
        
        for couche in livrable.xpath('.//couche'):
            chemin_couche=couche.getparent().get("chemin")
            conf["shape_{}_path".format(couche.get("id"))]=os.path.join(chemin_couche.replace("/","\\",),couche.get("fichier"))
            conf["shape_{}_nom".format(couche.get("id"))]=couche.get("nom")
            
        for elem in livrable.xpath(".//nommage"):
            format_fichier=format_fichier_xml(elem)
            nom="{}_format".format(prefixe_variable(elem,"nommage"))
            if nom not in conf:
                conf[nom]=[]
            conf[nom].append(format_fichier)
    
        conf={
            **conf,
            **{
                "{}_path".format(prefixe_variable(elem,"path")):elem.get("chemin")
                for elem in livrable.xpath(".//*[@chemin]")   
            }
        }
        
        for elem in livrable.xpath(".//proprietaire/*[not(self::dossier)]"):
            dossier=elem.getprevious()
            nommage=dossier.getchildren()
            nom_conf="{}_path".format(prefixe_variable(elem,"path"))
            
            if nommage:
                conf[nom_conf]=os.path.join(
                    *[
                        dossier.get("chemin"),
                        format_fichier_xml(elem.getprevious().getchildren()[0])
                    ],
                    elem.get("chemin")
                )
            else:
                conf[nom_conf]=os.path.join(
                        dossier.get("chemin"),
                        elem.get("chemin")
                )
                
        conf["dpt"] = livrable.get("dpt")
        conf.update({k:os.path.join(chemin_livrable,conf[k]) for k in conf if "path" in k})
        conf_dpt[conf["dpt"]]=conf
    
    return conf_dpt