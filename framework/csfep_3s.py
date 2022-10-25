def building_cstore(areaBLD, *, mass_ar_vn, mass_ar_lm, cf_log, **kwargs):
    """
    This function calculates amount of carbon stored in a building and
    amount of wood to be harvested for this building [t C]
    """
    y = (mass_ar_vn + mass_ar_lm) * areaBLD * cf_log
    # y=(mass_ar_mt_ps_co+mass_ar_mt_en_co+mass_ar_wfb_en_co)*areaBLD_co*cf_log;
    return y


def building_area(
    harvestedC,
    *,
    cf_log,
    mass_ar_mt_ps_co,
    mass_ar_mt_en_co,
    mass_ar_wfb_en_co,
    **kwargs
):
    """
    This function calculates floor area of buildings which can be constructed
    with given amount of wood
    """
    y = harvestedC / cf_log / (mass_ar_mt_ps_co + mass_ar_mt_en_co + mass_ar_wfb_en_co)
    return y


def building_cemi_mt(
    areaBLD, ik, *, mass_ar_lm, k_lmh, mass_ar_vn, k_vn, c2co2, **kwargs
):
    """
    This function calculates amount of carbon emitted at the manufacturing
    stage of timber construction materials [t C] assuming all emissions are CO2
    """
    v = (mass_ar_lm * k_lmh[ik] + mass_ar_vn * k_vn[ik]) * areaBLD / c2co2
    #    v=(mass_ar_mt_ps_co*k_mt(1)+mass_ar_mt_en_co*k_mt(1)+mass_ar_wfb_en_co*k_wfb(1))*areaBLD_co/c2co2
    return v


def building_cemi_sc(
    areaBLD, massconc, masssteal, massbrick, ik, *, k_con, k_stl, k_brk, c2co2, **kwargs
):
    """
    This function calculates amount of carbon emitted at the manufacturing
    stage of steel and concrete construction materials [t C]
    """
    z = (
        (massconc * k_con[ik] + masssteal * k_stl[ik] + massbrick * k_brk[ik])
        * areaBLD
        / c2co2
    )
    # z2=(mass_ar_stl_en_co*k_stl(1)+mass_ar_fbg_en_co*k_fbg(1)+mass_ar_gyp_en_co*k_gyp(1)+mass_ar_xps_en_co*k_xps(1))*areaBLD/c2co2;
    return z


def transport_cemi_mt(MatMass, distance, k, *, c2co2, **kwargs):
    """
    This function calculates amount of carbon emitted during transport
    stage of construction materials [t C] assuming all emissions are CO2
    """
    e = MatMass * distance * k / c2co2  # emissions from transport in [tC]
    return e


def wood_demand(carbonBLD, *, wood_used, material_used, **kwargs):
    """This function calculates wood needed to build timber building"""
    # tonne of C total amount of carbon needed to build building including processing losses
    w = carbonBLD / wood_used / material_used
    return w


def accum_c(carbonHarv, areaHarv, yri, *, acc_rate, **kwargs):
    """
    This function calculates number of years needed to accumulate harvested carbon
    using average carbon accumulation rate of a forest from the Cook-Paton
    database
    """
    yr = carbonHarv / acc_rate[yri] / areaHarv  # changed to python indexing
    return yr


def forest_crecov(spanBLD, areaHarv, yri, *, acc_rate, **kwargs):
    """
    This function calculates amount of carbon recovered in the forest during the life time
    of a building
    """
    cr = acc_rate[yri] * areaHarv * spanBLD
    return cr


def forest_caccum(areaPlanted, yrForest, yri, *, acc_rate, **kwargs):
    """
    This function calculates amount of carbon accumulated in the forest with
    area areaPlanted during a given period yrForest
    """
    cacc = acc_rate[yri] * areaPlanted * yrForest
    return cacc
