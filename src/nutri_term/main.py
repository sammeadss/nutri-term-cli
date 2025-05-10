#!/usr/bin/env python3

import argparse
from .calculator import (
        compute_bmr,
        compute_maintenance,
        compute_goal_calories,
        )

def cmd_profile(args):
    print(f"[profile] name={args.name}, weight={args.weight}, height={args.height}, age={args.age}, gender={args.gender}, activity={args.activity}")
            
def cmd_calculate(args):
    bmr = compute_bmr(
            weight=args.weight,
            height=args.height,
            age=args.age,
            gender=args.gender,
            )

    maintenance = compute_maintenance(bmr, args.activity_level)

    target = compute_goal_calories(maintenance, args.goal)

    print(f"BMR (Mifflin-St Jeor):   {bmr:.0f} kcal/day")
    print(f"Maintenance calories:    {maintenance:.0f} kcal/day")
    print(f"Target calories ({args.goal}): {target:.0f}")

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
       
    p_calc.add_argument("--weight", type=float, required=True, help="Weight in kg")
    p_calc.add_argument("--height", type=float, required=True, help="Height in cm")
    p_calc.add_argument("--age", type=int, required=True, help="Aye in years")
    p_calc.add_argument("--gender", choices=["male", "female"], required=True, help="Gender")
    p_calc.add_argument("--activity_level", choices=["sedentary", "light", "moderate", "high", "very high"], required=True, help="Activity level")
    p_calc.add_argument("--goal", choices=["maintenance", "lose", "gain"], default="maintenance", help="Nutrition goal")

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
