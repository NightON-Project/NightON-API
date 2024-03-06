import uvicorn
import sys
from fastapi import FastAPI, Depends, HTTPException, Response, Cookie, Security, status, Request, Header
from fastapi.security import HTTPBasic, HTTPBasicCredentials, OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from utils.entities import UserDataM, TenantM, PropertyM, OwnerM
from utils.controller import UserDataC, TenantC, PropertyC, OwnerC

from typing import Annotated

from utils.auth.auth_bearer import token_required
from utils.auth.auth_handler import generateJWT

app = FastAPI()

# Configuration CORS pour gérer les accès au web service
# middleware : fonction qui s'exécute à chaque appel d'un endpoint
origins = ["*"]  # Ajoutez ici vos origines autorisées
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/', response_model=dict)
async def start(req: Request):
    """
    Point de départ de nightON API.
    """
    return {'Message pour vous' : "Bonjour cher développeur, bienvenue dans la politique de confidentialité de nightON",
            'Politique de confidentialité' : "A voir",
            'Dernière màj' : "14/02/2024",
            #'header': req.headers.get('authorization'), # enlever
            'API Key': generateJWT(role_id='nightOnWebSiteApp')}


@app.post("/register", tags=['step One'])
async def registerUser(user_data: UserDataM.ClassUserDataM):
    """
    Créer nouvel utilisateur.
    """
    res = UserDataC.ClassUserDataC.addOneUser(obj_user=user_data)
    return {'API rep': res}   


@app.get("/login/request/{email_user}", tags=['step One'])
async def loginRequest(email_user: str):
    """
    Demande de login utilisateur.
    Envoie un code dans l'email.  
    """
    res = UserDataC.ClassUserDataC.loginRequest(email_user)
    return {'API rep': 'Vérifiez le mail envoyé.'}


@app.get("/login/auth/{email_user}/{code}", tags=['step One'])
async def loginAuthentification(email_user: str, code:str, response: Response):
    """
    Authentification utilisateur.
    ----------------------------
    @param email : email utilisateur.
    @param code : code 5 chiffres reçu par mail.
    @return : session id.
    """
    res = UserDataC.ClassUserDataC.loginAuth(email_user, code)
    if not res:
        raise HTTPException(status_code=403, detail='Please enter correct email or code')
    # !! a modif apres pour sécu :: hash reversible, jwt token
    response.set_cookie(key='connected_cookie', value=f'yes_{email_user}', expires=3*60)
    return {"API rep" : f"Bienvenue {email_user} !"}


@app.get("/login/auth/from_firebase/{email_user}", tags=['step One'])
async def firebaseLoginAuthentification(email_user: str, response: Response):
    """
    FAIRE UNE ROUTE POUR LES CAS FIREBASE 
    SI EMAIL VERIFIé ROUTE PAREILLE SS CODE 
    Authentification utilisateur en passant par firebase.
    ----------------------------
    @param email : email utilisateur.
    @return : session id.
    """
    res = UserDataC.ClassUserDataC.loginAuth(email_user, from_firebase=True)
    print('HERE', res)
    if not res:
        # si non creer compte juste à partir de l'adresse mail + noms fictifs (modif après)
        user_data = UserDataM.ClassUserDataM(firstname_user='FUser0000', lastname_user='LUser0000', email_user=email_user)
        UserDataC.ClassUserDataC.addOneUser(obj_user=user_data)
    # !! a modif apres pour sécu :: hash reversible, jwt token
    response.set_cookie(key='connected_cookie', value=f'yes_{email_user}', expires=3*60)
    return {"API rep" : f"Bienvenue {email_user} !"}

### PROFIL
@app.get("/auth_users/display_me")
def funcGetMe(connected_cookie: Annotated[str, Cookie()]=None):
    """
    Se base sur le cookie connecté pour afficher les userData de l'utilisateur.
    """
    if connected_cookie is None:
        raise HTTPException(status_code=403, detail='Please connect before.')
    
    # email stocké dans le cookie
    email_user = connected_cookie.split('_')[-1]
    me = UserDataC.ClassUserDataC.findOneByEmail(email_user)
    return me


@app.get("/auth_users/welcome", tags=['protected endpoints'])
# mettre une dépendance a loginAuth
async def funcWelcomeUser(current_user: Annotated[UserDataC.ClassUserDataM, Security(funcGetMe)]):
    """
    Affiche un message de bienvenue à l'utilisateur.
    Dépend de l'authentification de l'utilisateur.
    """
    return {'API rep': f'Bienvenue à toi {current_user.firstname_user} !'}


@app.post("/auth_users/update/me", tags=['UsersData'])
async def updateUserProfil(new_user: UserDataM.ClassUserDataM, current_user: Annotated[UserDataC.ClassUserDataM, Security(funcGetMe)]):
    """
    Mettre à jour un profil utilisateur.
    """
    res = UserDataC.ClassUserDataC.updateUserData(obj_user=new_user)
    return {'API rep': res}


@app.delete("/auth_users/delete/{email_user}", tags=['UsersData'])
async def deleteUser(email_user: str):
    """
    Supprimer utilisateur.
    """
    return 'Not ready'

