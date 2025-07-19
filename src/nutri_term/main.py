#!/usr/bin/env python3

import argparse
from .calculator import (
        compute_bmr,
        compute_maintenance,
        compute_goal_calories,
        )
from .user_profile import save_profile, load_profile
from .macros import macro_breakdown
from .food_database import lookup_food
import json
from pathlib import Path
from datetime import date

def cmd_profile(args):
    profile = {
            "name": args.name,
            "weight": args.weight,
            "height": args.height,
            "age": args.age,
            "gender": args.gender,
            "activity": args.activity_level,
            }

    save_profile(profile)
    print("Profile save to", load_profile_file := str(save_profil.__defaults__[0]) if False else "")
    print(profile)
            
def cmd_calculate(args):
    profile = load_profile()
    if profile is None:
        print("No profile found. Let's create one!")
        print()
        interactive_profile_setup()
        profile = load_profile()  # Reload the newly created profile

    weight = profile["weight"]
    height = profile["height"]
    age = profile["age"]
    gender = profile["gender"]
    activity = profile["activity"]
    goal = args.goal

    bmr = compute_bmr(weight, height, age, gender)
    maintenance = compute_maintenance(bmr, activity)
    target = compute_goal_calories(maintenance, goal) 

    print(f"BMR (Mifflin-St Jeor):   {bmr:.0f} kcal/day")
    print(f"Maintenance calories:    {maintenance:.0f} kcal/day")
    print(f"Target calories ({args.goal}): {target:.0f}")

    macros = macro_breakdown(
            target,
            profile["weight"],
            protein_ratio = args.protein_ratio,
            carb_ratio = args.carb_ratio,
            fat_ratio = args.fat_ratio
            )
    print()
    print(" Macro targets:")
    print(f" Protein: {macros['protein_g']:.0f} g")
    print(f" Carbohydrates: {macros['carbs_g']:.0f} g")
    print(f" Fats: {macros['fats_g']:.0f} g")

def cmd_log(args):
    profile = load_profile()
    if profile is None:
        print("No profile found. Let's create one!")
        print()
        interactive_profile_setup()
        profile = load_profile()  # Reload the newly created profile

    # 1. Look up the food in the database
    food = lookup_food(args.food)
    if not food:
        print(f"Food '{args.food}' not found in database.")
        return

    # 2. Calculate macros/calories for the specified amount (scale per 100g)
    amount = args.amount
    factor = amount / 100.0
    entry = {
        "food": args.food,
        "amount_g": amount,
        "protein": round(food["protein"] * factor, 2),
        "carbs": round(food["carbs"] * factor, 2),
        "fat": round(food["fat"] * factor, 2),
        "calories": round(food["calories"] * factor, 2),
    }

    # 3. Prepare log file path for today
    log_dir = Path.home() / ".nutri-term" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / f"{date.today().isoformat()}.json"

    # 4. Load existing log or start a new one
    if log_file.exists():
        with log_file.open("r", encoding="utf-8") as f:
            log = json.load(f)
    else:
        log = []

    # 5. Append the new entry and save
    log.append(entry)
    with log_file.open("w", encoding="utf-8") as f:
        json.dump(log, f, indent=2)

    # 6. Print confirmation and calculated macros
    print(f"Logged {amount}g of {args.food}:")
    print(f"  Protein:  {entry['protein']} g")
    print(f"  Carbs:    {entry['carbs']} g")
    print(f"  Fat:      {entry['fat']} g")
    print(f"  Calories: {entry['calories']} kcal")

