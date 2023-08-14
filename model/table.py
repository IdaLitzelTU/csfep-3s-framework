from model import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship


class Serializable:
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Catalog(Base, Serializable):
    __tablename__ = "catalog"

    id = Column(Integer, primary_key=True, index=True)
    dataset_name = Column(String, index=True)
    description = Column(String)
    organisation_name = Column(String)
    publisher_name = Column(String)
    version = relationship("Version", back_populates="catalog")
    data = relationship("Dataset", back_populates="catalog", cascade="all,delete")


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


class Material(Base, Serializable):
    __tablename__ = "materials"

    id = Column(String, primary_key=True)
    material = Column(String)
    reference = Column(String)
    best = Column(Float)
    min = Column(Float)
    max = Column(Float)
    istimber = Column(Boolean)


class Forest(Base, Serializable):
    __tablename__ = "forests"

    id = Column(String, primary_key=True)
    forest = Column(String)
    type = Column(String)
    location = Column(String)
    reference = Column(String)
    best = Column(Float)
    min = Column(Float)
    max = Column(Float)
