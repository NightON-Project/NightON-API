import uvicorn
import sys
from fastapi import FastAPI, Depends, HTTPException, Response, Cookie, Security
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.middleware.cors import CORSMiddleware
from utils.entities import UserDataM, TenantM, PropertyM
from utils.controller import UserDataC, TenantC, PropertyC

from typing import Annotated

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
async def start():
    """
    Point de départ de nightON API.
    """
    return {'Message pour vous' : "Bonjour cher développeur, bienvenue dans la politique de confidentialité de nightON",
            'Politique de confidentialité' : "On verra",
            'Dernière màj' : "17/01/2024"}


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

######### TENANTS ############

@app.post("/users/tenants/register", tags=['Tenants'])
async def registerTenant(new_tenant: TenantM.ClassTenantRegistering):
    """
    Créer nouveau locataire.
    """
    res = TenantC.ClassTenantC.addOneTenant(objIns=new_tenant)
    return {'API rep': res}   


####### BIENS A LOUER ##############
@app.get('/no_acceuil', tags=['Properties'])
async def displayAll():
    """
    Affichage par defaut, overview des logements.
    """
    res = PropertyC.ClassPropertyC.displayAll()
    return {'API rep': res}

@app.post('/add_property')
async def addProperty(prop:PropertyM.ClassPropertyM):
    #res = PropertyC.ClassPropertyC.addOne(prop)
    #return {'API rep': res}
    pass

if __name__ == "__main__":
    import multiprocessing
    multiprocessing.freeze_support()
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=False, workers=2)