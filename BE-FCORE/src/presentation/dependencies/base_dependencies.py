from fastapi import  Depends
from sqlalchemy.orm import Session
#Aplicacion
from src.application.ports.output.i_oficial_repository import IOficialRepository
from src.application.ports.output.i_rol_repository import IRolRepository
from src.application.ports.output.i_audit_logger import IAuditLogger

#Infraestructura
from src.infrastructure.database.repositories.sqlite_oficial_repository import SqliteOficialRepository
from src.infrastructure.database.repositories.sqlite_rol_repository import SqliteRolRepository
from src.infrastructure.logs.console_logger import ConsoleLogger
from src.infrastructure.security.bcrypt_password_hasher import BcryptPasswordHasher

bcrypt_hasher = BcryptPasswordHasher()

def get_db_session() -> Session:
    """
    Esta función es un 'dependency' de FastAPI.
    Crea una nueva sesión de DB para cada petición y la cierra al final.
    """
    from src.main import SessionLocal
    
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

def get_oficial_repository(db: Session = Depends(get_db_session)) -> IOficialRepository:
    return SqliteOficialRepository(session=db)

def get_rol_repository(db: Session = Depends(get_db_session)) -> IRolRepository:
    return SqliteRolRepository(session=db)

def get_audit_logger() -> IAuditLogger:
    return ConsoleLogger()


