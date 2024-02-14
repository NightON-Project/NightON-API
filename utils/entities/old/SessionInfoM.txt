from pydantic import BaseModel
from typing import Optional

class ClassSessionInfoM(BaseModel):
    """Reproduit le schema de la table sessions_infos dans la bdd.

    Args:
        BaseModel (_type_): _description_
    """
    id_session : str
    email_user : str
    mail_code : Optional[str] = ""
    is_active : Optional[bool] = False
    access_token : str
    refresh_token : Optional[str] = ""