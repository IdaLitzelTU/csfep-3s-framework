from framework import v3 as csfep_3s
import json
from model import get_db, cursor
import logging

logger = logging.getLogger(__name__)

if logger.hasHandlers():
    # Logger is already configured, remove all handlers
    logger.handlers = []

db = next(get_db())
materials = cursor.get_materials(db=db)
materials = [x.as_dict() for x in materials]
materials2 = cursor.get_materials2(db=db)
materials2 = [x.as_dict() for x in materials2]
forests = cursor.get_forests(db=db)
forests = [x.as_dict() for x in forests] #kg/ha/yr
energy_sources = cursor.get_energy_sources(db=db)
energy_sources = [x.as_dict() for x in energy_sources]
db.close()

meta = {
    "description": "FOREST TO CITY focusing on regional afforestation and potential development of timber economy, e.g., establish manufacturing construction materials for the afforested region",
    "version": "v3",  # version of the model
    "by": "Galina Churkina",  # author's name
    "contact": "ddi.support@dalberg.com",  # author's email address
}

cf_log = 0.5

params = {
    "cf_log": cf_log,
    "c2co2": 3.67,
    "k_truck": {"min": 0.17398, "best": 0.36024, "max": 0.55731},
    "k_sea": {"min": 0.013155, "best": 0.013155, "max": 0.013155},
    "c_material": {
        x["id"]: {
            "min_co2e": x["min_co2e"],
            "best_co2e": x["best_co2e"],
            "max_co2e": x["max_co2e"],
            "min_manuf_eec": x["min_manuf_eec"],
            "best_manuf_eec": x["best_manuf_eec"],
            "max_manuf_eec": x["max_manuf_eec"],
            "min_sourcing_eec": x["min_sourcing_eec"],
            "best_sourcing_eec": x["best_sourcing_eec"],
            "max_sourcing_eec": x["max_sourcing_eec"],
            "d_green": x["d_green"],
            "d_dry": x["d_dry"],
            "c_content": (
                x["c_content"]
                if x["c_content"] is not None
                else cf_log
                if x["is_timber"]
                else 0
            ),
            "is_timber": x["is_timber"],
        }
        for x in materials2
    },
    "c_acc_forest": {
        x["id"]: {"min": x["min"], "best": x["best"], "max": x["max"]} for x in forests
    },
}

