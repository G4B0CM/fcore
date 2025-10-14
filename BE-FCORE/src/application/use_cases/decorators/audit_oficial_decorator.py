from typing import List, Optional
from src.application.ports.output.i_audit_logger import IAuditLogger
from src.application.ports.input.i_admin_oficial_use_case import IAdminOficialUseCase
from src.application.models.oficial_commands import CreateOficialCommand, UpdateOficialCommand
from src.application.models.rol_commands import AssignRolCommand

from src.core.entities.oficial import Oficial
from src.core.entities.rol import Rol

from datetime import datetime

class AuditOficialDecorator(IAdminOficialUseCase):
    def __init__(self, use_case_to_wrap: IAdminOficialUseCase, audit_logger: IAuditLogger):
        self._wrapped = use_case_to_wrap
        self._auditor = audit_logger
    
    def create_oficial(self, command: CreateOficialCommand) -> Oficial:

        result = self._wrapped.create_oficial(command)
        
        self._auditor.log(
            action="Oficial Creado", 
            details={"Nombre": command.name , "Codigo Q": command.q_code ,"date_of_creation": datetime.now()} 
        )
        
        return result
        
        
    
    def get_all_oficiales(self) -> List[Oficial]:
        result = self._wrapped.get_all_oficiales()
        
        self._auditor.log(
            action="Listado de oficiales", 
            details={"Date_of_listation": datetime.now()} 
        )
        
        return result
    
    def get_oficial_by_id(self, id: int) -> Optional[Oficial]:
        result = self._wrapped.get_oficial_by_id(id)
        
        self._auditor.log(
            action="Busqueda de oficial por id", 
            details={"Id Oficial": id,"Date_of_search": datetime.now()} 
        )
        
        return result
    
    def get_oficial_by_qcode(self, qcode: str) -> Optional[Oficial]:
        result = self._wrapped.get_oficial_by_qcode(qcode)
        
        self._auditor.log(
            action="Busqueda de oficial por Código Q", 
            details={"Q Oficial": qcode,"Date_of_search": datetime.now()} 
        )
        
        return result
    
    def update_oficial(self, command: UpdateOficialCommand) -> Oficial:
        result = self._wrapped.update_oficial(command)
        
        self._auditor.log(
            action="Oficial Actualizado", 
            details={"Nombre": command.name, "Apellido" : command.lastname ,"date_of_creation": datetime.now()} 
        )
        
        return result
    
    def deactivate_oficial(self, qcode: str) -> bool:
        result = self._wrapped.deactivate_oficial(qcode)
        
        self._auditor.log(
            action="Desactivar Oficial", 
            details={"Q Oficial": qcode,"Date_of_deactivation": datetime.now()} 
        )
        
        return result
    
    def assign_rol_to_oficial(self, command: AssignRolCommand) -> Oficial:
        result = self._wrapped.assign_rol_to_oficial(command)
        
        self._auditor.log(
            action="Rol Asignado", 
            details={"Id": command.rol_id, "Oficial Id" : command.oficial_id ,"date_of_assignation": datetime.now()} 
        )
        
        return result

    def remove_rol_from_oficial(self, command: AssignRolCommand) -> Oficial:
        result = self._wrapped.remove_rol_from_oficial(command)
        
        self._auditor.log(
            action="Rol Desasignado", 
            details={"Id": command.rol_id, "Oficial Id" : command.oficial_id ,"date_of_assignation": datetime.now()} 
        )
        
        return result
    
    def get_roles_assigned(self, oficial_id: int) -> List[Rol]:
        result = self._wrapped.get_roles_assigned(oficial_id= oficial_id)
        
        self._auditor.log(
            action="Listado de roles de un oficial", 
            details={"Id Oficial": oficial_id, "Date_of_listation": datetime.now()} 
        )
        
        return result