from sqlalchemy.orm import Session
from . import table, schema
import json


def get_materials(db: Session):
    return db.query(table.Material).all()

def get_materials2(db: Session):
    return db.query(table.Material2).all()

def get_energy_sources(db: Session):
    return db.query(table.Energy_Sources).all()


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
    for var in body.data:
        # create dataset
        dataset = table.Dataset(
            catalog_id=catalog.id,
            key=var["name"],
            value=var["value"],
            inputtype=var["type"],
        )
        db.add(dataset)

    # publish dataset
    db.commit()

    return catalog.id


def cast_dict(data):
    out = {}
    for obj in json.loads(data):
        key = obj["name"]
        type = obj["type"]
        value = cast_to_type(obj["value"], type)
        out[key] = value
    return out


def get_dataset_data_object(db: Session, id: int):
    data = db.query(table.Dataset).filter(table.Dataset.catalog_id == id).all()
    out = []

    for entry in data:
        out.append({"name": entry.key, "value": entry.value, "type": entry.inputtype})
    return json.dumps(out)


def cast_to_array(value):
    """
    Assumption: All arrays store float values.
    """
    arr = json.loads(value)
    arr = [cast_to_type(x, "number") for x in arr]
    if len(arr) == 0:
        return [0, 0, 0]
    return arr


def cast_to_dict(value):
    """
    Sicherer Parser für flache und verschachtelte Gruppen-Strukturen.
    """
 
    if isinstance(value, str):
        dic = json.loads(value)
    else:
        dic = value

    for id, val in dic.items():
        if isinstance(val, dict):
            processed_sub_dict = {}
            for sub_key, sub_val in val.items():
                if sub_key == "mass":  # Oder allgemein auf Zahlen prüfen
                    processed_sub_dict[sub_key] = float(sub_val) if sub_val is not None else 0.0
                else:
                    processed_sub_dict[sub_key] = sub_val
            dic[id] = processed_sub_dict
        else:
            # Fallback für die alten, flachen Float-Dicionaries
            try:
                dic[id] = float(val) if val is not None else 0.0
            except (ValueError, TypeError):
                dic[id] = val # Falls es ein String oder null ist    
    return dic


def cast_to_array_of_dicts(value):
    arr = []
    for d in json.loads(value):
        for key, val in d.items():
            try:
                d[key] = json.loads(val)
            except (ValueError, TypeError):
                d[key] = val
        arr.append(d)
    return arr


def cast_to_type(value, type):
    dtypes = {
        "number": float,
        "array": cast_to_array,
        "group": cast_to_dict,
        "select": str,
        "staged_input": cast_to_array_of_dicts,
        "modal": cast_to_array,
        "populate": cast_to_array
    }
    parser_func = dtypes[type]
    try:
        v = parser_func(value)
    except Exception as e:
        raise ValueError("Value not casted to declared type: " + value)
    return v


def delete_dataset_entry(db: Session, id: int):
    delete_post = db.query(table.Catalog).filter(table.Catalog.id == id)
    try:
        exists = get_catalog_entry(db, id)
        if not exists:
            return {"code": 404, "message": "Dataset not found"}
        else:
            delete_post = db.query(table.Catalog).filter(table.Catalog.id == id)
            delete_post.delete(synchronize_session=False)
            db.commit()
            return {"code": 200, "message": f"Dataset {id} deleted"}

    except Exception as e:
        return {"code": 500, "message": e}
