from fastapi import HTTPException, status
from sqlalchemy.orm import Session # para trabajar con sesiones
from sqlalchemy import text # limpia el sql de posibles ataques de inyecion sql
from sqlalchemy.exc import SQLAlchemyError # se utiliza para el manejo de errores
from typing import Optional
import logging

logger = logging.getLogger(__name__)

def update_url_pdf(db: Session, cod: int, url: str) -> bool:
    try:
        query = text(f""" UPDATE programas_formacion SET url_pdf = :url_pdf 
                        WHERE cod_programa = :codigo """)
        
        db.execute(query, {"url_pdf":url, "codigo": cod})
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al guardar la url en el programa: {e}")
        raise Exception("Error de base de datos al actualizar la url en el programa")

def get_programa_by_cod(db: Session, cod: int):
    try:
        query = text(f""" SELECT * FROM programas_formacion 
                     WHERE cod_programa = :codigo """)
        
        result = db.execute(query, {"codigo": cod}).mappings().first()
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al consultar programa: {e}")
        raise Exception("Error de base de datos al consultar programa")
