from abc import ABC, abstractmethod

class IAuditLogger(ABC):
    @abstractmethod
    def log(self, action: str, details: dict):
        """Registra una acción de auditoría."""
        pass