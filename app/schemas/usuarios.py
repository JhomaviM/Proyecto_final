# Los schemas son las cosas que necesitamos para validar datos

from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class UsuarioBase(BaseModel):
    # Este es un esquema base, o sea que se utilizará en otros esquemas, por eso se usa otro esquema para la contraseña
    # BaseModel es una clase de pydantic que en este caso hereda atributos a la clase UserBase
    # Esto tiene que coincidir con la base de datos
    nombre_completo: str = Field(min_length=3, max_length=80) # Fileld quiere decir opciones
    id_rol: int
    correo: EmailStr
    num_documento: str = Field(min_length=8, max_length=12)

# Se crea un schema con la contraseña aparte para evitar que en una consulta se retorne la contraseña del usuario
class CrearUsaurio(UsuarioBase):
    contra_encript: str = Field(min_length=8)
    estado: bool = True

class RetornarUsuario(UsuarioBase):
    id_usuario: int
    estado: bool
    nombre_rol: str

class EditarUsuario(BaseModel):
    #Optional quiere decir que es opcional hacer el cambio o no, por eso solo se utiliza en actualizar
    nombre_completo: Optional[str] = Field(default=None, min_length=3, max_length=80)
    correo: Optional[EmailStr] = Field(default=None, min_length=6, max_length=100)
    num_documento: Optional[str] = Field(default=None, min_length=8, max_length=12)
    estado: Optional[bool] = None

# Para editar la contraseña
class EditarPass(BaseModel):
    id_usuario: int
    contra_anterior: str = Field(min_length=8)
    contra_nueva: str = Field(min_length=8)