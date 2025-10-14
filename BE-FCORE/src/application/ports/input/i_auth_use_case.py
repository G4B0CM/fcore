from abc import ABC, abstractmethod
from typing import Optional
from src.application.models.auth_command import LoginCommand, LoginResult

class IAuthUseCase(ABC):
    @abstractmethod
    def login(self, command: LoginCommand) -> Optional[LoginResult]:
        """
        Ejecuta el caso de uso de login.

        Returns:
            LoginResult si es exitoso, None si las credenciales son inválidas.
        """
        pass
    
    @abstractmethod
    def validate(self, token: str) -> bool:
        """Valida si un token proveniente del gateway es seguro"""
        pass