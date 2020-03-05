from quadraenv import QuadraSetEnv
from configparser_NT import conf
from query_ctrl_pj_ectriture import get_ref_img
import os
import pprint

pp = pprint.PrettyPrinter(indent=4)

config = conf('conf_ctrl_pj_ecriture.ini')
ipl = config.get('path', 'ipl')

Q= QuadraSetEnv(ipl)

reporting_error = {}
liste_path_all_DC = Q.chemins_cpta(categ="DC")


for path in  liste_path_all_DC:

    code_client = os.path.basename(path)
    liste_pj_compta = get_ref_img(os.path.join(path, 'qcompta.mdb'))
    contenu_fichier_img = os.listdir(os.path.join(path, "Images"))

    for pj_ecriture in liste_pj_compta[:1]:

        if pj_ecriture in contenu_fichier_img:
            pass
        else:
            pass
            #controle si existant dans le report précédent
            # Si oui on continu
            # si non on ajoute.
            

