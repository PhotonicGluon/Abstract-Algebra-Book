# IMPORTS
from sympy import Poly
from ntru.polynomials import reduce_coeffs, reduce_powers_and_coeffs


# FUNCTIONS
def get_public_key(n: int, p: int, q: int, g: Poly, inverse_q: Poly) -> Poly:
    return reduce_powers_and_coeffs(p * inverse_q * g, n, q)


def encrypt(n: int, p: int, q: int, phi: Poly, public_key: Poly, m: Poly) -> Poly:
    intermediate_poly = p * phi * public_key + m
    return reduce_powers_and_coeffs(intermediate_poly, n, q)


def decrypt(n: int, p: int, q: int, encrypted: Poly, private_key: Poly, inverse_of_f_in_p: Poly) -> Poly:
    a = reduce_powers_and_coeffs(private_key * encrypted, n, q, half_coeff=True)
    b = reduce_coeffs(a, p, half=True)
    return reduce_powers_and_coeffs(inverse_of_f_in_p * b, n, p, half_coeff=True)