assumptions = {
    "FOREST TO CITY": "focuses on regional afforestation and potential development of timber economy, e.g., establish manufacturing construction materials, for the afforested region.",
    "Building:": "Storage of carbon in structures is estimated for all materials containing biomass-based carbon of a structure as provided by a user.",
    "Scenarios:": "Carbon storage and emissions were estimated for three scenarios, which reflect variabilities in carbon accumulation rates in forests (min, best guess, max) and in carbon emission coefficients of construction materials (min, mean, max).",
    "Forest timber harvest:": """A part of the harvested biomass is left on site. It usually includes leaves, branches and tree tops, which are particularly nutrient rich and after decomposition provide those nutrients to the re-growing forests. Currently the default fraction of biomass converted to roundwood is 90%. This value is based on the interview results of forest rangers in Europe and may need to be adjusted for other parts of the world.
    """,
    "Manufacturing:": """Only a fraction of harvested timber goes into the constructed building and the respective carbon amounts will be stored there during the building’s lifespan. There are two major steps in manufacturing when various fractions of timber can be lost such as sawing and prefabrication of building’s parts. Here it is assumed that those timber fractions and associated carbon go into the scrap wood pool. The scrap wood can be used to produce various products from wood fiber insulation to wood chips or other biomass energy sources.
    Material substitution benefits are calculated by comparing the carbon emissions from production of conventional structure to timber structure. These emissions stem from material manufacturing and transport. Carbon emissions from manufacturing the same material can vary depending on the manufacturing technologies and energy sources. This variability was captured by using a range of values for material carbon emission coefficients where availble. """,
}
output_description = {
    "Scenarios\n": 
        "S1 uses minimum forest carbon accumulation rates, minimum material production emissions, and minimum transport emission coefficients.\n"
        "S2 uses best-guess accumulation rates, mean material production emissions, and best-guess transport emission coefficients.\n"
        "S3 uses maximum accumulation rates, maximum material production emissions, and maximum transport emission coefficients.\n",

    "Overview\n": 
        "After afforestation, the forest regrows over time and gradually accumulates carbon. "
        "Depending on the selected scenario, different carbon accumulation rates are used to estimate "
        "how much carbon is stored in the forest after the regrowth period. "
        "Part of the forest area is then harvested for timber production, while the harvesting intensity "
        "defines how much timber is actually removed from the harvested area. "
        "The model estimates how much carbon is harvested from the forest, "
        "how many timber-based buildings can be constructed, and the resulting total floor area of these buildings.",

    "Sink\n":
        "Describes the amount of carbon captured by the forest over the lifetime of the timber building. "
        "It is calculated using minimum, best-guess, or maximum accumulation rates depending on the scenario.\n"
        "• Carbon recovered in planted area: Total amount of carbon accumulated after harvest across the entire planted forest area over the building lifetime.\n"
        "• Time to replenish carbon in planted area: Time required for the planted forest area to regrow and replenish the carbon removed by harvesting.\n"
        "• Carbon recovered in harvested area: Total amount of carbon accumulated after harvest on the harvested share of the planted forest area over the building lifetime.\n"
        "• Time to replenish carbon in harvested area: Time required for the harvested area to regrow and replenish the carbon removed by harvesting.\n",

    "Substitution\n": 
        "Amount of carbon emissions avoided by using timber-based construction instead of conventional mineral-based construction. "
        "It is calculated as the difference between emissions from conventional materials and timber-based materials, "
        "including production and transport emissions.\n",

    "Storage\n": 
        "Amount of carbon stored in the timber-based building, plus carbon stored in scrap wood generated during the manufacturing process."
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
        "name": "biomass_used",
        "category": "Manufacturing",
        "display_name": "Share of biomass converted to roundwood",
        "description": "Proportion of harvested biomass converted into roundwood",
        "type": "number",
        "default": 90,
        "unit": "%",
        "min": 1,
        "max": 100,
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
        "description": "Mineral-based materials used in the timber building",
        "type": "group",
        "default": "None",
        "fields": json.dumps(
            [
                {
                    "name": x["id"],
                    "display_name": x["material"],
                    "description": f"{x['material']} mass",
                    "type": "number2",
                    "default": "None",
                    "unit": "kg",
                    "min": 0.1,
                    "max": 1000000,
                    "has_moisture_option": (
                        x["d_dry"] is not None and
                        x["d_green"] is not None
                    ),
                    "has_sourcing_option":(
                        x["min_sourcing_eec"] is not None and
                        x["best_sourcing_eec"] is not None and
                        x["max_sourcing_eec"] is not None
                    ),
                    "has_manufactoring_option":(
                        x["min_manuf_eec"] is not None and
                        x["best_manuf_eec"] is not None and
                        x["max_manuf_eec"] is not None
                    ),
                    "energy_sources": energy_sources,
                }
                for x in materials2
                if not x["is_timber"]
            ]
        ),
    },
    {
        "name": "timber_biomass_materials",
        "category": "Timber building frame",
        "display_name": "Select biomass-based materials",
        "description": "Biomass-based materials used in the timber building",
        "type": "group",
        "default": "None",
        "fields": json.dumps(
            [
                {
                    "name": x["id"],
                    "display_name": x["material"],
                    "description": f"{x['material']} mass",
                    "type": "number2",
                    "default": "None",
                    "unit": "kg",
                    "min": 0.1,
                    "max": 1000000,
                    "has_moisture_option": (
                        x["d_dry"] is not None and
                        x["d_green"] is not None
                    ),
                    "has_sourcing_option":(
                        x["min_sourcing_eec"] is not None and
                        x["best_sourcing_eec"] is not None and
                        x["max_sourcing_eec"] is not None
                    ),
                    "has_manufactoring_option":(
                        x["min_manuf_eec"] is not None and
                        x["best_manuf_eec"] is not None and
                        x["max_manuf_eec"] is not None
                    ),
                    "energy_sources": energy_sources,
                }
                for x in materials2
                if x["is_timber"]
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
        "unit": "kg",
    },
    {
        "name": "conventional_mineral_materials",
        "category": "Conventional building frame",
        "display_name": "Select mineral-based materials",
        "description": "Mineral-based materials used in the conventional building",
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
                    "has_moisture_option": (
                        x["d_dry"] is not None and
                        x["d_green"] is not None
                    ),
                    "has_sourcing_option":(
                        x["min_sourcing_eec"] is not None and
                        x["best_sourcing_eec"] is not None and
                        x["max_sourcing_eec"] is not None
                    ),
                    "has_manufactoring_option":(
                        x["min_manuf_eec"] is not None and
                        x["best_manuf_eec"] is not None and
                        x["max_manuf_eec"] is not None
                    ),
                    "energy_sources": energy_sources,
                }
                for x in materials2
                if not x["is_timber"]
            ]
        ),
    },
    {
        "name": "conventional_biomass_materials",
        "category": "Conventional building frame",
        "display_name": "Select biomass-based materials",
        "description": "Biomass-based materials used in the conventional building",
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
                    "has_moisture_option": (
                        x["d_dry"] is not None and
                        x["d_green"] is not None
                    ),
                    "has_sourcing_option":(
                        x["min_sourcing_eec"] is not None and
                        x["best_sourcing_eec"] is not None and
                        x["max_sourcing_eec"] is not None
                    ),
                    "has_manufactoring_option":(
                        x["min_manuf_eec"] is not None and
                        x["best_manuf_eec"] is not None and
                        x["max_manuf_eec"] is not None
                    ),
                    "energy_sources": energy_sources,
                }
                
                for x in materials2
                if x["is_timber"]
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
        "unit": "kg",
    },
]


