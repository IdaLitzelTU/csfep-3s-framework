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

meta = {"version": "2", "by": "Galina Churkina", "contact": "some.name@mail.com"}

params = {
    "cf_log": 0.5,
    "c2co2": 3.67,
    # TODO: move transport to BD?
    "k_truck": {"min": 0.00017398, "best": 0.00036024, "max": 0.00055731},
    "k_sea": {"min": 0.000013155, "best": 0.000013155, "max": 0.000013155},
    "c_material": {x["id"]: [x["min"], x["best"], x["max"]] for x in materials},
    "c_acc_forest": {x["id"]: [x["min"], x["best"], x["max"]] for x in forests},
}

assumptions = {
    "Timber scrap": "is included in Storage",
    "Timber reintroduced to the forest": "is included in Storage",
    "Transport emmission carbon benefit": "is included in Substitution",
    "Total carbon benefit": "is a sum of Sink and Substitution",
    "V2": "This model allows for more detailed material selection of both buildings",
}

input = [
    {
        "name": "building_floor_area",
        "category": "Building",
        "display_name": "Total floor area (m2)",
        "description": "The floor area in squared meters",
        "type": "number",
        "default": "None",
    },
    # {
    #     "name": "building_number",
    #     "category": "Building",
    #     "display_name": "Number of buildings (units)",
    #     "description": "Number of buildings built",
    #     "type": "number",
    #     "default": "None",
    # },
    {
        "name": "building_lifespan",
        "category": "Building",
        "display_name": "Expected life span of the building (years)",
        "description": "The expected life span of the building in years",
        "type": "number",
        "default": "None",
    },
    {
        "name": "conventional_materials",
        "category": "Conventional building materials",
        "display_name": "Select materials",
        "description": "Materials used in the building",
        "type": "group",
        "default": "None",
        "fields": json.dumps(
            [
                {
                    "name": x["id"],
                    "display_name": x["material"],
                    "description": f"{x['material']} quantity (kg)",
                    "type": "number",
                    "default": "None",
                }
                for x in materials
            ]
        ),
    },
    {
        "name": "conventional_transport_land",
        "category": "Conventional building transport",
        "display_name": "Land transport distance (km)",
        "description": "Land transport distance in kilometers",
        "type": "number",
        "default": "None",
    },
    {
        "name": "conventional_transport_water",
        "category": "Conventional building transport",
        "display_name": "Water transport distance (km)",
        "description": "Water transport distance in kilometers",
        "type": "number",
        "default": "None",
    },
    {
        "name": "substitution_materials",
        "category": "Timber building materials",
        "display_name": "Select materials",
        "description": "Materials used in the building",
        "type": "group",
        "default": "None",
        "fields": json.dumps(
            [
                {
                    "name": x["id"],
                    "display_name": x["material"],
                    "description": f"{x['material']} quantity (kg)",
                    "type": "number",
                    "default": "None",
                }
                for x in materials
            ]
        ),
    },
    {
        "name": "substitution_transport_land",
        "category": "Timber building transport",
        "display_name": "Land transport distance (km)",
        "description": "Land transport distance in kilometers",
        "type": "number",
        "default": "None",
    },
    {
        "name": "substitution_transport_water",
        "category": "Timber building transport",
        "display_name": "Water transport distance (km)",
        "description": "Water transport distance in kilometers",
        "type": "number",
        "default": "None",
    },
    {
        "name": "forest_type",
        "category": "Forest",
        "display_name": "Select forest type",
        "description": "Forest type",
        "type": "select",
        "default": "None",
        "options": json.dumps(
            [
                *[
                    {
                        "name": x["id"],
                        "display_name": x["forest"],
                    }
                    for x in forests
                ],
                *[{"name": "other", "display_name": "Other (input number)"}],
            ]
        ),
    },
    {
        "name": "forest_c_acc_rate",
        "category": "Forest",
        "display_name": "Carbon accumulation rate (tC/ha/y)",
        "description": "Carbon accumulation rate (min, best_guess, max) (comma separated) (leave blank for default value based on the forest type selected)",
        "type": "array[number]",
        "default": "None",
    },
    {
        "name": "forest_harvest_area",
        "category": "Forest",
        "display_name": "Harvested area (ha)",
        "description": "An area of forest harvested in hectares",
        "type": "number",
        "default": "None",
    },
    {
        "name": "forest_harvest_intensity",
        "category": "Forest",
        "display_name": "Harvest intensity (%)",
        "description": "An area of forest affected by harvest",
        "type": "number",
        "default": "None",
    },
    {
        "name": "forest_biomass_left",
        "category": "Forest",
        "display_name": "Harvested biomass left on site (%)",
        "description": "Proportion of harvested biomass left on site to provide nutrients for regeneration",
        "type": "number",
        "default": "10",
    },
    {
        "name": "manufacturing_prefabricated_used",
        "category": "Manufacturing",
        "display_name": "Prefabricated material used (%)",
        "description": "Proportion of prefabricated material used in construction",
        "type": "number",
        "default": "100",
    },
    {
        "name": "manufacturing_wood_used",
        "category": "Manufacturing",
        "display_name": "Roundwood used (%)",
        "description": "Proportion of roundwood used for material production",
        "type": "number",
        "default": "50",
    },
]


