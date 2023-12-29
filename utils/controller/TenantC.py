from utils.dao.UserDataDAO import *
from utils.dao.TenantDAO import *

from utils.entities.UserDataM import *
from utils.entities.TenantM import *

class ClassTenantC:

    @staticmethod
    def addOneTenant(objIns: ClassTenantRegistering):
        """
        Ajoute les données d'un nouveau tenant.
        """
        try:
            objUser: ClassUserDataM = ClassUserDataDAO().findAllByOne(key=objIns.email_user)
            
            if objUser is None:
                return 'UTILISATEUR NON ENREGISTRE'
            
            objTenant = ClassTenantM(
                            id_user=objUser.id_user,
                            moyen_paiement=objIns.moyen_paiement)

            res = ClassTenantDAO().insertOne(entity_instance=objTenant)
            if res == 0:
                return f'ERROR'
            else:
                return 'DONNEES ENREGISTREES'
        except Exception as e:
            print(f'erreur_ClassUserDataC.addOne() ::: {e}')
            return f'{e}'
    
    # next: methode Read tenant