from py_ecc.bn128 import G1, G2, pairing, multiply, curve_order, field_modulus, FQ, FQ2, FQ12, neg

# I manually picked these numbers by hand to get the test to pass
# -30 * 5 + 5 * 6 + (8 + 3 + 1) * 7 + 4 * 9 = 0

alpha1 = multiply(G1, 5)
print("alpha1", alpha1)
beta2 = multiply(G2, 6)
print("beta2", beta2)
gamma2 = multiply(G2, 7)
print("gamma2", gamma2)
delta2 = multiply(G2, 9)
print("delta2", delta2)

A1 = multiply(G1, 30)
print("A1", neg(A1))
B2 = multiply(G2, 5)
print("B2", B2)
C1 = multiply(G1, 4)
print("C1", C1)

x1 = 8
x2 = 3
x3 = 1
s = (x1 + x2 + x3) % curve_order
X1 = multiply(G1, s)
print("X1", X1)

result = (
    pairing(B2, neg(A1)) *
    pairing(beta2, alpha1) *
    pairing(gamma2, X1) *
    pairing(delta2, C1)
)

print("Pairing check passes:", result == FQ12.one())
