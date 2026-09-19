#!/usr/bin/env python3
"""Estimate body fat percentage from simple measurements.

Implements two published estimation methods:

  1. U.S. Navy circumference method
     Hodgdon, J.A. & Beckett, M.B. (1984), "Prediction of body density from
     skinfold and girth measurements", Naval Health Research Center; used in
     the U.S. Navy Physical Readiness Program.

  2. BMI method
     A population-level approximation derived from BMI, age and sex. Less
     precise than the circumference method because BMI does not separate
     muscle mass from fat mass.

Both methods return an ESTIMATE, not a clinical measurement.

No dependencies. Everything runs locally; nothing is sent anywhere.

Usage
-----
  US units (inches / pounds):
    python body_fat_calculator.py --unit us --sex male --age 30 \
        --weight 180 --height 70 --neck 15 --waist 34 --method navy

  Metric units (cm / kg):
    python body_fat_calculator.py --unit metric --sex female --age 30 \
        --weight 68 --height 165 --neck 33 --waist 76 --hip 96 --method navy

  BMI method (no tape measurements needed):
    python body_fat_calculator.py --unit metric --sex male --age 30 \
        --weight 82 --height 178 --method bmi

Note on the Navy equations: they are calibrated for INCHES. Metric inputs are
converted to inches before the formula is applied.
"""

import argparse
import math
import sys

# Category boundaries follow the American Council on Exercise (ACE) adult
# reference ranges, expressed here as upper-exclusive cut points.
# See ace-body-fat-ranges.csv for the same data in table form.
# Inclusive upper bounds. These match the reference table in
# ace-body-fat-ranges.csv (for example: male fitness 14-17, average 18-24),
# so a value of 17.5 falls into "average", not "fitness".
CATEGORY_MAX = {
    "male": [(5.0, "essential"), (13.0, "athletes"), (17.0, "fitness"),
             (24.0, "average")],
    "female": [(13.0, "essential"), (20.0, "athletes"), (24.0, "fitness"),
               (31.0, "average")],
}


def to_inches(value, unit):
    """Convert a length to inches."""
    return value if unit == "us" else value / 2.54


def to_kilos(value, unit):
    """Convert a mass to kilograms."""
    return value * 0.453592 if unit == "us" else value


def navy_method(sex, height, neck, waist, hip, unit):
    """U.S. Navy circumference method. Returns body fat percentage.

    height/neck/waist/hip are supplied in the given unit; they are converted
    to inches internally because the published equations use inches.
    """
    h = to_inches(height, unit)
    n = to_inches(neck, unit)
    w = to_inches(waist, unit)

    if h <= 0 or n <= 0 or w <= 0:
        raise ValueError("height, neck and waist must be positive")

    if sex == "male":
        diff = w - n
        if diff <= 0:
            raise ValueError("waist must be larger than neck")
        return 86.010 * math.log10(diff) - 70.041 * math.log10(h) + 36.76

    if hip is None:
        raise ValueError("hip measurement is required for the female Navy equation")
    hp = to_inches(hip, unit)
    if hp <= 0:
        raise ValueError("hip must be positive")
    diff = w + hp - n
    if diff <= 0:
        raise ValueError("waist + hip must be larger than neck")
    return 163.205 * math.log10(diff) - 97.684 * math.log10(h) - 78.387


def bmi_method(sex, age, weight, height, unit):
    """BMI method. Returns (body fat percentage, bmi)."""
    height_m = height * 0.0254 if unit == "us" else height / 100.0
    weight_kg = to_kilos(weight, unit)
    if height_m <= 0 or weight_kg <= 0:
        raise ValueError("height and weight must be positive")
    if age <= 0:
        raise ValueError("age must be positive")

    bmi = weight_kg / (height_m * height_m)
    bf = 1.20 * bmi + 0.23 * age - (16.2 if sex == "male" else 5.4)
    return bf, bmi


def classify(bf, sex):
    """Map a body fat percentage onto an ACE-style category name."""
    for upper, name in CATEGORY_MAX[sex]:
        if bf <= upper:
            return name
    return "higher"


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Estimate body fat percentage (U.S. Navy or BMI method).")
    parser.add_argument("--unit", choices=["us", "metric"], default="us",
                        help="us = inches/pounds, metric = cm/kg")
    parser.add_argument("--sex", choices=["male", "female"], required=True)
    parser.add_argument("--age", type=float, required=True)
    parser.add_argument("--weight", type=float, required=True)
    parser.add_argument("--height", type=float, required=True)
    parser.add_argument("--neck", type=float, help="required for the Navy method")
    parser.add_argument("--waist", type=float, help="required for the Navy method")
    parser.add_argument("--hip", type=float,
                        help="required for the Navy method when sex=female")
    parser.add_argument("--method", choices=["navy", "bmi"], default="navy")
    args = parser.parse_args(argv)

    try:
        if args.method == "navy":
            if args.neck is None or args.waist is None:
                parser.error("--neck and --waist are required for the Navy method")
            bf = navy_method(args.sex, args.height, args.neck, args.waist,
                             args.hip, args.unit)
            extra = ""
        else:
            bf, bmi = bmi_method(args.sex, args.age, args.weight,
                                 args.height, args.unit)
            extra = "  (BMI {:.1f})".format(bmi)
    except ValueError as exc:
        print("error: {}".format(exc), file=sys.stderr)
        return 2

    if not math.isfinite(bf) or bf <= 0 or bf >= 80:
        print("error: result out of plausible range ({:.2f}); check inputs".format(bf),
              file=sys.stderr)
        return 2

    weight_kg = to_kilos(args.weight, args.unit)
    fat_kg = weight_kg * bf / 100.0
    lean_kg = weight_kg - fat_kg

    print("body fat : {:.1f}%  [{}]{}".format(bf, classify(bf, args.sex), extra))
    print("fat mass : {:.1f} kg / {:.1f} lb".format(fat_kg, fat_kg * 2.20462))
    print("lean mass: {:.1f} kg / {:.1f} lb".format(lean_kg, lean_kg * 2.20462))
    print("method   : {}".format("U.S. Navy" if args.method == "navy" else "BMI"))
    print()
    print("This is an estimate, not a clinical measurement.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
