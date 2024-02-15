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
            
            objOwner = ClassOwnerM(# id owner est géré coté DAO
                            id_user=objUser.id_user,
                            status_demande=objIns.status_demande,
                            date_demande=objIns.date_demande)

            res_owner = ClassTenantDAO().insertOne(entity_instance=objOwner)

            # ensuite recup et sauvegarder les infos logement
            p_liste: list[ClassPropertyM] = objIns.logements

            for p in p_liste:
                # les logements sont déjà des instances de ClassPropertyM
                # donc on peut les insérer directement avec le DAO Property après avoir mis le availabiliy_status sur 'waiting'
                p.availabilty_status = 'waiting'
                res_p = ClassPropertyDAO().insertOne(entity_instance=p)
                # valider au fur et à mesure
                if res_p == 0:
                    print(f'Erreur_OwnerC.addOneOwner() :: {res_p}')
                    return f'ERROR WITH PROPERTIE(S)'

            if res_owner == 0:
                return f'ERROR WITH OWNER'
            else:
                return 'DEMANDE ENREGISTREE'
        except Exception as e:
            print(f'erreur_ClassOwnerC.addOneOwner() ::: {e}')
            return f'{e}'
    
    # next: methode Read tenant