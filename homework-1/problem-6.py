# Suppose we have the following polynomials:

# p(x)=52x^2+24x+61
# q(x)=40x^2+40x+58

# What is p(x) + q(x)? What is p(x) * q(x)?

# Use the `galois` library in Python to find the roots of p(x) and q(x).

# What are the roots of p(x)q(x)?

# p(x) + q(x) = 92x^2 + 64x + 119

# p(x) * q(x) = 2080x^4 + 3040x^3 + 6416x^2 + 3832x + 3538

import galois

p = 71
GF = galois.GF(p)

p = galois.Poly([52, 24, 61], field=GF)  # 52x^2 + 24x + 61
q = galois.Poly([40, 40, 58], field=GF)  # 40x^2 + 40x + 58

print("p(x) =", p)
print("q(x) =", q)

p_times_q = p * q

print("p(x) * q(x) =", p_times_q)

print("roots of p(x) =", p.roots())
print("roots of q(x) =", q.roots())
print("roots of p(x) * q(x) =", p_times_q.roots())