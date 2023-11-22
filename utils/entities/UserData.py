from pydantic import BaseModel
from typing import Optional

class ClassUserData(BaseModel):
    """
    Classe qui valide les données utilisateur. 
    """
    id_user: str
    firstname_user: str
    lastname_user: str
    birthdate_user: Optional[str] = None
    email_user: str
    telephone_user: Optional[str] = None
    pays: Optional[str] = None
    code_postal: Optional[str] = None
    ville: Optional[str] = None
    numero_rue: Optional[str] = None
    nom_rue: Optional[str] = None
    complement_adresse_1: Optional[str] = None
    complement_adresse_2: Optional[str] = None
    # Ajoutez d'autres champs au besoin