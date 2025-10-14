import re
from dataclasses  import dataclass
from typing import Optional, List, Set
from .rol import Rol
from src.core.errors.oficial_exceptions import OficialValidationError

@dataclass
class Oficial:
    _name : str
    _lastname : str
    _password_hash: str
    _q_code : str
    _roles: set[Rol] = None
    _is_active: bool = True
    _id : Optional[int] = None 
    
    def __post_init__(self):
        """Se ejecuta después de la inicialización para validar el estado."""
        if not self._name or len(self._name.strip()) == 0:
            raise OficialValidationError("El nombre del oficial no puede estar vacío.")
        if not self._lastname or len(self._lastname.strip()) == 0:
            raise OficialValidationError("El apellido del oficial no puede estar vacío.")
        if not self._password_hash:
            raise OficialValidationError("El hash de la contraseña no puede estar vacío.")
        if not self._q_code or not re.search(r"^Q\d{7,8}$",self._q_code): 
            raise OficialValidationError("El código Q debe empezar con 'Q' y tener 8 caracteres en total (ej: Q1234567).")

    @property
    def name(self) -> str:
        return self._name
    
    @property
    def lastname(self) -> str:
        return self._lastname

    @property
    def password_hash(self) -> str:
        return self._password_hash
    
    @property
    def q_code(self) -> str:
        return self._q_code
    
    @property
    def id(self) -> int | None:
        return self._id
    
    @property
    def roles(self) -> List[Rol]:
        """Devuelve los roles asignados, si han sido cargados."""
        return self._roles or []
    
    @property
    def is_active(self) -> bool:
        return self._is_active
    
    def update_details(self, name: str, lastname: str):
        """Actualiza los detalles del oficial y re-valida la entidad."""
        self._name = name
        self._lastname = lastname
        self.__post_init__()
    