from pydantic import BaseModel


class ClassTenantM(BaseModel):
    """
    Classe qui valide les données locataires.
    """
    #id_tenant: str
    id_user: str
    moyen_paiement: int
    # Ajoutez d'autres champs au besoin

class ClassTenantRegistering(BaseModel):
    """
    Classe qui valide les données à envoyer pour passer locataire.
    """
    email_user: str
    # plus les autres data en dehors de id_user
    # id_user est inféré grace à l'email dans la base
    moyen_paiement: int
    # ajouter autres champs au besoin
