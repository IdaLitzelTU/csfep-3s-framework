from framework import v2 as csfep_3s
import json
from model import get_db, cursor

db = next(get_db())
materials = cursor.get_materials(db=db)
materials = [x.as_dict() for x in materials]
forests = cursor.get_forests(db=db)
forests = [x.as_dict() for x in forests]
db.close()

meta = {
    "version": "2",
    "by": "Galina Churkina",
    "contact": "ddi.support@dalberg.com",
    "description": "v2 of the model is the 'City to Forest' version, focusing on building specific infrastructures such as building, bridges, etc. from timber",
}

params = {
    "cf_log": 0.5,
    "c2co2": 3.67,
    # TODO: move transport to DB?
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
    "V2 (CITY2FOREST) ": "focuses on building specific infrastructures such as building, bridge, etc. from timber.",
    "Building:": "Storage of carbon in structures is estimated for all materials containing biomass-based carbon of a structure as provided by a user.",
    "Scenarios:": """
    Carbon storage and emissions were estimated for three scenarios, which reflect variabilities in carbon accumulation
    rates in forests (min, best guess, max) and in carbon emission coefficients of construction materials (min, mean, max).
    """,
    "Forest regrows:": """In this version of the model, it is assumed that the forest immediately regrows after timber harvest with carbon accumulation rates
    appropriate for the geographic region and forest type. The carbon losses after timber harvest from enhanced soil respiration are assumed negligible as in selective cutting.
    This assumption leads to underestimation of forest losses if forest is clear cut.
    A range of carbon accumulation rates in forests is provided to capture the growth variability for different forest ages and in different climates.
    """,
    "Forest timber harvest:": """A part of the harvested biomass is left on site. It usually includes leaves, branches and tree tops, which are particularly nutrient rich and after decomposition provide those nutrients to the re-growing forests.
    Currently the default fraction of harvested biomass left on site is 10%. This value is based on the interview results of forest rangers in Europe and may need to be adjusted for other parts of the world.
    """,
    "Manufacturing:": """Only a fraction of harvested timber goes into the constructed building and the respective carbon amounts will be stored there during the building’s lifespan.
    There are two major steps in manufacturing when various fractions of timber can be lost such as sawing and prefabrication of building’s parts. Here it is assumed that those timber fractions and associated carbon go into the scrap wood pool.
    The scrap wood can be used to produce various products from wood fiber insolation to wood chips or other biomass energy sources.
    Material substitution benefits are calculated by comparing the carbon emissions from production of conventional structure to timber structure. These emissions stem from material manufacturing and transport.
    Carbon emissions from manufacturing the same material can vary depending on the manufacturing technologies and energy sources.
    This variability was captured by using a range of values for material carbon emission coefficients where availble. """,
}
input = [
    {
        "name": "building_floor_area",
        "category": "Building",
        "display_name": "Total floor area",
        "description": "The floor area",
        "type": "number",
        "default": "None",
        "unit": "m2",
        "min": 0.1,
        "max": 100000,
    },
    {
        "name": "building_lifespan",
        "category": "Building",
        "display_name": "Expected life span of the building",
        "description": "The expected life span of the building",
        "type": "number",
        "default": "None",
        "unit": "years",
        "min": 1,
        "max": 10000,
    },
    {
        "name": "conventional_mineral_materials",
        "category": "Conventional building",
        "display_name": "Select materials",
        "description": "Mineral-based materials used in the building",
        "type": "group",
        "default": "None",
        "fields": json.dumps(
            [
                {
                    "name": x["id"],
                    "display_name": x["material"],
                    "description": f"{x['material']} mass",
                    "type": "number",
                    "default": "None",
                    "unit": "kg",
                    "min": 0.1,
                    "max": 1000000,
                }
                for x in materials
                if not x["istimber"]
            ]
        ),
    },
    {
        "name": "conventional_biomass_materials",
        "category": "Conventional building",
        "display_name": "Select materials",
        "description": "Biomass-based materials used in the building",
        "type": "group",
        "default": "None",
        "fields": json.dumps(
            [
                {
                    "name": x["id"],
                    "display_name": x["material"],
                    "description": f"{x['material']} mass",
                    "type": "number",
                    "default": "None",
                    "min": 0.1,
                    "max": 1000000,
                }
                for x in materials
                if x["istimber"]
            ]
        ),
    },
    {
        "name": "c_emitted_transport_conventional",
        "category": "Conventional building materials transport",
        "display_name": "Carbon emitted transporting",
        "description": "Carbon emitted transporting materials for conventional building",
        "type": "modal",
        "default": "None",
        "unit": "kgC",
    },
    {
        "name": "timber_mineral_materials",
        "category": "Timber building",
        "display_name": "Select materials",
        "description": "Mineral-based materials used in the building",
        "type": "group",
        "default": "None",
        "fields": json.dumps(
            [
                {
                    "name": x["id"],
                    "display_name": x["material"],
                    "description": f"{x['material']} mass",
                    "type": "number",
                    "default": "None",
                    "unit": "kg",
                    "min": 0.1,
                    "max": 1000000,
                }
                for x in materials
                if not x["istimber"]
            ]
        ),
    },
    {
        "name": "timber_biomass_materials",
        "category": "Timber building",
        "display_name": "Select materials",
        "description": "Biomass-based materials used in the building",
        "type": "group",
        "default": "None",
        "fields": json.dumps(
            [
                {
                    "name": x["id"],
                    "display_name": x["material"],
                    "description": f"{x['material']} mass",
                    "type": "number",
                    "default": "None",
                    "min": 0.1,
                    "max": 1000000,
                }
                for x in materials
                if x["istimber"]
            ]
        ),
    },
    {
        "name": "c_emitted_transport_timber",
        "category": "Timber building materials transport",
        "display_name": "Carbon emitted transporting",
        "description": "Carbon emitted transporting materials for timber building",
        "type": "modal",
        "default": "None",
        "unit": "kgC",
    },
    {
        "name": "forest_c_acc_rate",
        "category": "Forest",
        "display_name": "Carbon accumulation rate",
        "description": "Carbon accumulation rate by forest type",
        "type": "populate",
        "default": "None",
        "unit": "kgC/ha/y",
        "options": json.dumps(
            [
                *[
                    {
                        "name": x["id"],
                        "display_name": x["forest"],
                        "values": [x["min"], x["best"], x["max"]],
                    }
                    for x in forests
                ],
                *[
                    {
                        "name": "other",
                        "display_name": "Other (input number)",
                        "values": "",
                    }
                ],
            ]
        ),
    },
    {
        "name": "forest_harvest_area",
        "category": "Forest",
        "display_name": "Harvested area",
        "description": "An area of forest harvested",
        "type": "number",
        "default": "None",
        "unit": "ha",
        "min": 0.01,
        "max": 1000000,
    },
    {
        "name": "forest_harvest_intensity",
        "category": "Forest",
        "display_name": "Harvesting intensity",
        "description": "An area of forest affected by harvest",
        "type": "number",
        "default": "None",
        "unit": "%",
        "min": 1,
        "max": 100,
    },
    {
        "name": "manufacturing_prefabricated_used",
        "category": "Manufacturing",
        "display_name": "Prefabricated material used",
        "description": "Proportion of prefabricated material used in construction",
        "type": "number",
        "default": "100",
        "unit": "%",
        "min": 1,
        "max": 100,
    },
    {
        "name": "manufacturing_wood_used",
        "category": "Manufacturing",
        "display_name": "Roundwood used",
        "description": "Proportion of roundwood used for material production",
        "type": "number",
        "default": "50",
        "unit": "%",
        "min": 1,
        "max": 100,
    },
]


