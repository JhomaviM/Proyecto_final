from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from core.config import settings

# Configurar hashing de contraseñas
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# Función para generar un hashed_password
def get_hashed_password(password: str):
    return pwd_context.hash(password)

# Función para verificar una contraseña hashada
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

# Función para crear un token JWT
def create_access_token(data: dict):
    to_encode = data.copy() # se crea una copia del diccionario guardando en to_encode
    expire = datetime.now(tz=timezone.utc) + timedelta(minutes=settings.jwt_access_token_expire_minutes) # se incrementa un tiempo a la hora actual para medir el tiempo de validez y se guarda en la variable expire
    to_encode.update({"exp": expire}) # al diccionario se agrega mediante actualizacion la clave y valor
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret, algorithm=settings.jwt_algorithm) # jwt crea un token seguro en esta linea recibiendo el diccionario, una clave segura y larga o palabra secreta que esta en config y el jwt_algorithm y se guarda en encoded_jwt
    return encoded_jwt

# Función para verificar si un token JWT es valido
def verify_token(token: str):
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm]) # en payload se guarda la decodificacion, recibiendo el token generado, la clave o palabra secreta y el algoritmo
        user_id = payload.get("sub")
        return int(user_id) if user_id is not None else None
    except jwt.ExpiredSignatureError: # Token ha expirado
        return None
    except JWTError as e:
        return None