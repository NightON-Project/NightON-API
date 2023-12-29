from abc import ABC, abstractmethod
from utils.dao.ConnexionDAO import ClassConnexionDB

class ClassModeleDAO(ABC):
    object_connection = ClassConnexionDB().getConnexion()

    # Opérations CRUD abstraites
    # INSERT
    @abstractmethod
    def insertOne(self, entity_instance) -> str:
        pass

    # SELECT
    @abstractmethod
    def findOne(self, key) -> list:
        pass

    @abstractmethod
    def findAll(self) -> list:
        pass

    @abstractmethod
    def findAllByOne(self, key) -> list:
        pass

    @abstractmethod
    def findAllByLike(self, key) -> list:
        pass

    # UPDATE
    @abstractmethod
    def modifyOne(self, key, entity_instance):
        pass

    # DELETE
    @abstractmethod
    def deleteOne(self, key):
        pass

    # GRANT ACCESS TO NIGHTON API
    @abstractmethod
    def createAPIUser(self, APIuser, pwd):
        pass

    @abstractmethod
    def createAPIRole(self, role):
        pass

    @abstractmethod
    def grantAPIRole(self, APIuser, pwd):
        pass

    def operationTable(self, query: str, values: tuple, error: str = 'Error_operationTable()'):
        """
        Fonction générique pour executer des requetes sur des tables.
        """
        try:
            self.cursor.execute(query, values,)  
            self.cursor.connection.commit()

            res = self.cursor.rowcount if self.cursor.rowcount != 0 else 0
            if res != 0 and 'RETURNING' in query:
                    res = self.cursor.fetchone()[0]
                    
            return res
        except Exception as e:
            print(f"{error} ::: {e}")
            self.cursor.connection.rollback()
            return 0
