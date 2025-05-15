def macro_breakdown(
        total_cals: float,
        weight_kg: float,
        protein_ratio: float = 1.0,
        carb_ratio: float = 0.40,
        fat_ratio: float = 0.30
        ) -> dict:

    weight_lb = weight_kg * 2.20462

    protein_g = weight_lb * protein_ratio
    protein_cals = protein_g * 4

    rem_cals = max(0.0, total_cals - protein_cals)

    carb_cals = rem_cals * carb_ratio
    fat_cals = rem_cals * fat_ratio

    return {
        "protein_g": protein_g,
        "carbs_g": carb_cals / 4,
        "fats_g": fat_cals / 9,
        }
