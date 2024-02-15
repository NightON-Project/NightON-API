from pydantic import BaseModel
from typing import Optional


class ClassUserDataM(BaseModel):
    """
    Classe qui valide les données utilisateur.
    """
    id_user: Optional[str] = ""
    firstname_user: str
    lastname_user: str
    birthdate_user: Optional[str] = ""
    email_user: str
    telephone_user: Optional[str] = ""
    pays: Optional[str] = ""
    code_postal: Optional[str] = ""
    ville: Optional[str] = ""
    numero_rue: Optional[str] = ""
    nom_rue: Optional[str] = ""
    complement_adresse_1: Optional[str] = ""
    complement_adresse_2: Optional[str] = ""
    # Ajoutez d'autres champs au besoin

    # add moyen de paiement
    
    # 14/02/2024 : les tables Tenant et Owner 
    # enregistrent les demandes de résa et de pub