def cmd_summary(args):
    profile = load_profile()
    if profile is None:
        print("No profile found. Let's create one!")
        print()
        interactive_profile_setup()
        profile = load_profile()  # Reload the newly created profile

    # Get today's log file path
    log_dir = Path.home() / ".nutri-term" / "logs"
    log_file = log_dir / f"{date.today().isoformat()}.json"
    
    # Check if today's log exists
    if not log_file.exists():
        print("No foods logged today.")
        print("Use 'nutri-term log --food <name> --amount <grams>' to log foods.")
        return
    
    # Load today's log
    with log_file.open("r", encoding="utf-8") as f:
        today_log = json.load(f)
    
    if not today_log:
        print("No foods logged today.")
        print("Use 'nutri-term log --food <name> --amount <grams>' to log foods.")
        return
    
    # Calculate today's totals
    total_calories = sum(entry["calories"] for entry in today_log)
    total_protein = sum(entry["protein"] for entry in today_log)
    total_carbs = sum(entry["carbs"] for entry in today_log)
    total_fat = sum(entry["fat"] for entry in today_log)
    
    # Calculate user's daily targets
    bmr = compute_bmr(profile["weight"], profile["height"], profile["age"], profile["gender"])
    maintenance = compute_maintenance(bmr, profile["activity"])
    # Default to maintenance goal for summary (could be made configurable)
    target_calories = maintenance
    
    # Get macro targets (using default ratios)
    macro_targets = macro_breakdown(target_calories, profile["weight"])
    target_protein = macro_targets["protein_g"]
    target_carbs = macro_targets["carbs_g"]
    target_fat = macro_targets["fats_g"]
    
    # Calculate percentages
    calories_pct = (total_calories / target_calories) * 100 if target_calories > 0 else 0
    protein_pct = (total_protein / target_protein) * 100 if target_protein > 0 else 0
    carbs_pct = (total_carbs / target_carbs) * 100 if target_carbs > 0 else 0
    fat_pct = (total_fat / target_fat) * 100 if target_fat > 0 else 0
    
    # Display summary
    print(f"📊 Daily Summary for {date.today().strftime('%B %d, %Y')}")
    print("=" * 50)
    print()
    
    # Show logged foods
    print("🍽️  Foods logged today:")
    for entry in today_log:
        print(f"   • {entry['amount_g']}g {entry['food']} ({entry['calories']:.0f} kcal)")
    print()
    
    # Show totals vs targets
    print("📈 Daily Totals vs Targets:")
    print(f"   Calories:  {total_calories:.0f} / {target_calories:.0f} kcal ({calories_pct:.1f}%)")
    print(f"   Protein:   {total_protein:.1f} / {target_protein:.1f} g ({protein_pct:.1f}%)")
    print(f"   Carbs:     {total_carbs:.1f} / {target_carbs:.1f} g ({carbs_pct:.1f}%)")
    print(f"   Fat:       {total_fat:.1f} / {target_fat:.1f} g ({fat_pct:.1f}%)")
    print()
    
    # Show progress indicators
    print("📊 Progress:")
    print(f"   Calories:  {'█' * min(int(calories_pct / 10), 10)}{'░' * (10 - min(int(calories_pct / 10), 10))} {calories_pct:.1f}%")
    print(f"   Protein:   {'█' * min(int(protein_pct / 10), 10)}{'░' * (10 - min(int(protein_pct / 10), 10))} {protein_pct:.1f}%")
    print(f"   Carbs:     {'█' * min(int(carbs_pct / 10), 10)}{'░' * (10 - min(int(carbs_pct / 10), 10))} {carbs_pct:.1f}%")
    print(f"   Fat:       {'█' * min(int(fat_pct / 10), 10)}{'░' * (10 - min(int(fat_pct / 10), 10))} {fat_pct:.1f}%")
    print()
    
    # Show remaining calories
    remaining_calories = target_calories - total_calories
    if remaining_calories > 0:
        print(f"🎯 You have {remaining_calories:.0f} calories remaining today.")
    elif remaining_calories < 0:
        print(f"⚠️  You're {abs(remaining_calories):.0f} calories over your target today.")
    else:
        print("🎯 Perfect! You've hit your calorie target exactly.")

