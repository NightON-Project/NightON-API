import uuid
from utils.dao.UserDataDAO import *
from utils.entities.UserDataM import *

from utils.mailer.mailerNightON import *


class ClassUserDataC:
    @staticmethod
    def checkUserExists(email: str):
        """Vérifie qu'un user existe avec cet email dans la base.

        Args:
            obj_user (ClassUserDataM)

        Returns:
            bool : True | False
        """
        try:
            res = False
            if ClassUserDataDAO().findAllByOne(key=email):
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
            if ClassUserDataC.checkUserExists(obj_user.email_user):
                return "USER ALREADY EXISTS"

            # obj_user = ClassUserDataM(**obj_user)
            # print(f"Type objet envoyé {type(obj_user)}")
            res = ClassUserDataDAO().insertOne(entity_instance=obj_user)

            if res == 0:
                return f"ERROR"
            else:
                return "DONNEES ENREGISTREES"
        except Exception as e:
            print(f"erreur_ClassUserDataC.addOne() ::: {e}")
            return f"{e}"

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
                return "AUCUN UTILISATEUR TROUVE"
            return res
        except Exception as e:
            print(f"erreur_ClassUserDaraC.findOneByEmail() ::: {e}")
            return "ERROR"

    @staticmethod
    def updateUserData(obj_user: ClassUserDataM):
        """
        Modifier les données d'un utilisateur par son email.
        Args:
            obj_user (ClassUserDataM): nouvelles données utilisateur
        """
        try:
            res = ClassUserDataDAO().modifyOne(
                key=obj_user.email_user, entity_instance=obj_user
            )
            if res == 0:
                return f"ERROR"
            else:
                return "DONNEES ENREGISTREES"
        except Exception as e:
            print(f"Erreur_ClassUserDataC.updateUserData() ::: {e}")
            return f"{e}"

    @staticmethod
    def deleteUser():
        pass

    @staticmethod
    def loginRequest(email: str) -> None:
        # try un display sans le faire
        try:
            res: ClassUserDataM = ClassUserDataC.findOneByEmail(email)
            if res == "AUCUN UTILISATEUR TROUVE":
                return res
            else:
                # res est pareil que objUser
                mailer = Mailer(timeout=5)
                mailer.sendEmail(
                    emailDestination=res.email_user,
                    mailTitle="VOTRE CODE DE CONNEXION",
                    mailContentTemplateFile="../mailer/mails/code_verification",
                    placeholders={
                        "surname": res.firstname_user,
                        "name": res.lastname_user,
                    },
                )

                code_value, operationResult = mailer.sendEmailCode(
                    emailDestination=res.email_user
                )
                # envoyer un mail
                # sauvegarder le code + email
                operationResult = True  # enlever après Titoune
                print(code_value)
                print(operationResult)
                if operationResult:
                    user_in_login_table = ClassUserDataDAO().loginTableRead(
                        res.email_user
                    )  # si le mail est present, update le code :: pas d'historique
                    if not user_in_login_table:
                        ClassUserDataDAO().loginTableInsert(
                            email=res.email_user, code=code_value
                        )
                    ClassUserDataDAO().loginTableUpdateCode(
                        code=code_value, email=res.email_user
                    )
                else:
                    print(f"Erreur_UserDataC.loginRequest()")
        except Exception as e:
            print(f"Erreur_UserDataC.loginRequest() ::: {e}")

    @staticmethod
    def loginAuth(email, code=None, from_firebase=False):
        try:
            if from_firebase:
                exists = ClassUserDataC.checkUserExists(email)
                print(f"does mail exists {exists}")
                if exists:
                    return True
                else:
                    return False

            # si auth pas faite avec firebase -> fonction dao de récup (email, code)
            res = ClassUserDataDAO().loginTableRead(email)
            print(res)
            if len(code) != 5:
                return False
            if res[0] == email and res[1] == code:
                return True
            else:
                return False
        except Exception as e:
            print(f"Erreur_UserDataC.loginAuth() ::: {e}")
