import uuid
from utils.dao.UserDataDAO import *
from utils.entities.UserDataM import *

from utils.mailer.mailerNightON import *

class ClassUserDataC:

    @staticmethod
    def checkUserExists(obj_user: ClassUserDataM):
        """Vérifie que le user existe dans  la base par son email.

        Args:
            obj_user (ClassUserDataM)

        Returns:
            bool : True | False
        """
        try:
            res = False
            if ClassUserDataDAO().findAllByOne(key=obj_user.email_user):
                res = True
            
            return res
        except Exception as e:
            raise e

    @staticmethod
    def addOneUser(obj_user: ClassUserDataM):
        """
        Ajoute les données d'un nouvel utilisateur.
        """
        try:
            # vverif si user exist
            if ClassUserDataC.checkUserExists():
                return 'USER ALREADY EXISTS'

            #obj_user = ClassUserDataM(**obj_user)
            #print(f"Type objet envoyé {type(obj_user)}")
            res = ClassUserDataDAO().insertOne(entity_instance=obj_user)

            if res == 0:
                return f'ERROR'
            else:
                return 'DONNEES ENREGISTREES'
        except Exception as e:
            print(f'erreur_ClassUserDataC.addOne() ::: {e}')
            return f'{e}'
        
    @staticmethod
    def findOneByEmail(email: str):
        """
        Trouver un utilisateur par son email.
        Args:
            email (str): email utilisateur. 
        Returns:
            ClassUserDataM object
        """
        try:
            res = ClassUserDataDAO().findAllByOne(email)
            if res is None:
                return 'AUCUN UTILISATEUR TROUVE'
            return res
        except Exception as e:
            print(f'erreur_ClassUserDaraC.findOneByEmail() ::: {e}')
            return 'ERROR'
    
    @staticmethod
    def updateUserData(obj_user: ClassUserDataM):
        """
        Modifier les données d'un utilisateur par son email.
        Args:
            obj_user (ClassUserDataM): nouvelles données utilisateur
        """
        try:
            res = ClassUserDataDAO().modifyOne(key=obj_user.email_user, entity_instance=obj_user)
            if res == 0:
                return f'ERROR'
            else:
                return 'DONNEES ENREGISTREES'
        except Exception as e:
            print(f'Erreur_ClassUserDataC.updateUserData() ::: {e}')
            return f'{e}'

    @staticmethod
    def deleteUser():
        pass

    @staticmethod
    def loginRequest(email: str):

        # try un display sans le faire
        try:
            res: ClassUserDataM = ClassUserDataC.findOneByEmail(email)
            if res == 'AUCUN UTILISATEUR TROUVE':
                return res
            else:
                # res est pareil que objUser
                mailer = Mailer(timeout=5) 
                mailer.sendEmail(
                    emailDestination = res.email_user,
                    mailTitle = 'VOTRE CODE DE CONNEXION',
                    mailContentTemplateFile = '../mailer/mails/code_verification',
                    placeholders = {
                        "surname": res.firstname_user,
                        "name": res.lastname_user
                    }
                )

                code_value, operationResult = mailer.sendEmailCode(emailDestination = res.email_user)
                # envoyer un mail 
                # sauvegarder le code + email
                operationResult = True # enlever après Titoune
                print(code_value)
                print(operationResult)
                if operationResult:
                    ClassUserDataDAO().loginTableInsert(email = res.email_user, code = code_value)
                else:
                    print(f"Erreur_UserDataC.loginRequest()")
        except Exception as e:
            print(f"Erreur_UserDataC.loginRequest() ::: {e}")

    @staticmethod
    def loginAuth(email, code):
        try:
            # fonction dao de récup (email, code)
            res = ClassUserDataDAO().loginTableRead(email)
            print(res)
            if res[0] == email and  res[1] == code:
                return True, uuid.uuid4()
            else:
                return False
        except Exception as e:
            print(f"Erreur_UserDataC.loginAuth() ::: {e}")