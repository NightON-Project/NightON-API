from UserData import ClassUserData 
from pydantic import BaseModel

class ClassTenant(BaseModel):
    """
    Classe qui valide les données locataires. 
    """
    id_tenant: str
    tenant_data: ClassUserData
    moyen_paiement: int
    # Ajoutez d'autres champs au besoin