# src/infrastructure/database/repositories/sqlite_oficial_repository.py (versión corregida)
from typing import List, Optional
from sqlalchemy.orm import Session, joinedload

from src.application.ports.output.i_oficial_repository import IOficialRepository
from src.core.entities.oficial import Oficial
from src.core.entities.rol import Rol
from src.infrastructure.database.models.oficial_db_model import OficialDbModel
from src.infrastructure.database.models.rol_db_model import RolDbModel

from src.core.errors.oficial_exceptions import OficialNotFoundError, OficialAlreadyDeactivatedError

class SqliteOficialRepository(IOficialRepository):
    
    def __init__(self, session: Session):
        self._session = session
        
    def create(self, oficial: Oficial) -> Oficial:
        # 1. Mapeamos de la entidad al modelo de BD
        oficial_db = OficialDbModel.from_entity(oficial)
        
        # 2. Añadimos el objeto a la sesión
        self._session.add(oficial_db)
        
        # 3. Hacemos "flush" para que la BD asigne el ID
        self._session.flush()
        self._session.refresh(oficial_db) # Actualizamos la instancia con los datos de la BD (como el ID)
        
        # 4. Mapeamos de vuelta a una entidad para devolver el objeto completo
        return oficial_db.to_entity()
        
    
    def find_by_qcode(self, qcode: str) -> Optional[Oficial]:
        oficial_db = self._session.query(OficialDbModel).filter(
            OficialDbModel.q_code == qcode
        ).first()

        if oficial_db:
            return oficial_db.to_entity()
        
        return None
    
    def get_all(self) -> List[Oficial]:
        oficiales_db = self._session.query(OficialDbModel).all()
        return [oficial_db.to_entity() for oficial_db in oficiales_db]
         
    
    def find_by_id(self, id: int) -> Optional[Oficial]:
        oficial_db = self._session.query(OficialDbModel).filter(
            OficialDbModel.id == id
        ).first()

        if oficial_db:
            return oficial_db.to_entity()
        
        return None
    
    def update(self, oficial: Oficial) -> Oficial:
        # 1. Buscamos el registro en la BD por su ID único.
        oficial_db = self._session.query(OficialDbModel).filter(
            OficialDbModel.id == oficial._id
        ).first()
        
        if not oficial_db:
            raise OficialNotFoundError(f"No se encontró un oficial con el ID {oficial.id}")

        # 2. MODIFICAMOS DIRECTAMENTE los atributos del objeto que SQLAlchemy está vigilando.
        oficial_db.name = oficial.name
        oficial_db.lastname = oficial.lastname # Mapeamos el set

        # 3. Hacemos flush para confirmar los cambios en la BD actual.
        self._session.flush()
        self._session.refresh(oficial_db)
        
        return oficial_db.to_entity()
    
    def deactivate(self, qcode: str) -> bool:
        oficial_to_deactivate = self._session.query(OficialDbModel).filter(
            OficialDbModel.q_code == qcode
        ).first()
        
        if not oficial_to_deactivate:
            raise OficialNotFoundError(f"No se encontró un oficial con el Q-Code {qcode}")

        if not oficial_to_deactivate.is_active:
            # Dejamos que esta excepción suba. ¡Es información útil!
            raise OficialAlreadyDeactivatedError(f"El oficial con Q-Code {qcode} ya está desactivado")

        oficial_to_deactivate.is_active = False
        self._session.flush()
        
        return True
    
    def assign_rol(self, oficial: Oficial, rol: Rol) -> None:
        oficial_db = self._session.query(OficialDbModel).filter_by(id=oficial.id).first()
        rol_db = self._session.query(RolDbModel).filter_by(id=rol.id).first()

        if oficial_db and rol_db and rol_db not in oficial_db.roles:
            oficial_db.roles.append(rol_db)
            self._session.flush()

    def remove_rol(self, oficial: Oficial, rol: Rol) -> None:
        oficial_db = self._session.query(OficialDbModel).filter_by(id=oficial.id).first()
        rol_db = self._session.query(RolDbModel).filter_by(id=rol.id).first()

        if oficial_db and rol_db and rol_db in oficial_db.roles:
            oficial_db.roles.remove(rol_db)
            self._session.flush()
            
    def find_roles_for_oficial(self, oficial_id: int) -> List[Rol]:
        oficial_db = self._session.query(OficialDbModel).filter_by(id=oficial_id).first()

        if not oficial_db:
            return []

        return [roles_db.to_entity() for roles_db in oficial_db.roles]
    
    def get_all_with_relations(self) -> List[Oficial]:
        """
        Implementa la carga ansiosa usando `joinedload`.
        Esto previene el problema N+1 al traer todos los datos
        relacionados en una sola consulta.
        """
        # 1. Empezamos la consulta como siempre.
        query = self._session.query(OficialDbModel)
        
        # 2. Usamos .options() para pasar las directivas de carga.
        #    Le pedimos que "una" la carga de los roles y las brand_sections.
        query = query.options(
            joinedload(OficialDbModel.roles),
            joinedload(OficialDbModel.brand_sections)
        )
        
        # 3. Ejecutamos la consulta y mapeamos los resultados.
        oficiales_db = query.all()
        
        return [oficial_db.to_entity() for oficial_db in oficiales_db]