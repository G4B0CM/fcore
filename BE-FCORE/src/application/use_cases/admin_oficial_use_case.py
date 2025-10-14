from typing import List, Optional
from src.application.ports.input.i_admin_oficial_use_case import IAdminOficialUseCase
from src.application.ports.output.i_oficial_repository import IOficialRepository
from src.application.ports.output.i_rol_repository import IRolRepository
from src.application.ports.output. i_password_hasher import IPasswordHasher
from src.application.models.oficial_commands import CreateOficialCommand, UpdateOficialCommand
from src.application.models.rol_commands import AssignRolCommand
from src.core.entities.oficial import Oficial
from src.core.entities.rol import Rol

from src.core.errors.oficial_exceptions import OficialAlreadyExistsError, OficialNotFoundError, OficialNotInAuthError
from src.core.errors.roles_exceptions import RolNotFoundError

class AdminOficialUseCase(IAdminOficialUseCase):
    def __init__(self, oficial_repository: IOficialRepository, 
                 rol_repository: IRolRepository,
                 password_hasher: IPasswordHasher,):
        self.oficial_repository = oficial_repository
        self.password_hasher = password_hasher
        self.rol_repository = rol_repository
        
    def create_oficial(self, command: CreateOficialCommand) -> Oficial:
        """
        Crea un nuevo oficial, hashea su contraseña y publica el evento de creación.
        """
        # 1. VERIFICAR: La regla de negocio de unicidad
        if self.oficial_repository.find_by_qcode(command.q_code):
            raise OficialAlreadyExistsError(f"Ya existe un oficial con el Q-Code {command.q_code}")

        # 2. PREPARAR: Hashear la contraseña
        hashed_password = self.password_hasher.hash_password(command.password)
        
        # 3. CONSTRUIR: Crear la instancia de la entidad correctamente
        oficial_entity = Oficial(
            _q_code=command.q_code,
            _name=command.name,
            _lastname=command.lastname,
            _password_hash=hashed_password
        )
        
        # 4. PERSISTIR: Guardar en nuestra base de datos primero
        created_oficial = self.oficial_repository.create(oficial=oficial_entity)
        return created_oficial
        
        
    
    def get_all_oficiales(self) -> List[Oficial]:
        """
        Devuelve una lista de todos los oficiales. Devuelve una lista vacía si no hay ninguno.
        """
        list_of_oficials = self.oficial_repository.get_all()
        return list_of_oficials
    
    def get_oficial_by_id(self, id: int) -> Optional[Oficial]:
        """
        Busca un oficial por su ID.
        """
        oficial = self.oficial_repository.find_by_id(id)
        if not oficial:
            raise OficialNotFoundError(f"No se encontró el oficial con id: {id}")
        
        return oficial
    
    def get_oficial_by_qcode(self, qcode: str) -> Optional[Oficial]:
        """
        Busca un oficial por su ID.
        """
        oficial = self.oficial_repository.find_by_qcode(qcode=qcode)
        if not oficial:
            raise OficialNotFoundError(f"No se encontró el oficial con código Q: {qcode}")
        
        return oficial
    
    def update_oficial(self, command: UpdateOficialCommand) -> Oficial:
        """
        Actualiza los datos de un oficial existente.
        """
        # 1. OBTENER: Buscamos al oficial existente por su ID único.
        oficial_to_update = self.oficial_repository.find_by_id(command.id)
        
        if not oficial_to_update:
            raise OficialNotFoundError(f"No se encontró un oficial con el ID {command.id}")
            
        # 2. MODIFICAR: Le pedimos a la propia entidad que se actualice.
        #    La lógica de qué y cómo se actualiza está encapsulada en la entidad.
        oficial_to_update.update_details(
            name=command.name,
            lastname=command.lastname
        )
        
        # 3. GUARDAR: Pasamos la entidad modificada al repositorio.
        updated_oficial = self.oficial_repository.update(oficial=oficial_to_update)
        
        return updated_oficial
    
    def deactivate_oficial(self, qcode: str) -> bool:
        """
        Desactiva un oficial (soft delete).
        """
        oficial = self.oficial_repository.deactivate(qcode=qcode)
        if not oficial:
            raise OficialNotFoundError(f"No se encontró el oficial con código Q: {qcode}")
        
        return oficial
    
    def assign_rol_to_oficial(self, command: AssignRolCommand) -> Oficial | None:
        oficial = self.get_oficial_by_id(command.oficial_id) # Reutilizamos la validación
        if not oficial:
            raise OficialNotFoundError(f"No se encontró el oficial con ID {command.oficial_id}")

        rol = self.rol_repository.find_by_id(command.rol_id)
        if not rol:
            raise RolNotFoundError(f"No se encontró el rol con ID {command.rol_id}")

        self.oficial_repository.assign_rol(oficial, rol)
        return self.get_oficial_by_id(command.oficial_id) # Devolvemos el estado actualizado

    def remove_rol_from_oficial(self, command: AssignRolCommand) -> Oficial | None:
        oficial = self.get_oficial_by_id(command.oficial_id)

        if not oficial:
            raise OficialNotFoundError(f"No se encontró el oficial con ID {command.oficial_id}")
        
        rol = self.rol_repository.find_by_id(command.rol_id)
        if not rol:
            raise RolNotFoundError(f"No se encontró el rol con ID {command.rol_id}")

        self.oficial_repository.remove_rol(oficial, rol)
        return self.get_oficial_by_id(command.oficial_id)
    
    def get_roles_assigned(self, oficial_id: int) -> List[Rol]:
        if not self.oficial_repository.find_by_id(oficial_id):
            raise OficialNotFoundError(f"No se encontró un oficial con el ID {oficial_id}")
            
        return self.oficial_repository.find_roles_for_oficial(oficial_id)