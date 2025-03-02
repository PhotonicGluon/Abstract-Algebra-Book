# IMPORTS
from sympy import Poly
from polynomials import reduce_coeffs, reduce_powers_and_coeffs


# FUNCTIONS
def get_public_key(n: int, p: int, q: int, g: Poly, inverse_q: Poly) -> Poly:
    return reduce_powers_and_coeffs(p * inverse_q * g, n, q)


def encrypt(n: int, p: int, q: int, phi: Poly, public_key: Poly, m: Poly) -> Poly:
    intermediate_poly = p * phi * public_key + m
    return reduce_powers_and_coeffs(intermediate_poly, n, q)


def decrypt(n: int, p: int, q: int, encrypted: Poly, private_key: Poly, inverse_of_f_in_p: Poly) -> Poly:
    a = reduce_powers_and_coeffs(private_key * encrypted, n, q, half_coeff=True)
    # print("a(x)", a.as_expr())
    b = reduce_coeffs(a, p, half=True)
    # print("b(x)", b.as_expr())
    almost_message = inverse_of_f_in_p * b
    # print(almost_message.as_expr())
    return reduce_powers_and_coeffs(almost_message, n, p, half_coeff=True)