def run(data, params, *args, **kwargs):
    """
    Make sure you have common data and output for each version of the model
    """
    # Calculate carbon storage in timber building and
    # carbon needed to be extracted from forest or demand for carbon

    # t C stored in materials before construction
    # TODO: If we allow for biomass materials in conventional building,
    # should we withdraw the c_stored_in_conventional_building from this value?
    c_stored_in_building = round(
        csfep_3s.c_stored_in_building(
            data["timber_biomass_materials"], **data, **params
        ),
        0,
    )  # kgC

    c_stored_in_materials = c_stored_in_building / (
        data["manufacturing_prefabricated_used"] * 0.01
    )

    # kgC stored in roundwood brought to the plant
    c_stored_in_roundwood = c_stored_in_materials / (
        data["manufacturing_wood_used"] * 0.01
    )

    c_needed_for_building = c_stored_in_roundwood / 0.9  # kgC stored in harested trees

    # FIXME: biomass left is 1 - harvest intensity?
    # kgC stored in scrap wood from material manufacturing and construction
    # number_of_buildings * c_stored_in_building
    c_harvest_2_scrap = c_stored_in_roundwood - c_stored_in_building
    # kgC returuned to forest
    c_harvest_2_forest = c_needed_for_building * 0.9

    # TODO Calculate time to replanish carbon debt in a forest
    years_to_regrow_forest = csfep_3s.years_to_accumulate(
        c_needed_for_building, "best", **data, **params
    )

    constants = {
        "Accumulated": 0,  # c_accum_forest
        "Buildings floor area m2": data["building_floor_area"],
        "Number of Buildings": 1,  # number_of_buildings = data["building_number"]
        "Harvested": round(c_needed_for_building / 1000, 0),
        "Years to Regrow Forest": round(years_to_regrow_forest, 0),
    }

    # RESULTS
    output = {
        "tC": {"constants": constants},
        "tCO2": {
            "constants": csfep_3s.convert_to_tco2(
                constants,
                params["c2co2"],
                [
                    "Buildings floor area m2",
                    "Number of Buildings",
                    "Years to Regrow Forest",
                ],
            )
        },
    }

    scenario_number = 1
    round_decimal = 2
    for pos, i in enumerate(["min", "best", "max"]):
        # define mineral building materials
        # define timber building material
        scoped_data = {}
        scenario_name = f"scenario_{scenario_number}"
        scenario_number = scenario_number + 1

        c_recovered_forest = csfep_3s.forest_recov(i, **data, **params)

        c_emitted_conventional = csfep_3s.emitted_manufacturing(
            i, data["conventional_biomass_materials"], **params
        ) + csfep_3s.emitted_manufacturing(
            i, data["conventional_mineral_materials"], **params
        )
        c_emitted_timber = csfep_3s.emitted_manufacturing(
            i, data["timber_biomass_materials"], **params
        ) + csfep_3s.emitted_manufacturing(
            i, data["timber_mineral_materials"], **params
        )

        # carbon substitution
        scoped_data["SC Production"] = round(
            c_emitted_conventional / 1000, round_decimal
        )
        scoped_data["SC Transport"] = round(
            data["c_emitted_transport_conventional"][pos] / 1000, round_decimal
        )

        scoped_data["MT Production"] = round(c_emitted_timber / 1000, round_decimal)
        # [0,0,0]
        scoped_data["MT Transport"] = round(
            data["c_emitted_transport_timber"][pos] / 1000, round_decimal
        )

        # carbon sink
        scoped_data["Carbon Recovered during Building Lifetime"] = round(
            c_recovered_forest / 1000, round_decimal
        )
        # carbon storage
        scoped_data["C2Scrap"] = round(c_harvest_2_scrap / 1000, round_decimal)
        scoped_data["C2Forest"] = round(c_harvest_2_forest / 1000, round_decimal)
        scoped_data["C2Buildings"] = round(c_stored_in_building / 1000, round_decimal)

        output["tC"][scenario_name] = scoped_data
        output["tCO2"][scenario_name] = csfep_3s.convert_to_tco2(
            scoped_data, params["c2co2"]
        )
    output["assumptions"] = assumptions
    return output
