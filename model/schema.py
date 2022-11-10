from pydantic import BaseModel


class Version(BaseModel):
    name: str

    class Config:
        orm_mode = True


class Dataset(BaseModel):
    key: str
    value: str
    datatype: str

    class Config:
        orm_mode = True


class Catalog(BaseModel):
    name: str
    description: str
    version: list[Version] = []
    data: list[Dataset] = []

    class Config:
        orm_mode = True


class CatalogCreate(BaseModel):
    name: str
    description: str
    version: str
    data: dict
