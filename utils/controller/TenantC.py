from utils.dao.UserDataDAO import *
from utils.dao.TenantDAO import *
from utils.dao.RentalAgreementDAO import *
from utils.dao.PropertyDAO import *

from utils.entities.UserDataM import *
from utils.entities.TenantM import *
from utils.entities.RentalAgreementM import *
from utils.entities.PropertyM import *

class ClassTenantC:

    @staticmethod
    def addOneTenant(objIns: ClassTenantRegisteringM):
        """
        Ajoute les données d'un nouveau tenant.
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

            objTenant = ClassTenantM(# id tenant est géré coté DAO
                            id_user=objUser.id_user,
                            status_demande=objIns.status_demande,
                            date_demande=objIns.date_demande,
                            email_user=objIns.email_user,
                            id_property=objIns.id_logement,
                            starting_date_demand=objIns.starting_date_demand,
                            ending_date_demand=objIns.ending_date_demand)

            res_tenant_dmd = ClassTenantDAO().insertOne(entity_instance=objTenant)
            if res_tenant_dmd == 0:
                return f'ERROR WHILE REGISTERING DEMAND'
            else:
                return 'DEMANDE ENREGISTREE'
        except Exception as e:
            print(f'erreur_ClassUserDataC.addOne() ::: {e}')
            return f'{e}'
    
    @staticmethod   
    def findOneTenant(id):
        """Assert qu'un tenant_id existe bien dans la base."""
        try:
            res = ClassTenantDAO().findAllByOne(key=id)
            if not res:
                return 'AUCUNE DEMANDE DE RESERVATION AVEC CET ID.'
            return res
        except Exception as e:
            print(f'Erreur ClassTenantC.findOneTenant() :: {e}')
            return {'error': str(e)}

    @staticmethod
    def findAllWaitingTenants():
        pass

    @staticmethod
    def validateTenant(id_tenant, id_property):
        """Valider une demande de reservation.
            Fait dans cet ordre : 
            - verifier existance de la demande
            - mettre le status sur approved
            - chercher le logement
            - creer un contrat et enregistrer
            - update le status du logement
        :param: tenant_id est id du demandeur
        :param: id_property est id du bien demandé.
        :returns: Message erreur/succes. Si succes, envoie contrat aussi.
        """
        try:
            # verif que tenant_id existe dans la table
            res = ClassTenantDAO().findAllByOne(key=id_tenant)
            if not res:
                return 'AUCUNE DEMANDE DE RESERVATION AVEC CET ID.'
            
            # update le status de tenant
            updated_demand = res
            updated_demand.status_demande = 'approved'
            res_bis = ClassTenantDAO().modifyOne(key=res.email_user, entity_instance=updated_demand)
            if not res_bis:
                return 'ERROR WHILE UPDATING DEMAND STATUS.'
            
            # insert un nouveau act_rent
            ### chercher le logement à partir de son id
            res_property = ClassPropertyDAO().findOne(key=id_property)
            if not res_property:
                return 'ERROR WHILE SEEKING PROPERTY.'

            contrat = ClassRentalAgreementM(
                id_tenant = updated_demand.id_tenant,
                id_owner = res_property.id_owner,
                id_property = updated_demand.id_property,
                starting_date_act_rent = updated_demand.starting_date_demand,
                ending_date_act_rent = updated_demand.ending_date_demand 
            )

            res_act_rent = ClassRentalAgreementDAO().insertOne(entity_instance=contrat)
            if not res_act_rent:
                return 'ERROR WHILE CREATING CONTRACT'
            
            ### enfin mettre le status du logement sur pas dispo
            res_status_property = ClassPropertyDAO().modifyStatus(key=res_property.id_property, new_status='pas dispo')
            if res_status_property == 0:
                return 'ERROR WHILE UPDATING PROPERTY STATUS'

            return 'DEMANDE VALIDEE', contrat # ou contrat formatté pour envoyer au tenant et au owner. 
                                              # ou utiliser le mailer direcetment ici.
        except Exception as e:
            print(f'Erreur ClassTenantC.validateTenant() :: {e}')
            return {'error': str(e)}

    @staticmethod
    def deleteTenant():
        """Supprimer une demande de reservation. (juste changer le status à refuser => garder un historique.)
        :param: tenant_id
        """
        try:
            # verif que tenant_id existe dans la table
            res = ClassTenantDAO().findAllByOne(key=id)
            if not res:
                return 'AUCUNE DEMANDE DE RESERVATION AVEC CET ID.'
            
            # update le status de tenant
            updated_demand = res
            updated_demand.status_demande = 'canceled'
            res_bis = ClassTenantDAO().modifyOne(key=res.email_user, entity_instance=updated_demand)
            if not res_bis:
                return 'ERROR WHILE UPDATING STATUS'
            
            return 'DEMANDE ANNULEE'
        except Exception as e:
            print(f'Erreur ClassTenantC.deleteTenant() :: {e}')
            return {'error': str(e)}