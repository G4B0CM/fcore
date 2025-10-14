from abc import ABC, abstractmethod
from typing import Optional, List

from src.application.models.oficial_commands import CreateOficialCommand, UpdateOficialCommand
from src.core.entities.oficial import Oficial
from src.core.entities.rol import Rol
from src.application.models.rol_commands import AssignRolCommand

class IAdminOficialUseCase(ABC):
    @abstractmethod
    def create_oficial(self, command: CreateOficialCommand) -> Oficial:
        """
        Crea un nuevo oficial, hashea su contraseña y publica el evento de creación.
        """
        pass
    
    @abstractmethod
    def get_all_oficiales(self) -> List[Oficial]:
        """
        Devuelve una lista de todos los oficiales. Devuelve una lista vacía si no hay ninguno.
        """
        pass
    
    @abstractmethod
    def get_oficial_by_id(self, id: int) -> Optional[Oficial]:
        """
        Busca un oficial por su ID.
        """
        pass
    
    @abstractmethod
    def get_oficial_by_qcode(self, qcode: str) -> Optional[Oficial]:
        """
        Busca un oficial por su ID.
        """
        pass
    
    @abstractmethod
    def update_oficial(self, command: UpdateOficialCommand) -> Oficial:
        """
        Actualiza los datos de un oficial existente.
        """
        pass
    
    @abstractmethod
    def deactivate_oficial(self, qcode: str) -> bool:
        """
        Desactiva un oficial (soft delete).
        """
        pass
    
    @abstractmethod
    def assign_rol_to_oficial(self, command: AssignRolCommand) -> Oficial:
        """Asigna un rol a un oficial."""
        pass

    @abstractmethod
    def remove_rol_from_oficial(self, command: AssignRolCommand) -> Oficial:
        """Remueve un rol de un oficial."""
        pass
    
    @abstractmethod
    def get_roles_assigned(self, oficial_id: int) -> List[Rol]:
        """Permite obtener todas las secciones de marca asiganadas a un oficial"""
        pass