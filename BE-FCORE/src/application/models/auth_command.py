# src/application/models/login_result.py
from dataclasses import dataclass

@dataclass(frozen=True)
class LoginResult:
    """Datos de salida de un login exitoso."""
    token: str
    user_id: int
    username: str


@dataclass(frozen=True) #Indica que es inmutable una vez creado
class LoginCommand:
    """Datos de entrada para el caso de uso de login."""
    username: str
    password: str