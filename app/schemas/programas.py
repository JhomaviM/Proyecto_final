from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class ProgramaBase(BaseModel):
    cod_programa: int
    version: str = Field(min_length=0, max_length=4)
    nombre: str = Field(min_length=0, max_length=200)
    nivel: str = Field(min_length=0, max_length=70)
    id_red: Optional[int] = None
    tiempo_duracion: int
    unidad_medida: Optional[str] = None
    estado: bool
    url_pdf: str = Field(min_length=0, max_length=180)

