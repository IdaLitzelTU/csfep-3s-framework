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
    #logger.info(f" Out: {out}")
    return out


def to_coef(x):
    return x / 100


def c_stored_in_building(materials,*, c_material, **kwargs):
    """
    This function calculates amount of carbon stored in a building and
    amount of wood to be harvested for this building [t C]
    """

    try:
        total = 0
        for material, values in materials.items():  # materials is { concrete: {'mass': 53, 'state': 'dry',...}} }
            # calculate mass of dry timber m_dry = (m_green * d_dry) / d_green
            if values["state"] == "fresh" and c_material[material]["d_green"] and c_material[material]["d_dry"]:
                values["mass"] = (values["mass"] * c_material[material]["d_dry"]) / c_material[material]["d_green"]

            total = total + (values["mass"] * c_material[material]["c_content"] )
        return total
    except Exception as e:
        logger.exception(e)


def total_mass(materials):
    try:
        total_m = sum(materials.values())
        #logger.info(f"Total building mass: {total_m} tC")
        return total_m
    except Exception as e:
        logger.exception(e)


def emitted_manufacturing(scenario, materials, energy_sources, *, c_material, c2co2, **kwargs):
    """
    Calculates the C emmitted by manufactoring and sourcing of the materials 
    dependent on the energy source used for sourcing and manufactoring [kg C]
    """
    co2e = scenario + "_co2e"
    manuf_eec = scenario + "_manuf_eec"
    sourcing_eec = scenario + "_sourcing_eec"
    try:
        total = 0
        for material, values in materials.items():
            # calculate c02 in material if co2 coeffi exist
            if c_material[material][co2e]:
                co2_in_material = c_material[material][co2e] * values["mass"] # co2/kg

            # calculate C02 in material if eec coeffi exist
            else :
                co2_manuf = 0
                co2_sourcing = 0 
                # if material was manufactored
                if values["manufacturing_energy_id"]:
                    # kgCO2 = kg * MJ/kg * kgCO2/MJ
                    co2_manuf = values["mass"] * c_material[material][manuf_eec] * next(x["emission_factor"] for x in energy_sources if int(x["id"]) == int(values["manufacturing_energy_id"]))
                # if material was sourced
                if values["sourcing_energy_id"]:
                    # kgCO2 = kg * MJ/kg * kgCO2/MJ
                    co2_sourcing = values["mass"] * c_material[material][sourcing_eec] * next(x["emission_factor"] for x in energy_sources if int(x["id"]) == int(values["sourcing_energy_id"]))
                
                co2_in_material = co2_sourcing + co2_manuf

            total = total + co2_in_material
        #logger.info(f"Building carbon stored: {total/ c2co2} kgC")
        return total / c2co2
    except Exception as e:
        logger.exception(e)


def emitted_transporting(mass, distance, coeff, *, c2co2, **kwargs):
    try:
        # m -> t * Km * (kg * C02) / t*km / c02/c
        c_emitted = ((mass / 1000) * distance * coeff) / c2co2 #kgC
        return c_emitted
    except Exception as e:
        logger.exception(e)


def wood_demand(carbon_bld, *, wood_used, material_used, **kwargs):
    """This function calculates wood needed to build timber building"""
    # tonne of C total amount of carbon needed to build building including processing losses
    try:
        w = carbon_bld / wood_used / material_used
        return w
    except Exception as e:
        logger.exception(e)


def years_to_accumulate(
    carbon_harv,  # should be in tonnes?
    scenario,
    intensity,
    **kwargs,
):
    """
    This function calculates number of years needed to accumulate harvested carbon
    using average carbon accumulation rate of a forest from the Cook-Paton
    database
    """
    try:
        # change harvest intensity to fraction
        yr = carbon_harv / carbon_accumulated_in_forest_per_year(scenario, intensity, **kwargs)
        return yr
    except Exception as e:
        logger.exception(e)
        return 0


def get_scenario_index(scenario, *args, **kwargs):
    index = {"min": 0, "best": 1, "max": 2}
    return index[scenario]



def carbon_accumulated_in_forest_per_year(
    scenario,
    intensity,
    *,
    forest_c_acc_rate,
    forest_harvest_area,
    forest_harvest_intensity,
    **kwargs,
):
    try:
        if not intensity:
            forest_harvest_intensity = 100
        c_acc_rate = forest_c_acc_rate[get_scenario_index(scenario)]
        c_acc = c_acc_rate * forest_harvest_area  * (forest_harvest_intensity * 0.01)
        return c_acc
    except Exception as e:
        logger.exception(e)
        return 0


def forest_recov(
    scenario,
    intensity,
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
            carbon_accumulated_in_forest_per_year(scenario, intensity, **kwargs)
            * building_lifespan
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
        return cacc
    except Exception as e:
        logger.exception(e)
