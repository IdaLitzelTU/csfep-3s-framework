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
                values_mass = (values["mass"] * c_material[material]["d_dry"]) / c_material[material]["d_green"]
            else: values_mass = values["mass"]
            print(":", material, c_material[material]["c_content"])
            total = total + (values_mass * c_material[material]["c_content"] * 0.01)
        return total
    except Exception as e:
        logger.exception(e)

        

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
    carbon harvested with harvest intensity 
    """
    try:
        return (
            c_accumulated_in_forest
            * to_coef(forest_harvest_intensity)
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
    """
    try:
        # change harvest intensity to fraction
        yr = carbon_harv / carbon_accumulated_in_forest_per_year(
            scenario, area, **kwargs
        )
        logger.info(
            f" bla: {carbon_harv, carbon_accumulated_in_forest_per_year(scenario, area, **kwargs)}")
        logger.info(
            f" yr: {yr}"
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


def emitted_manufacturing(scenario, materials, energy_sources, *, c_material, c2co2, **kwargs):
    """
    Calculates the C emmitted by manufactoring and sourcing of fresh materials 
    dependent on the energy source used for sourcing and manufactoring [kg C]
    """
    co2e = scenario + "_co2e"
    manuf_eec = scenario + "_manuf_eec"
    sourcing_eec = scenario + "_sourcing_eec"
    try:
        total = 0
        for material, values in materials.items():
            print("material", material , values["state"])
            # calculate fresh mass of timber m_green = (m_dry * d_green) / d_dry
            if values["state"] == "dry" and c_material[material]["d_green"] and c_material[material]["d_dry"]:
                mass_fresh = (values["mass"] * c_material[material]["d_green"]) / c_material[material]["d_dry"]
            else: mass_fresh = values["mass"]

            # calculate c in material if c coeffi exist
            if c_material[material][co2e]:
                c_in_material = (c_material[material][co2e] * mass_fresh) / c2co2 # c/kg
                

            # calculate C in material if eec coeffi exist
            else :
                c_manuf = 0
                c_sourcing = 0 

                # if material was sourced
                if values["sourcing_energy_id"]:
                    # kgC = kg * MJ/kg * kgC/MJ
                    c_sourcing = mass_fresh * c_material[material][sourcing_eec] * next(x["emission_factor"] for x in energy_sources if int(x["id"]) == int(values["sourcing_energy_id"]))
                    print("----sourc", material, mass_fresh, values["mass"], c_material[material][sourcing_eec], next(x["emission_factor"] for x in energy_sources if int(x["id"]) == int(values["sourcing_energy_id"])),"EMITTED", c_sourcing )
  

                # if material was manufactored
                if values["manufacturing_energy_id"]:
                    # kgC = kg * MJ/kg * kgC/MJ
                    c_manuf = mass_fresh * c_material[material][manuf_eec] * next(x["emission_factor"] for x in energy_sources if int(x["id"]) == int(values["manufacturing_energy_id"]))
                    print("----manuf", material, mass_fresh, values["mass"], c_material[material][manuf_eec], next(x["emission_factor"] for x in energy_sources if int(x["id"]) == int(values["manufacturing_energy_id"]) ),"EMITTED",  c_manuf)

                c_in_material = c_sourcing + c_manuf
                
            total = total + c_in_material
        #logger.info(f"Building carbon stored: {total} kgC")
        return total 
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
