from abc import ABC, abstractmethod
from typing import List, Optional
from src.core.entities.rol import Rol
from src.application.models.rol_commands import CreateRolCommand, UpdateRolCommand

class IAdminRolUseCase(ABC):
    """Interfaz para el caso de uso de administración de Roles."""

    @abstractmethod
    def create_rol(self, command: CreateRolCommand) -> Rol:
        """Crea un nuevo rol."""
        pass

    @abstractmethod
    def get_rol_by_id(self, id: int) -> Optional[Rol]:
        """Obtiene un rol por su ID."""
        pass
    
    @abstractmethod
    def get_all_roles(self) -> List[Rol]:
        """Obtiene todos los roles."""
        pass

    @abstractmethod
    def update_rol(self, command: UpdateRolCommand) -> Rol:
        """Actualiza un rol."""
        pass

    @abstractmethod
    def deactivate_rol(self, id: int) -> bool:
        """Desactiva un rol."""
        pass