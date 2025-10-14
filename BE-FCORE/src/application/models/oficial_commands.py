from dataclasses import dataclass

@dataclass(frozen=True)
class CreateOficialCommand:
    """Datos necesarios para crear un nuevo oficial."""
    q_code: str
    name: str
    lastname: str
    password: str 

@dataclass(frozen=True)
class UpdateOficialCommand:
    """Datos que se pueden actualizar de un oficial."""
    id: int
    name: str
    lastname: str