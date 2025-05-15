#!/usr/bin/env python3

import argparse
from .calculator import (
        compute_bmr,
        compute_maintenance,
        compute_goal_calories,
        )
from .user_profile import save_profile, load_profile
from .macros import macro_breakdown

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
        print("No profile found, please run the profile command first.")
        return

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
    print(f"[log] food={args.food}, amount={args.amount}")

def cmd_summary(args):
    print(f"[summary] Displaying today's macro summary...")

def main():
    parse = argparse.ArgumentParser(
            prog='nutri-term',
            description="Track your macros and calories from the terminal."
    )

    subparser = parse.add_subparsers(dest="command", required=True)

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
    args.func(args)

if __name__ == "__main__":
    main()
