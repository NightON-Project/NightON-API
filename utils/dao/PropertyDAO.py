
# infos à afficher overview : liste = [nom, categ, ss categ, dates_dispo, prix] 
# infos à afficher : tt overview + [description, ...]
# select {infos_to_show} from properties where status = 'dispo';

# select {infos_to_show} from properties where id_property = '';

# select {infos} from properties where id_proprio = '';

# insert into properties values ();

# update properties set xx= , ;

# delete from properties where id_property = '';

# delete from propertieis where id_proprio = '';

import os
import sys
import uuid
from utils.dao import ModelDAO

CURRENT_FILEPATH = os.path.dirname(os.path.abspath(__file__))
ENTITIES_FOLDER_PATH = os.path.join(CURRENT_FILEPATH, '..')
sys.path.insert(0, ENTITIES_FOLDER_PATH)

from entities.PropertyM import (ClassPropertyM, ClassPropertyOverviewM)

class ClassPropertyDAO(ModelDAO.ClassModeleDAO):
    def __init__(self):
        """
        Initialise un objet PropertyDAO en établissant une connexion à la base de données.
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

    def insertOne(self, entity_instance: ClassPropertyM) -> str:
        """
        Insère un objet dans la table Properties.
        --------------------------
        @params entity_instance: objet ClassPropertyM à insérer.
        @return: le nombre de lignes affectées.
        """
        print("- Requête insertion début ... ")
        try:
            query = "INSERT INTO properties_table VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            i = str(uuid.uuid4())
            values = (
                i,
                entity_instance.nom_affichage,
                entity_instance.prix,
                entity_instance.availabilty_status,
                entity_instance.date_dispo_debut,
                entity_instance.date_dispo_fin,
                entity_instance.category,
                entity_instance.ss_category,

                entity_instance.nbre_pieces,
                entity_instance.nbre_rooms,
                entity_instance.sup_totale_m2,
                entity_instance.has_bathroom,
                entity_instance.nbre_bathrooms,
                entity_instance.has_toilets,
                entity_instance.nbre_toilets,
                entity_instance.has_garden,
                entity_instance.sup_garden,
                entity_instance.has_pool,

                entity_instance.has_cameras,
                entity_instance.wifi_available,
                entity_instance.has_detecteur_fumee,
                entity_instance.has_climatiseur,
                entity_instance.has_place_parking,
                entity_instance.has_objets_cassables,
                entity_instance.descr_complementaire,

                entity_instance.url1,
                entity_instance.url2,
                entity_instance.url3,
                entity_instance.url4,
                entity_instance.url5,
                entity_instance.url6,
                entity_instance.url7,
                entity_instance.url8,
                entity_instance.url9,
                entity_instance.url10,

                entity_instance.pays,
                entity_instance.code_postal,
                entity_instance.ville,
                entity_instance.numero_rue,
                entity_instance.nom_rue,
                entity_instance.complement_adresse_1,
                entity_instance.complement_adresse_2,

                entity_instance.nighton_caution,
                entity_instance.nighton_caution_id,
                entity_instance.id_owner,
                entity_instance.confirmation_mairie,
                entity_instance.n0_declaration_meuble_mairie,
                entity_instance.assert_is_RP,
                entity_instance.assert_is_RS
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
            return f"Erreur_PropertyDAO.insertOne() ::: {e}"
            # annuler ttes les modifications non validées depuis le dernier commit()
            

    def findAllByOne(self, key: str) -> list:
        """
        Trouver un bien par key.
        ---------------------
        """
        pass

    def findAll(self) -> list[ClassPropertyOverviewM]:
        """
        Afficher tout. Afiner sur le statut = dispo
        ---------------------
        """
        try:
            query = """SELECT id_property,nom_affichage,prix,date_dispo_debut,date_dispo_fin,category,ss_category,id_owner,url1,url2,url3 FROM properties_table WHERE availability_status = 'dispo' """
            
            self.cur.execute(query)
            res = self.cur.fetchall()
            
            #ownerDao = ClassPropertyDAO()

            list_properties = []

            if len(res)>0:
                for r in res:
                    property = ClassPropertyOverviewM(
                        id_property=r[0],
                        nom_affichage=r[1],
                        prix=r[2],
                        date_dispo_debut=r[3],
                        date_dispo_fin=r[4],
                        category=r[5],
                        ss_category=r[6],
                        proprio_infos=r[7],
                        url1=r[8],
                        url2=r[9],
                        url3=r[10]
                        )

                    list_properties.append(property)
                return list_properties
            else:
                return []

        except Exception as e:
            print(f"Error_PersonsDAO.findAll() ::: {e}")

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
        Supprimer un bien de la db par son id:
        -------------------------
        """
        pass

    # GRANT ACCESS TO NIGHTON API
    def createAPIUser(self, APIuser, pwd):
        pass

    def createAPIRole(self, role):
        pass

    def grantAPIRole(self, APIuser, pwd):
        pass