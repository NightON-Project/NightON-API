from utils.dao.PropertyDAO import *
from utils.entities.PropertyM import *

class ClassPropertyC:

    @staticmethod
    def addOne(obj: ClassPropertyM):
        try:
            res = ClassPropertyDAO().insertOne(obj)
            # check if name is available before anthg because name will be used as key to display one 
            if res == 0:
                return f'ERROR'
            else:
                return 'DONNEES ENREGISTREES'
        except Exception as e:
            print(f'erreur_ClassPropertyC.addOne() :: {e}')
            return f'{e}'
    
    @staticmethod
    def displayAll():
        try:
            res = ClassPropertyDAO().findAll()
            # limiter les résultats/afficher dans un ordre ?
            return res
        except Exception as e:
            print(f'erreur_ClassPropertyC.displayAll() :: {e}')
            return f'{e}'
        
    @staticmethod
    def displayPropertyByName(nom_affichage: str):
        """Pour afficher les détails d'un seul logement.
        :returns : dict formatté + id_property(utilisé en cookie)
        """
        try:
            p: ClassPropertyM = ClassPropertyDAO().findAllByOne(key=nom_affichage)
            if not p: # when p is None
                return 'AUCUN LOGEMENT A CE NOM'
            
            # formattage de l'affichage
            localisation = f"{p.code_postal}, {p.ville}, {p.pays}"
            images = [p.url1, p.url2, p.url3, p.url4, p.url5, p.url6, p.url7, p.url8, p.url9, p.url10]
            images = list(filter(lambda x: x != "", set(images)))
            details_1 = {
                "nb_pieces": p.nbre_pieces,
                "nb_chambres": p.nbre_rooms,
                "nb_lits": "",
                "nb_salle_de_bain": p.nbre_bathrooms,
                "nb_jaccuzi": ""
            }
            details_2 = {
                "superficie_totale": p.sup_totale_m2,
                "superficie_jardin": p.sup_garden,
                "cameras": p.has_cameras,
                "wifi_dispo": p.wifi_available,
                "detecteur_fumee": p.has_detecteur_fumee,
                "climatiseurs": p.has_climatiseur,
                "parking": p.has_place_parking,
                "objets_cassables": p.has_objets_cassables
            }
            infos_owner = {
                "prenom": "___",
                "email" : "___"
            }
            
            p_format = {
                "nom": p.nom_affichage,
                "localisation": localisation,
                "images": images,
                "details_1": details_1,
                "details_2": details_2,
                "dates_disponibilites": {
                    "debut": p.date_dispo_debut, 
                    "fin": p.date_dispo_fin
                    },
                "prix": f"{p.prix} €",
                "description": p.descr_complementaire,
                "infos_proprietaire": infos_owner,
                "commentaires": ["", ""],
                "note_moyenne": "___"
            }

            return p_format, p.id_property
        except Exception as e:
            print(f"Erreur PropertyC.displayPropertyByName() :: {e}")
            return 'ERROR'


    @staticmethod
    def deleteProperty():
        pass