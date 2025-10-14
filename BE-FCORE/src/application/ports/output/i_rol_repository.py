from abc import ABC, abstractmethod
from typing import List, Optional
from src.core.entities.rol import Rol

class IRolRepository(ABC):
    """Interfaz para el repositorio de la entidad Rol."""

    @abstractmethod
    def create(self, rol: Rol) -> Rol:
        """Crea un nuevo rol y lo devuelve con su ID."""
        pass

    @abstractmethod
    def find_by_id(self, id: int) -> Optional[Rol]:
        """Busca un rol por su ID."""
        pass

    @abstractmethod
    def find_by_name(self, name: str) -> Optional[Rol]:
        """Busca un rol por su nombre."""
        pass

    @abstractmethod
    def get_all(self) -> List[Rol]:
        """Devuelve una lista de todos los roles."""
        pass

    @abstractmethod
    def update(self, rol: Rol) -> Rol:
        """Actualiza un rol existente."""
        pass

    @abstractmethod
    def deactivate(self, id: int) -> bool:
        """Desactiva (soft delete) un rol por su ID."""
        pass