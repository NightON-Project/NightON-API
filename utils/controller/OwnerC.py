from utils.dao.UserDataDAO import *
from utils.dao.OwnerDAO import *
from utils.dao.PropertyDAO import *

from utils.entities.UserDataM import *
from utils.entities.OwnerM import *
from utils.entities.PropertyM import *


class ClassOwnerC:

    @staticmethod
    def addOneOnwer(objIns: ClassOwnerRegisteringM):
        """
        Ajoute les données d'un nouveau owner.
        1. identifie le user dans la bdd, retourne UTILISATEUR NON ENREGISTRE si mauvais email
        2. si user reconnu, crée une demande de reservation avec status = 'waiting'
        """
        try:
            objUser: ClassUserDataM = ClassUserDataDAO().findAllByOne(key=objIns.email_user)
            
            if objUser is None:
                return 'UTILISATEUR NON ENREGISTRE'
            
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
            res_update_user = ClassUserDataDAO().modifyOne(key=objIns.email_user, entity_instance=objUserUpdated)
            if res_update_user == 0:
                return f'ERROR WHILE UPDATING USERDATA'            
            
            objOwner = ClassOwnerM(# id owner est géré coté DAO
                            id_user=objUser.id_user,
                            status_demande=objIns.status_demande,
                            date_demande=objIns.date_demande,
                            email_user=objIns.email_user)

            res_owner = ClassTenantDAO().insertOne(entity_instance=objOwner)

            # ensuite recup et sauvegarder les infos logement
            p_liste: list[ClassPropertyM] = objIns.logements

            for p in p_liste:
                # les logements sont déjà des instances de ClassPropertyM
                # donc on peut les insérer directement avec le DAO Property après avoir mis le availabiliy_status sur 'waiting'
                p.availabilty_status = 'en attente'
                res_p = ClassPropertyDAO().insertOne(entity_instance=p)
                # valider au fur et à mesure
                if res_p == 0:
                    print(f'Erreur_OwnerC.addOneOwner() :: {res_p}')
                    return f'ERROR WITH PROPERTIE(S)'

            if res_owner == 0:
                return f'ERROR WHILE REGISTERING OWNER'
            else:
                return 'DEMANDE ENREGISTREE'
        except Exception as e:
            print(f'erreur_ClassOwnerC.addOneOwner() ::: {e}')
            return f'{e}'
    
