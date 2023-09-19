import logging

logger = logging.getLogger(__name__)


# System housekeeping

if logger.hasHandlers():
    # Logger is already configured, remove all handlers
    logger.handlers = []


# Utility functions


def get_scenario_index(scenario):
    index = {"min": 0, "best": 1, "max": 2}
    return index[scenario]


def convert(object, coefficient, obsolve=[]):
    out = {}
    for key, value in object.items():
        try:
            if key not in obsolve and not isinstance(value, dict):
                out[key] = value * coefficient
            elif isinstance(value, dict):
                out[key] = convert(value, coefficient, obsolve)
            else:
                out[key] = value
        except Exception as e:
            logger.exception(e)
            out[key] = 0
    return out


def round_all(object, decimal, obsolve=[]):
    out = {}
    for key, value in object.items():
        try:
            if key not in obsolve and not isinstance(value, dict):
                out[key] = round(value, decimal)
            elif isinstance(value, dict):
                out[key] = convert(value, decimal, obsolve)
            else:
                out[key] = value
        except Exception as e:
            logger.exception(e)
            out[key] = 0
    return out


def to_coef(x):
    return x / 100


def total_mass(materials):
    try:
        total_m = sum(materials.values())
        logger.info(f"Total building mass: {total_m} tC")
        return total_m
    except Exception as e:
        logger.exception(e)


# Framework (in order of apperance)


def c_stored_in_building(materials, *, cf_log, c_material, **kwargs):
    """
    This function calculates amount of carbon stored in a building and
    amount of wood to be harvested for this building [t C]
    """

    try:
        total = 0
        for id, value in materials.items():  # materials is { concrete: value }
            if c_material.get(id, {"istimber": False}).get("istimber"):
                total = total + value
        total = total * cf_log
        logger.info(f"Building carbon stored: {total} kgC")
        return total
    except Exception as e:
        logger.exception(e)


def c_needed_for_building(
    c_stored_in_building,
    *,
    manufacturing_wood_used,
    manufacturing_prefabricated_used,
    **kwargs,
):
    """This function calculates wood needed to build timber building"""
    # tonne of C total amount of carbon needed to build building including processing losses
    try:
        w = (
            c_stored_in_building
            / to_coef(manufacturing_wood_used)
            / to_coef(manufacturing_prefabricated_used)
        )
        logger.info(f" Wood demand: {w}")
        return w
    except Exception as e:
        logger.exception(e)


def carbon_accumulated_in_forest_per_year(
    scenario,
    area,
    *,
    forest_c_acc_rate,
    **kwargs,
):
    try:
        c_acc_rate = forest_c_acc_rate[get_scenario_index(scenario)]
        c_acc = c_acc_rate * area
        return c_acc
    except Exception as e:
        logger.exception(e)
        return 0


def carbon_accumulated_in_forest(scenario, area, *, forest_regrow_time, **kwargs):
    """
    This function calculates amount of carbon accumulated in the forest with
    area areaPlanted during a given period yrForest
    """
    try:
        return (
            carbon_accumulated_in_forest_per_year(scenario, area, **kwargs)
            * forest_regrow_time
        )
    except Exception as e:
        logger.exception(e)
        return 0


def c_harvested_from_forest(
    c_accumulated_in_forest,
    *,
    forest_harvest_intensity,
    forest_harvest_area,
    forest_plant_area,
    **kwargs,
):
    """
    carbon harvested with harvest intensity cfHarvest from a subsection
    """
    try:
        return (
            c_accumulated_in_forest
            * to_coef(forest_harvest_intensity)
            * (forest_harvest_area / forest_plant_area)
        )
    except Exception as e:
        logger.exception(e)
        return 0


def years_to_accumulate(
    scenario,
    area,
    carbon_harv,  # should be in tonnes?
    **kwargs,
):
    """
    This function calculates number of years needed to accumulate harvested carbon
    using average carbon accumulation rate of a forest from the Cook-Paton
    database
    """
    try:
        # change harvest intensity to fraction
        yr = carbon_harv / carbon_accumulated_in_forest_per_year(
            scenario, area, **kwargs
        )
        logger.info(
            f"Number of years needed to accumulate harvested carbon using average carbon accumulation rate of a forest from the Cook-Paton database: {yr}"
        )
        return yr
    except Exception as e:
        logger.exception(e)
        return 0


def c_recovered_in_forest_over_building_lifetime(
    scenario,
    area,
    *,
    timber_building_lifespan,
    **kwargs,
):
    """
    This function calculates amount of carbon recovered in the forest during the life time
    of a building
    """
    try:
        # tCO2/ha/y * ha = tCO2/y
        cr = (
            carbon_accumulated_in_forest_per_year(scenario, area, **kwargs)
            * timber_building_lifespan
        )
        logger.info(
            f"Amount of carbon recovered in the forest during the life time of a building: {cr}"
        )
        return cr
    except Exception as e:
        logger.exception(e)


def emitted_manufacturing(scenario, materials, *, c_material, c2co2, **kwargs):
    """
    This function calculates amount of carbon stored in a building and
    amount of wood to be harvested for this building [t C]
    """
    try:
        total = 0
        for key, mass in materials.items():
            co2_in_material = c_material[key]  # co2/kg
            # kgco2/kg * kg = kgco2
            # before: m2 * tCo2 / m2 => tCo2 now: kg, kgCo2/kg -> kg * kgCo2 / kg => kgCo2 / 1000 -> tCo2
            total = total + (co2_in_material[scenario] * mass)
        logger.info(f"Building carbon stored: {total} kgC")
        return total / c2co2
    except Exception as e:
        logger.exception(e)


def emitted_transporting(mass, distance, coeff, *, c2co2, **kwargs):
    try:
        # m -> t * Km * (kg * C02) / t*km / c02/c
        c_emitted = ((mass / 1000) * distance * coeff) / c2co2
        logger.info(
            f"Carbon emissions during transport stage of construction materials [tC] assuming all emissions are CO2: {c_emitted}"
        )
        return c_emitted
    except Exception as e:
        logger.exception(e)
