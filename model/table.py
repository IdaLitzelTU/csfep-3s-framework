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

    data = relationship("Dataset", back_populates="catalog",cascade="all, delete-orphan")


class Version(Base, Serializable):
    __tablename__ = "compatibility"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    dataset = Column(Integer, ForeignKey("catalog.id"))
    catalog = relationship("Catalog", back_populates="version",cascade="all, delete")


class Dataset(Base, Serializable):
    __tablename__ = "dataset"

    id = Column(Integer, primary_key=True, index=True)
    catalog_id = Column(Integer, ForeignKey("catalog.id"))
    key = Column(String)
    value = Column(String)
    inputtype = Column(String)

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

class Material2(Base, Serializable):
    __tablename__ = "materials2"
    id = Column(String, primary_key=True)
    material = Column(String)
    min_co2e = Column(Float)
    best_co2e = Column(Float)
    max_co2e = Column(Float)
    min_manuf_eec = Column(Float)
    best_manuf_eec = Column(Float)
    max_manuf_eec = Column(Float)
    min_sourcing_eec = Column(Float)
    best_sourcing_eec = Column(Float)
    max_sourcing_eec = Column(Float)
    d_green = Column(Float)
    d_dry = Column(Float)
    c_content= Column(Float)
    reference = Column(String)
    is_timber = Column(Boolean)

class Energy_Sources(Base, Serializable):
    __tablename__ = "energy_sources"
    id = Column(String, primary_key=True)
    source = Column(String)
    emission_factor = Column(Float)
    reference = Column(String)

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
