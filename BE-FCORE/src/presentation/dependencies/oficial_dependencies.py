
from fastapi import  Depends

# Capa de Aplicación
from src.application.ports.output.i_oficial_repository import IOficialRepository
from src.application.ports.output.i_rol_repository import IRolRepository
from src.application.ports.output.i_password_hasher import IPasswordHasher
from src.application.ports.output.i_audit_logger import IAuditLogger
from src.application.ports.input.i_admin_oficial_use_case import IAdminOficialUseCase
from src.application.use_cases.admin_oficial_use_case import AdminOficialUseCase
from src.application.use_cases.decorators.audit_oficial_decorator import AuditOficialDecorator



# Capa de Presentación
from src.presentation.dependencies.base_dependencies import (get_oficial_repository, bcrypt_hasher,
                                                             get_rol_repository, get_audit_logger)

        
def get_admin_oficial_use_case(
    repo: IOficialRepository = Depends(get_oficial_repository),
    rol_repo: IRolRepository = Depends(get_rol_repository),
    hasher: IPasswordHasher = Depends(lambda: bcrypt_hasher),
    auditor: IAuditLogger = Depends(get_audit_logger)
) -> IAdminOficialUseCase:
    """
    Esta es la receta completa. FastAPI inyectará todas las piezas.
    """
    use_case = AdminOficialUseCase(
        oficial_repository=repo,
        rol_repository= rol_repo,
        password_hasher=hasher,
    )
    return AuditOficialDecorator(use_case_to_wrap=use_case, audit_logger=auditor)
