# IMPORTS
from sympy import ZZ, Poly, Symbol, latex
from sympy.polys.galoistools import gf_gcdex, gf_strip

# SETUP
x = Symbol("x")

# CONSTANTS
N = 8  # Maximum number of terms that a polynomial in R can have
MOD = 8  # Modulo to find the inverse for
PRIVATE_KEY = [1, 0, 0, -1, 1]  # Coefficients, in decreasing degree
POLYNOMIAL_G = [1, -1, 0, -1, 1]  # Coefficients, in decreasing degree

# PROCESSING
# Compute inverse polynomial
irreducible = Poly(x**N - 1)
polynomial_f = Poly(PRIVATE_KEY, x)
polynomial_g = Poly(POLYNOMIAL_G, x)

inverse = Poly(gf_gcdex(gf_strip(polynomial_f.all_coeffs()), irreducible.all_coeffs(), MOD, ZZ)[0], x).as_expr()

# Compute public key
raw_pub_key = inverse * Poly(POLYNOMIAL_G, x)
raw_pub_key_coeff = raw_pub_key.all_coeffs()[::-1]

pub_key_coeff = [0 for _ in range(N)]
for deg, coeff in enumerate(raw_pub_key_coeff):
    pub_key_coeff[deg % N] += coeff
for i in range(N):
    pub_key_coeff[i] %= MOD
pub_key_coeff = pub_key_coeff[::-1]
pub_key = Poly(pub_key_coeff, x)

# OUTPUT
print("f(x):")
print(polynomial_f.as_expr())
print(latex(polynomial_f.as_expr()))
print()
print("g(x):")
print(polynomial_g.as_expr())
print(latex(polynomial_g.as_expr()))
print()
print(f"Inverse modulo {MOD}:")
print(inverse)
print(latex(inverse))
print()
print("Public Key:")
print(pub_key.as_expr())
print(latex(pub_key.as_expr()))
