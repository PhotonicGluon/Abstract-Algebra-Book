# IMPORTS
from sympy import ZZ, Poly, Symbol, latex
from sympy.polys.galoistools import gf_gcdex, gf_strip

# SETUP
x = Symbol("x")

# CONSTANTS
N = 6  # Maximum number of terms that a polynomial in R can have
MOD = 16  # Modulo to find the inverse for
POLYNOMIAL = [1, 1, 0, -1]  # Coefficients, in decreasing degree

# PROCESSING
irreducible = Poly(x**N - 1)
polynomial = Poly(POLYNOMIAL, x)

inverse = Poly(gf_gcdex(gf_strip(polynomial.all_coeffs()), irreducible.all_coeffs(), MOD, ZZ)[0], x).as_expr()

print("Original Polynomial:")
print(polynomial.as_expr())
print(latex(polynomial.as_expr()))
print()
print(f"Inverse modulo {MOD}:")
print(inverse)
print(latex(inverse))
