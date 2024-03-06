from pydantic import BaseModel

from typing import Optional


class ClassRentalAgreementM(BaseModel):
    id_contrat: Optional[str]
    id_tenant: str
    id_owner: str
    id_property: str
    starting_date_act_rent: str
    ending_date_act_rent: str


class ClassRentalAgreementOverviewM(BaseModel):
    # pour afficher les ttes les infos contrats
    pass
