from framework import csfep_3s

meta = {"version": "1.0.1", "by": "Some Name", "contact": "some.name@mail.com"}

input = [
    {
        "name": "a_harvest",
        "category": "Forest",
        "display": "Harvested area (ha)",
        "description": "An area of forest harvested in hectars",
        "type": "number",
        "default": "None",
    },
    {
        "name": "biomass_left",
        "category": "Forest",
        "display": "Harvested biomass left on site to provide nutrients for regeneration",
        "description": "10% (default) of harvested biomass is left on site to provide nutrients for regeneration and 90% is roundwood used in manufacturing",
        "type": "number",
        "default": 0.1,
    },
    {
        "name": "acc_rate",
        "category": "Forest",
        "display": "Carbon accumulation rate in Carribean pine plantation (MgC or t per ha per year)",
        "description": "MgC or t per ha per year carbon accumulation rate in Carribean pine plantation",
        "type": "array[number]",
        "default": "None",
    },
    {
        "name": "wood_used",
        "category": "Manufacturing",
        "display": "Roundwood used for material production",
        "description": "50% (default) of roundwood is assumed to be used for material production",
        "type": "number",
        "default": 0.5,
    },
    {
        "name": "material_used",
        "category": "Manufacturing",
        "display": "Prefabricated material used in construction",
        "description": "100% (default) of prefabricated material is used in construction",
        "type": "number",
        "default": 1,
    },
    {
        "name": "dmnf1",
        "category": "Manufacturing",
        "display": "Land transport distance 1 (km)",
        "description": "km land transport distance 1",
        "type": "number",
        "default": "None",
    },
    {
        "name": "dmnf2",
        "category": "Manufacturing",
        "display": "Land transport distance 2 (km)",
        "description": "km land transport distance 2",
        "type": "number",
        "default": "None",
    },
    {
        "name": "dmnf3",
        "category": "Manufacturing",
        "display": "Sea transport distance 1 (km)",
        "description": "km sea transport distance 1",
        "type": "number",
        "default": "None",
    },
    {
        "name": "dmnf4",
        "category": "Manufacturing",
        "display": "Land transport distance 3 (km)",
        "description": "km land transport distance 3 e.g., from the material manufacturing facilities to the construction site",
        "type": "number",
        "default": "None",
    },
    {
        "name": "floor_area",
        "category": "Building",
        "display": "Floor area of one house (m2)",
        "description": "m2 floor area of one house",
        "type": "number",
        "default": "None",
    },
    {
        "name": "xl",
        "category": "Building",
        "display": "Expected life span of the building (years)",
        "description": "years expected life span of the building",
        "type": "number",
        "default": "None",
    },
    {
        "name": "mass_ar_lm",
        "category": "Building",
        "display": "Dried timber or lumber",
        "description": "dried timber or lumber",
        "type": "number",
        "default": "None",
    },
    {
        "name": "mass_ar_vn",
        "category": "Building",
        "display": "Plywood",
        "description": "plywood",
        "type": "number",
        "default": "None",
    },
    {
        "name": "mass_ar_st_it",
        "category": "Building",
        "display": "Steel in pilot house construction",
        "description": "steel in pilot house construction",
        "type": "number",
        "default": "None",
    },
    {
        "name": "mass_ar_con_t",
        "category": "Building",
        "display": "Concrete in pilot house construction",
        "description": "concrete in pilot house construction",
        "type": "number",
        "default": "None",
    },
    {
        "name": "mass_ar_brick",
        "category": "Building",
        "display": "Bricks",
        "description": "bricks",
        "type": "number",
        "default": "None",
    },
    {
        "name": "massARcon",
        "category": "Building",
        "display": "Reinforced concrete",
        "description": "reinforced concrete",
        "type": "number",
        "default": "None",
    },
    {
        "name": "mass_ar_mt_ps_co",
        "category": "Building",
        "display": "Primary structure commercial mid-rise",
        "description": "primary structure commercial mid-rise generic Table 2",
        "type": "number",
        "default": "None",
    },
    {
        "name": "mass_ar_mt_ps_rs",
        "category": "Building",
        "display": "Primary structure residential mid-rise",
        "description": "primary structure residential mid-rise generic Table 2",
        "type": "number",
        "default": "None",
    },
    {
        "name": "mass_ar_mt_en_co",
        "category": "Building",
        "display": "Enclosure timber commercial mid-rise",
        "description": "enclosure timber commercial mid-rise generic Table 3",
        "type": "number",
        "default": "None",
    },
    {
        "name": "mass_ar_mt_en_rs",
        "category": "Building",
        "display": "Enclosure timber residential mid-rise",
        "description": "enclosure timber residential mid-rise generic Table 3",
        "type": "number",
        "default": "None",
    },
    {
        "name": "mass_ar_wfb_en_co",
        "category": "Building",
        "display": "Enclosure wood fiber structure commercial mid-rise",
        "description": "enclosure wood fiber structure commercial mid-rise generic Table 3",
        "type": "number",
        "default": "None",
    },
    {
        "name": "mass_ar_wfb_en_rs",
        "category": "Building",
        "display": "Enclosure wood fiber structure resudential mid-rise",
        "description": "enclosure wood fiber structure resudential mid-rise generic Table 3",
        "type": "number",
        "default": "None",
    },
    {
        "name": "mass_ar_con_ps_co",
        "category": "Building",
        "display": "Primary structure commercial concrete mid-rise",
        "description": "primary structure commercial concrete mid-rise generic",
        "type": "number",
        "default": "None",
    },
    {
        "name": "mass_ar_stl_ps_co",
        "category": "Building",
        "display": "Primary structure commercial steel mid-rise",
        "description": "primary structure commercial steel mid-rise generic",
        "type": "number",
        "default": "None",
    },
    {
        "name": "mass_ar_stl_en_co",
        "category": "Building",
        "display": "Enclosure steel mid-rise",
        "description": "enclosure steel mid-rise generic",
        "type": "number",
        "default": "None",
    },
    {
        "name": "mass_ar_fbg_en_co",
        "category": "Building",
        "display": "Enclosure fiberglass mid-rise",
        "description": "enclosure fiberglass mid-rise generic",
        "type": "number",
        "default": "None",
    },
    {
        "name": "mass_ar_gyp_en_co",
        "category": "Building",
        "display": "Enclosure gypsum mid-rise",
        "description": "enclosure gypsum mid-rise generic",
        "type": "number",
        "default": "None",
    },
    {
        "name": "mass_ar_xps_en_co",
        "category": "Building",
        "display": "Enclosure XPS mid-rise",
        "description": "enclosure XPS mid-rise genericformat bank % set output format",
        "type": "number",
        "default": "None",
    },
]


def run(data, params, *args, **kwargs):

    """
    Make sure you have common data and output for each version of the model
    """

    w_materials_in_building = (data["massARcon"] + data["mass_ar_brick"]) * data[
        "floor_area"
    ]

    # Calculate carbon storage in timber building and carbon needed to be extracted from forest or demand for carbon
    c_stored_in_building = csfep_3s.building_cstore(
        data["floor_area"],
        mass_ar_vn=data["mass_ar_vn"],
        mass_ar_lm=data["mass_ar_lm"],
        cf_log=params["cf_log"],
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
    # years_to_regrow_forest = csfep_3s.accum_c(
    #     c_needed_for_building, data["a_harvest"], 0, **data)
    # c_recovered_forest = csfep_3s.forest_crecov(
    #     data["xl"], data["a_harvest"], 0, **data)

    # RESULTS
    output = {}

    for i in range(0, 3, 1):
        print(f"Scenario {i + 1}")
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
            data["massARcon"],
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

        print(output[f"scenario_{i + 1}"])
    return output
