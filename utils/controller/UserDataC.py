from utils.dao.UserDataDAO import *
from utils.entities.UserDataM import *

class ClassUserDataC:

    @staticmethod
    def addOneUser(obj_user: ClassUserDataM):
        """
        Ajoute les données d'un nouvel utilisateur.
        """
        try:
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
            res = ClassUserDataC.findOneByEmail(email)
            if res == 'AUCUN UTILISATEUR TROUVE':
                return res
            else:
                
                # envoyer un mail 
                # sauvegarder le code + email
                ClassUserDataDAO().loginTableInsert()
                pass
        except Exception as e:
            print(f"Erreur_UserDataC.loginRequest() ::: {e}")

    @staticmethod
    def loginAuth(email, code):
        try:
            # fonction dao de récup (email, code)

            res = ClassUserDataDAO().loginTableRead(email)

            if res[0] == email and  res[1] == code:
                return True
            else:
                return False
        except Exception as e:
            print(f"Erreur_UserDataC.loginAuth() ::: {e}")