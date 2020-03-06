from quadraenv import QuadraSetEnv
from configparser_NT import conf
from modele import get_pjinfos
from query_ctrl_pj_ectriture import Query_pj_ecriture
import os
import pprint

pp = pprint.PrettyPrinter(indent=4)

config = conf('conf_ctrl_pj_ecriture.ini')
ipl = config.get('path', 'ipl')

Q= QuadraSetEnv(ipl)
QPJE = Query_pj_ecriture()

reporting_error = {}
liste_path_all_DC = Q.chemins_cpta(categ="DC")


for path in  liste_path_all_DC:

    pj_infos = get_pjinfos(path)
    if pj_infos:
        if os.path.isdir(os.path.join(path, "Images")) :
            contenu_fichier_img = os.listdir(os.path.join(path, "Images"))
            for ref_img, infos_pj in pj_infos.items():
                if ref_img in contenu_fichier_img:
                    continue
                else:
                    pj_exist_in_pg = QPJE.check_pj_exist(ref_img)
                    if pj_exist_in_pg:
                        


    # # for pj_ecriture in liste_pj_compta[:1]:
    # #     print(liste_pj_compta)



        # if pj_ecriture in contenu_fichier_img:
        #     continue
        # else:
        #     infos_pj_ecriture = QPJE.check_pj_exist(pj_ecriture)
        #     if infos_pj_ecriture:
        #         continue
        #     else:
                
        #         QPJE.query_pj_missing()############ mettre es argument
            #controle si existant dans le report précédent
            # Si oui on continu
            # si non on ajoute.