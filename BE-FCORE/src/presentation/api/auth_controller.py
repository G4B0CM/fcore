from fastapi import APIRouter, Depends, HTTPException, status, Security
from fastapi.security import APIKeyHeader
# Importamos la INTERFAZ del caso de uso, no la implementación.
from src.application.ports.input.i_auth_use_case import IAuthUseCase

# Importamos nuestro proveedor de dependencias y los DTOs
from src.presentation.dependencies.auth_dependencies import get_auth_use_case
from src.presentation.dtos.auth_dto import AuthRequestDto

# Importamos la excepción de dominio para manejarla
from src.core.exceptions import InvalidCredentials,TokenValidationError, ExpiredTokenError

oauth2_scheme = APIKeyHeader(name="Authorization")

# Creamos un router. Es como un sub-módulo de la aplicación.
router = APIRouter(
    prefix="/auth",  # Todas las rutas en este archivo empezarán con /auth
    tags=["Authentication"]  # Agrupa las rutas en la documentación de Swagger
)

@router.post("/login", status_code=status.HTTP_200_OK)
def login(
    request: AuthRequestDto,
    auth_uc: IAuthUseCase = Depends(get_auth_use_case)
):
    """
    Endpoint para autenticar un usuario. El controlador es 'delgado'.
    Solo traduce de HTTP a comandos y de resultados a respuestas HTTP.
    """
    try:
        command = request.to_command()
        result = auth_uc.login(command)
        return {"Result": result, "token_type": "bearer"}

    except InvalidCredentials as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
        
@router.post("/validate", status_code=status.HTTP_200_OK)
def validate_access_token(
    token: str = Security(oauth2_scheme),
    validate_uc: IAuthUseCase = Depends(get_auth_use_case)
):
    """
    Endpoint que el API Gateway usará para validar un token.
    """
    try:
        # Extraemos el token real, quitando "Bearer "
        if not token.startswith("Bearer "):
             raise TokenValidationError("Formato de token inválido. Debe ser 'Bearer <token>'.")
        
        actual_token = token.split(" ")[1]
        
        payload = validate_uc.validate(token=actual_token)
        
        # Si todo va bien, devolvemos el contenido del token (o un simple OK)
        return {"status": "ok", "payload": payload}

    except (ExpiredTokenError, TokenValidationError) as e:
        # Capturamos nuestras excepciones de dominio y las convertimos en un error HTTP 401
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        # Error genérico para cualquier otra cosa
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ocurrió un error inesperado: {str(e)}"
        )
        