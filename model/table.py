from model import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class Serializable:
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Catalog(Base, Serializable):
    __tablename__ = "catalog"

    id = Column(Integer, primary_key=True, index=True)
    dataset_name = Column(String, index=True)
    description = Column(String, index=True)

    version = relationship("Version", back_populates="catalog")
    data = relationship("Dataset", back_populates="catalog")


class Version(Base, Serializable):

    __tablename__ = "compatibility"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    dataset = Column(Integer, ForeignKey("catalog.id"))
    catalog = relationship("Catalog", back_populates="version")


class Dataset(Base, Serializable):
    __tablename__ = "dataset"

    id = Column(Integer, primary_key=True, index=True)
    catalog_id = Column(Integer, ForeignKey("catalog.id"))
    key = Column(String)
    value = Column(String)
    datatype = Column(String)

    catalog = relationship("Catalog", back_populates="data")
