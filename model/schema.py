from pydantic import BaseModel


class Dataset(BaseModel):
    key: str
    value: str
    datatype: str

    class Config:
        orm_mode = True


class Version(BaseModel):
    name: str

    class Config:
        orm_mode = True


class CatalogData(BaseModel):
    dataset_name: str
    description: str
    data: list[Dataset] = []

    class Config:
        orm_mode = True


class CatalogVersion(BaseModel):
    id: int
    dataset_name: str
    description: str
    version: list[Version]

    class Config:
        orm_mode = True


class CatalogCreate(BaseModel):
    name: str
    description: str
    version: str
    data: dict
