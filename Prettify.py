def pretty_equation(left, right):
    equation = f"{left} = {right}"

    replacements = {

        "**2": "²",
        "**3": "³",
        "**4": "⁴",

        "*":"·",

        "sqrt(2)": "√2",
        "sqrt(3)": "√3",
        "sqrt(5)": "√5",
        "sqrt(6)": "√6",

        "sin(x)": "sin(x)",
        "cos(x)": "cos(x)",
        "tan(x)": "tan(x)",
        "cot(x)": "cot(x)",
    }

    for old, new in replacements.items():
        equation = equation.replace(old, new)

    return equation