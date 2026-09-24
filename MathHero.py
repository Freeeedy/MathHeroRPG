import random, json
from ValueGenerators import generate_value, generate_free_values, generate_derived_variables
from SolutionsGenerator import generate_solutions
from sympy import sympify
from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application
)

transformations = standard_transformations + (implicit_multiplication_application,)


with open("templates.json", "r", encoding="utf-8") as f:
    data = json.load(f)


def choose_template(difficulty):
    available = [ #list of available templates
        template
        for template in data["templates"]
        if template["difficulty"] == difficulty
    ]
    return random.choice(available)

def substitue_values(equation, values):
    left, right = equation.split("=")

    left = left.replace("·", "*")
    right = right.replace("·", "*")

    left = left.replace("²", "**2")
    right = right.replace("²", "**2")

    left = left.replace("⁴", "**4")
    right = right.replace("⁴", "**4")

    left = left.replace("tg", "tan")
    right = right.replace("tg", "tan")

    left = parse_expr(
        left,
        local_dict=values,
        transformations=transformations
    )

    right = parse_expr(
        right,
        local_dict=values,
        transformations=transformations
    )

    return left, right


template = choose_template("genius")
equation = template["equation"]

values = generate_free_values(template)
values = generate_derived_variables(template, values)

left, right = substitue_values(equation, values)

solutions = generate_solutions(template, values)

#print(template["equation"])
#print(values)
print(template["method"])

print(left, "=", right)

print(solutions)