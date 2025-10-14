from fastapi import Depends
from sqlalchemy.orm import Session

# Importamos las interfaces que nuestros controladores van a pedir
from src.application.ports.input.i_auth_use_case import IAuthUseCase
from src.application.ports.output.i_oficial_repository import IOficialRepository

# Importamos las implementaciones concretas para construir el caso de uso
from src.application.use_cases.auth_use_case import AuthUserUseCase
from src.infrastructure.security.bcrypt_password_hasher import BcryptPasswordHasher
from src.infrastructure.security.jwt_token_provider import JwtTokenProvider
from src.infrastructure.config.settings import settings

# Importamos la función que nos da la sesión de la BD y las dependencias ya creadas

from src.presentation.dependencies.base_dependencies import bcrypt_hasher,get_oficial_repository

jwt_provider = JwtTokenProvider(secret_key=settings.SECRET_KEY, expiration_delta_minutes=30)


def get_auth_use_case(oficials_repo : IOficialRepository = Depends(get_oficial_repository)) -> IAuthUseCase:
    """
    Esta función es un 'proveedor' de dependencias.
    Sabe cómo construir un LoginUserUseCase completo.
    FastAPI se encargará de llamarla cuando un endpoint la necesite.
    """
    
    # 2. Ensamblamos y devolvemos la instancia del caso de uso
    return AuthUserUseCase(
        auth_repository= oficials_repo,
        password_hasher=bcrypt_hasher,
        token_provider=jwt_provider
    )