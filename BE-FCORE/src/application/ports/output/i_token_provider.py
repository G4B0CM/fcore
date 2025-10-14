from abc import ABC, abstractmethod
from typing import Dict

class ITokenProvider(ABC):
    @abstractmethod
    def generate_token(self, subject: str) -> str:
        pass
    @abstractmethod
    def validate_token(self, token: str) -> Dict:
        pass
