from src.application.ports.output.i_audit_logger import IAuditLogger

class ConsoleLogger(IAuditLogger):
    def log(self, action: str, details: dict):
        """Registra una acción de auditoría."""
        print(f"acción: {action} \n detalles: {details}")