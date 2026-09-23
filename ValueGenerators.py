import random
from sympy import Rational, sqrt, pi

def standard_sine_value():
    values = [
        0,
        Rational(1, 2),
        Rational(-1, 2),
        sqrt(2) / 2,
        -sqrt(2) / 2,
        sqrt(3) / 2,
        -sqrt(3) / 2,
        1,
        -1
    ]

    return random.choice(values)

def standard_cosine_value():
    values = [
        0,
        Rational(1, 2),
        Rational(-1, 2),
        sqrt(2) / 2,
        -sqrt(2) / 2,
        sqrt(3) / 2,
        -sqrt(3) / 2,
        1,
        -1
    ]

    return random.choice(values)

def standard_tangent_value():
    values = [
        0,
        1,
        -1,
        sqrt(3) / 3,
        -sqrt(3) / 3,
        sqrt(3),
        -sqrt(3)
    ]

    return random.choice(values)

def standard_cotangent_value():
    values = [
        0,
        1,
        -1,
        sqrt(3) / 3,
        -sqrt(3) / 3,
        sqrt(3),
        -sqrt(3)
    ]

    return random.choice(values)

def positive_standard_sine_value():
    values = [
        Rational(1, 2),
        sqrt(2) / 2,
        sqrt(3) / 2,
        1
    ]

    return random.choice(values)

def positive_standard_cosine_value():
    values = [
        Rational(1, 2),
        sqrt(2) / 2,
        sqrt(3) / 2,
        1
    ]

    return random.choice(values)

def positive_standard_tangent_value():
    values = [
        1,
        sqrt(3) / 3,
        sqrt(3)
    ]

    return random.choice(values)

def nonzero_integer():
    values = [
        -6, -5, -4, -3, -2, -1,
        1, 2, 3, 4, 5, 6
    ]

    return random.choice(values)

def integer():
    values = [
        -6, -5, -4, -3, -2, -1,
        0,
        1, 2, 3, 4, 5, 6
    ]

    return random.choice(values)

def rational_in_unit_interval():
    values = [
        0,
        Rational(1, 2),
        Rational(-1, 2),
        1,
        -1
    ]

    return random.choice(values)

def positive_integer():
    values = [
        1,
        2,
        3,
        4,
        5,
        6
    ]

    return random.choice(values)

def standard_angle():
    values = [
        0,
        pi / 6,
        pi / 4,
        pi / 3,
        pi / 2,
        2 * pi / 3,
        3 * pi / 4,
        5 * pi / 6,
        pi
    ]

    return random.choice(values)

def standard_sine_magnitude():
    values = [
        0,
        Rational(1, 2),
        sqrt(2) / 2,
        sqrt(3) / 2,
        1
    ]

    return random.choice(values)

def standard_cosine_magnitude():
    values = [
        0,
        Rational(1, 2),
        sqrt(2) / 2,
        sqrt(3) / 2,
        1
    ]

    return random.choice(values)

def standard_sine_squared_value():
    values = [
        0,
        Rational(1, 4),
        Rational(1, 2),
        Rational(3, 4),
        1
    ]

    return random.choice(values)

def standard_cosine_squared_value():
    values = [
        0,
        Rational(1, 4),
        Rational(1, 2),
        Rational(3, 4),
        1
    ]

    return random.choice(values)

def standard_tangent_squared_value():
    values = [
        0,
        Rational(1, 3),
        1,
        3
    ]

    return random.choice(values)

def amplitude():
    values = [
        1,
        2,
        3,
        4,
        5
    ]

    return random.choice(values)

VALUE_GENERATORS = {
    "standard_sine_value": standard_sine_value,
    "standard_cosine_value": standard_cosine_value,
    "standard_tangent_value": standard_tangent_value,
    "standard_cotangent_value": standard_cotangent_value,
    "positive_standard_sine_value": positive_standard_sine_value,
    "positive_standard_cosine_value": positive_standard_cosine_value,
    "positive_standard_tangent_value": positive_standard_tangent_value,
    "nonzero_integer": nonzero_integer,
    "integer": integer,
    "rational_in_unit_interval": rational_in_unit_interval,
    "positive_integer": positive_integer,
    "standard_angle": standard_angle,
    "standard_sine_magnitude": standard_sine_magnitude,
    "standard_cosine_magnitude": standard_cosine_magnitude,
    "standard_sine_squared_value": standard_sine_squared_value,
    "standard_cosine_squared_value": standard_cosine_squared_value,
    "standard_tangent_squared_value": standard_tangent_squared_value,
    "amplitude": amplitude,
}

def generate_value(variable):
    value_type = variable["type"]

    if value_type not in VALUE_GENERATORS:
        raise ValueError(f"Unknown value type: {value_type}")

    return VALUE_GENERATORS[value_type]()

def generate_free_values(template):
    values = {}

    for name, variable in template["variables"].items():
        if variable["role"] == "free":
            values[name] = generate_value(variable)

    return values

def generate_derived_variables(template, values):
    for name, variable in template["variables"].items():
        if variable["role"] == "derived":
            values[name] = eval(variable["formula"], {}, values) #applies the named values to the formula with the named variables 

    return values
