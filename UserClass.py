import uvicorn
import mysql.connector
from fastapi import FastAPI
from pydantic import BaseModel


# Create user | read | update | delete

class UserClass(BaseModel):
    """
    Valider données utilisateur. 
    """
    uid: str
    email: str
    displayName: str
    # Ajoutez d'autres champs au besoin



app = FastAPI()

# Configuration de la connexion à la base de données SQL Server : mettre les configs dans un YAML/json et créer un docker pour tester la bdd en localhost
db_config = {
    "host": "localhost",
    "port": "2309",
    "user": "root",
    "password": "root",
    "database": "test_nighton"
}

@app.post("/enregistrer-utilisateur/")
async def createUser(user: UserClass):
    try:
        # Établissez la connexion à la base de données MySQL
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Insérez les données d'authentification dans la base de données
        insert_query = "INSERT INTO userdata (user_id, user_email, display_user_name) VALUES (%s, %s, %s)"
        insert_values = (user.uid, user.email, user.displayName)
        cursor.execute(insert_query, insert_values)

        # Validez les changements et fermez la connexion
        conn.commit()
        cursor.close()
        conn.close()

        return {"message": "Données d'authentification enregistrées avec succès"}

    except Exception as e:
        return {"error": str(e)}
        #   "error": "1054 (42S22): Unknown column 'uid' in 'field list'" -> la colonne n'existe pas dans la table cible aka mauvais nom

    

@app.get("/afficher-utilisateur/")
async def readUser():
    """
    """
    pass


@app.post("/modifier-utilisateur")
async def updateUser():
    """
    """
    pass


@app.post("/supprimer-utilisateur")
async def deleteUser():
    """
    """
    pass


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)