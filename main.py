from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.router import usuarios
from app.router import municipio
from app.router import auth
from app.router import cargar_archivos
from app.router import programas

app = FastAPI() # crear un objeto de la clase FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

# Incluir en el objeto app los routers
app.include_router(usuarios.router, prefix="/usuario", tags=["servicios usuarios"]) # al objeto app le incluye los routers que esten en el archivo usuarios, usando el prefijo usuario. tags permite agrupar todas los routers bajo ese nombre
app.include_router(municipio.router, prefix="/municipio", tags=["municipios"])
app.include_router(auth.router, prefix="/access", tags=["Servicios de Loggin"])
app.include_router(cargar_archivos.router, prefix="/cargar_archivo", tags=["Servicios de upload"])
app.include_router(programas.router)

# Configuración de CORS para permitir todas las solicitudes desde cualquier origen, CORS = permisos de quien puede acceder a las rutas
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir solicitudes desde cualquier origen, tambien se puede poner el dominio o IP en vez de * para mayor seguridad en usar la ruta, se puede poner varios frontend porque es una lista[]
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # Permitir estos métodos HTTP
    allow_headers=["*"],  # Permitir cualquier encabezado en las solicitudes
)

#decorador usando FastAPI()
@app.get("/") # creando ruta raiz
def read_root():
    return {
                "message": "ok",
                "autor": "ADSO 2925888"
            }