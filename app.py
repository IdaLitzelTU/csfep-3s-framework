from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from client import model_export
import logging
from sqlalchemy.orm import Session

from model import SessionLocal, engine, Base, schema, cursor

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# TODO: add token authentication

# setup loggers
logging.config.fileConfig("logging.conf", disable_existing_loggers=False)
logger = logging.getLogger(__name__)


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


data = {
    "a_harvest": 0.74,
    "biomass_left": 0.1,
    "acc_rate": [3.3, 5, 6.7],
    "wood_used": 0.5,
    "material_used": 1,
    "dmnf1": 0,
    "dmnf2": 0,
    "dmnf3": 0,
    "dmnf4": 200,
    "floor_area": 18,
    "xl": 20,
    "mass_ar_lm": 0.108,
    "mass_ar_vn": 0,
    "mass_ar_st_it": 0.00043,
    "mass_ar_con_t": 0.02347,
    "mass_ar_brick": 0.661,
    "mass_ar_con": 0.451,
    "mass_ar_mt_ps_co": 0.209,
    "mass_ar_mt_ps_rs": 0.194,
    "mass_ar_mt_en_co": 0.06,
    "mass_ar_mt_en_rs": 0.028,
    "mass_ar_wfb_en_co": 0.021,
    "mass_ar_wfb_en_rs": 0.01,
    "mass_ar_con_ps_co": 0.608,
    "mass_ar_stl_ps_co": 0.083,
    "mass_ar_stl_en_co": 0.01,
    "mass_ar_fbg_en_co": 0.002,
    "mass_ar_gyp_en_co": 0.013,
    "mass_ar_xps_en_co": 0.002,
}


@app.get("/")
async def root():
    logger.info("Root page")
    return {"message": "Hello World"}


@app.get("/model")
def get_model_versions():
    """
    returns all existing model versions
    """
    logger.debug(f"Existing model versions: {list(model_export.keys())}")
    return {"message": "OK", "results": list(model_export.keys())}


@app.get("/model/{version}")
def get_model_information(version: str):
    """
    get information on a specific model version if it exists
    """
    logger.info(f"Retrieving model version {version} metadata")
    model = model_export.get(version)
    if model:
        try:
            input = model.get("input")
            meta = model.get("meta")
            response = {"input": input, "meta": meta}
        except Exception as e:
            logger.exception(e)
    else:
        logger.debug("Cannot find version specified: {version}")
        return {
            "message": "error",
            "results": f"""Cannot find version specified.
            Version specified is {version}.
            Only following version are available {list(model_export.keys())}""",
        }

    return {"message": "OK", "results": response}


# TODO: have a ?parameter ?dataset to be able to run the model with stored datasets
@app.post("/model/{version}")
def run_model_version(version, body=data):
    """Runs the specified model version and returns the output of the model"""
    logger.info(f"Running model {version} with {body}")
    model = model_export.get(version)
    if model:
        model_executable = model.get("exec")
        results = model_executable(data=body, params=model.get("params"))
        logger.info(f"Model results: {results}")
    else:
        logger.debug(
            f"Cannot find version {version}. Only following version are available {', '.join(list(model_export.keys()))}"
        )
        return {
            "message": "OK",
            "results": f"""Cannot find version specified. Version specified is {version}.
                        Only following version are available {', '.join(list(model_export.keys()))}""",
        }
    return {"message": "OK", "results": results}


@app.get("/result")
def run_model_version_with_dataset(
    version: str, dataset: int, db: Session = Depends(get_db)
):
    logger.info(f"Running model version {version} with the dataset ID {dataset}")
    body = cursor.get_dataset_data_object(db=db, id=dataset)
    return run_model_version(version=version, body=body)


@app.get("/catalog", response_model=list[schema.CatalogVersion])
def get_catalog_entries_with_compatibiltiy(db: Session = Depends(get_db)):
    logger.info(f"Fetching catalog")
    return cursor.get_all_cataglog_entries(db=db)


@app.post("/dataset")
def put_dataset(body: schema.CatalogCreate, db: Session = Depends(get_db)):
    logger.info(f"Saved dataset: {body}")
    return cursor.put_dataset_object(db=db, body=body)


@app.get("/dataset/{id}", response_model=schema.CatalogData)
def get_dataset_by_id(id: int, db: Session = Depends(get_db)):
    logger.info(f"Retrieved dataset {id}")
    return cursor.get_catalog_entry(db=db, id=id)
