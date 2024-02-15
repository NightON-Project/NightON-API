
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
            

    def findAllByOne(self, key: str) -> ClassPropertyM:
        """
        Trouver un bien par key.
        ---------------------
        :param key: nom du bien.
        :returns: objet property.
        """
        try:
            query = f"""SELECT * FROM properties_table WHERE availability_status = 'dispo' AND nom_affichage = %s"""
            values = (key,)

            self.cur.execute(query, values)
            res = self.cur.fetchone()

            if not res:
                return None
            else:
                p = ClassPropertyM(
                        # general : 8
                        id_property = res[0],
                        nom_affichage = res[1],
                        prix = res[2],
                        availabilty_status = res[3],
                        date_dispo_debut = res[4],
                        date_dispo_fin = res[5],
                        category = res[6],
                        ss_category = res[7],
                        # details global 17
                        nbre_pieces = res[8],
                        nbre_rooms = res[9],
                        sup_totale_m2 = res[10],
                        has_bathroom = res[11],
                        nbre_bathrooms = res[12],
                        has_toilets = res[13],
                        nbre_toilets = res[14],
                        has_garden = res[15],
                        sup_garden = res[16],
                        has_pool = res[17],
                        has_cameras = res[18],
                        wifi_available = res[19],
                        has_detecteur_fumee = res[20],
                        has_climatiseur = res[21],
                        has_place_parking = res[22],
                        has_objets_cassables = res[23],
                        descr_complementaire = res[24],
                        # images 10
                        url1 = res[25],
                        url2 = res[26],
                        url3 = res[27],
                        url4 = res[28],
                        url5 = res[29],
                        url6 = res[30],
                        url = res[31],
                        url8 = res[32],
                        url9 = res[33],
                        url10 = res[34],
                        # localisation 7
                        pays = res[35],
                        code_postal = res[36],
                        ville = res[37],
                        numero_rue = res[38],
                        nom_rue = res[39],
                        complement_adresse_1 = res[40],
                        complement_adresse_2 = res[41],
                        # legal
                        nighton_caution = res[42],
                        nighton_caution_id = res[43],
                        id_owner = res[44],
                        confirmation_mairie = res[45],
                        n0_declaration_meuble_mairie = res[46],
                        assert_is_RP = res[47],
                        assert_is_RS = res[48],
                )

                return p
        except Exception as e:
            print(f"Erreur_PropertyDAO.findAllByOne() :: {e}")
            return {"error": str(e)}


    def findAll(self) -> list[ClassPropertyOverviewM]:
        """
        Afficher tout. Affiner sur le statut = dispo
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
        """
        Trouver un bien par key.
        ---------------------
        :param key: id_property du bien.
        :returns: objet property.
        """
        try:
            query = f"""SELECT * FROM properties_table WHERE id_property = %s"""
            values = (key,)

            self.cur.execute(query, values)
            res = self.cur.fetchone()

            if not res:
                return None
            else:
                p = ClassPropertyM(
                        # general : 8
                        id_property = res[0],
                        nom_affichage = res[1],
                        prix = res[2],
                        availabilty_status = res[3],
                        date_dispo_debut = res[4],
                        date_dispo_fin = res[5],
                        category = res[6],
                        ss_category = res[7],
                        # details global 17
                        nbre_pieces = res[8],
                        nbre_rooms = res[9],
                        sup_totale_m2 = res[10],
                        has_bathroom = res[11],
                        nbre_bathrooms = res[12],
                        has_toilets = res[13],
                        nbre_toilets = res[14],
                        has_garden = res[15],
                        sup_garden = res[16],
                        has_pool = res[17],
                        has_cameras = res[18],
                        wifi_available = res[19],
                        has_detecteur_fumee = res[20],
                        has_climatiseur = res[21],
                        has_place_parking = res[22],
                        has_objets_cassables = res[23],
                        descr_complementaire = res[24],
                        # images 10
                        url1 = res[25],
                        url2 = res[26],
                        url3 = res[27],
                        url4 = res[28],
                        url5 = res[29],
                        url6 = res[30],
                        url = res[31],
                        url8 = res[32],
                        url9 = res[33],
                        url10 = res[34],
                        # localisation 7
                        pays = res[35],
                        code_postal = res[36],
                        ville = res[37],
                        numero_rue = res[38],
                        nom_rue = res[39],
                        complement_adresse_1 = res[40],
                        complement_adresse_2 = res[41],
                        # legal
                        nighton_caution = res[42],
                        nighton_caution_id = res[43],
                        id_owner = res[44],
                        confirmation_mairie = res[45],
                        n0_declaration_meuble_mairie = res[46],
                        assert_is_RP = res[47],
                        assert_is_RS = res[48],
                )

                return p
        except Exception as e:
            print(f"Erreur_PropertyDAO.findOne() :: {e}")
            return {"error": str(e)}

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