def interactive_profile_setup():
    """Interactive profile setup for new users."""
    print("Welcome to Nutri-Term! Let's get you started...")
    print()
    
    # Get user information with validation
    name = input("What's your name? ").strip()
    while not name:
        name = input("Name cannot be empty. What's your name? ").strip()
    
    # Weight validation
    while True:
        try:
            weight = float(input("What's your weight in kg? "))
            if weight <= 0 or weight > 500:
                print("Please enter a realistic weight between 1-500 kg.")
                continue
            break
        except ValueError:
            print("Please enter a valid number.")
    
    # Height validation
    while True:
        try:
            height = float(input("What's your height in cm? "))
            if height <= 0 or height > 300:
                print("Please enter a realistic height between 1-300 cm.")
                continue
            break
        except ValueError:
            print("Please enter a valid number.")
    
    # Age validation
    while True:
        try:
            age = int(input("What's your age? "))
            if age <= 0 or age > 120:
                print("Please enter a realistic age between 1-120.")
                continue
            break
        except ValueError:
            print("Please enter a valid number.")
    
    # Gender validation
    while True:
        gender = input("What's your gender? (male/female): ").lower().strip()
        if gender in ["male", "female"]:
            break
        print("Please enter 'male' or 'female'.")
    
    # Activity level with clear descriptions
    print("\nWhat's your activity level?")
    print("  1. Sedentary (little/no exercise, desk job)")
    print("  2. Light (light exercise 1-3 days/week)")
    print("  3. Moderate (moderate exercise 3-5 days/week)")
    print("  4. Active (hard exercise 6-7 days/week)")
    print("  5. Very Active (very hard exercise, physical job)")
    
    activity_map = {
        "1": "sedentary",
        "2": "light", 
        "3": "moderate",
        "4": "active",
        "5": "very_active"
    }
    
    while True:
        choice = input("Choose (1-5): ").strip()
        if choice in activity_map:
            activity = activity_map[choice]
            break
        print("Please enter a number between 1-5.")
    
    # Create and save profile
    profile = {
        "name": name,
        "weight": weight,
        "height": height,
        "age": age,
        "gender": gender,
        "activity": activity
    }
    
    save_profile(profile)
    print(f"\nProfile created successfully! Welcome, {name}!")
    print()

def main():
    parse = argparse.ArgumentParser(
            prog='nutri-term',
            description="Track your macros and calories from the terminal."
    )

    subparser = parse.add_subparsers(dest="command", required=False)

    p = subparser.add_parser("profile", help="Create or update your user profile")
    p.add_argument("--name", type=str, required=True, help="Your name")
    p.add_argument("--weight", type=float, required=True, help="Weight in kg")
    p.add_argument("--height", type=float, required=True, help="Height in cm")
    p.add_argument("--age", type=int, required=True, help="Age in years")
    p.add_argument("--gender", choices=["male", "female"], required=True, help="Gender")
    p.add_argument("--activity_level", choices=["sedentary", "light", "moderate", "high", "very high"], required=True, help="Activity level")
    p.set_defaults(func=cmd_profile)

    p_calc = subparser.add_parser(
            "calculate",
            help="Compute BMR, maintenance, and target calories"
            )
    
    p_calc.add_argument("--goal", choices=["maintenance", "lose", "gain"], default="maintenance", help="Nutrition goal")

    p_calc.add_argument("--protein-ratio", type=float, default=1.0, help="Grams of protein per pound of bodyweight")

    p_calc.add_argument("--carb-ratio", type=float, default=0.40, help="Fraction of remaining calories as carbohydrates")

    p_calc.add_argument("--fat-ratio", type=float, default=0.30, help="Fraction of remaining calories as fats")

    p_calc.set_defaults(func=cmd_calculate)
     
    l = subparser.add_parser("log", help="Log a food item")
    l.add_argument("--food", type=str, required=True, help="Food name or ID")
    l.add_argument("--amount", type=float, required=True, help="Quantity in grams")
    l.set_defaults(func=cmd_log)
 
    s = subparser.add_parser("summary", help="Show today's macro summary")
    s.set_defaults(func=cmd_summary)

    args = parse.parse_args()
    
    # Handle first-time user experience
    if args.command is None:
        # No command given - check if profile exists
        profile = load_profile()
        if profile is None:
            # First-time user - start interactive setup
            interactive_profile_setup()
            print("Welcome to Nutri-Term!")
            print()
            print("Available commands:")
            print("  profile     Create or update your user profile")
            print("  calculate   Compute BMR, maintenance, and target calories")
            print("  log         Log a food item")
            print("  summary     Show today's macro summary")
            print()
            print("Try: nutri-term calculate --goal lose")
        else:
            # Returning user - show help
            print("Welcome to Nutri-Term!")
            print()
            print("Available commands:")
            print("  profile     Create or update your user profile")
            print("  calculate   Compute BMR, maintenance, and target calories")
            print("  log         Log a food item")
            print("  summary     Show today's macro summary")
            print()
            print("Try: nutri-term calculate --goal lose")
        return
    
    # Execute the command
    args.func(args)

if __name__ == "__main__":
    main()
