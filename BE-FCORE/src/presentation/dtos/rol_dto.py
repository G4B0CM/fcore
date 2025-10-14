from dataclasses import dataclass
from src.application.models.rol_commands import CreateRolCommand, UpdateRolCommand
from src.core.entities.rol import Rol

@dataclass(frozen=True)
class CreateRolDto:
    name: str
    description: str

    def to_command(self) -> CreateRolCommand:
        return CreateRolCommand(name=self.name, description=self.description)

@dataclass(frozen=True)
class UpdateRolDto:
    name: str
    description: str

    def to_command(self, rol_id: int) -> UpdateRolCommand:
        return UpdateRolCommand(id=rol_id, name=self.name, description=self.description)

@dataclass(frozen=True)
class RolResponseDto:
    id: int
    name: str
    description: str
    is_active: bool

    @staticmethod
    def from_entity(rol: Rol) -> "RolResponseDto":
        return RolResponseDto(
            id=rol.id,
            name=rol.main_name,
            description=rol.description,
            is_active=rol.is_active
        )