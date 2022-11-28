from sqlalchemy.orm import Session
from . import table, schema
import json


def get_version_compatible_datasets(db: Session, version: str):
    return db.query(table.Version).filter(table.Version.name == version).all()


def get_all_cataglog_entries(db: Session):
    return db.query(table.Catalog).all()


def get_catalog_entry(db: Session, id: int):
    return db.query(table.Catalog).filter(table.Catalog.id == id).first()


def put_dataset_object(db: Session, body: schema.CatalogCreate):

    name = body.dataset_name
    description = body.description
    model_version = body.version
    publisher = body.publisher_name
    org = body.organisation_name

    # create catalogue object
    catalog = table.Catalog(
        dataset_name=name,
        description=description,
        publisher_name=publisher,
        organisation_name=org,
    )
    db.add(catalog)
    db.flush()
    db.refresh(catalog)

    # create version object
    # TODO: validate compatibility
    version = table.Version(name=model_version, dataset=catalog.id)
    db.add(version)

    for key, value in body.data.items():
        # create dataset
        dataset = table.Dataset(
            catalog_id=catalog.id, key=key, value=value, datatype="string"
        )
        db.add(dataset)

    # publish dataset
    db.commit()

    return catalog.id


def cast_dict(data):
    out = {}
    for key, value in data.items():
        out[key] = cast_to_type(value)
    return out


def get_dataset_data_object(db: Session, id: int):
    data = db.query(table.Dataset).filter(table.Dataset.catalog_id == id).all()
    out = {}

    for entry in data:
        out[entry.key] = entry.value
    return out


def cast_to_type(value, type=""):

    # dtypes = {
    #     "number": float,
    #     "array": json.loads
    # }

    # typeCast = dtypes.get(type, float)
    # v = typeCast(value)

    try:
        v = float(value)
    except Exception as e:
        v = json.loads(value)

    return v
