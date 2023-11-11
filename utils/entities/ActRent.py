from Tenant import ClassTenant
from Owner import ClassOwner
from Property import ClassProperty
from pydantic import BaseModel

class ActRent(BaseModel):
    id_act_rent: str
    tenant_act_rent: ClassTenant
    owner_act_rent: ClassOwner
    property_act_rent: ClassProperty
    start_date_act_rent: str
    end_date_act_rent: str