import pytest
from nutri_term.calculator import (
        compute_bmr,
        compute_maintenance,
        compute_goal_calories,
        )

# Test known BMR values for Mifflin-St Jeor
def test_compute_bmr_male():
    # weight = 100kg, height = 178cm, age = 21, male
    expected = 10*100 + 6.25*178 - 5*21 + 5
    assert compute_bmr(100, 178, 21, "male") == pytest.approx(expected)

def test_compute_bmr_female():
    # same but female
    expected = 10*100 + 6.25*178 - 5*21 - 161
    assert compute_bmr(100, 178, 21, "female") == pytest.approx(expected)

# Test maintenance multipliers
@pytest.mark.parametrize("activity,factor", [
    ("sedentary", 1.2),
    ("light", 1.375),
    ("moderate", 1.55),
    ("active", 1.725),
    ("very_active", 1.9),
    ])

def test_compute_maintenance_calories(activity, factor):
    bmr = 1500
    assert compute_maintenance(bmr, activity) == pytest.approx(1500 * factor)

# Test goal adjustments
def test_compute_goal_calories():
    maintenance = 2000
    assert compute_goal_calories(maintenance, "maintenance") == pytest.approx(2000)
    assert compute_goal_calories(maintenance, "lose") == pytest.approx(2000 * 0.85)
    assert compute_goal_calories(maintenance, "gain") == pytest.approx(2000 * 1.15)
