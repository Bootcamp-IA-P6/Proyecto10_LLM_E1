from pydantic import BaseModel
from typing import Optional


class CompanyProfile(BaseModel):
    name: str
    sector: str
    tone: str = "profesional"
    description: Optional[str] = ""


# Almacenamiento en memoria (se resetea al reiniciar el servidor)
_current_profile: Optional[CompanyProfile] = None


def save_profile(profile: CompanyProfile) -> CompanyProfile:
    global _current_profile
    _current_profile = profile
    return _current_profile


def get_profile() -> Optional[CompanyProfile]:
    return _current_profile


def get_profile_as_text() -> str:
    if _current_profile is None:
        return ""
    return (
        f"Empresa: {_current_profile.name}. "
        f"Sector: {_current_profile.sector}. "
        f"Tono de comunicación: {_current_profile.tone}. "
        f"Descripción: {_current_profile.description}"
    )