"""Unit-aware ingredient merging for the meal planner.

merge_ingredients(items) takes a list of (ingredient, quantity, unit) and
returns a list of (ingredient, [display strings]), one entry per ingredient.

Amounts are converted to a base unit (ml for volume, g for weight), summed,
then converted back to the friendliest unit. Count units (each, clove, can...)
are summed as-is. Volume and weight of the same ingredient are NOT merged
(that needs a per-ingredient density), so both show up on the same line.
"""
from collections import defaultdict
from fractions import Fraction

VOLUME_ML = {"tsp": 4.92892, "tbsp": 14.7868, "fl oz": 29.5735, "cup": 236.588,
             "pint": 473.176, "quart": 946.353, "ml": 1.0, "l": 1000.0}
WEIGHT_G = {"g": 1.0, "kg": 1000.0, "oz": 28.3495, "lb": 453.592}
COUNT_UNITS = {"each", "clove", "can", "pinch", "slice", "bunch"}
METRIC = {"ml", "l", "g", "kg"}

# (unit, ml per unit, smallest amount worth showing in that unit, rounding step)
US_VOLUME_CHAIN = [("cup", 236.588, 0.25, 8), ("tbsp", 14.7868, 1, 4), ("tsp", 4.92892, 0, 4)]
METRIC_VOLUME_CHAIN = [("l", 1000.0, 1, 4), ("ml", 1.0, 0, 1)]
US_WEIGHT_CHAIN = [("lb", 453.592, 1, 4), ("oz", 28.3495, 0, 4)]
METRIC_WEIGHT_CHAIN = [("kg", 1000.0, 1, 4), ("g", 1.0, 0, 1)]


def family(unit):
    if unit in VOLUME_ML:
        return "volume"
    if unit in WEIGHT_G:
        return "weight"
    if unit in COUNT_UNITS:
        return "count:" + unit
    raise ValueError(f"Unknown unit: {unit!r}")


def to_base(qty, unit):
    return qty * (VOLUME_ML.get(unit) or WEIGHT_G.get(unit) or 1.0)


def fmt_number(x, denom):
    f = Fraction(round(x * denom), denom)
    whole, rem = divmod(f.numerator, f.denominator)
    rem_f = Fraction(rem, f.denominator)
    if rem == 0:
        return str(whole), f
    frac = f"{rem_f.numerator}/{rem_f.denominator}"
    return (f"{whole} {frac}" if whole else frac), f


def fmt_amount(total_base, chain):
    """Pick the biggest unit that shows the total cleanly."""
    for unit, size, minimum, denom in chain:
        q = total_base / size
        if q < minimum * 0.99:
            continue
        text, rounded = fmt_number(q, denom)
        last = unit == chain[-1][0]
        if rounded == 0:
            continue
        if last or abs(q - float(rounded)) / q < 0.03:
            return f"{text} {unit}{'s' if unit == 'cup' and rounded > 1 else ''}"
    return f"{total_base:.0f} {chain[-1][0]}"


def merge_ingredients(items):
    totals = defaultdict(lambda: defaultdict(float))
    metric_only = defaultdict(lambda: defaultdict(lambda: True))
    for name, qty, unit in items:
        if qty <= 0:
            raise ValueError("Quantity must be positive")
        fam = family(unit)
        key = name.strip().lower()
        totals[key][fam] += to_base(qty, unit) if not fam.startswith("count") else qty
        if unit not in METRIC:
            metric_only[key][fam] = False

    result = []
    for name in sorted(totals):
        parts = []
        for fam, total in sorted(totals[name].items()):
            if fam == "volume":
                chain = METRIC_VOLUME_CHAIN if metric_only[name][fam] else US_VOLUME_CHAIN
                parts.append(fmt_amount(total, chain))
            elif fam == "weight":
                chain = METRIC_WEIGHT_CHAIN if metric_only[name][fam] else US_WEIGHT_CHAIN
                parts.append(fmt_amount(total, chain))
            else:
                unit = fam.split(":")[1]
                text, _ = fmt_number(total, 4)
                parts.append(text if unit == "each" else f"{text} {unit}")
        result.append((name, parts))
    return result
