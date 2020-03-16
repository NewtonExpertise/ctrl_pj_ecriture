# coding: utf-8

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email import encoders
import os

class relance_mail():
    def __init__(self):

        self.mail = ''
        self.msg = MIMEMultipart()
        self.host = 'smtp.serinyatelecom.fr'
        self.port = 25


    def corps_tableau(self, Dossier, refimg, NumeroCompte, Periode_ecriture, Ligne_folio, Libelle, Solde, NumeroPiece, CodeOperateur, DateSysSaisie):
        """
        Alimente le tableau contenu dans le corps du mail.
        """
        # nous pouvons intégrer le niveau de relance dans le tableau.
        corps_tableau = f"""
                <tr>
                    <td style="text-align: left; padding:2px; padding-left: 20px; padding-right: 40px;">{Dossier}</td>
                    <td style="text-align: left; padding:2px; padding-left: 20px; padding-right: 40px;">{refimg}</td>
                    <td style="text-align: left; padding:2px; padding-left: 20px; padding-right: 40px;">{NumeroCompte}</td>
                    <td style="text-align: left; padding:2px; padding-left: 20px; padding-right: 40px;">{Periode_ecriture}</td>
                    <td style="text-align: right; padding:2px; padding-left: 20px; padding-right: 40px;">{Ligne_folio}</td>
                    <td style="text-align: right; padding:2px; padding-left: 20px; padding-right: 40px;">{Libelle}</td>
                    <td style="text-align: right; padding:2px; padding-left: 20px; padding-right: 40px;">{Solde}</td>
                    <td style="text-align: right; padding:2px; padding-left: 20px; padding-right: 40px;">{NumeroPiece}</td>
                    <td style="text-align: right; padding:2px; padding-left: 20px; padding-right: 40px;">{CodeOperateur}</td>
                    <td style="text-align: right; padding:2px; padding-left: 20px; padding-right: 40px;">{DateSysSaisie}</td>
                </tr>
            """
        return corps_tableau

    def piece_jointe(self, pathpiècejointe):
        """
        Ajoute une pièce jointe au mail.
        """

        with open(pathpiècejointe, "rb") as f:   ## Ouverture du fichier
            pieceJointe = MIMEBase('application', 'octet-stream')    ## Encodage de la pièce jointe en Base64
            pieceJointe.set_payload(f.read())
            encoders.encode_base64(pieceJointe)
            pieceJointe.add_header('Content-Disposition', "piece; filename= %s" % pathpiècejointe)
            self.msg.attach(pieceJointe)   ## Attache de la pièce jointe à l'objet "message" 

        

    def corps_mail(self, corps_tableau):
        
        self.msg['Subject'] = "Reporting pièces jointes "

        message = f"""<html>
        <body>
            <p style="width: 50px; font-family:Calibri;">
                <p style="text-align : justify ; ">Contrôle présence pièces jointes reporting.</p>

                <fieldset style="border-radius:8px; border: thick double; border-color: #F6A737;">
                    <legend style="padding:5px; text-align:center"><strong style='text-align:center;'>Liste des dossiers et pièces jointes manquantes : </strong></legend>
                    <table style="border-collapse: collapse;margin:auto"  style="border-radius:8px; border: thick double; border-color: #F6A737;" >
                    
                        <thead style="background-color: #F6A737">
                            <tr>
                                <th style="text-align: left; padding:2px; padding-left: 20px; padding-right: 40px;">Dossier</th>
                                <th style="text-align: left; padding:2px; padding-left: 20px; padding-right: 40px;">Ref image</th>
                                <th style="text-align: left; padding:2px; padding-left: 20px; padding-right: 40px;">Compte</th>
                                <th style="text-align: left; padding:2px; padding-left: 20px; padding-right: 40px;">Periode ecriture</th>
                                <th style="text-align: left; padding:2px; padding-left: 20px; padding-right: 40px;">Ligne folio</th>
                                <th style="text-align: left; padding:2px; padding-left: 20px; padding-right: 40px;">Libelle</th>
                                <th style="text-align: left; padding:2px; padding-left: 20px; padding-right: 40px;">Solde</th>
                                <th style="text-align: left; padding:2px; padding-left: 20px; padding-right: 40px;">Num Piece</th>
                                <th style="text-align: left; padding:2px; padding-left: 20px; padding-right: 40px;">Operateur</th>
                                <th style="text-align: left; padding:2px; padding-left: 20px; padding-right: 40px;">DateSysSaisie</th>
                            </tr>
                        </thead>
                        <tbody>
                        {corps_tableau}
                        </tbody>
                       
                    </table>
                    
                </fieldset>
                <br>
                
                Cordialement.<br>

                <p
                    style="margin-left: 50px; color: rgb(138, 138, 138); font-size: 13px; font-family:  'Trebuchet MS', 'Lucida Sans Unicode', 'Lucida Grande', 'Lucida Sans', Arial, sans-serif ;">
                    22 rue Raymond Aron -
                    76130 <strong>Mont-Saint-Aignan</strong><br>
                    32 rue de Londres - 75009 <strong>Paris </strong><br>
                    <strong>Tél.Mont-Saint-Aignan : </strong>02 35 12 20 60 <br>
                    <strong>Tél.Paris : </strong>01 53 20 42 86<br>
                    <strong>Fax : </strong>02 35 61 39 49<br>
                    <strong><a href="http://www.newtonexpertise.com/">www.newtonexpertise.com</a></strong> <br>
                    <strong>Retrouvez-nous sur les réseaux sociaux</strong><br>
                    <a href="https://www.facebook.com/newtonexpertise?fref=ts">Facebook</a>
                    <a href="https://twitter.com/NewtonExpertise">Twitter</a>
                </p>
                <p style="margin-left: 50px;""><strong
                        style="font-family: 'Gill Sans' , 'Gill Sans MT' , Calibri, 'Trebuchet MS' , sans-serif;">Pour
                    mieux vous accompagner dans vos projets et faire vivre vos idées, l’équipe de <strong
                        style="color:rgb(197, 118, 0)">Newton Expertise</strong> s’engage à vos côtés pour vous offrir un
                    service personnalisé.</strong>
                </p>
                <p style=" margin-left: 50px; color: rgb(156, 146, 146); font-size: 13px;">L'intégrité de ce message n'étant
                    pas assurée sur internet, Newton Expertise ne peut être
                    tenu responsable de son contenu. Toute utilisation ou diffusion non autorisée est interdite.
                    Si vous n'êtes pas destinataire de ce message, merci de le détruire et d'avertir l'expéditeur.</p>

            </p>
        </body>

        </html>
        """
        self.msg.attach(MIMEText(message,'html'))
        

    def add_img_corp_mail(self):

        with open(r'C:\Users\mathieu.leroy\Desktop\relance_client_test\imgmail.jpg', 'rb') as i:
            logo = MIMEImage(i.read())
        logo.add_header('Content-ID', '<logo_newton>')
        self.msg.attach(logo)


    def send_mail(self, list_destinataire):


        print(list_destinataire)
        mailserver = smtplib.SMTP(self.host , self.port)

        try:
            x=mailserver.sendmail('mathieu.leroy@newtonexpertise.com', list_destinataire, self.msg.as_string())

            print(x)
        except smtplib.SMTPException as e:
            print(e)

        mailserver.quit()

# nicolas.rollet@newtonexpertise.com
# mathieu.leroy@newtonexpertise.com
# jasmine.lefebvre@newtonexpertise.com

    # def set_mail_relance(self):

if __name__ == '__main__':
    x= relance_mail()
    i=1
    a=""
    while i < 10:
        i+=1
        a += x.corps_tableau("Dossier", "refimg", "Periode_ecriture", "Ligne_folio", "Libelle", "Solde", "NumeroPiece", "CodeOperateur", "DateSysSaisie")

    x.corps_mail("mathieu.leroy@newtonexpertise.com",a)
    x.send_mail()