######### DEMANDES CLIENT ############
@app.post("/users/demande_reservation", tags=['Tenants'])
# on peut récupérer son email de son cookie de connexion
# il faudrait pouvoir récupérer l'id_property 
async def registerTenant(
    new_tenant: TenantM.ClassTenantRegisteringM,
    connected_cookie: Annotated[str, Cookie()]=None,
    current_property_cookie: Annotated[str, Cookie()]=None
    ):
    """
    Créer une nouvelle demande pour être locataire.
    On a un statut 'waiting' au départ
    Ensuite une fois valide passe à : 'approved'
    """
    if current_property_cookie is None:
        raise HTTPException(status_code=500, detail='Internal Error cannot identify property.')

    if connected_cookie is None:
        raise HTTPException(status_code=403, detail='Please connect before.')

    # email stocké dans le cookie
    email_user = connected_cookie.split('_')[-1]
    id_property = current_property_cookie.split('_')[-1]
    # me = UserDataC.ClassUserDataC.findOneByEmail(email_user)
    # identifie le user dans la bdd, retourne UTILISATEUR NON ENREGISTRE si mauvais cookie
    new_tenant.email_user = email_user
    new_tenant.id_logement = id_property
    res = TenantC.ClassTenantC.addOneTenant(objIns=new_tenant)

    return {'API rep': res}   

@app.post("/users/demande_publication", tags=['Owners'])
# on devrait pouvoir récupérer son email de son cookie de connexion
async def registerOwner(
    new_owner: OwnerM.ClassOwnerRegisteringM,
    connected_cookie: Annotated[str, Cookie()]=None
    ):
    """
    Créer une nouvelle demande pour publier son logement.
    On a un statut 'waiting' au départ
    Ensuite une fois valide passe à : 'approved'
    """
    if connected_cookie is None:
        raise HTTPException(status_code=403, detail='Please connect before.')
    email_user = connected_cookie.split('_')[-1]
    # identifie le user dans la bdd, retourne UTILISATEUR NON ENREGISTRE si mauvais cookie
    new_owner.email_user = email_user
    res = OwnerC.ClassOwnerC.addOneOnwer(objIns=new_owner)
    return {'API rep': res}   


####### BIENS A LOUER ##############
@app.get('/acceuil', tags=['Properties'])
async def displayAll():
    """Affichage par defaut, overview des logements."""
    res = PropertyC.ClassPropertyC.displayAll()
    return {'API rep': res}

@app.get('/acceuil/{nom_property}')
async def displayPropertyDetails(nom_property: str, response: Response):
    """Afficher les details d'un logement par son nom.
    Btw placer un cookie qui correspond au logement current.
    """
    res, id_property = PropertyC.ClassPropertyC.displayPropertyByName(nom_affichage=nom_property)
    response.set_cookie(key='current_property_cookie', value=f'prop_{id_property}', expires=10*60)
    return {'API rep': res}


######## ADMIN: VALIDATION DES DEMANDES ##########
from enum import Enum

class status(Enum):
  c = 'cancel'
  w = 'waiting'
  a = 'approved'

  @classmethod
  def all(cls):
    return [status.a.value, status.b.value, status.c.value, status.d.value]

# send mail to proprio
# validate owner
# validate tenant -> create contrat
@app.get('/approvals/reservation/{property_id}/{tenant_id}/{new_status}')
def changeStatusTenantDemand(
    tenant_id: str=None,
    property_id: str=None, 
    new_status: str=None
    ):
    if tenant_id and new_status:
        new_status = new_status.lower()
        if new_status not in status.all():
            raise HTTPException(status_code=401, detail=f'Wrong status. Choose between {status.all()}')

        if new_status == status.c:
            res = TenantC.ClassTenantC.deleteTenant(tenant_id)
            
        if new_status == status.a:
            res = TenantC.ClassTenantC.validateTenant(tenant_id, property_id)
    else:
        res = 'Please provide tenant_id and/or new_status.'
    return {'API rep': res}


@app.get('/approvals/publication/{owner_id}/{property_id}/{new_status}')
def changeStatusOwnerDemand(
    owner_id,
    property_id,
    new_status
    ):
    if owner_id and new_status:
        new_status = new_status.lower()
        if new_status not in status.all():
            raise HTTPException(status_code=401, detail=f'Wrong status. Choose between {status.all()}')

        if new_status == status.c:
            res = OwnerC.ClassOwnerC.deleteOwner(owner_id, property_id)
            pass
            
        if new_status == status.a:
            res = OwnerC.ClassOwnerC.validateOwner(owner_id, property_id)
    else:     
        res = 'Please provide owner_id and/or new_status.'
    return {'API rep': res}


@app.post('/approvals/reservation/send_notification')
def sendNotifToOwner():
    """Envoyer un mail de notification aux proprio qd il ya une demande de resa."""
    content = ""
    pass

@app.post('/approvals/reservation/send_notification')
def sendNotifToTenant():
    """Envoyer un mail de confirmation avec un certain contenu."""
    content = ""
    pass



if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)#, reload=True)