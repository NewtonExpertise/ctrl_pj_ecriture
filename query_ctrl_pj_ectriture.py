from mdbagent import MdbConnect

def get_ref_img(mdbpath):
    sql = f"""
    SELECT NumeroCompte, CodeJournal, Folio , LigneFolio, PeriodeEcriture, JourEcriture, Libelle, MontantTenuDebit, MontantTenuCredit, NumeroPiece, CodeLettrage, CodeOperateur, DateSysSaisie, RefImage
    FROM Ecritures
    WHERE RefImage <> ''
    """
    with MdbConnect(mdbpath) as mdb:
        data = mdb.query(sql)
    return data

def query_save_reporting():
    sql = f"""
    INSERT INTO 

    """