from TenantM import ClassTenantM
from OwnerM import ClassOwnerM
from PropertyM import ClassPropertyM
from pydantic import BaseModel


class ClassActRentM(BaseModel):
    id_act_rent: str
    tenant_act_rent: ClassTenantM
    owner_act_rent: ClassOwnerM
    property_act_rent: ClassPropertyM
    start_date_act_rent: str
    end_date_act_rent: str
