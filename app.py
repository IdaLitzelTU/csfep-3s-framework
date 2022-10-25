from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from client import model_export
from client.parameters import model_parameters

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
    "massARcon": 0.451,
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
    return {"message": "Hello World"}


@app.get("/model")
def get_model_versions():
    """
    returns all existing model versions
    """
    return {"message": "OK", "results": ";".join(model_export.keys())}


@app.get("/model/{version}")
def get_model_information(version: str):
    """
    get information on a specific model version if it exists
    """
    model = model_export.get(version)
    if model:
        input = model.get("input")
        meta = model.get("meta")
        response = {"input": input, "meta": meta}
    else:
        return {
            "message": "error",
            "results": f"""Cannot find version specified. Version specified is {version}. 
                                                Only following version are available {', '.join(list(model_export.keys()))}""",
        }

    return {"message": "OK", "results": response}


@app.get("/dataset")
def get_dataset(name):
    pass


@app.put("/dataset")
def put_dataset(body):
    pass


# TODO: have a ?parameter ?dataset to be able to run the model with stored datasets
@app.post("/model/{version}")
def run_model_version(version, body=data):
    """Runs the specified model version and returns the output of the model"""
    model = model_export.get(version)
    if model:
        model_executable = model.get("exec")
        try:
            # TODO: save the body of the input
            results = model_executable(data=body, params=model_parameters)
        except Exception as e:
            return {"message": "error", "results": f"{e}"}
    else:
        return {
            "message": "OK",
            "results": f"""Cannot find version specified. Version specified is {version}. 
                                                Only following version are available {', '.join(list(model_export.keys()))}""",
        }
    return {"message": "OK", "results": results}
