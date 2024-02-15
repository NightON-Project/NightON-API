import os
import sys
import uuid
from utils.dao import ModelDAO

CURRENT_FILEPATH = os.path.dirname(os.path.abspath(__file__))
ENTITIES_FOLDER_PATH = os.path.join(CURRENT_FILEPATH, '..')
sys.path.insert(0, ENTITIES_FOLDER_PATH)

from utils.entities.RentalAgreementM import ClassRentalAgreementM

class ClassRentalAgreementDAO(ModelDAO.ClassModeleDAO):
    def __init__(self):
        """
        Initialise un objet RentalAgreementDAO en établissant une connexion à la base de données.
        """
        try:
            print('- [PropertyDAO] Initialisation de la connexion ... ')
            self.conn = ModelDAO.ClassModeleDAO.object_connection
            print('- Obj connexion ok ... ')
            self.conn.reconnect()
            self.cur = self.conn.cursor()
            print('-> Connexion ouverte ...\n -> En attente de requêtes ... ')
        except Exception as e:
            print('HERE ERROR ', e)
            raise e


    def insertOne(self, entity_instance: ClassRentalAgreementM) -> str:
        """
        Insère un objet dans la table RentalAgreement.
        --------------------------
        @params entity_instance: objet ClassRentalAgreementM à insérer.
        @return: le nombre de lignes affectées.
        """
        print("- Requête insertion début ... ")
        try:
            query = "INSERT INTO rental_agreements VALUES (%s, %s, %s, %s, %s, %s)"
            i = str(uuid.uuid4())
            values = (
                i,
                entity_instance.id_tenant,
                entity_instance.id_owner,
                entity_instance.id_property,
                entity_instance.starting_date_act_rent,
                entity_instance.ending_date_act_rent,
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

    def findAllByOne(self, key) -> ClassRentalAgreementM:
        """"""
        try:
            pass
        except Exception as e:
            print(f"Erreur_ActRentDAO.findAllByOne() :: {e}")
            return {"error": str(e)}            

    def findAllByLike(self, key) -> list:
        pass

    # UPDATE
    def modifyOne(self, key, entity_instance):
        """"""
        try:
            pass
        except Exception as e:
            print(f"Erreur_ActRentDAO.modifyOne() ::: {e}")
            return f"Erreur_ActRentDAO.modifyOne() ::: {e}"
        finally:
            self.cur.close()


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

