from sqlalchemy import Table, Column, Integer, ForeignKey

from .base import Base

oficial_rol_association = Table(
    'oficial_rol_association', Base.metadata,
    Column('oficial_id', Integer, ForeignKey('oficial.id'), primary_key=True),
    Column('rol_id', Integer, ForeignKey('roles.id'), primary_key=True)
)