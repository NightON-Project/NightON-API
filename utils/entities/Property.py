from pydantic import BaseModel

class ClassProperty(BaseModel):
    id_property: str
    id_owner: str
    type_property: str
    is_available: bool
    is_insured: bool
    price_renting: float
    price_caution: float
    description_global: str