from typing import List, Optional
from sqlalchemy.orm import Session
from src.application.ports.output.i_rol_repository import IRolRepository
from src.core.entities.rol import Rol
from src.infrastructure.database.models.rol_db_model import RolDbModel
from src.core.errors.roles_exceptions import RolNotFoundError, RolAlreadyDeactivatedError

class SqliteRolRepository(IRolRepository):

    def __init__(self, session: Session):
        self._session = session

    def create(self, rol: Rol) -> Rol:
        rol_db = RolDbModel.from_entity(rol)
        self._session.add(rol_db)
        self._session.flush()
        self._session.refresh(rol_db)
        return rol_db.to_entity()

    def find_by_id(self, id: int) -> Optional[Rol]:
        rol_db = self._session.query(RolDbModel).filter_by(id=id).first()
        return rol_db.to_entity() if rol_db else None

    def find_by_name(self, name: str) -> Optional[Rol]:
        rol_db = self._session.query(RolDbModel).filter_by(name=name).first()
        return rol_db.to_entity() if rol_db else None

    def get_all(self) -> List[Rol]:
        roles_db = self._session.query(RolDbModel).all()
        return [rol_db.to_entity() for rol_db in roles_db]

    def update(self, rol: Rol) -> Rol:
        rol_db = self._session.query(RolDbModel).filter_by(id=rol.id).first()
        if not rol_db:
            raise RolNotFoundError(f"Error interno: No se encontró el rol con ID {rol.id} para actualizar.")
        
        rol_db.name = rol.main_name
        rol_db.description = rol.description
        rol_db.is_active = rol.is_active
        
        self._session.flush()
        self._session.refresh(rol_db)
        return rol_db.to_entity()

    def deactivate(self, id: int) -> bool:
        rol_db = self._session.query(RolDbModel).filter_by(id=id).first()
        if not rol_db:
            raise RolNotFoundError(f"No se encontró un rol con el ID {id}")
        if not rol_db.is_active:
            raise RolAlreadyDeactivatedError(f"El rol con ID {id} ya está desactivado.")
        
        rol_db.is_active = False
        self._session.flush()
        return True