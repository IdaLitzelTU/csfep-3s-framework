from framework import v3 as csfep_3s
import json
from model import get_db, cursor

db = next(get_db())
materials = cursor.get_materials(db=db)
materials = [x.as_dict() for x in materials]
forests = cursor.get_forests(db=db)
forests = [x.as_dict() for x in forests]
db.close()

meta = {
    "description": "v3 of the model is the 'Forest to City' version, focusing on regional afforestation and potential development of timber economy, e.g., establish manufacturing construction materials for the afforested region",
    "version": "v3",  # version of the model
    "by": "Galina Churkina",  # author's name
    "contact": "ddi.support@dalberg.com",  # author's email address
}

params = {
    "cf_log": 0.5,
    "c2co2": 3.67,
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
    "V3 (FOREST2CITY)": "focuses on regional afforestation and potential development of timber economy, e.g., establish manufacturing construction materials, for the afforested region.",
    "Building:": "Storage of carbon in structures is estimated for all materials containing biomass-based carbon of a structure as provided by a user.",
    "Scenarios:": """
    Carbon storage and emissions were estimated for three scenarios, which reflect variabilities in carbon accumulation 
    rates in forests (min, best guess, max) and in carbon emission coefficients of construction materials (min, mean, max).
    """,
    "Forest timber harvest:": """A part of the harvested biomass is left on site. It usually includes leaves, branches and tree tops, 
    which are particularly nutrient rich and after decomposition provide those nutrients to the re-growing forests. 
    Currently the default fraction of harvested biomass left on site is 10%. This value is based on the interview results of forest rangers in Europe and may need to be adjusted for other parts of the world.
    """,
    "Manufacturing:": """Only a fraction of harvested timber goes into the constructed building and the respective carbon amounts will be stored there during the building’s lifespan. 
    There are two major steps in manufacturing when various fractions of timber can be lost such as sawing and prefabrication of building’s parts. Here it is assumed that those timber fractions and associated carbon go into the scrap wood pool. 
    The scrap wood can be used to produce various products from wood fiber insolation to wood chips or other biomass energy sources.
    Material substitution benefits are calculated by comparing the carbon emissions from production of conventional structure to timber structure. These emissions stem from material manufacturing and transport. 
    Carbon emissions from manufacturing the same material can vary depending on the manufacturing technologies and energy sources. 
    This variability was captured by using a range of values for material carbon emission coefficients where availble. """,
}
output_description = {
    "V2 (CITY) ": "focuses on building specific infrastructures such as building, bridge, etc. from timber.",
}

# Planted forest area’ [ha] and ‘Forest regrow time’ [years].
input = [
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
        "name": "forest_plant_area",
        "category": "Forest",
        "display_name": "Planted forest area",
        "description": "Area planted with forest",
        "type": "number",
        "default": "None",
        "unit": "ha",
    },
    {
        "name": "forest_regrow_time",
        "category": "Forest",
        "display_name": "Forest regrow time",
        "description": "Time it takes for forest to regrow",
        "type": "number",
        "default": "None",
        "unit": "years",
    },
    {
        "name": "forest_harvest_area",
        "category": "Forest",
        "display_name": "Harvested area",
        "description": "An area of forest harvested",
        "type": "number",
        "default": "None",
        "unit": "ha",
    },
    {
        "name": "forest_harvest_intensity",
        "category": "Forest",
        "display_name": "Harvesting intensity",
        "description": "An area of forest affected by harvest",
        "type": "number",
        "default": "None",
        "unit": "%",
    },
    {
        "name": "manufacturing_wood_used",
        "category": "Manufacturing",
        "display_name": "Share of roundwood used",
        "description": "Proportion of harvested roundwood used for timber material production",
        "type": "number",
        "default": "50",
        "unit": "%",
        "min": 1,
        "max": 100,
    },
    {
        "name": "manufacturing_prefabricated_used",
        "category": "Manufacturing",
        "display_name": "Share of prefabricated material used",
        "description": "Proportion of prefabricated timber material used in the building construction",
        "type": "number",
        "default": "100",
        "unit": "%",
        "min": 1,
        "max": 100,
    },
    {
        "name": "timber_building_floor_area",
        "category": "Timber building frame",
        "display_name": "Total floor area",
        "description": "The floor area",
        "type": "number",
        "default": "None",
        "unit": "m2",
    },
    {
        "name": "timber_building_lifespan",
        "category": "Timber building frame",
        "display_name": "Expected life span of the building",
        "description": "The expected life span of the building",
        "type": "number",
        "default": "None",
        "unit": "years",
    },
    {
        "name": "timber_mineral_materials",
        "category": "Timber building frame",
        "display_name": "Select mineral-based materials",
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
                }
                for x in materials
                if not x["istimber"]
            ]
        ),
    },
    {
        "name": "timber_biomass_materials",
        "category": "Timber building frame",
        "display_name": "Select biomass-based materials",
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
                    "unit": "kg",
                }
                for x in materials
                if x["istimber"]
            ]
        ),
    },
    {
        "name": "c_emitted_transport_timber",
        "category": "Timber building transport",
        "display_name": "Carbon emitted transporting",
        "description": "Carbon emitted transporting materials for timber building",
        "type": "modal",
        "default": "None",
        "unit": "km",
    },
    {
        "name": "conventional_mineral_materials",
        "category": "Conventional building frame",
        "display_name": "Select mineral-based materials",
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
                }
                for x in materials
                if not x["istimber"]
            ]
        ),
    },
    {
        "name": "conventional_biomass_materials",
        "category": "Conventional building frame",
        "display_name": "Select biomass-based materials",
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
                    "unit": "kg",
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
        "unit": "km",
    },
]


