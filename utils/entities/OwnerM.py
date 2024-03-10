from utils.entities.UserDataM import ClassUserDataM
from utils.entities.PropertyM import ClassPropertyM
from pydantic import BaseModel
from typing import Optional


class ClassOwnerM(BaseModel):
    """
    Classe qui valide les données de proprio.
    """

    id_owner: Optional[str]
    id_user: str
    status_demande: Optional[str] = "waiting"
    date_demande: Optional[str] = "01-01-1900"
    email_user: Optional[str]
    # Ajoutez d'autres champs au besoin


class ClassOwnerRegisteringM(BaseModel):
    """
    Données à envoyer pour une demande de publication proprio.
    """

    email_user: Optional[str] = ""
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

    logements: list[ClassPropertyM]  # peut ajouter plusieurs propriétés

    date_demande: Optional[str] = "01-01-1900"  # a revoir
    # Ajoutez d'autres champs au besoin
