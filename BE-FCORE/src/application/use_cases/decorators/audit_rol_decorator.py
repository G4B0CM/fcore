from typing import List, Optional
from src.application.ports.output.i_audit_logger import IAuditLogger
from src.application.ports.input.i_admin_rol_use_case import IAdminRolUseCase
from src.application.models.rol_commands import CreateRolCommand, UpdateRolCommand

from src.core.entities.rol import Rol

from datetime import datetime

class AuditRolDecorator(IAdminRolUseCase):
    def __init__(self, use_case_to_wrap: IAdminRolUseCase, audit_logger: IAuditLogger):
        self._wrapped = use_case_to_wrap
        self._auditor = audit_logger
    
    def create_rol(self, command: CreateRolCommand) -> Rol:
        result = self._wrapped.create_rol(command)
        
        self._auditor.log(
            action="Rol creado", 
            details={"Nombre": command.name , "date_of_creation": datetime.now()} 
        )
        
        return result
    
    def get_all_roles(self) -> List[Rol]:        
        result = self._wrapped.get_all_roles()
        
        self._auditor.log(
            action="Listado de roles", 
            details={"Date_of_listation": datetime.now()} 
        )
        
        return result
    
    def get_rol_by_id(self, id: int) -> Optional[Rol]:
        result = self._wrapped.get_rol_by_id(id)
        
        self._auditor.log(
            action="Busqueda de rol por id", 
            details={"Id rol": id,"Date_of_search": datetime.now()} 
        )
        
        return result
    
    def update_rol(self, command: UpdateRolCommand) -> Rol:
        result = self._wrapped.update_rol(command)
        
        self._auditor.log(
            action="Rol Actualizado", 
            details={"Nombre": command.name, "date_of_modification": datetime.now()} 
        )
        
        return result
    
    def deactivate_rol(self, id: int) -> bool:
        result = self._wrapped.deactivate_rol(id)
        
        self._auditor.log(
            action="Desacivar sección de marca", 
            details={"Sección de marca": id,"Date_of_deactivation": datetime.now()} 
        )
        
        return result
    