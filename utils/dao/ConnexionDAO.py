import mysql.connector
import json


class ClassConnexionDB:
    def __init__(self):
        self.object_my_sql_conx = None
        self.params = None
        self.__PATH_TO_DB_CONFIG: str = "./ressources/config/db_config.json"

    def getConnexion(self, MODE="test"):
        """
        Configuration de la connexion à la base de données  SQL.
        Les configs sont dans un json.
        --------------------------------------
        @params MODE : str : 'local' ou 'test' ou 'prod'
        @return Objconn : mysql.connector.connector() object instance
        """
        print("- class connexionDB() is running ...")
        print("- config/Config.json is loading ...")

        with open(self.__PATH_TO_DB_CONFIG, "r") as secret:
            db_infos = json.load(secret)

        db_config = db_infos[MODE]

        try:
            self.object_my_sql_conx = mysql.connector.connect(**db_config)
            print(f"-> Connected sucessfully to {MODE} database !")
        except Exception as e:
            print(f"Erreur dans ConnexionDB.getConnexion() en MODE[{MODE}] ::: {e}")
            raise e
        return self.object_my_sql_conx
