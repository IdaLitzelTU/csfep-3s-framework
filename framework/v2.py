import logging

logger = logging.getLogger(__name__)

if logger.hasHandlers():
    # Logger is already configured, remove all handlers
    logger.handlers = []


## Build a class Building
## Build a class Forest

def calculate_scrap(c_needed_for_building, c_stored_in_roundwood, c_stored_in_materials, c_stored_in_building):
    try:
        scrap_roundwood = (
            c_stored_in_roundwood
            - c_stored_in_materials
        )
        scrap_material = (
            c_stored_in_materials
            - c_stored_in_building
        )
        logger.info(f"c_needed_for_building: {c_needed_for_building}")
        logger.info(f"c_stored_in_roundwood: {c_stored_in_roundwood}")
        logger.info(f"c_stored_in_materials: {c_stored_in_materials}")
        logger.info(f"c_stored_in_building: {c_stored_in_building} in kgC")
        logger.info(f"scrap_roundwood: {scrap_roundwood}")
        logger.info(f"scrap_material: {scrap_material}")
        return (
            scrap_roundwood,
            scrap_material,
        )
    except Exception as e:
        logger.exception(e)


def convert_to_tco2(object, coefficient, obsolve=[]):
    out = {}
    for key, value in object.items():
        if key not in obsolve and not isinstance(value, dict):
            out[key] = value * coefficient
        elif isinstance(value, dict):
            out[key] = convert_to_tco2(value, coefficient, obsolve)
        else:
            out[key] = value
    return out


def to_coef(x):
    return x / 100


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


def total_mass(materials):
    try:
        total_m = sum(materials.values())
        logger.info(f"Total building mass: {total_m} tC")
        return total_m
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


def wood_demand(carbon_bld, *, wood_used, material_used, **kwargs):
    """This function calculates wood needed to build timber building"""
    # tonne of C total amount of carbon needed to build building including processing losses
    try:
        w = carbon_bld / wood_used / material_used
        logger.info(f" Wood demand: {w}")
        return w
    except Exception as e:
        logger.exception(e)


def years_to_accumulate(
    carbon_harv,  # should be in tonnes?
    scenario,
    **kwargs,
):
    """
    This function calculates number of years needed to accumulate harvested carbon
    using average carbon accumulation rate of a forest from the Cook-Paton
    database
    """
    try:
        # change harvest intensity to fraction
        yr = carbon_harv / carbon_accumulated_in_forest_per_year(scenario, **kwargs)
        logger.info(
            f"Number of years needed to accumulate harvested carbon using average carbon accumulation rate of a forest from the Cook-Paton database: {yr}"
        )
        return yr
    except Exception as e:
        logger.exception(e)
        return 0


def get_scenario_index(scenario, *args, **kwargs):
    index = {"min": 0, "best": 1, "max": 2}
    return index[scenario]


def carbon_accumulated_in_forest_per_year(
    scenario,
    *,
    forest_c_acc_rate,
    forest_harvest_area,
    forest_harvest_intensity,
    **kwargs,
):
    try:
        c_acc_rate = forest_c_acc_rate[get_scenario_index(scenario)]
        c_acc = c_acc_rate * forest_harvest_area * (forest_harvest_intensity * 0.01)
        return c_acc
    except Exception as e:
        logger.exception(e)
        return 0


def forest_recov(
    scenario,
    *,
    building_lifespan,
    **kwargs,
):
    """
    This function calculates amount of carbon recovered in the forest during the life time
    of a building
    """
    try:
        # tCO2/ha/y * ha = tCO2/y
        cr = (
            carbon_accumulated_in_forest_per_year(scenario, **kwargs)
            * building_lifespan
        )
        logger.info(
            f"Amount of carbon recovered in the forest during the life time of a building: {cr}"
        )
        return cr
    except Exception as e:
        logger.exception(e)


def forest_accum(area_planted, period_years, scenario, *, acc_rate, **kwargs):
    """
    This function calculates amount of carbon accumulated in the forest with
    area area_planted during a given period yr_forest
    """
    try:
        cacc = acc_rate[scenario] * area_planted * period_years
        logger.info(
            f"Amount of carbon accumulated in the forest with area {area_planted} during a given period {yr_forest}: {cacc}"
        )
        return cacc
    except Exception as e:
        logger.exception(e)