def run(data, params, *args, **kwargs):
    # kg C stored in all materials in the timber construction (dry)
    # kg C stored in all materials in the timber construction (dry)
    c_stored_in_building = csfep_3s.c_stored_in_building(
            data["timber_biomass_materials"], **data, **params)# kgC 
    + csfep_3s.c_stored_in_building(
            data["timber_mineral_materials"], **data, **params)# kgC

   # calculate c needed in:  building <- materials <- roundwood <- forest
    c_stored_in_materials = c_stored_in_building  / (data["manufacturing_prefabricated_used"] * 0.01)
    c_stored_in_roundwood = c_stored_in_materials / (data["manufacturing_wood_used"] * 0.01)
    c_needed_for_building = c_stored_in_roundwood / (data["biomass_used"]*0.01)  # kgC stored in harvested trees

    # calculate scrap wood for one building
    (scrap_roundwood, scrap_material) = csfep_3s.calculate_scrap(
        c_needed_for_building,
        c_stored_in_roundwood,
        c_stored_in_materials, 
        c_stored_in_building)
    
    c_stored_in_scrap = scrap_roundwood + scrap_material #kgC


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

        ## Sink
        # How much carbon accumulated in the forest_harvested_area in the forest_regrow_time?
        c_accumulated_in_forest = csfep_3s.carbon_accumulated_in_forest(
            scenario, data["forest_harvest_area"], **data, **params
        )

        # How much carbon is harvested from forest_harvested_area given harvest intensity
        c_harvested = csfep_3s.c_harvested_from_forest(
            c_accumulated_in_forest, **data, **params
        )

        # How much time it will it take to regrow carbon in forest_harvest_area
        years_to_regrow_forest = csfep_3s.years_to_accumulate(
            scenario, data["forest_harvest_area"], c_harvested, **data, **params
        )

        # How much time it will it take to regrow carbon in forest_planted_area
        years_to_regrow_plant_forest = csfep_3s.years_to_accumulate(
            scenario, data["forest_plant_area"], c_harvested, **data, **params
        )

        # How much carbon will be recovered in the forest given lifespann of the building?
        c_recovered_in_forest = csfep_3s.c_recovered_in_forest_over_building_lifetime(
            scenario, data["forest_harvest_area"], **data, **params
        )

        # How much carbon will be recovered in the forest given lifespann of the building?
        c_recovered_in_plant_forest = csfep_3s.c_recovered_in_forest_over_building_lifetime(
            scenario, data["forest_plant_area"], **data, **params
        )

        # How many buildings can be built given carbon harvested?
        number_of_building_possible = c_harvested  // c_needed_for_building

        # What is the total building area?
        total_building_area = (
            number_of_building_possible * data["timber_building_floor_area"]
        )

        # Total carbon stored in all buildings
        total_c_in_building = number_of_building_possible * c_stored_in_building


        ## Substitution
        # conventional
        c_emitted_conventional_manufacturing = (csfep_3s.emitted_manufacturing(
            scenario, data["conventional_biomass_materials"], energy_sources, **params
        ) + csfep_3s.emitted_manufacturing(
            scenario, data["conventional_mineral_materials"],energy_sources, **params
        ) ) * number_of_building_possible

        c_emitted_conventional_transporting = (
            data["c_emitted_transport_conventional"][
                csfep_3s.get_scenario_index(scenario)
            ]
            * number_of_building_possible
        )
        # timber based
        c_emitted_timber_manufacturing = (csfep_3s.emitted_manufacturing(
            scenario, data["timber_biomass_materials"], energy_sources, **params
        ) + csfep_3s.emitted_manufacturing(
            scenario, data["timber_mineral_materials"], energy_sources, **params
        ) ) * number_of_building_possible

        print("c timber:",c_emitted_timber_manufacturing)

        c_emitted_timber_transporting = (
            data["c_emitted_transport_timber"][csfep_3s.get_scenario_index(scenario)]
            * number_of_building_possible
        )

        scoped_data["c_accumulated"] = c_accumulated_in_forest
        scoped_data["c_harvested"] = c_harvested 
        scoped_data["c_recovered"] = c_recovered_in_forest
        scoped_data["c_recovered_plant"] = c_recovered_in_plant_forest
        scoped_data["c_lost"] = c_stored_in_scrap * number_of_building_possible
        scoped_data["c_in_building"] = total_c_in_building
        scoped_data["years_to_regrow_forest"] = years_to_regrow_forest
        scoped_data["years_to_regrow_plant_forest"] = years_to_regrow_plant_forest
        scoped_data["building_area"] = total_building_area
        scoped_data["number_of_buildings"] = number_of_building_possible
        scoped_data["conventional_manufacturing"] = c_emitted_conventional_manufacturing
        scoped_data["conventional_transporting"] = c_emitted_conventional_transporting
        scoped_data["timber_manufacturing"] = c_emitted_timber_manufacturing
        scoped_data["timber_transporting"] = c_emitted_timber_transporting
        scoped_data = csfep_3s.convert(
            scoped_data,
            1 / 1000,
            obsolve=["years_to_regrow_forest", "years_to_regrow_plant_forest", "number_of_buildings", "building_area"], #converted into tC
        )

        scoped_data = csfep_3s.round_all(scoped_data, round_decimal)

        output["tC"][scenario_name] = scoped_data
        scoped_data_in_co2 = csfep_3s.convert(
            scoped_data,
            params["c2co2"],
            obsolve=["years_to_regrow_forest","years_to_regrow_plant_forest", "number_of_buildings", "building_area"],
        )
        scoped_data_in_co2 = csfep_3s.round_all(scoped_data_in_co2, round_decimal)
        output["tCO2"][scenario_name] = scoped_data_in_co2
    output["assumptions"] = assumptions
    output["output_description"] = output_description
    return output
