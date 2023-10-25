# IMPORTS
from sympy import div, Poly
from sympy.core.numbers import NegativeInfinity
from sympy.abc import x


# FUNCTIONS
def reduce_coeffs(poly: Poly, mod: int, half=False) -> Poly:  # `half` refers to restricting coefficients to 1/2 of `mod`
    coeffs = poly.all_coeffs()
    reduced_coeffs = []
    for coeff in coeffs:
        temp = coeff % mod
        if half and temp > mod // 2:
            temp -= mod
        reduced_coeffs.append(temp)

    return Poly(reduced_coeffs, x)


def reduce_powers(poly: Poly, mod: int) -> Poly:
    return poly % Poly(x ** mod - 1)


def reduce_powers_and_coeffs(poly: Poly, degree_mod: int, coeff_mod: int, half_coeff=False) -> Poly:
    return reduce_coeffs(reduce_powers(poly, degree_mod), coeff_mod, half=half_coeff)


def almost_inv_poly_for_prime(polynomial: Poly, n: int, p: int):
    """
    See https://ntru.org/f/tr/tr014v1.pdf, page 3
    """

    k = 0
    b = Poly([1], x)
    c = Poly([0], x)
    f = polynomial
    g = Poly(x ** n - 1)

    import time
    while True:
        if isinstance(f.degree(), NegativeInfinity):
            raise ValueError(f"Polynomial not invertible using polynomials of degree smaller than {n} and modulo {p}")

        while f.all_coeffs()[-1] == 0:
            f = div(f, x)[0]
            c *= x
            k += 1

        if f.degree() == 0:
            b = pow(f.all_coeffs()[-1], -1, p) * b
            b = reduce_coeffs(b, p)

            power_to_multiply = (n - k) % n
            return reduce_powers(x ** power_to_multiply * b, n)

        if f.degree() < g.degree():
            f, g = g, f
            b, c = c, b

        u = f.all_coeffs()[-1] * pow(g.all_coeffs()[-1], -1, p) % p
        f = reduce_coeffs(f - u * g, p)
        b = reduce_coeffs(b - u * c, p)


def almost_inv_poly_for_prime_power(polynomial: Poly, n: int, p: int, r: int) -> Poly:
    """
    See https://ntru.org/f/tr/tr014v1.pdf, page 2
    """

    inverse = almost_inv_poly_for_prime(polynomial, n, p)

    target = p ** r
    q = p
    while q < target:
        q *= q
        inverse = reduce_powers_and_coeffs(inverse * (2 - polynomial * inverse), n, q)

    return reduce_coeffs(inverse, target)
