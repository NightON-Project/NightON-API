from utils.dao.UserDataDAO import *
from utils.dao.OwnerDAO import *
from utils.dao.PropertyDAO import *

from utils.entities.UserDataM import *
from utils.entities.OwnerM import *
from utils.entities.PropertyM import *

import uuid


class ClassOwnerC:
    @staticmethod
    def addOneOnwer(objIns: ClassOwnerRegisteringM):
        """
        Ajoute les données d'un nouveau owner.
        Fais dans cet ordre :
            1. identifie le user dans la bdd, retourne UTILISATEUR NON ENREGISTRE si mauvais email
            2. MAJ les user data
            3. Crée une demande de publication avec status = 'waiting'
            4. Enregistre la property avec status_de_disponibilité = 'en attente/waiting' (va chercher l'id du owner)
        """
        try:
            objUser: ClassUserDataM = ClassUserDataDAO().findAllByOne(
                key=objIns.email_user
            )

            if objUser is None:
                return "UTILISATEUR NON ENREGISTRE"

            objUserUpdated = objUser
            # mise à jour des attributs
            objUserUpdated.firstname_user = objIns.prenom
            objUserUpdated.lastname_user = objIns.nom
            objUserUpdated.birthdate_user = objIns.date_naissance
            # objUserUpdated.email_user=objIns.email_user
            objUserUpdated.numero_rue = objIns.numero_rue
            objUserUpdated.nom_rue = objIns.nom_rue
            objUserUpdated.ville = objIns.ville
            objUserUpdated.code_postal = objIns.code_postal
            # et les complements adresse 1 et 2 ?
            # et le numero de telephone ?
            objUserUpdated.url1_piece = objIns.url_piece1
            objUserUpdated.url2_piece = objIns.url_piece2
            res_update_user = ClassUserDataDAO().modifyOne(
                key=objIns.email_user, entity_instance=objUserUpdated
            )
            if res_update_user == 0:
                return f"ERROR WHILE UPDATING USERDATA"

            objOwner = ClassOwnerM(  # id owner est géré coté DAO si non renseigné 
                id_owner=str(uuid.uuid4()),
                id_user=objUser.id_user,
                status_demande=objIns.status_demande,
                date_demande=objIns.date_demande,
                email_user=objIns.email_user,
            )

            res_owner = ClassOwnerDAO().insertOne(entity_instance=objOwner)

            # ensuite recup et sauvegarder les infos logement
            p_liste: list[ClassPropertyM] = objIns.logements

            for p in p_liste:
                # les logements sont déjà des instances de ClassPropertyM
                # donc on peut les insérer directement avec le DAO Property après avoir mis le availabiliy_status sur 'waiting'
                p.availabilty_status = "waiting"
                # update avec le id_owner généré lors de l'enregistrement de la demande.
                p.id_owner = objOwner.id_owner
                res_p = ClassPropertyDAO().insertOne(entity_instance=p)
                # valider au fur et à mesure
                if res_p == 0:
                    print(f"Erreur_OwnerC.addOneOwner() :: {res_p}")
                    return f"ERROR WITH PROPERTIE(S)"

            if res_owner == 0:
                return f"ERROR WHILE REGISTERING OWNER"
            else:
                return "DEMANDE ENREGISTREE"
        except Exception as e:
            print(f"erreur_ClassOwnerC.addOneOwner() ::: {e}")
            return f"{e}"

    @staticmethod
    def findAllWaitingOwners():
        pass

    @staticmethod
    def validateOwner(id_owner, id_property):
        """
        Valider une demande de publication.
        Fait dans cet ordre:
         - verifier existance de la demamnde
         - mettre le status sur approved
         - chercher le logement
         - update le status du logement
        :param id_owner: id du demandeur.
        :param id_property: id du logement publié.
        :returns: Message succes/erreur.
        """
        try:
            res = ClassOwnerDAO().findAllByOne(key=id_owner)
            if not res:
                return "AUCUNE DEMANDE DE PUBLICATION AVEC CET ID."

            # update status de owner
            updated_demand = res
            updated_demand.status_demande = "approved"
            res_bis = ClassOwnerDAO().modifyOne(
                key=res.email_user, entity_instance=updated_demand
            )
            if not res_bis:
                return "ERREUR WHILE UPDATING DEMAND STATUS."

            res_property = ClassPropertyDAO().findOne(key=id_property)
            if not res_property:
                return "ERROR WHILE SEEKING PROPERTY."

            # update la dispo du logement.
            res_status_property = ClassPropertyDAO().modifyStatus(
                key=res_property.id_property, new_status="dispo"
            )
            if res_status_property == 0:
                return "ERROR WHILE UPDATING PROPERTY STATUS."

            return "DEMANDE APPROUVEE."

        except Exception as e:
            print(f"Erreur ClassOwnerC.validateOwner() :: {e}")
            return {"error": str(e)}

    @staticmethod
    def deleteOwner(id_owner, id_property):
        """Supprimer une demande de publication.
        Fait dans cet ordre :
            - changer le status de la demande à canceled => garder historique
            - la dispo de la property passe sur 'supprimee/publication annulee'.
        :param owner_id:
        )"""
        try:
            res = ClassOwnerDAO().findAllByOne(key=id_owner)
            if not res:
                return "AUCUNE DEMANDE DE PUBLICATION AVEC CET ID."

            updated_demand = res
            updated_demand.status_demande = "canceled"
            res_bis = ClassOwnerDAO().modifyOne(
                key=res.email_user, entity_instance=updated_demand
            )
            if not res_bis:
                return "ERROR WHILE UPDATING STATUS."

            ### chercher le logement à partir de son id
            res_property = ClassPropertyDAO().findOne(key=id_property)
            if not res_property:
                return "ERROR WHILE SEEKING PROPERTY."
            res_status_property = ClassPropertyDAO().modifyStatus(
                key=res_property.id_property, new_status="deleted"
            )
            if not res_status_property:
                return "ERROR WHILE DELETING PROPERTY."

            return "DEMANDE ANNULEE."

        except Exception as e:
            print(f"Erreur ClassOwnerC.deleteOwner() :: {e}")
            return {"error": str(e)}
