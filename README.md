# Body Fat Calculator Reference

Formulas, reference ranges, and a small dependency-free tool for estimating body
fat percentage. Everything here runs locally; nothing is uploaded anywhere.

## What's in here

| File | What it is | What it's for |
|---|---|---|
| `body_fat_calculator.py` | Runnable Python tool, no dependencies | Estimate body fat percentage from the command line using either method |
| `body-fat-formulas.md` | Both equations written out, plus a worked example | Port the math into another language |
| `ace-body-fat-ranges.csv` | Adult body fat category ranges (ACE), both sexes | Look up a category, or label results programmatically |
| `why-estimates-disagree.md` | Why two methods give different numbers on the same person | Interpret results without chasing noise |

## Quick start

Requires Python 3. No packages to install.

```bash
# U.S. Navy method, US units (inches / pounds)
python body_fat_calculator.py --unit us --sex male --age 30 \
    --weight 180 --height 70 --neck 15 --waist 34

# U.S. Navy method, metric units (cm / kg); hip is required for women
python body_fat_calculator.py --unit metric --sex female --age 30 \
    --weight 68 --height 165 --neck 33 --waist 76 --hip 96

# BMI method, no tape measurements needed
python body_fat_calculator.py --unit metric --sex male --age 30 \
    --weight 82 --height 178 --method bmi
```

Example output:

```
body fat : 17.5%  [average]
fat mass : 14.3 kg / 31.5 lb
lean mass: 67.3 kg / 148.5 lb
method   : U.S. Navy
```

## Input and output fields

Inputs accepted by the tool (and by the equivalent form on the site):

| Field | Required | Notes |
|---|---|---|
| `unit` | yes | `us` (in/lb) or `metric` (cm/kg) |
| `method` | yes | `navy` or `bmi` |
| `sex` | yes | `male` or `female` — selects the equation |
| `age` | yes | years |
| `weight` | yes | lb or kg, per `unit` |
| `height` | yes | in or cm, per `unit` |
| `neck` | navy only | in or cm |
| `waist` | navy only | in or cm |
| `hip` | navy only, women | in or cm |

Outputs: body fat percentage, category label (`essential` / `athletes` /
`fitness` / `average` / `higher`), fat mass, lean mass — and BMI when using the
BMI method.

## Notes on accuracy

The U.S. Navy equations are calibrated for inches; metric inputs are converted
before the formula is applied. Both methods return an estimate based on
population averages, so the same person can produce meaningfully different
numbers depending on the method — this is normal, and
`why-estimates-disagree.md` explains why.

Category boundaries are inclusive upper limits (for men, `fitness` ends at 17
and `average` ends at 24), so a result of 17.5% is labelled `average`.

An interactive version of both methods is available at
[aibodyfatcalculator.com](https://aibodyfatcalculator.com/body-fat-calculator).

## Sources

- U.S. Navy circumference equations: Hodgdon, J.A. & Beckett, M.B. (1984),
  Naval Health Research Center.
- Category ranges: American Council on Exercise (ACE) adult guidelines.

## License

MIT — see `LICENSE`.
