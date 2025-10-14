from abc import ABC, abstractmethod

class IPasswordHasher(ABC):
    @abstractmethod
    def hash_password(self, unhashed_password : str) -> str:
        pass
    
    @abstractmethod
    def verify_password(self, plain_password: str, hash: str) -> bool:
        pass
