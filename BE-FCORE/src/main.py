# src/main.py

import logging
import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

# --- Importaciones de nuestra arquitectura ---
# Capa de Presentación (DTOs y Controladores implícitos en los endpoints)
from presentation.api.auth_controller import router

# Capa de Infraestructura
from src.infrastructure.config.settings import settings
from src.infrastructure.security.bcrypt_password_hasher import BcryptPasswordHasher
from src.infrastructure.security.jwt_token_provider import JwtTokenProvider

#Infrstructure
from src.infrastructure.database.models.base import Base
from src.infrastructure.database.models import oficial_db_model
#Presentation
from presentation.api.oficial_controller import oficial_router
from presentation.api.rol_controller import rol_router

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY', 'default-super-secret-key')
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./oficials.db')

origins = [
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ]

# --- 2. Configuración de la Base de Datos ---
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

# --- FastAPI App ---
app = FastAPI(title="Back-end de Gestión de Oficiales")
        
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app.include_router(router)
app.include_router(oficial_router)
app.include_router(rol_router) 

app.add_middleware(CORSMiddleware,
    allow_origins= origins,  # Permitir todas las fuentes (ajustar en producción)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.get("/", tags=["Health Check"])
def read_root():
    """Endpoint de salud para verificar que el gateway está vivo."""
    return {"status": "ok", "message": "Back-end is running"}

@app.middleware("http")
async def exception_handler_middleware(request: Request, call_next):
    """
    Middleware que captura cualquier excepción no controlada,
    la registra y devuelve una respuesta de error genérica.
    """
    try:
        # Intenta procesar la petición normalmente
        response = await call_next(request)
        return response
    except Exception as e:
        # Si ocurre CUALQUIER error inesperado...
        # 1. Lo registramos para poder depurarlo (en la consola o en un archivo)
        logger.error(f"Error no controlado en {request.method} {request.url}: {e}", exc_info=True)
        
        # 2. Devolvemos una respuesta genérica y segura al cliente
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Ocurrió un error interno en el servidor."},
        )
