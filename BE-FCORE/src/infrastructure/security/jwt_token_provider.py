# src/infrastructure/security/jwt_token_provider.py (versión corregida)
import jwt
import logging 
from typing import Dict
from datetime import datetime, timedelta, timezone
from src.core.exceptions import ExpiredTokenError, TokenValidationError
from src.application.ports.output.i_token_provider import ITokenProvider
from ..config.settings import Settings

logger = logging.getLogger(__name__)

class JwtTokenProvider(ITokenProvider):
    
    def __init__(self, secret_key: str, algorithm: str = 'HS256', expiration_delta_minutes: int = 60):
        """
        Inicializa el proveedor de tokens.
        
        Args:
            secret_key: La clave secreta para firmar los tokens.
            algorithm: El algoritmo de firma a usar.
            expiration_delta_minutes: El tiempo de vida del token en minutos.
        """
        self._secret_key = secret_key
        self._algorithm = algorithm
        self._expiration_delta = timedelta(minutes=expiration_delta_minutes)

    def generate_token(self, subject: str) -> str:
        """Genera un nuevo token JWT para un 'subject' (q_code)."""
        issued_at = datetime.now(timezone.utc)
        expires_at = issued_at + self._expiration_delta
        
        payload = {
            'sub': subject, # <-- Usamos el subject (string)
            'iat': issued_at,
            'exp': expires_at
        }
        
        return jwt.encode(payload, self._secret_key, algorithm=self._algorithm)
    
    def validate_token(self, token: str) -> Dict:
        """
        Valida un token. Si es válido, devuelve el payload.
        Si no, lanza una excepción específica.
        """
        try:
            payload = jwt.decode(
                token,
                self._secret_key,
                algorithms=[self._algorithm],
                options={"verify_exp": True}
            )
            logger.info(payload)
            return payload
        except jwt.ExpiredSignatureError:
            # 3. Usamos el logger para registrar el error
            logger.warning("Intento de validación con token expirado.")
            raise ExpiredTokenError("El token ha expirado.")
        except jwt.InvalidTokenError as e:
            logger.warning(f"Intento de validación con token inválido: {e}")
            raise TokenValidationError(f"El token es inválido: {e}")
        except Exception as e:
            logger.warning(f"Excepcion producida: {e}")
            