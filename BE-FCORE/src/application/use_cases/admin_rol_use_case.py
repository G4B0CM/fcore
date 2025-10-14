from typing import List, Optional
from src.application.ports.input.i_admin_rol_use_case import IAdminRolUseCase
from src.application.ports.output.i_rol_repository import IRolRepository
from src.application.models.rol_commands import CreateRolCommand, UpdateRolCommand
from src.core.entities.rol import Rol
from src.core.errors.roles_exceptions import RolNotFoundError, RolAlreadyExistsError

class AdminRolUseCase(IAdminRolUseCase):
    
    def __init__(self, rol_repository: IRolRepository):
        self._rol_repository = rol_repository

    def create_rol(self, command: CreateRolCommand) -> Rol:
        if self._rol_repository.find_by_name(command.name):
            raise RolAlreadyExistsError(f"El rol con nombre '{command.name}' ya existe.")
        
        rol_entity = Rol(
            _id=None,
            _main_name=command.name,
            _description=command.description
        )
        return self._rol_repository.create(rol_entity)

    def get_rol_by_id(self, id: int) -> Optional[Rol]:
        return self._rol_repository.find_by_id(id)

    def get_all_roles(self) -> List[Rol]:
        return self._rol_repository.get_all()

    def update_rol(self, command: UpdateRolCommand) -> Rol:
        rol_to_update = self._rol_repository.find_by_id(command.id)
        if not rol_to_update:
            raise RolNotFoundError(f"No se encontró un rol con el ID {command.id}")

        # Verificamos si el nuevo nombre ya está en uso por OTRO rol
        existing_rol_with_name = self._rol_repository.find_by_name(command.name)
        if existing_rol_with_name and existing_rol_with_name.id != command.id:
            raise RolAlreadyExistsError(f"El nombre de rol '{command.name}' ya está en uso.")

        rol_to_update.update_details(
            new_main_name=command.name,
            new_description=command.description
        )
        return self._rol_repository.update(rol_to_update)

    def deactivate_rol(self, id: int) -> bool:
        if not self._rol_repository.find_by_id(id):
            raise RolNotFoundError(f"No se encontró un rol con el ID {id}")
        
        return self._rol_repository.deactivate(id)