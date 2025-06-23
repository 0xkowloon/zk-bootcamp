from mod_exp import mod_exp

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def mod_inverse(value, p):
  if value == 0:
    raise ValueError("0 has no multiplicative inverse")

  if gcd(value, p) != 1:
    raise ValueError("Value and modulus must be coprime")

  return mod_exp(value, p - 2, p)