def compute_bmr(weight: float, height: float, age: int, gender: str) -> float:
    if gender == "male":
        return 10 * weight + 6.25 * height - 5 * age + 5
    else:
        return 10 * weight + 6.25 * height - 5 * age - 161

def compute_maintenance(bmr: float, activity: str) -> float:
    factors = {
            "sedentary": 1.2,
            "light": 1.375,
            "moderate": 1.55,
            "active": 1.725,
            "very_active": 1.9,
            }

    return bmr * factors.get(activity, 1.2)

def compute_goal_calories(maintenance: float, goal: str) -> float:
    if goal == "lose":
        return maintenance * 0.85
    elif goal == "gain":
        return maintenance * 1.15
    else:
        return maintenance
