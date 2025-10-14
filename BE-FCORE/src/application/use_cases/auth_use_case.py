from typing import Dict

from src.application.ports.output.i_oficial_repository import IOficialRepository
from src.application.ports.output.i_password_hasher import IPasswordHasher
from src.application.ports.output.i_token_provider import ITokenProvider
from src.core.exceptions import InvalidCredentials, TokenValidationError
from src.application.ports.input.i_auth_use_case import IAuthUseCase
from src.application.models.auth_command import LoginCommand, LoginResult

class AuthUserUseCase(IAuthUseCase):
    def __init__(
        self,
        auth_repository: IOficialRepository,
        password_hasher: IPasswordHasher,
        token_provider: ITokenProvider
    ):
        self._auth_repository = auth_repository
        self._password_hasher = password_hasher
        self._token_provider = token_provider

    def login(self, command) -> LoginResult:
        # 1. Buscar al usuario
        user = self._auth_repository.find_by_qcode(command.username)
        if not user:
            raise InvalidCredentials("Credenciales invalidas")

        # 2. Verificar la contraseña
        if not self._password_hasher.verify_password(command.password, user.password_hash):
            raise InvalidCredentials("Credenciales invalidas")
        
        # 3. Generar y devolver el token
        token = self._token_provider.generate_token(subject=user.q_code)
        
        result_user = LoginResult(token=token,user_id=user.id,username=user.q_code)
        return result_user
    
    def validate(self, token: str) -> Dict:
        """
        Valida el token usando el proveedor.
        Devuelve el payload si es exitoso o permite que las excepciones
        de TokenValidationError fluyan hacia la capa de presentación.
        """     
        return self._token_provider.validate_token(token=token)
        
        