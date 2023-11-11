from pydantic import BaseModel
from typing import Optional

class ClassUserData(BaseModel):
    """
    Classe qui valide les données utilisateur. 
    """
    id_user: str
    name_user: str
    birthdate_user: str
    email_user: str
    telephone_user: str
    pays: str
    code_postal: str
    ville: str
    numero_rue: str
    nom_rue: str
    complement_adresse_1: Optional[str] = None
    complement_adresse_2: Optional[str] = None
    # Ajoutez d'autres champs au besoin