from typing import TYPE_CHECKING
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from .associations import oficial_rol_association
from src.core.entities.oficial import Oficial

from src.infrastructure.database.models.base import Base

class OficialDbModel(Base):
    __tablename__ = 'oficial'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(length=30))
    lastname = Column(String(length=30))
    password_hash = Column(String)
    q_code = Column(String(8),unique=True)
    is_active = Column(Boolean)
    
    roles = relationship(
        "RolDbModel",
        secondary=oficial_rol_association,
        back_populates="oficiales",
        lazy="joined"  # ¡Importante! Carga los roles automáticamente con el oficial
    )
    
    def to_entity(self) -> Oficial:
        # Convertimos los números de la BD directamente a Enums
        try:
            roles_entity_list = [db_rol.to_entity() for db_rol in self.roles]
        except ValueError:
            # Si un valor de la BD no corresponde a un Enum, es un error de integridad de datos
            raise ValueError("Dato corrupto en la base de datos para Turn o FreeDays")

        return Oficial(
            _id=self.id,
            _name=self.name,
            _lastname=self.lastname,
            _password_hash=self.password_hash,
            _q_code=self.q_code,
            _roles=roles_entity_list,
            _is_active=self.is_active,
        )
        
    @staticmethod
    def from_entity(oficial: Oficial) -> "OficialDbModel":
        
        return OficialDbModel(
            id=oficial._id,
            name=oficial.name,
            lastname=oficial.lastname,
            password_hash=oficial.password_hash,
            q_code=oficial.q_code,
            is_active=oficial.is_active
        )