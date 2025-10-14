from dataclasses import dataclass

@dataclass(frozen=True)
class CreateRolCommand:
    name: str
    description: str

@dataclass(frozen=True)
class UpdateRolCommand:
    id: int
    name: str
    description: str
    
@dataclass(frozen=True)
class AssignRolCommand:
    oficial_id: int
    rol_id: int