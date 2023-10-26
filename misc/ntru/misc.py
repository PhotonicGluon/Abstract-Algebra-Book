# IMPORTS
import yaml
from sympy import latex, Poly


# FUNCTIONS
def read_params(params_file: str) -> dict:
    with open(params_file, "r") as f:
        contents = yaml.load(f, yaml.Loader)

    return contents


def my_latex(poly: Poly) -> str:
    latex_str = latex(poly)
    return latex_str.replace("{", "").replace("}", "").replace(" x", "x")


def split_into_base_and_power(possible_prime_power: int) -> tuple:
    base = 2
    while possible_prime_power % base != 0 and base * base <= possible_prime_power:
        base += 1

    if possible_prime_power % base != 0:
        return possible_prime_power, 1  # Is a prime

    power = 0
    num = possible_prime_power
    while num % base == 0:
        num //= base
        power += 1

    if num != 1:
        raise ValueError(f"{possible_prime_power} is not a prime power")
    return base, power
