from pydantic import BaseModel
from typing import Optional

class ClassPropertyOverviewM(BaseModel):
    id_property: str
    nom_affichage: str
    prix: float
    date_dispo_debut: str
    date_dispo_fin: str
    category: str
    ss_category: str
    proprio_infos: Optional[str]
    url1: str
    url2: str
    url3: str


class ClassPropertyDetailsM(BaseModel):
    """Equivaut pratiquement à ClassPropertyM sauf le legal"""
    pass    


class ClassPropertyM(BaseModel):    
    
    # general : 8
    id_property: str
    nom_affichage: str
    prix: float 
    availabilty_status: str # field validator ou enum {dispo, reservé, plus dispo}
    date_dispo_debut: str #
    date_dispo_fin: str #
    category: str # (RP, Terrain, RS)
    ss_category: str # (Maison, Appart)
    
    # details global 17
    nbre_pieces: int # 1 - 100 int
    nbre_rooms: int # 1-100 int
    sup_totale_m2: float
    has_bathroom: bool
    nbre_bathrooms: int
    has_toilets: bool
    nbre_toilets: int
    has_garden: bool
    sup_garden: float
    has_pool: bool

    has_cameras: bool
    wifi_available: bool
    has_detecteur_fumee: bool

    has_climatiseur: bool
    has_place_parking: bool
    has_objets_cassables: bool
    descr_complementaire: str #texte à remplir VARCHAR(5000)

    # images 10
    url1: str
    url2: str
    url3: str
    url4: Optional[str] = ""
    url5: Optional[str] = ""
    url6: Optional[str] = ""
    url7: Optional[str] = ""
    url8: Optional[str] = ""
    url9: Optional[str] = ""
    url10: Optional[str] = ""

    # localisation 7
    pays: Optional[str] = ""
    code_postal: Optional[str] = ""
    ville: Optional[str] = ""
    numero_rue: Optional[str] = ""
    nom_rue: Optional[str] = ""
    complement_adresse_1: Optional[str] = ""
    complement_adresse_2: Optional[str] = ""

    # legal 7 
    nighton_caution: Optional[bool] = False
    nighton_caution_id: Optional[str] = ""
    id_owner: str
    confirmation_mairie : bool
    n0_declaration_meuble_mairie : str # ou int jsp
    assert_is_RP : bool
    assert_is_RS : bool