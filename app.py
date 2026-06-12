from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from client import model_export
import logging
import logging.config
from sqlalchemy.orm import Session


from model import get_db, engine, Base, schema, cursor

Base.metadata.create_all(bind=engine)

# TODO: add token authentication

# setup loggers
# logging.config.fileConfig("logging.conf", disable_existing_loggers=False)
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) # shows logger.info in the console


app = FastAPI(debug=True)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
    meta = {}
    for key in model_export.keys():
        meta[key] = model_export[key].get("meta")
    return {"message": "OK", "results": list(model_export.keys()), "meta": meta}


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
            assumptions = model.get("assumptions")
            response = {"input": input, "meta": meta, "assumptions": assumptions}
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


@app.post("/run/{version}")
def run_model_version(version: str, body: str):
    """Runs the specified model version and returns the output of the model"""
    logger.info(f"Running model {version} with body")
    model = model_export.get(version)

    if model:
        model_executable = model.get("exec")

        results = model_executable(
            data=cursor.cast_dict(body), params=model.get("params")
        )
        #logger.info(f"Model results: {results}")
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
def run_model_version_with_dataset_id(
    version: str, dataset: int, db: Session = Depends(get_db)
):
    logger.info(f"Running model version {version} with the dataset ID ")
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


@app.delete("/dataset/{id}")
def delete_dataset_by_id(id: int, db: Session = Depends(get_db)):
    logger.info(f"Delete dataset: {id}")
    body = cursor.delete_dataset_entry(db=db, id=id)
    return body
