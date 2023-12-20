import time
from time import sleep
from threading import Thread
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from random import randint
from json import load
from typing import Optional

REFRESH_TIME = 3

# Base email for code verification
TITTLE_CODE_VERIF = "NightON : Code de Vérification {code}"
HTML_FILE_CODE_VERIF = "code_verification"


class Mailer:
    data = None

    def __init__(self):
        self.loadConfigData()
        self.initSMTPConnection()
        # Scheduled Refresh connection in a separate thread
        Thread(target=self.refreshConnection).start()

    def initSMTPConnection(self):
        if self.isValidConfig():
            smtp_server = self.data["smtp"]
            smtp_port = self.data["port"]
            smtp_username = self.data["username"]
            smtp_password = self.data["password"]
            try:
                self.server = SMTP_SSL(smtp_server, smtp_port)
                self.server.login(smtp_username, smtp_password)
            except:
                print("<NIGHTON_MAILER> : Impossible de se connecter au serveur SMTP")
            print("<NIGHTON_MAILER> : SERVEUR SMT Connecté")

    def loadConfigData(self):
        try:
            with open('config.json') as f:
                self.data = load(f)
        except:
            print("<NIGHTON_MAILER> : Erreur dans la lecture de la config")
            self.data = {}

    def isValidConfig(self):
        return bool(self.data)

    def sendEmailCode(self, emailDestination: str) -> int:
        code = randint(10000, 99999)
        self.sendEmail(emailDestination, TITTLE_CODE_VERIF, HTML_FILE_CODE_VERIF, {"code" : code})
        return code

    def sendEmail(self, emailDestination: str, mailTitle: str, mailContentTemplateFile: str, placeholders: dict = {}):
        from_address = self.data["username"]
        message = MIMEMultipart()
        message['From'] = from_address
        message['To'] = emailDestination
        message['Subject'] = mailTitle

        body = self.readMailTemplate(mailContentTemplateFile)
        for k, v in placeholders.items():
            body = body.replace("{" + k + "}", str(v))

        # Utilisez 'html' comme type de contenu pour le message
        message.attach(MIMEText(body, 'html'))

        print(f"<NIGHTON_MAILER> : mail {mailContentTemplateFile}.html envoyé à {emailDestination} avec succès")
        self.server.sendmail(self.data["username"], emailDestination, message.as_string())

    def refreshConnection(self):
        while True:
            sleep(REFRESH_TIME)
            try:
                self.server.quit()
            except:
                pass
            self.initSMTPConnection()

    def __del__(self):
        try:
            self.server.quit()
        except:
            pass

    def readMailTemplate(self, mailFile: str) -> str:
        try:
            buffer = open(f"mails/{mailFile}.html", 'rb')
        except OSError:
            print(f"<NIGHTON_MAILER> : Impossible d'ouvrir le fichier mails/{mailFile}.html")
            return ""

        with buffer:
            return str(buffer.read().decode('utf-8'))