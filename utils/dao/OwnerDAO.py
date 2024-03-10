import os
import sys
import uuid
from utils.dao import ModelDAO

CURRENT_FILEPATH = os.path.dirname(os.path.abspath(__file__))
ENTITIES_FOLDER_PATH = os.path.join(CURRENT_FILEPATH, "..")
sys.path.insert(0, ENTITIES_FOLDER_PATH)

from entities.UserDataM import ClassUserDataM
from entities.OwnerM import ClassOwnerM


class ClassOwnerDAO(ModelDAO.ClassModeleDAO):
    def __init__(self):
        """
        Initialise un objet UserDataDAO en établissant une connexion à la base de données.
        """
        try:
            print("- [UserDataDAO] Initialisation de la connexion ... ")
            self.conn = ModelDAO.ClassModeleDAO.object_connection
            print("- Obj connexion ok ... ")
            self.conn.reconnect()
            self.cur = self.conn.cursor()
            print("-> Connexion ouverte ...\n -> En attente de requêtes ... ")
        except Exception as e:
            print("HERE ERROR ", e)
            raise e

    def insertOne(self, entity_instance: ClassOwnerM) -> str:
        """
        Insère un objet dans la table Owners.
        --------------------------
        @params entity_instance: objet ClassOwnerM à insérer.
        @return: le nombre de lignes affectées.
        """
        print("- Requête insertion début ... ")
        try:
            query = "INSERT INTO owners VALUES (%s, %s, %s, %s, %s)"
            if not entity_instance.id_owner:
                entity_instance.id_owner = str(uuid.uuid4())
            values = (
                entity_instance.id_owner,
                entity_instance.id_user,
                entity_instance.status_demande,
                entity_instance.date_demande,
                entity_instance.email_user,
            )

            self.cur.execute(query, values)
            self.conn.commit()  # fin de la transaction
            self.cur.close()
            self.conn.close()
            print("- Requête insertion fin ... ")
            return self.cur.rowcount if self.cur.rowcount != 0 else 0
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

    def findAllByOne(self, key) -> ClassOwnerM:
        """Trouver une demande par le owner_id."""
        try:
            query = """SELECT * FROM owners WHERE owner_id = %s"""
            values = (key,)
            self.cur.execute(query, values)
            res = self.cur.fetchone()

            if not res:
                return None
            else:
                o = ClassOwnerM(
                    id_owner=res[0],
                    id_user=res[1],
                    status_demande=res[2],
                    date_demande=res[3],
                    email_user=res[4],
                )
                return o
        except Exception as e:
            print(f"Erreur_OwnerDAO.findAllByOne() :: {e}")
            return {"error": str(e)}

    def findAllByLike(self, key) -> list:
        pass

    # UPDATE
    def modifyOne(self, key, entity_instance):
        pass

    def modifyStatus(self, key: str, new_status: str):
        """Requete spéciale pour modifier le status d'une demande de publication.
        :param key est id_owner
        :param new_status est str dans la liste ['cancel', 'waiting' 'approved']
        """
        try:
            query = """UPDATE owners SET status_demande=%s WHERE id_owner=%s"""
            values = (
                new_status,
                key,
            )

            self.cur.execute(query, values)
            self.cur.commit()
            return self.cur.rowcount if self.cur.rowcount != 0 else 0
        except Exception as e:
            print(f"Erreur_OwnerDAO.modifyStatus() ::: {e}")
            return f"Erreur_OwnerDAO.modifyStatus() ::: {e}"
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
