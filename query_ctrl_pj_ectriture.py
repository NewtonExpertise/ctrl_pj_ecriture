from mdbagent import MdbConnect
from postgreagent import PostgreAgent
from configparser_NT import conf
from collections import OrderedDict




class Query_pj_ecriture():

    def __init__(self):
        config = conf('conf_ctrl_pj_ecriture.ini')
        host = config.get('postgre_conf', 'host')
        user = config.get('postgre_conf', 'user')
        password = config.get('postgre_conf', 'password')
        port = config.get('postgre_conf', 'port')
        dbname = config.get('postgre_conf', 'dbname')
        self.conf_postgre = OrderedDict([('host', host), ('user', user), ('password', password), ('port', port), ('dbname', dbname)])
    
    
    # BDD QUADRA

    def get_periode_exercice(self, mdbpath):
        """
        Renvoie la listes des mois de l'exercice.
        """
        sql = """
        SELECT DebutExercice, FinExercice, DateLimiteSaisie
        FROM Dossier1
        """
        with MdbConnect(mdbpath) as mdb:
            periode = mdb.query(sql)
        
        for debut, fin , limite in periode:
            periode_ex = {"debut":debut, "fin":fin, "limite":limite}
        return periode_ex

    def get_ref_img(self, mdbpath):
        sql = f"""
        SELECT NumeroCompte, CodeJournal, Folio , LigneFolio, PeriodeEcriture,
                JourEcriture, Libelle, MontantTenuDebit, MontantTenuCredit, 
                NumeroPiece, CodeLettrage, CodeOperateur, DateSysSaisie, RefImage
        FROM Ecritures
        WHERE RefImage <> ''
        """
        with MdbConnect(mdbpath) as mdb:
            data = mdb.query(sql)
        return data


    # BDD POSTGRE
    def query_pj_missing_insert_pg(self, Code_client, Cloture, NumeroCompte, CodeJournal,
                                Folio, LigneFolio, PeriodeEcriture, 
                                JourEcriture, Libelle, Solde, NumeroPiece,
                                CodeLettrage, CodeOperateur, DateSysSaisie,RefImage):
        sql = f"""
        INSERT INTO pj_ecriture (Code_client, Cloture, NumeroCompte, CodeJournal,
                                Folio, LigneFolio, PeriodeEcriture, 
                                JourEcriture, Libelle, Solde, NumeroPiece,
                                CodeLettrage, CodeOperateur, DateSysSaisie, RefImage)
        VALUES ({Code_client}, {Cloture}, {NumeroCompte}, {CodeJournal},
                                {Folio}, {LigneFolio}, {PeriodeEcriture}, 
                                {JourEcriture}, {Libelle}, {Solde}, {NumeroPiece},
                                {CodeLettrage}, {CodeOperateur}, {DateSysSaisie},{RefImage})
        """
        with PostgreAgent(self.conf_postgre) as db:
            pass
    

    def check_pj_exist(self, RefImage):
        sql = f"""
        SELECT Code_client, Cloture, NumeroCompte, Libelle, Solde, CodeOperateur, DateSysSaisie, RefImage
        FROM pj_ecriture
        WHERE RefImage = {RefImage}
        """
        with PostgreAgent(self.conf_postgre) as db:
            pass