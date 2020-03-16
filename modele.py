from query_ctrl_pj_ectriture import Query_pj_ecriture
import os


QPJE = Query_pj_ecriture()


def get_pjinfos_bdd_quadra(path):
    liste_pj_compta = QPJE.get_ref_img(os.path.join(path, 'qcompta.mdb'))
    pj_compta_info = {}
    if liste_pj_compta:
        code_client = os.path.basename(path)
        for NumeroCompte, CodeJournal, Folio , LigneFolio, PeriodeEcriture,\
            JourEcriture, Libelle, MontantTenuDebit, MontantTenuCredit,NumeroPiece,\
            CodeLettrage, CodeOperateur, DateSysSaisie, RefImage in  liste_pj_compta:
            if MontantTenuCredit:
                Solde = MontantTenuCredit
            elif MontantTenuDebit:
                Solde = MontantTenuDebit

            pj_compta_info[RefImage] = {'code_client':code_client, 'NumeroCompte':NumeroCompte, 'CodeJournal':CodeJournal,
                            'Folio':Folio , 'LigneFolio':LigneFolio,'PeriodeEcriture':PeriodeEcriture,
                            'JourEcriture':JourEcriture, 'Libelle':Libelle, 'Solde':Solde,'NumeroPiece':NumeroPiece,
                            'CodeLettrage':CodeLettrage, 'CodeOperateur':CodeOperateur,'DateSysSaisie':DateSysSaisie}
            
    return pj_compta_info

if __name__ == "__main__":
    import pprint
    pp= pprint.PrettyPrinter(indent=4)
    pp.pprint(get_pjinfos(r'\\srvquadra\Qappli\Quadra\DATABASE\cpta\DC\000004'))