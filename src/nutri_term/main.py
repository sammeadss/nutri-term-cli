#!/usr/bin/env python3
"""
nutri-term: a CLI tool to track daily macros and calories from the terminal. # module docstring
"""
#-----------------------------------------------------------------------------
# Import argparse to easily define and parse command-line arguments
import argparse 
#-----------------------------------------------------------------------------
# First four simple functions for subcommands (update)
def cmd_profile(args): 
    # profile command: collects/updates important user info needed for macro and calorie calculation
    print(f"[profile] name={args.name}, weight={args.weight}, height={args.height}, age={args.age}, gender={args.gender}, activityLvl={args.activityLvl}")
            
def cmd_calculate(args):
    # calculate command: calculates approximate macro and calories intake based on user info
    print(f"[calculate] goal={args.goal}")

def cmd_log(args):
    # log command: records food and macro entries
    print(f"[log] food={args.food}, amount={args.amount}")

def cmd_summary(args):
    # summary command: shows the summary of the current day
    print(f"[summary] Displaying today's macro summary...")
#-----------------------------------------------------------------------------
def main():
    # (1) Create the top-level parser 
    parse = argparse.ArgumentParser(
            prog='nutri-term',
            description="Track your macros and calories from the terminal."
    )

    # (2) Enable subcommands
    subparser = parse.add_subparsers(dest="command", required=True)

    # (3) PROFILE subcommand
    p = subparser.add_parser("profile", help="Create or update your user profile")
    p.add_argument("--name", type=str, required=True, help="Your name")
    p.add_argument("--weight", type=float, required=True, help="Weight in kg")
    p.add_argument("--height", type=float, required=True, help="Height in cm")
    p.add_argument("--age", type=int, required=True, help="Aye in years")
    p.add_argument("--gender", choices=["male", "female"], required=True, help="Gender")
    p.add_argument("--activityLvl", choices=["sedentary (rarely exercise)", "light (1-3 days of exercise or physical job)", "moderate (4-5 days of focused exercise)", "high (6-7 days of intense exercise)"], required=True, help="Activity level")
    p.set_defaults(func=cmd_profile)

    # (4) CALCULATE subcommand
    c = subparser.add_parser("calculate", help="Compute maintenance and goal macros")
    c.add_argument("--goal", choices=["maintenance", "lose", "gain"], default="maintenance", help="Nutrition goal")
    c.set_defaults(func=cmd_calculate)

    # (5) LOG subcommand
    l = subparser.add_parser("log", help="Log a food item")
    l.add_argument("--food", type=str, required=True, help="Food name or ID")
    l.add_argument("--amount", type=float, required=True, help="Quantity in grams")
    l.set_defaults(func=cmd_log)

    # (6) SUMMARY command
    s = subparser.add_parser("summary", help="Show today's macro summary")
    s.set_defaults(func=cmd_summary)

    # (7) Parse and dispatch
    args = parse.parse_args()
    args.func(args)
if __name__ == "__main__":
    main()
