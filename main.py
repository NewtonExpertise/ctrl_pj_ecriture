from quadraenv import QuadraSetEnv
from configparser_NT import conf
from modele import get_pjinfos_bdd_quadra
from query_ctrl_pj_ectriture import Query_pj_ecriture
from mail_suivie_pj import relance_mail
import os
from datetime import datetime
import pprint

pp = pprint.PrettyPrinter(indent=4)

config = conf('conf_ctrl_pj_ecriture.ini')
ipl = config.get('path', 'ipl')

Q= QuadraSetEnv(ipl)
QPJE = Query_pj_ecriture()

reporting_error = {}


#on récupère le chemin de chaque dossier
liste_path_all_DC = Q.chemins_cpta(categ="DC")
i=0
rapport_txt = False

for path in  liste_path_all_DC:
    i+=1
    # if i <15 :
    print("Avancement : "+str(i/len(liste_path_all_DC)*100))
    try:
        pj_infos_quadra = get_pjinfos_bdd_quadra(path)
    except Exception as e:
        print('ERRRREUUURRRRR')
        print(e)
        print(path)
    if pj_infos_quadra:
        if os.path.isdir(os.path.join(path, "Images")) :
            contenu_fichier_img = os.listdir(os.path.join(path, "Images"))
            for ref_img, infos_pj in pj_infos_quadra.items():
                if ref_img in contenu_fichier_img:
                    continue
                else:
                    infos_missing_pj_pg = QPJE.get_infos_pj(ref_img)

                if infos_missing_pj_pg:
                    continue
                else:
                    # insertion PG
                    periode_ex = QPJE.get_periode_exercice(os.path.join(path, 'qcompta.mdb'))
                    infos_pj['cloture'] = periode_ex['fin']
                    reporting_error[ref_img] = infos_pj
                    QPJE.query_pj_missing_insert_pg(infos_pj['code_client'], infos_pj['cloture'].strftime("%d/%m/%Y"), infos_pj['NumeroCompte'],infos_pj['CodeJournal'],
                                                    infos_pj['Folio'], infos_pj['LigneFolio'], infos_pj['PeriodeEcriture'].strftime("%d/%m/%Y"),
                                                    infos_pj['JourEcriture'], infos_pj['Libelle'],
                                                    infos_pj['Solde'], infos_pj['NumeroPiece'], infos_pj['CodeLettrage'], infos_pj['CodeOperateur'],
                                                    infos_pj['DateSysSaisie'].strftime("%d/%m/%Y"), ref_img)

mail = relance_mail()
corps_tableau = ""

rapport_txt = 'Dossier;Ref image;Compte;Periode ecriture;Ligne folio;Libelle;Solde;Num Piece;Operateur;DateSysSaisie\n'
if reporting_error:
    for ref_img, infos_pj in reporting_error.items():

        corps_tableau += mail.corps_tableau(infos_pj['code_client'] ,ref_img, infos_pj['NumeroCompte'], infos_pj['PeriodeEcriture'], 
                                            infos_pj['LigneFolio'], infos_pj['Libelle'], infos_pj['Solde'], 
                                            infos_pj['NumeroPiece'], infos_pj['CodeOperateur'], infos_pj['DateSysSaisie'])
    
        rapport_txt += f"{infos_pj['code_client']};{ref_img};{infos_pj['NumeroCompte']} \
        ;{infos_pj['PeriodeEcriture']};{infos_pj['LigneFolio']};{infos_pj['Libelle']} \
        ;{infos_pj['Solde']};{infos_pj['NumeroPiece']};{infos_pj['CodeOperateur']};{infos_pj['DateSysSaisie']}\n"
                        
if rapport_txt:
    with open('rapport_pj_missing.txt', "w") as rapport:
        rapport.write(rapport_txt)
else:
    with open('rapport_pj_missing.txt', "w") as rapport:
        rapport.write("Pas de PJ manquante")

mail.piece_jointe('rapport_pj_missing.txt')
print(corps_tableau)
mail.corps_mail(corps_tableau)
mail.send_mail(['mathieu.leroy@newtonexpertise.com', 'mathieu.leroy@newtonexpertise.com'])

