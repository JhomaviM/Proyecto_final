
from fastapi import APIRouter, UploadFile, File, Depends
import pandas as pd
from sqlalchemy.orm import Session
from io import BytesIO
from app.crud.cargar_archivos import insertar_datos_en_bd
from core.database import get_db

router = APIRouter()

@router.post("/upload-excel-pe04/")
async def upload_excel(
    file: UploadFile = File(...), # recibe el archivo usando la clase UploadFile y lo guarda en file, donde File(...) indica que se recibe el archivo con el nombre tal cual
    db: Session = Depends(get_db)
):
    contents = await file.read() # convierte el excel en codigo binario y se guarda en contents
    df = pd.read_excel( # df es datframes, es la abreviatura
        BytesIO(contents), # lee el contenido binario
        engine="openpyxl", # motor para leer el excel
        skiprows=4, # las filas que se descartan del principio, indicando desde donde se inicia a leer
        usecols=["IDENTIFICADOR_FICHA", "CODIGO_REGIONAL", "NOMBRE_REGIONAL", "CODIGO_CENTRO", "NOMBRE_CENTRO", "CODIGO_PROGRAMA", "VERSION_PROGRAMA", "NOMBRE_PROGRAMA_FORMACION", "ESTADO_CURSO", "NIVEL_FORMACION", "NOMBRE_JORNADA", "FECHA_INICIO_FICHA", "FECHA_TERMINACION_FICHA", "ETAPA_FICHA", "MODALIDAD_FORMACION", "NOMBRE_RESPONSABLE", "NOMBRE_EMPRESA", "NOMBRE_MUNICIPIO_CURSO", "NOMBRE_PROGRAMA_ESPECIAL"],  # Nombres reales de las columnas del archivo excel a utilizar en la base de datos
        dtype=str # se convierte a tipo string todo lo contenido en el excel
    )
    print(df.head())  # imprimiendo la cabecera del dataframe, que muestra los nombre de las columnas
    print(df.columns) # imprimo columnas
    print(df.dtypes) # imprimo tipo de datos

    # Renombrar columnas del archivo excel a los nombres de los campos en las tablas de la base de datos
    df = df.rename(columns={
        "IDENTIFICADOR_FICHA": "ficha",
        "CODIGO_REGIONAL": "cod_regional",
        "NOMBRE_REGIONAL": "nombre_regional",
        "CODIGO_CENTRO": "cod_centro",
        "NOMBRE_CENTRO": "nombre_centro",
        "CODIGO_PROGRAMA": "cod_programa",
        "VERSION_PROGRAMA": "version",
        "NOMBRE_PROGRAMA_FORMACION": "nombre",
        "ESTADO_CURSO": "estado",
        "NIVEL_FORMACION": "nivel",
        "NOMBRE_JORNADA": "jornada",
        "FECHA_INICIO_FICHA": "fecha_inicio",
        "FECHA_TERMINACION_FICHA": "fecha_fin",
        "ETAPA_FICHA": "etapa",
        "MODALIDAD_FORMACION": "modalidad",
        "NOMBRE_RESPONSABLE": "responsable",
        "NOMBRE_EMPRESA": "nombre_empresa",
        "NOMBRE_MUNICIPIO_CURSO": "nombre_municipio",
        "NOMBRE_PROGRAMA_ESPECIAL": "nombre_programa_especial"
        
    })

    print(df.head())  # paréntesis
    print(df.columns)
    
    # si quieren que funcione en todos los centros de pais 
    # crear codigo para llenar regionales centros y eliminar la siguiente linea.
    # df = df[df["cod_centro"] == '9121'] # Esto sirve par agregar una nueva columna con un valor en todas las filas

    # Eliminar filas con valores faltantes en campos obligatorios
    required_fields = [
        "ficha", "cod_centro", "cod_programa", "version", "nombre", 
        "fecha_inicio", "fecha_fin", "etapa", "responsable", "nombre_municipio"
    ]
    df = df.dropna(subset=required_fields) # en df elimina todas las filas donde no esten los campos diligenciados obligatorios según la lista required_fields y se guarda nuevamente en df

    # Convertir columnas a tipo numérico
    for col in ["ficha", "cod_programa", "cod_centro", "cod_regional"]: # se indica que columnas deben cambiar su tipo de dato
        df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64") # convierte a numerico el tipo de dato que viene de ser string

    print(df.head())  # paréntesis
    print(df.dtypes)

    # Convertir fechas
    df["fecha_inicio"] = pd.to_datetime(df["fecha_inicio"], errors="coerce").dt.date
    df["fecha_fin"] = pd.to_datetime(df["fecha_fin"], errors="coerce").dt.date

    # Asegurar columnas no proporcionadas
    df["hora_inicio"] = "00:00:00"
    df["hora_fin"] = "00:00:00"
    df["aula_actual"] = ""

    # Crear DataFrame de programas únicos
    df_programas = df[["cod_programa", "version", "nombre", "nivel"]].drop_duplicates() # de las columnas indicadas del dataframe principal se sacan y se crea un nuevo dataframe df_programas, se eliminan datos repetidos o duplicados.
    df_programas["tiempo_duracion"] = 0 # se asigna un valor o un campo vacio a una fila
    df_programas["estado"] = 1
    df_programas["url_pdf"] = ""

    print(df_programas.head())
    
    df_centros = df[["cod_centro", "nombre_centro", "cod_regional", "nombre_regional"]].drop_duplicates()
    
    print(df_centros.head())

    resultados = insertar_datos_en_bd(db, df_programas, df_centros)
    return resultados