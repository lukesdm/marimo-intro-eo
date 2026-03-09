class SCL:
    """Classes in the Scene Classification Layer"""

    Mask = 0
    Sat = 1
    Dark = 2
    Shadow = 3
    Veg = 4
    Bare = 5
    Water = 6
    Unknown = 7
    Cl_Med = 8
    Cl_High = 9
    Cl_Cirrus = 10
    Snow = 11


scl_names = {
    SCL.Mask: "No data",
    SCL.Sat: "Saturated",
    SCL.Dark: "Dark",
    SCL.Shadow: "Shadow",
    SCL.Veg: "Vegetated",
    SCL.Bare: "Bare/Non-Veg",
    SCL.Water: "Water",
    SCL.Unknown: "Unknown",
    SCL.Cl_Med: "Cloud (medium prob.)",
    SCL.Cl_High: "Cloud (high prob.)",
    SCL.Cl_Cirrus: "Cloud (cirrus)",
    SCL.Snow: "Snow/ice",
}

scl_colors = {
    SCL.Mask: "#000000",
    SCL.Sat: "#FF0000",
    SCL.Dark: "#3F3F3F",
    SCL.Shadow: "#833C09",
    SCL.Veg: "#00FF00",
    SCL.Bare: "#FFFF03",
    SCL.Water: "#0300CC",
    SCL.Unknown: "#757171",
    SCL.Cl_Med: "#AEAAAA",
    SCL.Cl_High: "#D0CECE",
    SCL.Cl_Cirrus: "#00CCFF",
    SCL.Snow: "#FF66FF",
}

scl_cmap = {str(i): scl_colors[i] for i in range(len(scl_colors))}
