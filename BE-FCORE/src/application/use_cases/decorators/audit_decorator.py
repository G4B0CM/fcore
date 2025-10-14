from src.application.ports.output.i_audit_logger import IAuditLogger
from src.application.ports.input.i_auth_use_case import IAuthUseCase
from src.application.models.login_command import LoginCommand
from src.application.models.login_result import LoginResult
from datetime import datetime
from typing import Optional

class AuditDecorator(IAuthUseCase):
    def __init__(self, use_case_to_wrap: IAuthUseCase, audit_logger: IAuditLogger):
        self._wrapped = use_case_to_wrap
        self._auditor = audit_logger

    def login(self, command: LoginCommand ) -> Optional[LoginResult]:
        result = self._wrapped.login(command)
        
        # Si tiene éxito, registramos la auditoría
        self._auditor.log(
            action="User Logged in", 
            details={"username": command.username ,"date_of_login": datetime.today()} 
        )
        
        return result
    
    def validate(self, token:str ) -> bool:
        result = self._wrapped.validate(token=token)
        
        # Si tiene éxito, registramos la auditoría
        self._auditor.log(
            action="Token validated", 
            details={"Token": token, "Result": result, "date_of_login": datetime.today()}
        )
        
        return result