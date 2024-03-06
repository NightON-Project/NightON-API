from pydantic import BaseModel
from typing import Optional


class ClassTenantM(BaseModel):
    """
    Classe qui valide les données locataires.
    """

    id_tenant: Optional[str]
    id_user: str
    status_demande: str
    date_demande: str
    email_user: str
    id_property: str
    starting_date_demand: str = "31-01-1900"
    ending_date_demand: str = "02-01-1900"
    # Ajoutez d'autres champs au besoin


class ClassTenantRegisteringM(BaseModel):
    """
    Valide les données à envoyer pour passer locataire.
    """

    email_user: Optional[str]
    # plus les autres data en dehors de id_user
    # id_user est inféré grace à l'email dans la base
    nom: str
    prenom: str
    date_naissance: str
    numero_rue: str
    nom_rue: str
    ville: str
    code_postal: str
    url_piece1: str
    url_piece2: str
    status_demande: str = "waiting"  # waiting or approved
    date_demande: Optional[str] = "01-01-1900"  # a revoir
    id_logement: Optional[str]  # est le nom du logement ou son id
    starting_date_demand: str = "31-01-1900"
    ending_date_demand: str = "02-01-1900"
    # ajouter autres champs au besoin
