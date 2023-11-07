from framework import v2 as csfep_3s
import json
from fastapi import Depends
from model import get_db, cursor

db = next(get_db())
materials = cursor.get_materials(db=db)
materials = [x.as_dict() for x in materials]
forests = cursor.get_forests(db=db)
forests = [x.as_dict() for x in forests]
db.close()

meta = {
    "version": "Transport Calculator v1",
    "by": "Galina Churkina",
    "contact": "ddi.support@dalberg.com",
    "description": "vTC is a transport calculator, which can help you compute the transport emissions, to insert into the chosen model version",
}

params = {
    "cf_log": 0.5,
    "c2co2": 3.67,
    # TODO: move transport to DB? kgco2/t/km
    "k_rail": {"min": 0.02601, "best": 0.02601, "max": 0.02601},
    "k_truck": {"min": 0.17398, "best": 0.36024, "max": 0.55731},
    "k_sea": {"min": 0.013155, "best": 0.013155, "max": 0.013155},
    "c_material": {
        x["id"]: {
            "min": x["min"],
            "best": x["best"],
            "max": x["max"],
            "istimber": x["istimber"],
        }
        for x in materials
    },
    "c_acc_forest": {
        x["id"]: {"min": x["min"], "best": x["best"], "max": x["max"]} for x in forests
    },
}

assumptions = {
    "Transport Calculator": "allows you to compute carbon emmissions for the defined steps",
    "Step name": "describes where your materials were moved e.g from forest to sawmill",
    "Mode of transport": "defines the way materials were transported in this step",
    "Mass in step": "is the mass of the materials transported in the current step",
    "Distance in step": "is distance materials travelling using the transport in step",
}

input = [
    {
        "name": "transport_stages",
        "category": "Transport Calculator",
        "display_name": "",
        "type": "staged_input",
        "fields": json.dumps(
            [
                {
                    "name": "step_name",
                    "display_name": "Step name",
                    "description": "Step name",
                    "type": "text",
                    "default": "None",
                },
                {
                    "name": "transport_type",
                    "display_name": "Type",
                    "description": "Mode of transport",
                    "type": "select",
                    "options": json.dumps(
                        [
                            {"name": "k_sea", "display_name": "By Sea"},
                            {"name": "k_truck", "display_name": "By Truck"},
                            {"name": "k_rail", "display_name": "By Rail"},
                        ]
                    ),
                },
                {
                    "name": "mass",
                    "display_name": "Material mass",
                    "description": "Mass in step",
                    "type": "number",
                    "default": "None",
                    "unit": "kg",
                },
                {
                    "name": "distance",
                    "display_name": "Step distance",
                    "description": "Distance in step",
                    "type": "number",
                    "default": "None",
                    "unit": "km",
                },
            ]
        ),
    }
]


def run(data, params, *args, **kwargs):
    emmissions = {"min": 0, "best": 0, "max": 0}

    output = {}
    for step in data.get("transport_stages"):
        for guess in ["min", "best", "max"]:
            coeff = step["transport_type"]
            coeff_value = params.get(coeff).get(guess)
            emmissions[guess] += csfep_3s.emitted_transporting(
                step["mass"], step["distance"], coeff_value, **params
            )
    output["emmissions"] = emmissions
    output["assumptions"] = assumptions

    return output