def run(data, params, *args, **kwargs):
    """
    Make sure you have common data and output for each version of the model
    """

    # Calculate carbon storage in timber building and
    # carbon needed to be extracted from forest or demand for carbon

    # t C stored in materials before construction
    c_stored_in_building = csfep_3s.c_stored_in_building(
        data["substitution_materials"], **data, **params
    )  # KgC

    conventional_building_mass = csfep_3s.total_mass(
        data["conventional_materials"]
    )  # KG
    substitution_building_mass = csfep_3s.total_mass(
        data["substitution_materials"]
    )  # KG

    c_stored_in_materials = c_stored_in_building / (
        data["manufacturing_prefabricated_used"] / 100
    )
    # tC stored in roundwood brought to the plant
    c_stored_in_roundwood = c_stored_in_materials / (
        data["manufacturing_wood_used"] / 100
    )

    c_needed_for_building = c_stored_in_roundwood / (
        1 - data["forest_biomass_left"] / 100
    )  # tC stored in harested trees

    # c_accum_forest = 0
    # number_of_buildings = data[
    #     "building_number"
    # ]  # number of buildings to be built from harvested wood

    # # tCstored in buildings constructed from harvested wood
    # c_buildings = number_of_buildings * c_stored_in_building

    # FIXME: biomass left is 1 - harvest intensity?
    # tC stored in scrap wood from material manufacturing and construction
    c_harvest_2_scrap = c_stored_in_roundwood - c_stored_in_building
    c_harvest_2_forest = (
        c_needed_for_building * data["forest_biomass_left"] / 100
    )  # tC returuned to forest

    # Calculate time to replanish carbon debt in a forest
    # changed index as python starts from 0 not 1
    years_to_regrow_forest = csfep_3s.years_to_accumulate(
        c_needed_for_building, "best", **data, **params
    )

    constants = {
        "Accumulated": 0,
        "Buildings floor area m2": data["building_floor_area"],
        "Number of Buildings": 1,
        "Harvested": c_needed_for_building,
        "Years to Regrow Forest": years_to_regrow_forest,
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

    for i in ["min", "best", "max"]:
        ## define conventional building materials
        ## define timber building material
        scoped_data = {}
        scenario_number = 1
        scenario_name = f"scenario_{scenario_number}"
        scenario_number = scenario_number + 1

        c_recovered_forest = csfep_3s.forest_recov(i, **data, **params)

        c_emitted_conventional = csfep_3s.emitted_manufacturing(
            i, data["conventional_materials"], **params
        )

        c_emitted_substitution = csfep_3s.emitted_manufacturing(
            i, data["substitution_materials"], **params
        )

        c_emitted_transport_conventional = csfep_3s.emitted_transporting(
            conventional_building_mass,
            data["conventional_transport_land"],
            params["k_truck"][i],
            **params,
        ) + csfep_3s.emitted_transporting(
            conventional_building_mass,
            data["conventional_transport_water"],
            params["k_sea"][i],
            **params,
        )

        c_emitted_transport_substitution = csfep_3s.emitted_transporting(
            substitution_building_mass,
            data["substitution_transport_land"],
            params["k_truck"][i],
            **params,
        ) + csfep_3s.emitted_transporting(
            substitution_building_mass,
            data["substitution_transport_water"],
            params["k_sea"][i],
            **params,
        )

        scoped_data["conventional"] = {
            "production": c_emitted_conventional,
            "transport": c_emitted_transport_conventional,
        }
        scoped_data["substitution"] = {
            "production": c_emitted_substitution,
            "transport": c_emitted_transport_substitution,
        }

        scoped_data["recovered"] = c_recovered_forest

        scoped_data["C2Scrap"] = c_harvest_2_scrap
        scoped_data["C2Forest"] = c_harvest_2_forest
        scoped_data["C2Buildings"] = c_stored_in_building

        output["tC"][scenario_name] = scoped_data
        output["tCO2"][scenario_name] = csfep_3s.convert_to_tco2(
            scoped_data, params["c2co2"]
        )

    output["assumptions"] = assumptions
    return output
