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


def cast_dict(obj):
    if isinstance(obj, dict):
        out = {}
        for key, value in obj.items():
            if isinstance(value, str):
                try:
                    out[key] = float(value)
                except ValueError:
                    try:
                        nested_dict = json.loads(value)
                        if isinstance(nested_dict, dict):
                            out[key] = cast_dict(nested_dict)
                        elif isinstance(nested_dict, list):
                            out[key] = [float(item) for item in nested_dict]
                        else:
                            out[key] = value
                    except json.JSONDecodeError:
                        out[key] = value
            else:
                out[key] = cast_dict(value)
        return out
    else:
        return obj



def get_dataset_data_object(db: Session, id: int):
    data = db.query(table.Dataset).filter(table.Dataset.catalog_id == id).all()
    out = {}

    for entry in data:
        out[entry.key] = entry.value
    return out

""" 
def cast_to_type(value, type=""):
    if is_valid_json(value):
        v = json.loads(value)
        if is_valid_json(v):
            print("---nested dict",v)
            v = cast_to_type(v)
    else:
        try:
            v = float(value)
        except Exception as e:
            print("---ERROR",e)
            v = str(value)
    # dtypes = ('dict','float','string','')

    # typeCast = dtypes.get(type, float)
    # v = typeCast(value)

    # try:
    #     # is it valid json? -> jsonloads -> cast each value
    #     # if not -> try to float 
    #     # else to string
    #     v = float(value)
    # except Exception as e:
    #     if value.startswith('{'):
    #         v = cast_to_type(json.loads(value))
    #     else:
    #         v = str(value)
    print(f'---cast{v}')
    return v

def is_valid_json(json_string):
    try:
        json.loads(json_string)
        return True
    except ValueError:
        return False
"""