# Body fat estimation formulas

Two methods for estimating body fat percentage from simple measurements, with
the equations written out so you can implement them yourself.

Both produce an **estimate**, not a measurement. They are built on population
data, so two people with identical measurements can still differ.

---

## 1. U.S. Navy circumference method

Developed by Hodgdon and Beckett at the Naval Health Research Center (1984) and
used in the U.S. Navy Physical Readiness Program.

**Important:** the published equations are calibrated for **inches**. If you
work in centimetres, convert to inches first (cm / 2.54) — feeding centimetres
directly into these constants produces badly wrong results.

### Male

```
BF% = 86.010 * log10(waist - neck) - 70.041 * log10(height) + 36.76
```

### Female

```
BF% = 163.205 * log10(waist + hip - neck) - 97.684 * log10(height) - 78.387
```

### Variables

| Variable | How to measure |
|---|---|
| `height` | Standing height, inches |
| `neck` | Around the neck just below the larynx, tape sloping slightly downward to the front, inches |
| `waist` | Around the waist at the navel for men; at the narrowest point for women, inches |
| `hip` | Around the hips at the widest point (women only), inches |

`log10` is the base-10 logarithm.

### Constraints

- Male: `waist` must be greater than `neck`.
- Female: `waist + hip` must be greater than `neck`.
- Otherwise the logarithm is undefined.

---

## 2. BMI method

Needs only height, weight, age and sex. Less precise, because BMI does not
distinguish muscle mass from fat mass — a muscular person can be pushed into a
higher body fat bracket than they actually are.

```
BMI = weight_kg / height_m^2

male:   BF% = 1.20 * BMI + 0.23 * age - 16.2
female: BF% = 1.20 * BMI + 0.23 * age - 5.4
```

---

## 3. Derived values

```
fat_mass  = weight * BF% / 100
lean_mass = weight - fat_mass
```

---

## 4. Worked example (output of the included script)

Input: male, age 30, weight 180 lb, height 70 in, neck 15 in, waist 34 in.

| Method | Result | Category |
|---|---|---|
| U.S. Navy | **17.5%** | average |
| BMI | **21.7%** (BMI 25.8) | average |

Derived (from the Navy result): fat mass 14.3 kg / 31.5 lb, lean mass 67.3 kg /
148.5 lb.

The two methods differ by 4.2 percentage points on the *same person*. That gap
is normal and is the reason this repository ships the ranges table separately
from any single formula — see `why-estimates-disagree.md`.

These numbers were produced by running `body_fat_calculator.py` with the inputs
above; they are reproducible with:

```bash
python body_fat_calculator.py --unit us --sex male --age 30 \
    --weight 180 --height 70 --neck 15 --waist 34 --method navy
```

---

## 5. Category boundaries

See `ace-body-fat-ranges.csv`. The bounds are **inclusive** upper limits
(male: fitness ends at 17, average ends at 24), which is why 17.5% is reported
as `average` rather than `fitness`.

---

## Sources

- Hodgdon, J.A. & Beckett, M.B. (1984), *Prediction of body density from
  skinfold and girth measurements*, Naval Health Research Center. Basis of the
  U.S. Navy circumference equations.
- American Council on Exercise (ACE), adult body fat category ranges — used for
  the category table and for `classify()` in the script.
- BMI conversion (1.20 / 0.23 / 16.2 / 5.4): the widely used BMI-derived
  approximation. Its paper-level provenance is commonly attributed to
  Deurenberg-style BMI-to-body-fat work; treat it as a rough cross-check rather
  than a precise result.
