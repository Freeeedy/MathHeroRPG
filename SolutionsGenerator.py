import re
import sympy as sp

# ---------------------------------------------------------------------------
# Instead of one hand-written solver per "method" name, we read the
# `construction` block that already exists on every template:
#
#   "target":            e.g. "sin(x)", "cos(n*x)", "tg(x + phi)", "sin^2(x)"
#   "guaranteed_values"  or
#   "guaranteed_roots":  the value(s) the target is known to equal
#   "guaranteed_branches": (only used by double_angle_factoring) a list of
#                          independent "lhs = rhs" equations to union together
#
# Every method in templates.json reduces to one of a handful of shapes:
#   func(coeff*x + phase) = value          (direct / linear / multi-angle / phase-shift)
#   func(coeff*x + phase)^2 = value        (squared -> value's sqrt, both signs)
#   union of several such equations         (quadratic-substitution roots, biquadratic,
#                                            factoring branches)
#
# so a single generic engine can solve all of them.
# ---------------------------------------------------------------------------

FUNC_ALIASES = {
    "sin": "sin",
    "cos": "cos",
    "tg": "tan",
    "tan": "tan",
    "cotg": "cot",
    "cot": "cot",
}

TARGET_RE = re.compile(r"(sin|cos|cotg|cot|tg|tan)\((.*)\)")
PHASE_RE = re.compile(r"([+-])(\w+)$")
COEFF_RE = re.compile(r"(\w+)\*x$")


def _parse_target(target_str):
    """Break a construction 'target' string into (func, coeff, phase, squared)."""
    s = target_str.strip()
    squared = "^2" in s or "\u00b2" in s
    s = s.replace("^2", "").replace("\u00b2", "")

    m = TARGET_RE.match(s.strip())
    if not m:
        raise ValueError(f"Cannot parse target: {target_str}")

    func_name = FUNC_ALIASES[m.group(1)]
    inner = m.group(2).replace(" ", "")

    phase_name, phase_sign = None, 1
    pm = PHASE_RE.search(inner)
    if pm and pm.group(2) != "x":
        phase_sign = 1 if pm.group(1) == "+" else -1
        phase_name = pm.group(2)
        inner = inner[: pm.start()]

    if inner == "x":
        coeff = 1
    else:
        cm = COEFF_RE.match(inner)
        if not cm:
            raise ValueError(f"Cannot parse coefficient in target: {target_str}")
        coeff = cm.group(1)

    return {
        "func": func_name,
        "coeff": coeff,
        "phase_name": phase_name,
        "phase_sign": phase_sign,
        "squared": squared,
    }


def _coeff_value(coeff, values):
    if coeff == 1:
        return 1
    if isinstance(coeff, str) and coeff.isdigit():
        return int(coeff)
    return values[coeff]


def _base_families(func_name, value):
    """u = offset + period*k solves func(u) = value; return the (offset, period) branches."""
    if func_name == "sin":
        base = sp.asin(value)
        return [(base, 2 * sp.pi), (sp.pi - base, 2 * sp.pi)]
    if func_name == "cos":
        base = sp.acos(value)
        return [(base, 2 * sp.pi), (-base, 2 * sp.pi)]
    if func_name == "tan":
        base = sp.atan(value)
        return [(base, sp.pi)]
    if func_name == "cot":
        base = sp.acot(value)
        return [(base, sp.pi)]
    raise ValueError(f"Unknown function: {func_name}")


def _solve_equation(func_name, coeff, phase, value):
    """Solve func(coeff*x + phase) = value for x in [0, 2*pi)."""
    pi_f = float(sp.pi)
    eps = 1e-6
    seen = set()
    found = []

    for offset, period in _base_families(func_name, value):
        # generous k-range: cheap, and guarantees full coverage for the
        # small integer coefficients (<=4) used across all templates
        for k in range(-20, 21):
            u = offset + period * k
            x = (u - phase) / coeff
            x_num = float(x)

            if -eps <= x_num < 2 * pi_f - eps:
                x_num = max(0.0, x_num)
                key = round(x_num, 6)
                if key not in seen:
                    seen.add(key)
                    found.append(sp.simplify(x))

    return found


def _solve_target(target_info, value, values):
    coeff = _coeff_value(target_info["coeff"], values)
    phase = 0
    if target_info["phase_name"] is not None:
        phase = target_info["phase_sign"] * values[target_info["phase_name"]]

    if target_info["squared"]:
        sq = sp.sqrt(value)
        candidates = [sq] if sq == 0 else [sq, -sq]
        solutions = []
        for c in candidates:
            solutions.extend(_solve_equation(target_info["func"], coeff, phase, c))
        return solutions

    return _solve_equation(target_info["func"], coeff, phase, value)


def _eval_entry(entry, values):
    """guaranteed_values/roots entries are small expressions like 'v', '-v', 'w'."""
    if isinstance(entry, str):
        return sp.sympify(entry, locals=values)
    return entry


def generate_solutions(template, values):
    construction = template["construction"]
    solutions = []

    if "guaranteed_branches" in construction:
        # e.g. double_angle_factoring: ["cos(x) = 0", "sin(x) = v"] - independent
        # equations whose solution sets get unioned together
        for branch in construction["guaranteed_branches"]:
            lhs, rhs = branch.split("=")
            target_info = _parse_target(lhs.strip())
            rhs_value = sp.sympify(rhs.strip(), locals=values)
            solutions.extend(_solve_target(target_info, rhs_value, values))
    else:
        target_info = _parse_target(construction["target"])
        entries = (
            construction.get("guaranteed_values")
            or construction.get("guaranteed_roots")
            or []
        )
        for entry in entries:
            value = _eval_entry(entry, values)
            solutions.extend(_solve_target(target_info, value, values))

    # dedupe (numerically) and sort
    unique = []
    seen = set()
    for sol in solutions:
        key = round(float(sol), 6)
        if key not in seen:
            seen.add(key)
            unique.append(sp.simplify(sol))

    return sorted(unique, key=lambda s: float(s))