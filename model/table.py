from model import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class Catalog(Base):
    __tablename__ = "catalog"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)

    version = relationship("Version", back_populates="catalog")
    data = relationship("Dataset", back_populates="catalog")


class Version(Base):

    __tablename__ = "compatibility"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    dataset = Column(Integer, ForeignKey("catalog.id"))
    catalog = relationship("Catalog", back_populates="version")


class Dataset(Base):
    __tablename__ = "dataset"

    id = Column(Integer, primary_key=True, index=True)
    catalog_id = Column(Integer, ForeignKey("catalog.id"))
    key = Column(String)
    value = Column(String)
    datatype = Column(String)

    catalog = relationship("Catalog", back_populates="data")
