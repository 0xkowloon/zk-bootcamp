# Given an R1CS of the form

# $$
# L\mathbf{\vec{[s]_1}}\odot R\mathbf{\vec{[s]_2}} = O\mathbf{\vec{[s]}_{1}}\odot\vec{[G_2]_2}
# $$

# Where L, R, and O are n x m matrices of field elements and **s** is a vector of G1, G2, or G1 points

# Write python code that verifies the formula.

# You can check the equality of G12 points in Python this way:

# ```python
# a = pairing(multiply(G2, 5), multiply(G1, 8))
# b = pairing(multiply(G2, 10), multiply(G1, 4))
# eq(a, b)
# ```

# **Hint:** Each row of the matrices is a separate pairing.

# **Hint:** When you get **s** encrypted with both G1 and G2 generators, you don’t know whether or not they have the same discrete logarithm. However, it is straightforward to check using another equation. Figure out how to discover if sG1 == sG2 if you are given the elliptic curve points but not s.

# Solidity cannot multiply G2 points, do this assignment in Python.

import numpy as np
import random
from py_ecc.bn128 import add, multiply, pairing, eq, G1, G2, neg
from py_ecc.fields import bn128_FQ, bn128_FQ2

L = np.array([
  [0,0,3,0,0,0],
  [0,0,0,0,1,0],
  [0,0,5,0,0,0]
])

R = np.array([
  [0,0,1,0,0,0],
  [0,0,0,1,0,0],
  [0,0,0,1,0,0]
])

O = np.array([
  [0,0,0,0,1,0],
  [0,0,0,0,0,1],
  [-3,1,1,2,0,-1]
])

x = random.randint(1,1000)
y = random.randint(1,1000)

out = 3 * x * x * y + 5 * x * y - x - 2 * y + 3
v1 = 3*x*x
v2 = v1 * y
w = np.array([1, out, x, y, v1, v2])

wG1 = [multiply(G1, w_i) for w_i in w]
wG2 = [multiply(G2, w_i) for w_i in w]

def matmul(constraint, witness):
  assert len(constraint) == len(witness), "constraint and witness must have the same length"
  result = multiply(witness[0], 0)
  for i in range(len(constraint)):
    if constraint[i] > 0:
      result = add(result, multiply(witness[i], constraint[i]))
    elif constraint[i] < 0:
      result = add(result, neg(multiply(witness[i], -constraint[i])))

  return result

def verify_r1cs(L, Ls, R, Rs, O, Os):
  number_of_constraints = len(L)
  assert number_of_constraints == len(R) == len(O), "L, R, and O must have the same number of constraints"

  for i in range(number_of_constraints):
    assert eq(pairing(G2, Ls[i]), pairing(Rs[i], G1)), "witness is not the same"
    Lw = matmul(L[i], Ls)
    Rw = matmul(R[i], Rs)
    Ow = matmul(O[i], Os)
    assert eq(pairing(Rw, Lw), pairing(G2, Ow)), "system contains an inequality"

verify_r1cs(L, wG1, R, wG2, O, wG1)