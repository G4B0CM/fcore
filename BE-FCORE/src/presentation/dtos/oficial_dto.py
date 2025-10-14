from dataclasses import dataclass
from src.core.entities.oficial import Oficial
from src.application.models.oficial_commands import CreateOficialCommand, UpdateOficialCommand

@dataclass(frozen=True)
class CreateOficialDto:
    """Datos necesarios para crear un nuevo oficial."""
    q_code: str
    name: str
    lastname: str
    password: str
    
    def to_command(self) -> CreateOficialCommand:

        return CreateOficialCommand(
            name=self.name,
            lastname=self.lastname,
            password=self.password,
            q_code=self.q_code
        )

@dataclass(frozen=True)
class UpdateOficialDto:
    """Datos que se pueden actualizar de un oficial."""
    id: int
    name: str
    lastname: str
    
    def to_command(self) -> UpdateOficialCommand:
        return UpdateOficialCommand(
            id = self.id,
            name=self.name,
            lastname=self.lastname
        )
        
@dataclass(frozen=True)
class ResponseOficialDto:
    """Datos de respuesta al crear un oficial."""
    id: int
    qcode: str
    is_active : bool
    
    @staticmethod
    def from_entity(oficial: Oficial) -> "ResponseOficialDto":
        return ResponseOficialDto(id = oficial._id, qcode= oficial.q_code, is_active= oficial.is_active)
        