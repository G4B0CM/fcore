from dataclasses  import dataclass
from typing import Optional
from src.core.errors.roles_exceptions import RolesValidationError

@dataclass
class Rol:
    
    _id : Optional[int]
    _main_name : str
    _description: str
    _is_active : bool = True
    
    @property
    def id(self) -> int | None:
        return self._id
    
    @property
    def main_name(self) -> str:
        return self._main_name
    
    @property
    def is_active(self) -> bool:
        return self._is_active
    
    @property
    def  description(self) -> str:
        return self._description
    
    def __post_init__(self):
        if not self._main_name or len(self._main_name.strip()) == 0:
            raise RolesValidationError("El nombre de un rol no puede estar vacío.")
        
    def update_details(self, new_main_name: str, new_description :str) -> None:
        """Actualiza los detalles del oficial y re-valida la entidad."""
        self._main_name = new_main_name
        self._description = new_description
        self.__post_init__()
        
        
        