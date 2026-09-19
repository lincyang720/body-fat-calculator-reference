# Why body fat estimates disagree

If you measure yourself with three methods in one afternoon, you will very
likely get three different numbers. This is expected, and it is the single most
common source of confusion for anyone tracking body composition at home.

This document explains *why*, and what to do about it. It contains no invented
accuracy figures — only the mechanisms that cause disagreement.

---

## The core reason: they measure different things

Body fat percentage is not directly observable. Every method measures a
*proxy* and converts it into a percentage using a formula fitted to a
particular population. Different proxies, different populations, different
answers.

| Method | What it actually measures |
|---|---|
| Circumference equations (U.S. Navy) | Girth measurements fed into a population-fitted equation |
| Skinfold calipers | Thickness of subcutaneous fat at specific sites |
| Bioelectrical impedance (BIA) | Electrical resistance of body tissues |
| DEXA | Tissue attenuation of X-rays at two energies |
| Hydrostatic weighing | Body density via underwater weight |
| Air-displacement plethysmography | Body volume via air displacement |
| Visual / photo estimate | Shape cues interpreted by a human or a model |

Because the underlying quantity differs, two methods can both be "working
correctly" and still disagree by several percentage points on the same person.

---

## Variables that move a single reading

Each of these shifts a result without the person's actual body fat changing:

- **Hydration** — affects impedance methods strongly, and body volume slightly.
- **Meal timing and recent food** — changes abdominal girth and body mass.
- **Time of day** — people are typically slightly taller in the morning and
  carry different fluid distribution later.
- **Training in the last 24h** — muscle inflammation and fluid shift change
  girth and impedance.
- **Sodium and carbohydrate intake** — drives water retention.
- **Menstrual cycle** — shifts fluid and girth for many women.
- **Operator technique** — skinfold and tape results depend heavily on locating
  the same landmark every time.
- **Device and protocol** — different BIA devices and different lab protocols
  are not interchangeable.

---

## What this means in practice

1. **Pick one primary method.** Switching methods mid-cut destroys the
   comparability of your data.
2. **Standardise conditions.** Same time of day, similar hydration, same
   landmarks, same device.
3. **Read the trend, not the reading.** A single number carries little
   information. Several readings across several weeks carry a lot more.
4. **Treat the category, not the decimal, as the signal.** A change from 17.5%
   to 18.0% is noise. A sustained move across a category boundary over a month
   is information.
5. **Do not average across methods.** Averaging two methods that measure
   different proxies does not produce a more accurate number; it produces a
   number that corresponds to no method at all.

---

## When a clinical measurement is worth it

Home methods are for *tracking*. If you need an absolute value — for a
medical decision, a competition weigh-in, or research — use a laboratory method
(DEXA, hydrostatic weighing, or multi-compartment modelling) administered by a
trained operator, and treat that as the reference point.

---

## Related files in this repository

- `body-fat-formulas.md` — the two equations implemented here, worked example.
- `body_fat_calculator.py` — runnable implementation of both methods.
- `ace-body-fat-ranges.csv` — the category boundaries used to label results.
