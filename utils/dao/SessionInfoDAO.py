import os
import sys
import uuid
import time
from utils.dao import ModelDAO

CURRENT_FILEPATH = os.path.dirname(os.path.abspath(__file__))
ENTITIES_FOLDER_PATH = os.path.join(CURRENT_FILEPATH, '..')
sys.path.insert(0, ENTITIES_FOLDER_PATH)

from entities.UserDataM import ClassUserDataM
from entities.SessionInfoM import ClassSessionInfoM

class ClassSessionInfoDAO(ModelDAO.ClassModeleDAO):
    def __init__(self):
        """
        Initialise un objet DAO en établissant une connexion à la base de données.
        """
        try:
            print('- [SessionInfoDAO] Initialisation de la connexion ... ')
            self.conn = ModelDAO.ClassModeleDAO.object_connection
            print('- Obj connexion ok ... ')
            self.conn.reconnect()
            self.cur = self.conn.cursor()
            print('-> Connexion ouverte ...\n -> En attente de requêtes ... ')
        except Exception as e:
            print('HERE ERROR ', e)
            raise e

    def insertOne(self, entity_instance: ClassSessionInfoM) -> str:
        """
        Est createSession. 
        Insère une ligne dans la table SessionInfo.
        --------------------------
        @params entity_instance: ClassSessionInfoM. 
        @return: la SessionId.
        """
        print("- Requête insertion début ... ")
        try:
            query = "INSERT INTO sessions_infos VALUES (%s, %s, %s, %s, %s, %s)"
            session_id = str(uuid.uuid4())
            values = (
                entity_instance.id_session,
                entity_instance.email_user,
                entity_instance.mail_code,
                entity_instance.is_active,
                entity_instance.access_token,
                entity_instance.refresh_token,
            )

            self.cur.execute(query, values)
            self.conn.commit()  # fin de la transaction
            self.cur.close()
            self.conn.close()
            print('- Requête insertion fin ... ')
            return session_id if self.cur.rowcount!=0 else None
        except Exception as e:
            self.cur.rollback()
            self.cur.close()
            self.conn.close()
            return f"Erreur_SessionInfoDAO.insertOne() ::: {e}"
            # annuler ttes les modifications non validées depuis le dernier commit()
                  

    # SELECT
    def findOne(self, key):
        try:
            query = "SELECT * FROM sessions_infos WHERE session_id = key"
            self.cur.execute(query)
            res = self.cur.fetchone()
            
            if (len(res) > 0) or res is not None:
                
                session = ClassSessionInfoM(res[0], res[1], res[2], res[3])
                return session
            else:
                return None

        except Exception as e:
            print(f"Erreur_SessionInfoDAO.findOne() ::: {e}")
        

    def findAll(self) -> list[ClassSessionInfoM]:
        try:
            query = "SELECT * FROM sessions_infos"
            self.cur.execute(query)
            res = self.cur.fetchall()
            
            sessions: list[ClassSessionInfoM] = []

            if len(res) > 0:
                for r in res:
                    session = ClassSessionInfoM(r[0], r[1], r[2], r[3])
                    sessions.append(session)
                return sessions
            else:
                return []

        except Exception as e:
            print(f"Erreur_SessionInfoDAO.findAll() ::: {e}")

    def findAllByOne(self, key) -> list:
        pass

    def findAllByLike(self, key) -> list:
        pass

    # UPDATE
    def modifyOne(self, key, entity_instance):
        pass

    # DELETE
    def deleteOne(self, key):
        query = '''DELETE FROM Towns WHERE id = %s;'''
        values =  (id,)
        error = "Erreur_TownsDAO.delete()"
        return super().operationTable(query, values,error)

    # GRANT ACCESS TO NIGHTON API
    def createAPIUser(self, APIuser, pwd):
        pass

    def createAPIRole(self, role):
        pass

    def grantAPIRole(self, APIuser, pwd):
        pass

