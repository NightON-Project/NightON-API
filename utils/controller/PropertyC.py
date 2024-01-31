from utils.dao.PropertyDAO import *
from utils.entities.PropertyM import *

class ClassPropertyC:

    @staticmethod
    def addOne(obj: ClassPropertyM):
        try:
            res = ClassPropertyDAO().insertOne(obj)
            if res == 0:
                return f'ERROR'
            else:
                return 'DONNEES ENREGISTREES'
        except Exception as e:
            print(f'erreur_ClassPropertyC.addOne() :: {e}')
            return f'{e}'
    
    @staticmethod
    def displayAll():
        try:
            res = ClassPropertyDAO().findAll()
            # limiter les résultats/afficher dans un ordre ?
            return res
        except Exception as e:
            print(f'erreur_ClassPropertyC.displayAll() :: {e}')
            return f'{e}'
        
        