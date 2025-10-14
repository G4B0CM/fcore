from dataclasses import dataclass
from src.application.models.auth_command import LoginCommand

@dataclass
class AuthRequestDto:
    username : str
    password : str
    
    def to_command(self)->LoginCommand:
        return LoginCommand( username = self.username, password = self.password)
    
@dataclass
class AuthResponseDto:
    username : str
    token : str
    status : int