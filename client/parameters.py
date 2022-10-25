# PARAMETER LIST ----------------------------------------------------------
# Constants

model_parameter_desc = {
    "cf_log": "fraction of carbon in wood",
    "c2co2": "tons of CO2 associated with one ton of carbon",
    "k_lms": "softwood dried lumber low intensity production, Ruuska",
    "k_lmh": "hardwood dried lumber low intensity production, Ruuska report",
    "k_mt": "mass timber Table 6 from Pomp. and Montcaster 2018",
    "k_wfb": "wood fiber Table 4 wood fiber from Ruuska report",
    "k_vn": "Ökobaudat, mean, OSB Table 6 from Pomp. and Montcaster 2018",
    "k_stl": "steel from Pomp. and Montcaster 2018",
    "k_con": "concrete from Pomp. and Montcaster 2018",
    "k_fbg": "fiberglass, Ruuska",
    "k_gyp": "gypsum, Ruuska",
    "k_xps": "Polystyrene XPS, Ruuska",
    "k_brk": "brick all values from ICE DB V3.0 (Clay_Bricks sheet of excell)",
    "k_truck": "17t, 7.5-17t, 3.5-7.5t truck Table 6 from de Wolf et al 2017",
    "k_sea": "sea cargo Table 6 from de Wolf et al 2017",
}

model_parameters = {
    "cf_log": 0.5,
    "c2co2": 3.67,
    "k_lms": [0.12, 0.12, 0.12],
    "k_lmh": [0.16, 0.21, 0.26],
    "k_mt": [0.2, 0.44, 0.72],
    "k_wfb": [0.24, 0.24, 0.24],
    "k_vn": [0.3, 0.35, 0.409],
    "k_stl": [1.34, 2.11, 3.81],
    "k_con": [0.033, 0.145, 0.295],
    "k_fbg": [3.15, 3.15, 3.15],
    "k_gyp": [1.97, 1.97, 1.97],
    "k_xps": [3.3, 3.3, 3.3],
    "k_brk": [0.179, 0.225, 0.354],
    "k_truck": [0.00017398, 0.00036024, 0.00055731],
    "k_sea": 0.000013155,
}
