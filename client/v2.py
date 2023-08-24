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
    "k_truck": {"min": 0.00017398, "best": 0.00036024, "max": 0.00055731}, # should it be * 1000 since it's kilos not tonns?
    "k_sea": {"min": 0.000013155, "best": 0.000013155, "max": 0.000013155}, # should it be * 1000 since it's kilos not tonns?
    "c_material": {x["id"]: {"min": x["min"], "best": x["best"], "max": x["max"], "istimber": x["istimber"]} for x in materials},
    "c_acc_forest": {x["id"]: {"min": x["min"], "best": x["best"], "max": x["max"]} for x in forests},
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
        "name": "mineral_based_materials",
        "category": "Mineral based building materials",
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
        "name": "mineral_based_transport_land",
        "category": "Mineral based building transport",
        "display_name": "Land transport distance (km)",
        "description": "Land transport distance in kilometers",
        "type": "number",
        "default": "None",
    },
    {
        "name": "mineral_based_transport_water",
        "category": "Mineral based building transport",
        "display_name": "Water transport distance (km)",
        "description": "Water transport distance in kilometers",
        "type": "number",
        "default": "None",
    },
    {
        "name": "timber_materials",
        "category": "Biomass based / Timber building materials",
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
        "name": "timber_transport_land",
        "category": "Biomass based / Timber building transport",
        "display_name": "Land transport distance (km)",
        "description": "Land transport distance in kilometers",
        "type": "number",
        "default": "None",
    },
    {
        "name": "timber_transport_water",
        "category": "Biomass based / Timber building transport",
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
        "type": "array",
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
    c_stored_in_building = round(csfep_3s.c_stored_in_building(
        data["timber_materials"], **data, **params
    ), 0)  # kgC

    mineral_based_building_mass = csfep_3s.total_mass(
        data["mineral_based_materials"]
    )  # KG
    timber_building_mass = csfep_3s.total_mass(
        data["timber_materials"]
    )  # KG
    c_stored_in_materials = c_stored_in_building / (data["manufacturing_prefabricated_used"] * 0.01)
    
    # kgC stored in roundwood brought to the plant
    c_stored_in_roundwood = c_stored_in_materials / (data["manufacturing_wood_used"] * 0.01)
    

    c_needed_for_building = c_stored_in_roundwood / (1 - (data["forest_biomass_left"] * 0.01))  # kgC stored in harested trees
    
    # FIXME: biomass left is 1 - harvest intensity?
    # kgC stored in scrap wood from material manufacturing and construction
    c_harvest_2_scrap = c_stored_in_roundwood - c_stored_in_building # number_of_buildings * c_stored_in_building
    c_harvest_2_forest = c_needed_for_building * data["forest_biomass_left"] * 0.01 # kgC returuned to forest

    # TODO Calculate time to replanish carbon debt in a forest
    years_to_regrow_forest = csfep_3s.years_to_accumulate(
        c_needed_for_building, "best", **data, **params
    ) 

    constants = {
        "Accumulated": 0, # c_accum_forest
        "Buildings floor area m2": data["building_floor_area"],
        "Number of Buildings": 1, #     number_of_buildings = data["building_number"]
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
    for i in ["min", "best", "max"]:
        ## define mineral building materials
        ## define timber building material
        scoped_data = {}
        scenario_name = f"scenario_{scenario_number}"
        scenario_number = scenario_number + 1

        c_recovered_forest = csfep_3s.forest_recov(i, **data, **params)

        c_emitted_mineral = csfep_3s.emitted_manufacturing(
            i, data["mineral_based_materials"], **params
        )

        c_emitted_timber = csfep_3s.emitted_manufacturing(
            i, data["timber_materials"], **params
        )
        # convert mass to tonn
        c_emitted_transport_mineral = csfep_3s.emitted_transporting(
            mineral_based_building_mass / 1000,
            data["mineral_based_transport_land"],
            params["k_truck"][i],
            **params,
        ) + csfep_3s.emitted_transporting(
            mineral_based_building_mass / 1000,
            data["mineral_based_transport_water"],
            params["k_sea"][i],
            **params,
        )

        c_emitted_transport_timber = csfep_3s.emitted_transporting(
            timber_building_mass / 1000,
            data["timber_transport_land"],
            params["k_truck"][i],
            **params,
        ) + csfep_3s.emitted_transporting(
            timber_building_mass / 1000,
            data["timber_transport_water"],
            params["k_sea"][i],
            **params,
        )
        #carbon substitution
        scoped_data["SC Production"] = round(c_emitted_mineral / 1000, round_decimal)
        scoped_data["SC Transport"] = round(c_emitted_transport_mineral, round_decimal)
        
        scoped_data["MT Production"] = round(c_emitted_timber / 1000, round_decimal)
        scoped_data["MT Transport"] = round(c_emitted_transport_timber, round_decimal)
        
        
        #carbon sink
        scoped_data["Carbon Recovered during Building Lifetime"] = round(c_recovered_forest / 1000, round_decimal)
        #carbon storage
        scoped_data["C2Scrap"] = round(c_harvest_2_scrap / 1000, round_decimal)
        scoped_data["C2Forest"] = round(c_harvest_2_forest / 1000, round_decimal)
        scoped_data["C2Buildings"] = round(c_stored_in_building / 1000, round_decimal)

        output["tC"][scenario_name] = scoped_data
        output["tCO2"][scenario_name] = csfep_3s.convert_to_tco2(
            scoped_data, params["c2co2"]
        )
    output["assumptions"] = assumptions
    return output