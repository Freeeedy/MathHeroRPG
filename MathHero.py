import random, json
from ValueGenerators import generate_value, generate_free_values, generate_derived_variables
from SolutionsGenerator import generate_sloutions
from sympy import sympify


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
    left = left.replace("tg", "tan")
    right = right.replace("tg", "tan")

    left = sympify(left, locals=values)
    right = sympify(right, locals=values)

    return left, right


template = choose_template("normal")
equation = template["equation"]

values = generate_free_values(template)
values = generate_derived_variables(template, values)

left, right = substitue_values(equation, values)

solutions = generate_sloutions(template, values)

#print(template["equation"])
#print(values)
print(template["method"])

print(left, "=", right)

print(solutions)