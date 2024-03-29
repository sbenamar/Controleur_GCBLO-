from lxml import etree
import os,zipfile,glob

def format_fichier_xml(elem):
    format_pre=["pre_code_zasro","code_zasro","separateur_zasro_etr","code_etr","branche_optique"]
    format_post=["nom"]
    format_variables_complexes=["pt1_pt2","insee_id"]
    format_variables_simples=["commune","id","canton","pt1"]
    
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

def get_conf_xml(chemin_courant,xml_livrables_path="conf/livrables.xml",type_livrable=False,zone_livrable=False,return_conf=None):
    parser = etree.XMLParser(dtd_validation=True)
    try:
        root = etree.parse(xml_livrables_path,parser)
    except etree.XMLSyntaxError as e:
        print("Mauvais schema XML: "+str(e))
        exit()
    
    conf_dpt={}
    duplicate_cd21=True
    
    #Gerer le cas ou il y a plusieurs fois un element pour mettre plusieurs chemins
    for livrable in root.xpath("//livrable"):
        conf,dpt={},livrable.get("dpt")
        conf["code_zasro"]=None
        conf["code_zasro_alt"]=None
        conf["archive"]=False
        
        if (dpt,type_livrable,zone_livrable) == ("CD21","EXE","Distribution"):
            try:
                chemin_livrable=os.path.join(chemin_courant,"Livrable")
                
                if return_conf is not None:
                    try:
                        zipf = glob.glob(os.path.join(chemin_livrable,"*.zip"))
                        if len(zipf) == 1:
                            zipfile.ZipFile(zipf[0], "r").extractall(chemin_livrable)
                    except Exception as e:
                        pass
                
                dossier_livrable=glob.glob(os.path.join(chemin_livrable,"*/"))[-1]
                chemin_livrable=os.path.join(chemin_livrable,dossier_livrable)
                conf["code_zasro"]=dossier_livrable[:14]
                conf["code_zasro_alt"]= (lambda x:x[:-2]+x[-2].replace("0","")+x[-1])(conf["code_zasro"])
                conf["archive"]=True
                duplicate_cd21=False
            except:
                pass
        else:
            chemin_livrable=os.path.join(chemin_courant,"Commande")

        conf["dossier_path"]=chemin_livrable
        conf["app_path"]=chemin_courant
        conf["livrable_path"]=os.path.join(chemin_courant,"Livrable")
        
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
    
    conf_dpt["CD39"],conf_dpt["CD58"],conf_dpt["CD70"],conf_dpt["CD71"]=[conf_dpt["CDXX"].copy() for nb in range(4)]
    conf_dpt["CD39"]["dpt"]="CD39"
    conf_dpt["CD58"]["dpt"]="CD58"
    conf_dpt["CD70"]["dpt"]="CD70"
    conf_dpt["CD71"]["dpt"]="CD71"
    
    if duplicate_cd21:
        conf_dpt["CD21"]=conf_dpt["CDXX"].copy()
        conf_dpt["CD21"]["dpt"]="CD21"
    
    if return_conf is not None:
        return_conf[0]=conf_dpt
    return conf_dpt
