from UserDataM import ClassUserDataM
from pydantic import BaseModel


class ClassOwnerM(BaseModel):
    """
    Classe qui valide les données de proprio.
    """

    id_tenant: str
    owner_data: ClassUserDataM
    moyen_paiement: int
    # Ajoutez d'autres champs au besoin
