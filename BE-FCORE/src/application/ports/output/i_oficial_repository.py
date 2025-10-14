from abc import ABC, abstractmethod
from typing import List, Optional
from src.core.entities.oficial import Oficial
from src.core.entities.rol import Rol

class IOficialRepository(ABC):
    @abstractmethod
    def create(self, oficial: Oficial) -> Oficial:
        """
        Guarda un nuevo oficial en la base de datos y devuelve la entidad con su ID asignado.
        """
        pass
    
    @abstractmethod
    def find_by_qcode(self, qcode: str) -> Optional[Oficial]:
        """
        Busca un oficial por su Q-code. Devuelve el oficial o None si no se encuentra.
        """
        pass
    
    @abstractmethod
    def get_all(self) -> List[Oficial]:
        """
        Devuelve todos los oficiales.
        """
        pass
    
    @abstractmethod
    def find_by_id(self, id: int) -> Optional[Oficial]:
        """
        Busca un oficial por su ID. Devuelve el oficial o None si no se encuentra.
        """
        pass
    
    @abstractmethod
    def update(self, oficial: Oficial) -> Oficial:
        """
        Actualiza los datos de un oficial existente y devuelve la entidad actualizada.
        """
        pass
    
    @abstractmethod
    def deactivate(self, qcode: str) -> bool:
        """
        Desactiva un oficial (soft delete). Devuelve True si tuvo éxito.
        """
        pass
    
    @abstractmethod
    def assign_rol(self, oficial: Oficial, rol: Rol) -> None:
        """Asigna un rol a un oficial."""
        pass

    @abstractmethod
    def remove_rol(self, oficial: Oficial, rol: Rol) -> None:
        """Remueve un rol de un oficial."""
        pass
    
    @abstractmethod
    def find_roles_for_oficial(self, oficial_id: int) -> List[Rol]:
        """
        Devuelve una lista de los roles asignados a un oficial específico.
        """
        pass
    
    @abstractmethod
    def get_all_with_relations(self) -> List[Oficial]:
        """
        Devuelve todos los oficiales, cargando de forma eficiente
        sus relaciones (roles y brand_sections).
        """
        pass
    