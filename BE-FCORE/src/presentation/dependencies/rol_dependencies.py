from fastapi import  Depends

# Capa de Aplicación
from src.application.ports.output.i_rol_repository import IRolRepository
from src.application.ports.output.i_audit_logger import IAuditLogger
from src.application.ports.input.i_admin_rol_use_case import IAdminRolUseCase
from src.application.use_cases.admin_rol_use_case import AdminRolUseCase
from src.application.use_cases.decorators.audit_rol_decorator import AuditRolDecorator

# Capa de Infraestructura
from src.presentation.dependencies.base_dependencies import get_rol_repository, get_audit_logger

        
def get_admin_rol_use_case(
    repo: IRolRepository = Depends(get_rol_repository),
    auditor: IAuditLogger = Depends(get_audit_logger)
) -> IAdminRolUseCase:
    """
    Esta es la receta completa. FastAPI inyectará todas las piezas.
    """
    use_case = AdminRolUseCase( 
        rol_repository= repo
    )
    return AuditRolDecorator(use_case_to_wrap=use_case, audit_logger=auditor)
