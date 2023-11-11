from UserData import ClassUserData
from pydantic import BaseModel

class ClassOwner(BaseModel):
    """
    Classe qui valide les données de proprio. 
    """
    id_tenant: str
    owner_data: ClassUserData
    moyen_paiement: int
    # Ajoutez d'autres champs au besoin