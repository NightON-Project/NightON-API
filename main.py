import uvicorn
import sys
from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from utils.entities import UserDataM
from utils.controller import UserDataC

from utils.entities import TenantM
from utils.controller import TenantC

app = FastAPI()

Privacy_Policy = '''
Confidentialité et sécurité : Nous accordons la priorité à la protection de vos informations et avons mis en place des mesures de sécurité appropriées pour prévenir l'accès, la divulgation ou la modification non autorisés. Seul le personnel autorisé a accès à ces informations, et il est lié par des obligations de confidentialité.

Restrictions d'accès et d'exploration : L'accès non autorisé à notre application, y compris toute tentative d'exploration de son fonctionnement en accédant à la racine de l'API, est strictement interdit. Toute violation de cette politique de confidentialité ou de nos conditions d'utilisation peut entraîner des mesures disciplinaires, y compris la résiliation du compte et, si nécessaire, des poursuites judiciaires.

Conservation des informations : Nous conservons vos informations aussi longtemps que nécessaire pour atteindre les objectifs énoncés dans cette politique de confidentialité, sauf si une période de conservation plus longue est requise ou autorisée par la loi.

Changements à la politique de confidentialité : Nous nous réservons le droit de modifier cette politique de confidentialité à tout moment. Tous les changements seront effectifs dès leur publication sur notre site Web ou dans l'application. Il est de votre responsabilité de consulter régulièrement cette politique de confidentialité pour toute mise à jour.

Consentement : En utilisant notre application, vous consentez à la collecte, à l'utilisation et à la divulgation de vos informations conformément à cette politique de confidentialité.

Dernière mise à jour : 06/12/2023
'''

@app.get('/', response_model=dict)
async def start():
    """
    Point de départ de nightON API.
    """
    return {'Message pour vous ':"Bonjour cher développeur/utilisateur, BIENVENUE dans la politique de confidentialité de nightON",
            'Politique de confidentialité' : Privacy_Policy}


@app.post("/users/register", tags=['step One'])
async def registerUser(user_data: UserDataM.ClassUserDataM):
    """
    Créer nouvel utilisateur.
    """
    response = UserDataC.ClassUserDataC.addOneUser(obj_user=user_data)
    return {'response': response}   


@app.get("/users/login/request/{email_user}", tags=['step One'])
async def loginRequest(email_user: str):
    """
    Demande de login utilisateur.
    Envoie un code dans l'email.  
    """
    response = UserDataC.ClassUserDataC.loginRequest(email_user)
    return {'response': response}


@app.get("/users/login/authentify/{email_user}/{code}", tags=['step One'])
async def loginAuthentification(email_user: str, code:str):
    """
    Authentification utilisateur.
    ----------------------------
    @param email : email utilisateur.
    @param code : code 5 chiffres reçu par mail.
    @return : session id.
    """
    response = UserDataC.ClassUserDataC.loginAuth(email_user, code)
    # renvoyer un session_id avec un timeout
    return {'response': response}


@app.get("/users/display/{email_user}", tags=['protected endpoints'])
# mettre une dépendance a loginAuth
async def displayUserInfos(email_user: str):
    """
    Afficher données utilisateur.
    """
    response = UserDataC.ClassUserDataC.findOneByEmail(email_user)
    return {'response': response}


@app.post("/users/update", tags=['UsersData'])
async def updateUserProfil(user: UserDataM.ClassUserDataM):
    """
    Mettre à jour un profil utilisateur.
    """
    response = UserDataC.ClassUserDataC.updateUserData(obj_user=user)
    return {'response': response}


@app.delete("/users/delete/{email_user}", tags=['UsersData'])
async def deleteUser(email_user: str):
    """
    Supprimer utilisateur.
    """
    pass

######### TENANTS ############

@app.post("/users/{email}/tenants/register", tags=['Tenants'])
async def registerTenant(new_tenant: TenantM.ClassTenantRegistering):
    """
    Créer nouveau locataire.
    """
    response = TenantC.ClassTenantC.addOneTenant(objIns=new_tenant)
    return {'response': response}   




if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)