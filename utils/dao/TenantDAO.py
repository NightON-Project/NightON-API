import os
import sys
import uuid
from utils.dao import ModelDAO

CURRENT_FILEPATH = os.path.dirname(os.path.abspath(__file__))
ENTITIES_FOLDER_PATH = os.path.join(CURRENT_FILEPATH, '..')
sys.path.insert(0, ENTITIES_FOLDER_PATH)

from entities.UserDataM import ClassUserDataM
from entities.TenantM import ClassTenantM

class ClassTenantDAO(ModelDAO.ClassModeleDAO):
    def __init__(self):
        """
        Initialise un objet UserDataDAO en établissant une connexion à la base de données.
        """
        try:
            print('- [UserDataDAO] Initialisation de la connexion ... ')
            self.conn = ModelDAO.ClassModeleDAO.object_connection
            print('- Obj connexion ok ... ')
            self.conn.reconnect()
            self.cur = self.conn.cursor()
            print('-> Connexion ouverte ...\n -> En attente de requêtes ... ')
        except Exception as e:
            print('HERE ERROR ', e)
            raise e

    def insertOne(self, entity_instance: ClassTenantM) -> str:
        """
        Insère un objet dans la table Tenant.
        --------------------------
        @params entity_instance: objet ClassTenantM à insérer.
        @return: le nombre de lignes affectées.
        """
        print("- Requête insertion début ... ")
        try:
            query = "INSERT INTO tenants VALUES (%s, %s, %s)"
            i = str(uuid.uuid4())
            values = (
                i,
                entity_instance.id_user,
                entity_instance.moyen_paiement,
            )

            self.cur.execute(query, values)
            self.conn.commit()  # fin de la transaction
            self.cur.close()
            self.conn.close()
            print('- Requête insertion fin ... ')
            return self.cur.rowcount if self.cur.rowcount!=0 else 0
        except Exception as e:
            self.cur.rollback()
            self.cur.close()
            self.conn.close()
            return f"Erreur_UserDataDAO.insertOne() ::: {e}"
            # annuler ttes les modifications non validées depuis le dernier commit()
                  

    # SELECT
    def findOne(self, key) -> list:
        pass

    def findAll(self) -> list:
        pass

    def findAllByOne(self, key) -> list:
        pass

    def findAllByLike(self, key) -> list:
        pass

    # UPDATE
    def modifyOne(self, key, entity_instance):
        pass

    # DELETE
    def deleteOne(self, key):
        pass

    # GRANT ACCESS TO NIGHTON API
    def createAPIUser(self, APIuser, pwd):
        pass

    def createAPIRole(self, role):
        pass

    def grantAPIRole(self, APIuser, pwd):
        pass

    

