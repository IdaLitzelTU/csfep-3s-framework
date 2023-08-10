from sqlalchemy.orm import Session
from . import table, schema
import json


def get_materials(db: Session):
    return db.query(table.Material).all()


def get_forests(db: Session):
    return db.query(table.Forest).all()


def get_version_compatible_datasets(db: Session, version: str):
    return db.query(table.Version).filter(table.Version.name == version).all()


def get_all_cataglog_entries(db: Session):
    return db.query(table.Catalog).all()


def get_catalog_entry(db: Session, id: int):
    return db.query(table.Catalog).filter(table.Catalog.id == id).first()


def determine_type(value):
    try:
        output = float(value)
    except:
        try:
            output = json.loads(value)
        except:
            output = value
    return output.__class__.__name__


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
        datatype = determine_type(value)
        dataset = table.Dataset(
            catalog_id=catalog.id, key=key, value=value, datatype=datatype
        )
        db.add(dataset)

    # publish dataset
    db.commit()

    return catalog.id


def cast_dict(data):
    out = {}
    for key, value in data.items():
        datatype = determine_type(value)
        out[key] = cast_to_type(value, datatype)
    return out


def get_dataset_data_object(db: Session, id: int):
    data = db.query(table.Dataset).filter(table.Dataset.catalog_id == id).all()
    out = {}

    for entry in data:
        out[entry.key] = entry.value
    return out


def cast_to_array(value):
    """
    Assumption: All arrays store float values.
    """
    arr = json.loads(value)
    arr = [cast_to_type(x, "float") for x in arr]
    return arr


def cast_to_dict(value):
    """
    Assumption: All dicts store float values.
    """
    dic = json.loads(value)
    for id, val in dic.items():
        dic[id] = cast_to_type(val, type="float")
    return dic


def cast_to_type(value, type):
    dtypes = {
        "float": float,
        "list": cast_to_array,
        "dict": cast_to_dict,
        "str": str,
    }
    parser_func = dtypes[type]
    try:
        v = parser_func(value)
    except Exception as e:
        raise ValueError("Value not casted to declared type: " + value)
    return v

