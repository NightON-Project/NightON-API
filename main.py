import json
import uuid
import uvicorn
import mysql.connector
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from utils.entities.UserData import ClassUserData
#from utils.debugTools import scriptLogger

app = FastAPI()


def connect_to_mysql_db(MODE='test'):
    """
    Configuration de la connexion à la base de données SQL Server
    Les configs sont dans un json et créer un docker pour tester la bdd en localhost
    @params MODE : str : 'local' | 'test' | 'prod'
    @return Objconn : mysql.connector.connector() object instance
    """
    print('>> Connexion..')
    PATH_TO_DB_CONFIG: str = './ressources/secret/db_config.json'

    with open(PATH_TO_DB_CONFIG, "r") as f:
        db_infos = json.load(f)

    db_config = db_infos[MODE]

    try:
        ObjectMySQLConn = mysql.connector.connect(**db_config)
        print(f"-> Connected sucessfully to {MODE} database !\n")
    except Exception as e:
        print(f"Erreur dans connect_to_db() en MODE : {MODE} ::: {e}")

    return ObjectMySQLConn


def execute_creation_script(PATH_TO_SQL_CREA_SCRIPT='./ressources/create_nighton_db.txt'):

    with open(PATH_TO_SQL_CREA_SCRIPT, 'r') as cq:
        crea_db_query = cq.readlines()[0]
    
    try:
        print(">> DB creation...")  
        conn = connect_to_mysql_db(MODE='test')
        cursor = conn.cursor()
        cursor.execute(crea_db_query)
        print('-> DB created !\n')
    except Exception as e:
        print(f"Erreur dans execute_creation_script() ::: {e}")
        raise e


# Route pour creer un nouveau user
@app.post("/users/")
async def createUser(user: ClassUserData):

    try:
        # connexion à la base de données MySQL
        conn = connect_to_mysql_db()
        cursor = conn.cursor()

        # verifer que la table existe : si non on executer le script de création  
        execute_creation_script()

        # Insérez les données d'authentification dans la base de données
        i = str(uuid.uuid4())
        insert_query = "INSERT INTO userdata_v1 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        insert_values = (i,
                         user.name_user,
                         user.birthdate_user,
                         user.email_user,
                         user.telephone_user,
                         user.pays,
                         user.code_postal,
                         user.ville,
                         user.numero_rue,
                         user.nom_rue,
                         user.complement_adresse_1,
                         user.complement_adresse_2)
        
        cursor.execute(insert_query, insert_values)

        # Validez les changements et fermez la connexion
        conn.commit()
        cursor.close()
        conn.close()

        return {"message": "Données d'authentification enregistrées avec succès"}

    except Exception as e:
        return {"error": str(e)}
        #   exple : "error": "1054 (42S22): Unknown column 'uid' in 'field list'" -> la colonne n'existe pas dans la table cible aka mauvais nom


# route pour afficher un utilisateur 
@app.get("/users/{id_user}", response_model=ClassUserData)
async def readUser(id_user: str):

    # connexion à la base de données MySQL
    conn = connect_to_mysql_db()
    cursor = conn.cursor()


    read_query = "SELECT * FROM userdata_v1 WHERE id_user=%s"
    read_values = (id_user,) # id_user renseigné dans la def de la fonction 
    
    cursor.execute(read_query, read_values)
    user = cursor.fetchone()
    cursor.close()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    else:
        user = {'id_user': user[0], 
                'name_user': user[1],
                'birthdate_user': user[2],
                'email_user': user[3],
                'telephone_user': user[4],
                'pays': user[5],
                'code_postal': user[6],
                'ville': user[7],
                'numero_rue': user[8],
                'nom_rue': user[9],
                'complement_adresse_1': user[10],
                'complement_adresse_2': user[11]}
    return user

# route pour maj les donnees personnelles d'un user
@app.put("/users/{user_id}")
async def updateUser(user: ClassUserData):
    """
    """
    try: 
        # connexion à la base de données MySQL
        conn = connect_to_mysql_db()
        cursor = conn.cursor()

        # verifier que le user existe

        # màj ses data
        update_query = "UPDATE userdata_v1 SET name_user=%s, birthdate_user=%s, email_user=%s, telephone_user=%s, pays=%s, code_postal=%s, ville=%s, numero_rue=%s, nom_rue=%s, complement_adresse_1=%s, complement_adresse_2=%s WHERE id_user=%s"
        update_values = (user.name_user,
                        user.birthdate_user,
                        user.email_user,
                        user.telephone_user,
                        user.pays,
                        user.code_postal,
                        user.ville,
                        user.numero_rue,
                        user.nom_rue,
                        user.complement_adresse_1,
                        user.complement_adresse_2,
                        user.id_user)

        cursor.execute(update_query, update_values)
        conn.commit()
        cursor.close()

        return {'message': 'Données mises à jour avec succès !'}
    except Exception as e:
        return {"error": str(e)}

# route pour delete
@app.delete("/users/{id_user}")
async def deleteUser(id_user: str):
    """
    """
    try: 
        # connexion à la base de données MySQL
        conn = connect_to_mysql_db()
        cursor = conn.cursor()
        delete_query = "DELETE FROM userdata_v1 WHERE id_user=%s"
        delete_values = (id_user,)
        cursor.execute(delete_query, delete_values)
        conn.commit()
        cursor.close()
        return {'message : ' f'Utilisateur {id_user} supprimé !'}
    except Exception as e:
        return {f'error : str({e})'}

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)