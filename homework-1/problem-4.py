from mod_inverse import mod_inverse

# The inverse of a 2 x 2 matrix $A$ is

# $$
# A^{-1}=\frac{1}{\text{det}}\begin{bmatrix}d & -b\\-c & a\end{bmatrix}
# $$

# where $A$ is

# $$
# A = \begin{bmatrix}a & b\\c & d\end{bmatrix}
# $$

# And the determinant det is

# $$
# \text{det}=a \times d-b\times c
# $$

# Compute the inverse of the following matrix in the finite field:

# $$
# \begin{bmatrix}1 & 1\\1 & 4\end{bmatrix}
# $$

# Verify your answer by checking that

# $$
# AA^{-1}=I
# $$

# Where $I$ is the identity matrix.

p = 71

a = 1
b = 1
c = 1
d = 4

matrix = [
  [a, b],
  [c, d]
]

det = (a * d - b * c) % p

if det == 0:
  raise ValueError("Matrix is not invertible")

mod_inverse_of_det = mod_inverse(det, p)

inverse_matrix = [
  [d * mod_inverse_of_det % p, mod_inverse(-b, p) * mod_inverse_of_det % p],
  [mod_inverse(-c, p) * mod_inverse_of_det % p, a * mod_inverse_of_det % p]
]

inverse_a = inverse_matrix[0][0]
inverse_b = inverse_matrix[0][1]
inverse_c = inverse_matrix[1][0]
inverse_d = inverse_matrix[1][1]

identity_matrix = [
  [(a * inverse_a + b * inverse_c) % p, (a * inverse_b + b * inverse_d) % p],
  [(c * inverse_a + d * inverse_c) % p, (c * inverse_b + d * inverse_d) % p]
]

print(identity_matrix)

assert(identity_matrix[0][0] == 1)
assert(identity_matrix[0][1] == 0)
assert(identity_matrix[1][0] == 0)
assert(identity_matrix[1][1] == 1)