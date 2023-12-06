def db_connection_decorator(fonction):
    def wrapper(*args, **kwargs):
        try:
            resultats = fonction(*args, **kwargs)
        except Exception as e:
            print(f'Erreur dans {fonction.__name__} ::: {e}') 
        return resultats
    return wrapper