import logging

logger = logging.getLogger(__name__)

if logger.hasHandlers():
        # Logger is already configured, remove all handlers
        logger.handlers = []

def building_cstore(area_bld, *, mass_ar_vn, mass_ar_lm, cf_log, **kwargs):
    """
    This function calculates amount of carbon stored in a building and
    amount of wood to be harvested for this building [t C]
    """
    try:
        y = (mass_ar_vn + mass_ar_lm) * area_bld * cf_log
        logger.info(f"Building carbon stored: {y} tC")
        return y
    except Exception as e:
        logger.exception(e)


def building_area(
    harvested_c,
    *,
    cf_log,
    mass_ar_mt_ps_co,
    mass_ar_mt_en_co,
    mass_ar_wfb_en_co,
    **kwargs,
):
    """
    This function calculates floor area of buildings which can be constructed
    with given amount of wood
    """
    try:
        y = (
            harvested_c
            / cf_log
            / (mass_ar_mt_ps_co + mass_ar_mt_en_co + mass_ar_wfb_en_co)
        )
        logger.info("Building floor area which can be constructed: {y}")
        return y
    except Exception as e:
        logger.exception(e)


def building_cemi_mt(
    area_bld, ik, *, mass_ar_lm, k_lmh, mass_ar_vn, k_vn, c2co2, **kwargs
):
    """
    This function calculates amount of carbon emitted at the manufacturing
    stage of timber construction materials [t C] assuming all emissions are CO2
    """
    try:
        v = (mass_ar_lm * k_lmh[ik] + mass_ar_vn * k_vn[ik]) * area_bld / c2co2
        logger.info(
            f"Amount of carbon emmitted at manufacturing stage of timber construction materials assuming all emissions are C02: {v}"
        )
        return v
    except Exception as e:
        logger.exception(e)


def building_cemi_sc(
    area_bld,
    massconc,
    masssteal,
    massbrick,
    ik,
    *,
    k_con,
    k_stl,
    k_brk,
    c2co2,
    **kwargs
):
    """
    This function calculates amount of carbon emitted at the manufacturing
    stage of steel and concrete construction materials [t C]
    """
    try:
        z = (
            (massconc * k_con[ik] + masssteal * k_stl[ik] + massbrick * k_brk[ik])
            * area_bld
            / c2co2
        )
        logger.info(
            f"Carbon emmissions at the manufacturing stage of steel and concrete construction materials: {z}"
        )
        return z
    except Exception as e:
        logger.exception(e)

def transport_cemi_mt(mat_mass, distance, k, *, c2co2, **kwargs):
    """
    This function calculates amount of carbon emitted during transport
    stage of construction materials [t C] assuming all emissions are CO2
    """
    try:
        e = mat_mass * distance * k / c2co2  # emissions from transport in [tC]
        logger.info(
            f"Carbon emissions during transport stage of construction materials [tC] assuming all emissions are CO2: {e}"
        )
        return e
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


def accum_c(carbon_harv, area_harv, yri, *, acc_rate, **kwargs):
    """
    This function calculates number of years needed to accumulate harvested carbon
    using average carbon accumulation rate of a forest from the Cook-Paton
    database
    """
    try:
        yr = carbon_harv / acc_rate[yri] / area_harv  # changed to python indexing
        logger.info(
            f"Number of years needed to accumulate harvested carbon using average carbon accumulation rate of a forest from the Cook-Paton database: {yr}"
        )
        return yr
    except Exception as e:
        logger.exception(e)


def forest_crecov(span_bld, area_harv, yri, *, acc_rate, **kwargs):
    """
    This function calculates amount of carbon recovered in the forest during the life time
    of a building
    """
    try:
        cr = acc_rate[yri] * area_harv * span_bld
        logger.info(
            f"Amount of carbon recovered in the forest during the life time of a building: {cr}"
        )
        return cr
    except Exception as e:
        logger.exception(e)


def forest_caccum(area_planted, yr_forest, yri, *, acc_rate, **kwargs):
    """
    This function calculates amount of carbon accumulated in the forest with
    area area_planted during a given period yr_forest
    """
    try:
        cacc = acc_rate[yri] * area_planted * yr_forest
        logger.info(
            f"Amount of carbon accumulated in the forest with area {area_planted} during a given period {yr_forest}: {cacc}"
        )
        return cacc
    except Exception as e:
        logger.exception(e)
