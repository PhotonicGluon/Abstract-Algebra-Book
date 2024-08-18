# IMPORTS
from sympy import Poly
from sympy.abc import x

from core_functions import get_public_key, encrypt, decrypt
from misc import read_params, split_into_base_and_power, my_latex
from polynomials import almost_inv_poly_for_prime, almost_inv_poly_for_prime_power

# CONSTANTS
PARAMS_FILE = "params.yml"


# SETUP
# Read parameters
params = read_params(PARAMS_FILE)

n = params["N"]
p = params["p"]
q = params["q"]
irreducible = Poly(x**params["N"] - 1)
polynomial_f = Poly(params["private_key"], x)
polynomial_g = Poly(params["polynomial_g"], x)
encoding_fuzz = Poly(params["encoding_fuzz"], x)
message = Poly(params["message_polynomial"], x)

# Split q into its base and power
q_base, q_power = split_into_base_and_power(q)

# PROCESSING
# Compute inverse polynomials
inverse_p = almost_inv_poly_for_prime(polynomial_f, n, p)
inverse_q = almost_inv_poly_for_prime_power(polynomial_f, n, q_base, q_power)

# Compute public key
public_key = get_public_key(n, p, q, polynomial_g, inverse_q)

# Create encrypted message
encrypted = encrypt(n, p, q, encoding_fuzz, public_key, message)

# Attempt decryption
decrypted = decrypt(n, p, q, encrypted, polynomial_f, inverse_p)

# OUTPUT
print("f(x):")
print(polynomial_f.as_expr())
print(my_latex(polynomial_f.as_expr()))
print()
print("g(x):")
print(polynomial_g.as_expr())
print(my_latex(polynomial_g.as_expr()))
print()
print("phi(x):")
print(encoding_fuzz.as_expr())
print(my_latex(encoding_fuzz.as_expr()))
print()
print("Message polynomial:")
print(message.as_expr())
print(my_latex(message.as_expr()))
print()

print(f"Inverse modulo {p}:")
print(inverse_p.as_expr())
print(my_latex(inverse_p.as_expr()))
print()
print(f"Inverse modulo {q}:")
print(inverse_q.as_expr())
print(my_latex(inverse_q.as_expr()))
print()

print("Public Key:")
print(public_key.as_expr())
print(my_latex(public_key.as_expr()))
print()

print("Encrypted:")
print(encrypted.as_expr())
print(my_latex(encrypted.as_expr()))
print()

print("Decrypted:")
print(decrypted.as_expr())
print(my_latex(decrypted.as_expr()))
print()

print("Is transmission successful?")
print("Yes" if message == decrypted else "No")
