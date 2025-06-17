# What is Lagrange interpolation and what does it do?

# Find a polynomial that crosses through the points (0, 1), (1, 2), (2, 1).

# Use this Stackoverflow answer as a starting point: https://stackoverflow.com/a/73434775

# Good explanation of Lagrange interpolation: https://www.youtube.com/watch?v=bzp_q7NDdd4

# Lagrange interpolation is a method in numerical analysis and algebra for finding a polynomial that exactly passes through a given set of points.

import galois

GF = galois.GF(71)

x = GF([0, 1, 2])
y = GF([1, 2, 1])

f = galois.lagrange_poly(x, y)

print(f)

assert f(0) == 1
assert f(1) == 2
assert f(2) == 1