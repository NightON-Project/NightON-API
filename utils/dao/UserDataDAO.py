import os
import sys
import uuid
from utils.dao import ModelDAO

CURRENT_FILEPATH = os.path.dirname(os.path.abspath(__file__))
ENTITIES_FOLDER_PATH = os.path.join(CURRENT_FILEPATH, '..')
sys.path.insert(0, ENTITIES_FOLDER_PATH)

from entities.UserDataM import ClassUserDataM

class ClassUserDataDAO(ModelDAO.ClassModeleDAO):
    def __init__(self):
        """
        Initialise un objet UserDataDAO en établissant une connexion à la base de données.
        """
        try:
            print('- [UserDataDAO] Initialisation de la connexion ... ')
            self.conn = ModelDAO.ClassModeleDAO.object_connection
            print('- Obj connexion ok ... ')
            #print(type(self.conn))
            #print(self.conn.__dict__)
            self.conn.reconnect()
            self.cur = self.conn.cursor()
            #print(type(self.cur))
            #print(self.cur.__dict__)
            print('-> Connexion ouverte ...\n -> En attente de requêtes ... ')
        except Exception as e:
            print('HERE ERROR ', e)
            raise e

    def insertOne(self, entity_instance: ClassUserDataM) -> str:
        """
        Insère un objet dans la table UserData.
        --------------------------
        @params entity_instance: objet ClassUserDataM à insérer.
        @return: le nombre de lignes affectées.
        """
        print("- Requête insertion début ... ")
        try:
            query = "INSERT INTO userdata VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            i = str(uuid.uuid4())
            values = (
                i,
                entity_instance.firstname_user,
                entity_instance.lastname_user,
                entity_instance.birthdate_user,
                entity_instance.email_user,
                entity_instance.telephone_user,
                entity_instance.pays,
                entity_instance.code_postal,
                entity_instance.ville,
                entity_instance.numero_rue,
                entity_instance.nom_rue,
                entity_instance.complement_adresse_1,
                entity_instance.complement_adresse_2,
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
            

    def findAllByOne(self, key: str) -> list:
        """
        Trouver un user par key.
        ---------------------
        @param key: clé de recherche : email user.
        @return: Objet trouvé.
        """
        try:
            query = "SELECT * FROM userdata WHERE email_user = %s"
            values = (key,)

            self.cur.execute(query, values)
            res = self.cur.fetchone()
            #print(f"HERE {res}")

            if not res:
                return None
            else:
                u = ClassUserDataM(
                    firstname_user = res[1],
                    lastname_user = res[2],
                    email_user = res[4]
                )
                #assert isinstance(u, ClassUserDataM), f"ERRERU ICI"
                #print('HERE2 ', u)
                u.id_user = res[0]
                #u.firstname_user = res[1]
                #u.lastname_user = res[2]
                u.birthdate_user = res[3]
                #u.email_user = res[4]
                u.telephone_user = res[5]
                u.pays = res[6]
                u.code_postal = res[7]
                u.ville = res[8]
                u.numero_rue = res[9]
                u.nom_rue = res[10]
                u.complement_adresse_1 = res[11]
                u.complement_adresse_2 = res[12]
                
                #print('HERE 3', u)
            return u
        except Exception as e:
            print(f"Erreur_UserDataDAO.findAllByOne() ::: {e}")
            #raise e
            return {"error": str(e)}
        finally:
            self.cur.close()

    def findAll(self) -> list:
        pass

    def findOne(self, key) -> list:
        pass

    def findAllByLike(self, key) -> list:
        pass

    def modifyOne(self, key: str, entity_instance):
        """
        update user par key (email).
        ----------------------
        @params: key : clé du prédicat : est email_user
        @params: entity_instance : est objet ClassUserDataM 
        @return: dict {"error"|"message": ...}
        """
        try:
            query = "UPDATE userdata SET firstname_user=%s, lastname_user=%s, birthdate_user=%s, email_user=%s, telephone_user=%s, pays=%s, code_postal=%s, ville=%s, numero_rue=%s, nom_rue=%s, complement_adresse_1=%s, complement_adresse_2=%s WHERE email_user=%s"
            values = (
                entity_instance.firstname_user,
                entity_instance.lastname_user,
                entity_instance.birthdate_user,
                entity_instance.email_user,
                entity_instance.telephone_user,
                entity_instance.pays,
                entity_instance.code_postal,
                entity_instance.ville,
                entity_instance.numero_rue,
                entity_instance.nom_rue,
                entity_instance.complement_adresse_1,
                entity_instance.complement_adresse_2,
                key
            )

            self.cur.execute(query, values)
            self.cur.commit()
            return self.cur.rowcount if self.cur.rowcount!=0 else 0
        except Exception as e:
            print(f"Erreur_UserDataDAO.modifyOne() ::: {e}")
            return f"Erreur_UserDataDAO.modifyOne() ::: {e}"
        finally:
            self.cur.close()

    def deleteOne(self, key):
        """
        Supprimer un utilisateur de la db:
        -------------------------
        @param key: email utilisateur
        @return: str message
        """
        try:
            query = "DELETE FROM userdata WHERE email_user=%s"
            values = (key,)
            self.cur.execute(query, values)
            self.cur.connection.commit()
            return {"message": f"Utilisateur {key} supprimé !"}
        except Exception as e:
            return {"message": f"error ::: {e}"}
        finally:
            self.cur.close()

    # GRANT ACCESS TO NIGHTON API
    def createAPIUser(self, APIuser, pwd):
        pass

    def createAPIRole(self, role):
        pass

    def grantAPIRole(self, APIuser, pwd):
        pass

    # specials
    def loginTableInsert(self, email:str, code:str):
        try:
            query = "INSERT INTO login_table VALUES (%s, %s)"
            values = (email, code,)

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
            return f"Erreur_UserDataDAO.loginTableInsert() ::: {e}"

    def loginTableUpdateCode(self, code:str, email:str):
        try:
            query = "UPDATE login_table SET code=%s WHERE email_user=%s"
            values = (code, email,)

            self.cur.execute(query, values)
            self.conn.commit()  # fin de la transaction
            self.cur.close()
            self.conn.close()
            print('- Requête màj fin ... ')
            return self.cur.rowcount if self.cur.rowcount!=0 else 0
        except Exception as e:
            self.cur.rollback()
            self.cur.close()
            self.conn.close()
            return f"Erreur_UserDataDAO.loginTableUpdate() ::: {e}"

    def loginTableRead(self, email):
        try:
            query = "SELECT * FROM login_table WHERE email_user = %s"
            values = (email,)

            self.cur.execute(query, values)
            res = self.cur.fetchone()
            #print(res)
            return res
        except Exception as e:
            print(f"Erreur_UserDataDAO.loginTableRead() ::: {e}")
            return {"error": str(e)}
        finally:
            self.cur.close()        
        