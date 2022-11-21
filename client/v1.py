from framework import csfep_3s

meta = {"version": "1.0.1", "by": "Some Name", "contact": "some.name@mail.com"}

params = {
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

input = [
    {
        "name": "a_harvest",
        "category": "Forest",
        "display_name": "Harvested area (ha)",
        "description": "An area of forest harvested in hectares",
        "type": "number",
        "default": "None",
    },
    {
        "name": "biomass_left",
        "category": "Forest",
        "display_name": "Harvested biomass left on site",
        "description": "Proportion of harvested biomass left on site to provide nutrients for regeneration",
        "type": "number",
        "default": 0.1,
    },
    {
        "name": "acc_rate",
        "category": "Forest",
        "display_name": "Carbon accumulation rate (MgC or t per ha per year)",
        "description": "Carbon accumulation rate in Carribean pine plantation in metric tonnes of carbon (MgC) or ton per hectares per year ",
        "type": "array[number]",
        "default": "None",
    },
    {
        "name": "wood_used",
        "category": "Manufacturing",
        "display_name": "Roundwood used",
        "description": "Proportion of roundwood used for material production",
        "type": "number",
        "default": 0.5,
    },
    {
        "name": "material_used",
        "category": "Manufacturing",
        "display_name": "Prefabricated material used",
        "description": "Proportion of prefabricated material used in construction",
        "type": "number",
        "default": 1,
    },
    {
        "name": "dmnf1",
        "category": "Manufacturing",
        "display_name": "Land transport distance 1 (km)",
        "description": "Land transport distance 1 in kilometers",
        "type": "number",
        "default": "None",
    },
    {
        "name": "dmnf2",
        "category": "Manufacturing",
        "display_name": "Land transport distance 2 (km)",
        "description": "Land transport distance 2 in kilometers",
        "type": "number",
        "default": "None",
    },
    {
        "name": "dmnf3",
        "category": "Manufacturing",
        "display_name": "Sea transport distance 1 (km)",
        "description": "Sea transport distance 1 in kilometers",
        "type": "number",
        "default": "None",
    },
    {
        "name": "dmnf4",
        "category": "Manufacturing",
        "display_name": "Land transport distance 3 (km)",
        "description": "Land transport distance 3 in kilometers e.g., from the material manufacturing facilities to the construction site",
        "type": "number",
        "default": "None",
    },
    {
        "name": "floor_area",
        "category": "Building",
        "display_name": "Floor area of one house (m2)",
        "description": "The floor area of one house in squared meters",
        "type": "number",
        "default": "None",
    },
    {
        "name": "xl",
        "category": "Building",
        "display_name": "Expected life span of the building (years)",
        "description": "The expected life span of the building in years",
        "type": "number",
        "default": "None",
    },
    {
        "name": "mass_ar_lm",
        "category": "Building",
        "display_name": "Dried timber or lumber (t/m2)",
        "description": "Material intensity of dried timber or lumber used in tonnes per meter square",
        "type": "number",
        "default": "None",
    },
    {
        "name": "mass_ar_vn",
        "category": "Building",
        "display_name": "Plywood (t/m2)",
        "description": "Material intensity of plywood used in tonnes per meter square",
        "type": "number",
        "default": "None",
    },
    {
        "name": "mass_ar_st_it",
        "category": "Building",
        "display_name": "Steel in pilot house construction (t/m2)",
        "description": "Material intensity of steel used in pilot house construction in tonnes per meter square",
        "type": "number",
        "default": "None",
    },
    {
        "name": "mass_ar_con_t",
        "category": "Building",
        "display_name": "Concrete in pilot house construction (t/m2)",
        "description": "Material intensity of concrete used in pilot house construction in tonnes per meter square",
        "type": "number",
        "default": "None",
    },
    {
        "name": "mass_ar_brick",
        "category": "Building",
        "display_name": "Bricks (t/m2)",
        "description": "Material intensity of bricks used in tonnes per meter square",
        "type": "number",
        "default": "None",
    },
    {
        "name": "mass_ar_con",
        "category": "Building",
        "display_name": "Reinforced concrete (t/m2)",
        "description": "Material intensity of reinforced concrete used in tonnes per meter square",
        "type": "number",
        "default": "None",
    },
    {
        "name": "mass_ar_mt_ps_co",
        "category": "Building",
        "display_name": "Primary structure commercial mid-rise generic building (t/m2)",
        "description": "Material intensity of a primary structure commercial mid-rise generic building in tonnes per meter square",
        "type": "number",
        "default": "None",
    },
    {
        "name": "mass_ar_mt_ps_rs",
        "category": "Building",
        "display_name": "Primary structure residential mid-rise generic building (t/m2)",
        "description": "Material intensity of a primary structure residential mid-rise generic building in tonnes per meter square",
        "type": "number",
        "default": "None",
    },
    {
        "name": "mass_ar_mt_en_co",
        "category": "Building",
        "display_name": "Enclosure timber commercial mid-rise generic (t/m2)",
        "description": "Material intensity of enclosure timber in commercial mid-rise generic building in tonnes per meter square",
        "type": "number",
        "default": "None",
    },
    {
        "name": "mass_ar_mt_en_rs",
        "category": "Building",
        "display_name": "Enclosure timber residential mid-rise generic (t/m2)",
        "description": "Material intensity of enclosure timber in residential mid-rise generic building in tonnes per meter square",
        "type": "number",
        "default": "None",
    },
    {
        "name": "mass_ar_wfb_en_co",
        "category": "Building",
        "display_name": "Enclosure wood fiber structure commercial mid-rise (t/m2)",
        "description": "Material intensity of enclosure wood fiber structure in commercial mid-rise generic building in tonnes per meter square",
        "type": "number",
        "default": "None",
    },
    {
        "name": "mass_ar_wfb_en_rs",
        "category": "Building",
        "display_name": "Enclosure wood fiber structure residential mid-rise (t/m2)",
        "description": "Material intensity of enclosure wood fiber structure in residential mid-rise generic building in tonnes per meter square",
        "type": "number",
        "default": "None",
    },
    {
        "name": "mass_ar_con_ps_co",
        "category": "Building",
        "display_name": "Primary structure commercial concrete mid-rise generic (t/m2)",
        "description": "Material intensity of a primary structure commercial concrete mid-rise generic building in tonnes per meter square",
        "type": "number",
        "default": "None",
    },
    {
        "name": "mass_ar_stl_ps_co",
        "category": "Building",
        "display_name": "Primary structure commercial steel mid-rise generic (t/m2)",
        "description": "Material intensity of a primary structure commercial steel mid-rise generic building in tonnes per meters square",
        "type": "number",
        "default": "None",
    },
    {
        "name": "mass_ar_stl_en_co",
        "category": "Building",
        "display_name": "Enclosure steel mid-rise generic (t/m2)",
        "description": "Material intensity of enclosure steel in mid-rise generic building in tonnes per meter square",
        "type": "number",
        "default": "None",
    },
    {
        "name": "mass_ar_fbg_en_co",
        "category": "Building",
        "display_name": "Enclosure fiberglass mid-rise generic (t/m2)",
        "description": "Material intensity of enclosure fiberglass in mid-rise generic building in tonnes per meter square",
        "type": "number",
        "default": "None",
    },
    {
        "name": "mass_ar_gyp_en_co",
        "category": "Building",
        "display_name": "Enclosure gypsum mid-rise generic (t/m2)",
        "description": "Material intensity of enclosure gypsum in mid-rise generic building in tonnes per meter square",
        "type": "number",
        "default": "None",
    },
    {
        "name": "mass_ar_xps_en_co",
        "category": "Building",
        "display_name": "Enclosure XPS mid-rise generic (t/m2)",
        "description": "Material intensity of enclosure XPS in mid-rise generic building in tonnes per meter square",
        "type": "number",
        "default": "None",
    },
]


def run(data, params, *args, **kwargs):

    """
    Make sure you have common data and output for each version of the model
    """

    w_materials_in_building = (data["mass_ar_con"] + data["mass_ar_brick"]) * data[
        "floor_area"
    ]

    # Calculate carbon storage in timber building and carbon needed to be extracted from forest or demand for carbon
    c_stored_in_building = csfep_3s.building_cstore(
        data["floor_area"], **data, **params
    )

    # t C stored in materials before construction
    c_stored_in_materials = c_stored_in_building / data["material_used"]

    # tC stored in roundwood brought to the plant
    c_stored_in_roundwood = c_stored_in_materials / data["wood_used"]
    c_needed_for_building = c_stored_in_roundwood / (
        1 - data["biomass_left"]
    )  # tC stored in harested trees

    c_accum_forest = 0
    number_of_buildings = 1  # number of buildings to be built from harvested wood
    c_harvested = c_needed_for_building

    # tCstored in buildings constructed from harvested wood
    c_buildings = number_of_buildings * c_stored_in_building

    # tC stored in scrap wood from material manufacturing and construction
    c_harvest_2_scrap = c_stored_in_roundwood - c_buildings
    c_harvest_2_forest = (
        c_needed_for_building * data["biomass_left"]
    )  # tC returuned to forest

    # floor area of constructed buildings
    building_area_built = number_of_buildings * data["floor_area"]

    # Calculate time to replanish carbon debt in a forest
    # changed index as python starts from 0 not 1
    years_to_regrow_forest = csfep_3s.accum_c(
        c_needed_for_building, data["a_harvest"], 0, **data
    )
    c_recovered_forest = csfep_3s.forest_crecov(
        data["xl"], data["a_harvest"], 0, **data
    )

    # RESULTS
    output = {}
    # Calculations for min, mean, and max CO2 emissions values
    for i in range(0, 3, 1):
        output[f"scenario_{i + 1}"] = {}

        list1 = ["Accumulated", "Harvested", "C2Scrap", "C2Forest", "C2Buildings"]
        list2 = [
            "MassTimber",
            "MT transport",
            "SteelConcrete",
            "SC transport",
            "Difference",
        ]

        #   Calculate carbon emissions from building production and material transport
        c_emitted_building_timber = csfep_3s.building_cemi_sc(
            building_area_built,
            data["mass_ar_con_t"],
            data["mass_ar_st_it"],
            0,
            i,
            k_con=params["k_con"],
            k_stl=params["k_stl"],
            k_brk=params["k_brk"],
            c2co2=params["c2co2"],
        ) + csfep_3s.building_cemi_mt(
            building_area_built,
            i,
            mass_ar_lm=data["mass_ar_lm"],
            k_lmh=params["k_lmh"],
            mass_ar_vn=data["mass_ar_vn"],
            k_vn=params["k_vn"],
            c2co2=params["c2co2"],
        )

        c_emitted_building_steel_concrete = csfep_3s.building_cemi_sc(
            building_area_built,
            data["mass_ar_con"],
            0,
            data["mass_ar_brick"],
            i,
            k_con=params["k_con"],
            k_stl=params["k_stl"],
            k_brk=params["k_brk"],
            c2co2=params["c2co2"],
        )

        c_emitted_building_transport_timber = (
            csfep_3s.transport_cemi_mt(
                c_harvested / params["cf_log"],
                data["dmnf1"],
                params["k_truck"][i],
                c2co2=params["c2co2"],
            )
            + csfep_3s.transport_cemi_mt(
                c_stored_in_roundwood / params["cf_log"],
                data["dmnf2"],
                params["k_truck"][i],
                c2co2=params["c2co2"],
            )
            + csfep_3s.transport_cemi_mt(
                c_stored_in_materials / params["cf_log"],
                data["dmnf3"],
                params["k_sea"],
                c2co2=params["c2co2"],
            )
            + csfep_3s.transport_cemi_mt(
                c_stored_in_building / params["cf_log"],
                data["dmnf4"],
                params["k_truck"][i],
                c2co2=params["c2co2"],
            )
        )

        c_emitted_transport_conven = csfep_3s.transport_cemi_mt(
            w_materials_in_building,
            data["dmnf4"],
            params["k_truck"][i],
            c2co2=params["c2co2"],
        )

        units = ["tC", "tCO2"]
        for unit in units:
            df = {}
            df["Unit"] = unit

            for index, value in enumerate(
                [
                    c_accum_forest,
                    c_harvested,
                    c_harvest_2_scrap,
                    c_harvest_2_forest,
                    c_buildings,
                ]
            ):
                if unit == "tC":
                    df[list1[index]] = value
                else:
                    df[list1[index]] = value * params["c2co2"]

            for index, value in enumerate(
                [
                    c_emitted_building_timber,
                    c_emitted_building_transport_timber,
                    c_emitted_building_steel_concrete,
                    c_emitted_transport_conven,
                    c_emitted_building_steel_concrete - c_emitted_building_timber,
                ]
            ):

                if unit == "tC":
                    df[list2[index]] = value
                else:
                    df[list2[index]] = value * params["c2co2"]

            output[f"scenario_{i + 1}"][unit] = df

        output[f"scenario_{i + 1}"]["Buildings floor area m2"] = building_area_built
        output[f"scenario_{i + 1}"]["Number of Buildings"] = number_of_buildings

    return output