def run(data, params, *args, **kwargs):
    # How much carbon required per building?
    c_stored_in_building = csfep_3s.c_stored_in_building(
        data["timber_biomass_materials"], **data, **params
    )

    # How much carbon we need to harvest assuming loss in manufacturing?
    c_needed_for_building = csfep_3s.c_needed_for_building(
        c_stored_in_building, **data, **params
    )

    # RESULTS
    output = {
        "tC": {},
        "tCO2": {},
    }

    scenario_number = 1
    round_decimal = 2
    for scenario in ["min", "best", "max"]:
        scoped_data = {}
        scenario_name = f"scenario_{scenario_number}"
        scenario_number = scenario_number + 1

        # How much carbon is generated on site harversed over the years that
        # the forest growing?
        c_accumulated_in_forest = csfep_3s.carbon_accumulated_in_forest(
            scenario, data["forest_plant_area"], **data, **params
        )

        # How much carbon is harvested from forest given harvest intencity
        c_harvested = csfep_3s.c_harvested_from_forest(
            c_accumulated_in_forest, **data, **params
        )

        # How much time it will take to regrow carbon in the forest?
        years_to_regrow_forest = csfep_3s.years_to_accumulate(
            scenario, data["forest_harvest_area"], c_harvested, **data, **params
        )

        # How much carbon will be recovered in the forest given lifespawn of the building?
        c_recovered_in_forest = csfep_3s.c_recovered_in_forest_over_building_lifetime(
            scenario, data["forest_harvest_area"], **data, **params
        )

        # How many buildings can be built given carbon harvested?
        number_of_building_possible = (c_harvested * 0.9) // c_needed_for_building

        # What is the total building area?
        total_building_area = (
            number_of_building_possible * data["timber_building_floor_area"]
        )

        # Total carbon stored in all buildings
        total_c_in_building = number_of_building_possible * c_stored_in_building

        # Scrap/waste not used in production
        c_in_scrap = (c_harvested * 0.9) - total_c_in_building

        c_emitted_conventional_manufacturing = (
            csfep_3s.emitted_manufacturing(
                scenario, data["conventional_biomass_materials"], **params
            )
            + csfep_3s.emitted_manufacturing(
                scenario, data["conventional_mineral_materials"], **params
            )
        ) * number_of_building_possible

        c_emitted_conventional_transporting = (
            data["c_emitted_transport_conventional"][
                csfep_3s.get_scenario_index(scenario)
            ]
            * number_of_building_possible
        )

        c_emitted_timber_manufacturing = (
            csfep_3s.emitted_manufacturing(
                scenario, data["timber_biomass_materials"], **params
            )
            + csfep_3s.emitted_manufacturing(
                scenario, data["timber_mineral_materials"], **params
            )
        ) * number_of_building_possible

        c_emitted_timber_transporting = (
            data["c_emitted_transport_timber"][csfep_3s.get_scenario_index(scenario)]
            * number_of_building_possible
        )

        scoped_data["c_accumulated"] = c_accumulated_in_forest
        scoped_data["c_harvested"] = c_harvested * 0.9
        scoped_data["c_recovered"] = c_recovered_in_forest
        scoped_data["c_forest"] = c_harvested * 0.1
        scoped_data["c_lost"] = c_in_scrap
        scoped_data["c_in_building"] = total_c_in_building
        scoped_data["years_to_regrow_forest"] = years_to_regrow_forest
        scoped_data["building_area"] = total_building_area
        scoped_data["number_of_buildings"] = number_of_building_possible
        scoped_data["conventional_manufacturing"] = c_emitted_conventional_manufacturing
        scoped_data["conventional_transporting"] = c_emitted_conventional_transporting
        scoped_data["timber_manufacturing"] = c_emitted_timber_manufacturing
        scoped_data["timber_transporting"] = c_emitted_timber_transporting
        scoped_data = csfep_3s.convert(
            scoped_data,
            1 / 1000,
            obsolve=["years_to_regrow_forest", "number_of_buildings", "building_area"],
        )

        scoped_data = csfep_3s.round_all(scoped_data, round_decimal)

        output["tC"][scenario_name] = scoped_data
        scoped_data_in_co2 = csfep_3s.convert(
            scoped_data,
            params["c2co2"],
            obsolve=["years_to_regrow_forest", "number_of_buildings", "building_area"],
        )
        scoped_data_in_co2 = csfep_3s.round_all(scoped_data_in_co2, round_decimal)
        output["tCO2"][scenario_name] = scoped_data_in_co2
    output["assumptions"] = assumptions
    output["output_description"] = output_description
    return output
