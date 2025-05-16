import pytest
from nutri_term.macros import macro_breakdown

def test_macro_breakdown():
    # 2000 kcal, 50 kg = 110.23 lb --> protein = 110.23g --> 440.92 kcal
    target = 2000
    lb = 50 * 2.20462
    macros = macro_breakdown(target, weight_kg=50)
    # protein_g exactly lb * 1.0
    assert macros["protein_g"] == pytest.approx(lb)
    # remaining cals = 2000 - (lb*4)
    rem = target - lb * 4
    # default carb_ratio = 0.40 --> carb_cals = rem * 0.40 --> grams = /4
    assert macros["carbs_g"] == pytest.approx((rem * 0.40) / 4)
    # default fat_ratio = 0.30 --> fat_cals = rem * 0.30 --> grams = /9
    assert macros["fats_g"] == pytest.approx((rem * 0.30) / 9)
