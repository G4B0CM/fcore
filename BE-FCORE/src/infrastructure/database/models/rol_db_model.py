from sqlalchemy import Column, Integer, String, Boolean
from .base import Base
from src.core.entities.rol import Rol
from sqlalchemy.orm import relationship
from .associations import oficial_rol_association

class RolDbModel(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    
    oficiales = relationship(
        "OficialDbModel",
        secondary=oficial_rol_association,
        back_populates="roles"
    )

    def to_entity(self) -> Rol:
        return Rol(
            _id=self.id,
            _main_name=self.name,
            _description=self.description,
            _is_active=self.is_active
        )

    @staticmethod
    def from_entity(rol: Rol) -> "RolDbModel":
        return RolDbModel(
            id=rol.id,
            name=rol.main_name,
            description=rol.description,
            is_active=rol.is_active
        )