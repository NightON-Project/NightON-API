import time
from time import sleep
from threading import Thread
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from random import randint
from json import load
from typing import Optional

# Base email for code verification
TITTLE_CODE_VERIF = "NightON : Code de Vérification {code}"
HTML_FILE_CODE_VERIF = "code_verification"


class Mailer:
    data = None

    def __init__(self, timeout : int):
        '''
        Constructeur,
        timeout -> correspond au temps de refresh avant de renouveler la connexion au serveur SMTP (car la connexion
        peut se perdre en route) et de refresh la config du serveur.
        '''
        self.timeout = timeout
        self.loadConfigData()
        self.initSMTPConnection()
        # On lance dans un thread différent la fonctionnalité de refresh de la connexion.
        Thread(target=self.refreshConnection).start()

    def initSMTPConnection(self):
        '''
        Méthode qui initialise ou actualise la connexion au serveur SMTP
        '''
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
            #print("<NIGHTON_MAILER> : SERVEUR SMT Connecté")
    def isValidConfig(self):
        return "smtp", "port", "username", "password" in self.data.keys()
    def loadConfigData(self):
        '''
        Méthode qui lit et met à jour la configuration au SMTP (de cette manière on peut switch de serveur SMTP sans
        interrompre l'execution du programme (car la config se met à jour tout les $REFRESH_TIME secondes.
        '''
        try:
            with open('config.json') as f:
                self.data = load(f)
        except:
            print("<NIGHTON_MAILER> : Erreur dans la lecture de la config")
            self.data = {}

    def sendEmailCode(self, emailDestination: str) -> (int, bool):
        '''
        Méthode qui a pour but d'envoyer un mail particulier puisqu'elle s'occupe aussi de générer un code aléatoire
        puis de le passer en paramètre à la fonction sendEmail.
        '''
        import os
        # récupérer le chemin du répertoire courant
        path = os.getcwd()
        print("Le répertoire courant est : " + path)
        # récupérer le nom du répertoire courant
        repn = os.path.basename(path)
        print("Le nom du répertoire est : " + repn)
        code = randint(10000, 99999)
        return code, self.sendEmail(emailDestination, TITTLE_CODE_VERIF, HTML_FILE_CODE_VERIF, {"code" : code})

    def sendEmail(self, emailDestination: str, mailTitle: str, mailContentTemplateFile: str, placeholders: dict = {}) -> bool:
        '''
        Méthode principale du programme,
        Elle prend en entrée :
        - emailDestination  : email de destination (pas de checking de si l'email est valide)
        - mailTitle         : titre du mail
        - mailContentTemplateFile : chemin vers le contenu HTML à lire
        - placeholders      : placeholders permet de remplir le contenu HTML qui est statique avec des paramètres dynamiques à remplacer directement

        Fonctionnement :
        Cette méthode va lire le contenu du fichier HTML donné en entrée en y remplaçant les placeholders par des réelles
        variables calculées en amont de la fonction.

        Exemple :
        <font color="aqua">Votre code est {code}</font>
        => on va remplacer {code} par la donnée en entrée.
        '''
        from_address = self.data["username"]
        message = MIMEMultipart()
        message['From'] = from_address
        message['To'] = emailDestination

        body, state = self.readMailTemplate(mailContentTemplateFile)
        for k, v in placeholders.items():
            body = body.replace("{" + k + "}", str(v))
            mailTitle = mailTitle.replace("{" + k + "}", str(v))

        # Utilisez 'html' comme type de contenu pour le message
        message.attach(MIMEText(body, 'html'))
        message['Subject'] = mailTitle

        print(f"<NIGHTON_MAILER> : mail {mailContentTemplateFile}.html envoyé à {emailDestination} avec succès")
        self.server.sendmail(self.data["username"], emailDestination, message.as_string())
        return state

    def refreshConnection(self):
        '''
        Met à jour la connection
        '''
        while True:
            sleep(self.timeout)
            try:
                self.server.quit()
            except:
                pass
            self.loadConfigData()
            self.initSMTPConnection()

    def __del__(self):
        try:
            self.server.quit()
        except:
            pass

    def readMailTemplate(self, mailFile: str) -> (str, bool):
        '''
        Lit le fichier html donné en entrée et renvoie le resultat sous forme d'une chaine de caractère et d'un booléen
        qui vérifie que l'opération s'est correctement déroulé.
        '''

        try:
            buffer = open(f"./mailer/mails/{mailFile}.html", 'rb')
        except OSError:
            print(f"<NIGHTON_MAILER> : Impossible d'ouvrir le fichier mails/{mailFile}.html")
            return "", False

        with buffer:
            return str(buffer.read().decode('utf-8')), True