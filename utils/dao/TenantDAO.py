import os
import sys
import uuid
from utils.dao import ModelDAO

CURRENT_FILEPATH = os.path.dirname(os.path.abspath(__file__))
ENTITIES_FOLDER_PATH = os.path.join(CURRENT_FILEPATH, "..")
sys.path.insert(0, ENTITIES_FOLDER_PATH)

from entities.UserDataM import ClassUserDataM
from entities.TenantM import ClassTenantM


class ClassTenantDAO(ModelDAO.ClassModeleDAO):
    def __init__(self):
        """
        Initialise un objet UserDataDAO en établissant une connexion à la base de données.
        """
        try:
            print("- [TenantDAO] Initialisation de la connexion ... ")
            self.conn = ModelDAO.ClassModeleDAO.object_connection
            print("- Obj connexion ok ... ")
            self.conn.reconnect()
            self.cur = self.conn.cursor()
            print("-> Connexion ouverte ...\n -> En attente de requêtes ... ")
        except Exception as e:
            print("HERE ERROR ", e)
            raise e

    def insertOne(self, entity_instance: ClassTenantM) -> str:
        """
        Insère un objet dans la table Tenants.
        --------------------------
        @params entity_instance: objet ClassTenantM à insérer.
        @return: le nombre de lignes affectées.
        """
        print("- Requête insertion début ... ")
        try:
            query = "INSERT INTO tenants VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            i = str(uuid.uuid4())
            values = (
                i,
                entity_instance.id_user,
                entity_instance.status_demande,
                entity_instance.date_demande,
                entity_instance.email_user,
                entity_instance.id_property,
                entity_instance.starting_date_demand,
                entity_instance.ending_date_demand,
            )

            self.cur.execute(query, values)
            self.conn.commit()  # fin de la transaction
            print("- Requête insertion fin ... ")
            return self.cur.rowcount if self.cur.rowcount != 0 else 0
        except Exception as e:
            #self.cur.rollback()
            return f"Erreur_TenantDAO.insertOne() ::: {e}"
            # annuler ttes les modifications non validées depuis le dernier commit()
        finally:
            self.cur.close()
            self.conn.close()

    # SELECT
    def findOne(self, key) -> list:
        pass

    def findAll(self) -> list:
        pass

    def findAllByOne(self, key) -> ClassTenantM:
        """Trouver une demande par le tenant_id."""
        try:
            query = """SELECT * FROM tenants WHERE tenant_id = %s"""
            values = (key,)

            self.cur.execute(query, values)
            res = self.cur.fetchone()

            if not res:
                return None
            else:
                t = ClassTenantM(
                    id_tenant=res[0],
                    id_user=res[1],
                    status_demande=res[2],
                    date_demande=res[3],
                    email_user=res[4],
                    id_property=res[5],
                    starting_date_demand=res[6],
                    ending_date_demand=res[7],
                )
                return t
        except Exception as e:
            print(f"Erreur_TenantDAO.findAllByOne() :: {e}")
            return {"error": str(e)}

    def findAllByLike(self, key) -> list:
        pass

    # UPDATE
    def modifyOne(self, key, entity_instance):
        """Mettre à jour le status d'une demande par l'email_user."""
        try:
            query = """UPDATE tenants SET id_tenant=%s, id_user=%s, status_demande=%s, date_demande=%s, email_user=%s, id_property=%s, starting_date_demand=%s, ending_date_demand=%s WHERE email_user=%s"""
            values = (
                entity_instance.id_tenant,
                entity_instance.id_user,
                entity_instance.status_demande,
                entity_instance.date_demande,
                entity_instance.email_user,
                entity_instance.id_property,
                entity_instance.starting_date_demand,
                entity_instance.ending_date_demand,
                key,
            )
            self.cur.execute(query, values)
            self.cur.commit()
            return self.cur.rowcount if self.cur.rowcount != 0 else 0
        except Exception as e:
            print(f"Erreur_TenantDAO.modifyOne() ::: {e}")
            return f"Erreur_TenantDAO.modifyOne() ::: {e}"
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
