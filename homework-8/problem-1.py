# Create a graph with 2 nodes and 1 edge and write constraints for a 3-coloring. T the 3-coloring to a rank 1 constraint system. If you forgot how to do this, consult the chapter on arithmetic circuits.

# We have 2 nodes n1 and n2

# Each node must be assigned exactly one of 3 colors (red, green, blue).
# We encode this using binary indicator variables:

# Let the color of each node ni be represented by 3 variables:

# xi1 = 1 if color is red else 0
# xi2 = 1 if color is green else 0
# xi3 = 1 if color is blue else 0

# xi1, xi2, and xi3 all have to be 0 or 1.

# ```
# xij * (xij - 1) = 0 for j in 1..3
# ```

# Only 1 of xij can be 1. It is the node's color.

# ```
# xi1 + xi2 + xi3 = 1
# ```

# The color of n1 and n2 cannot be the same, which means n1 * n2 cannot be equal to 1. As long as one of the two is 0, the product is 0.

# ```
# xi1 * xi2 = 0
# ```

# The witness should contain all 6 variables and the constant 1

# [1,x11,x12,x13,x21,x22,x23]

# Each row represents one constraint:

# 1. (x11 + x12 + x13) * 1 = 1
# 2. (x21 + x22 + x23) * 1 = 1
# 3. x11 * (x11 - 1) = 0
# 4. x12 * (x12 - 1) = 0
# 5. x13 * (x13 - 1) = 0
# 6. x21 * (x21 - 1) = 0
# 7. x22 * (x22 - 1) = 0
# 8. x23 * (x23 - 1) = 0
# 9. x11 * x21 = 0
# 10. x12 * x22 = 0
# 11. x13 * x23 = 0

L = [
  [0,1,1,1,0,0,0],
  [0,0,0,0,1,1,1],
  [0,1,0,0,0,0,0],
  [0,0,1,0,0,0,0],
  [0,0,0,1,0,0,0],
  [0,0,0,0,1,0,0],
  [0,0,0,0,0,1,0],
  [0,0,0,0,0,0,1],
  [0,1,0,0,0,0,0],
  [0,0,1,0,0,0,0],
  [0,0,0,1,0,0,0],
]

R = [
  [1,0,0,0,0,0,0],
  [1,0,0,0,0,0,0],
  [-1,1,0,0,0,0,0],
  [-1,0,1,0,0,0,0],
  [-1,0,0,1,0,0,0],
  [-1,0,0,0,1,0,0],
  [-1,0,0,0,0,1,0],
  [-1,0,0,0,0,0,1],
  [0,0,0,0,1,0,0],
  [0,0,0,0,0,1,0],
  [0,0,0,0,0,0,1],
]

O = [
  [1,0,0,0,0,0,0],
  [1,0,0,0,0,0,0],
  [0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0],
]

import numpy as np

def verify_r1cs(A, B, C, w):
    result = np.matmul(C, w) == np.multiply(np.matmul(A, w), np.matmul(B, w))
    assert result.all(), "system contains an inequality"

try:
    w = [1, 1, 0, 0, 1, 0, 0]
    verify_r1cs(L, R, O, w)
except AssertionError:
    print("Matching red")

try:
    w = [1, 0, 1, 0, 0, 1, 0]
    verify_r1cs(L, R, O, w)
except AssertionError:
    print("Matching green")

try:
    w = [1, 0, 0, 1, 0, 0, 1]
    verify_r1cs(L, R, O, w)
except AssertionError:
    print("Matching blue")

# Red and green
w = [1, 1, 0, 0, 0, 1, 0]
verify_r1cs(L, R, O, w)

# Red and blue
w = [1, 1, 0, 0, 0, 0, 1]
verify_r1cs(L, R, O, w)

# Green and blue
w = [1, 0, 1, 0, 0, 0, 1]
verify_r1cs(L, R, O, w)

# Green and red
w = [1, 0, 1, 0, 1, 0, 0]
verify_r1cs(L, R, O, w)

# Blue and green
w = [1, 0, 0, 1, 0, 1, 0]
verify_r1cs(L, R, O, w)

# Blue and red
w = [1, 0, 0, 1, 1, 0, 0]
verify_r1cs(L, R, O, w)
