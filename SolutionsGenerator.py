import sympy as sp

def solve_tangent(v):
    base = sp.atan(v)

    solutions = []

    for k in range(-2, 2 + 1):
        x = sp.sympify(base + k * sp.pi)

        if 0 <= x < 2 * sp.pi:
            solutions.append(x)

    return solutions

def solve_cotangent(v):
    base = sp.acot(v)

    solutions = []

    for k in range(-2, 2 + 1):
        x = sp.sympify(base + k * sp.pi)

        if 0 <= x < 2 * sp.pi:
            solutions.append(x)

    return solutions

def solve_sine(v):
    base = sp.asin(v)

    solutions = []

    for k in range(-2, 3):
        x1 = sp.simplify(base + 2 * k * sp.pi)
        x2 = sp.simplify(sp.pi - base + 2 * k * sp.pi)

        if 0 <= x1 < 2 * sp.pi and x1 not in solutions:
            solutions.append(x1)

        if 0 <= x2 < 2 * sp.pi and x2 not in solutions:
            solutions.append(x2)

    return sorted(solutions, key=lambda x: float(x))

def solve_cosine(v):
    base = sp.acos(v)

    solutions = []

    for k in range(-2, 3):
        x1 = sp.simplify(base + 2 * k * sp.pi)
        x2 = sp.simplify(-base + 2 * k * sp.pi)

        if 0 <= x1 < 2 * sp.pi and x1 not in solutions:
            solutions.append(x1)

        if 0 <= x2 < 2 * sp.pi and x2 not in solutions:
            solutions.append(x2)

    return sorted(solutions, key=lambda x: float(x))

def solve_linear_isolation_sin(values):
    a = values["a"]
    b = values["b"]

    v = -b / a

    return solve_sine(v)

SOLUTION_GENERATORS = {
    "linear_isolation_tan": solve_tangent,
    "linear_isolation_sin": solve_sine,
    "linear_isolation_cos": solve_cosine,
    "linear_isolation_cot": solve_cotangent,
    "direct_sine": solve_sine,
    "direct_cosine": solve_cosine,
    "direct_tangent": solve_tangent,
    "direct_cotangent": solve_cotangent,
    "linear_isolation_sin": solve_linear_isolation_sin
}


def generate_sloutions(template, values):
    method = template["method"]

    if method not in SOLUTION_GENERATORS:
        raise ValueError(f"Unknown solution method: {method}")

    return SOLUTION_GENERATORS[method](values["v"])