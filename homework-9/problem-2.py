# Alice and Bob have matrices A and B. They want to know if, for some v, that
# A v = B v
# Here, the matrices A and B have n rows and m columns.
# For example, let
# A = ( 9 4 5 )
#     ( 8 3 4 )
#     ( 7 9 11 )
# B = ( 2 4 6 )
#     ( 1 3 5 )
#     ( 7 9 11 )
# v = ( 1 )
#     ( 3 )
#     ( 7 )
# Alice and Bob could compute and publish A v and B v respectively, but that would not be succinct.
# Instead, Alice and Bob doe Lagrange interpolation on the columns of A and B, turning them into m polynomials. That is, A gets turned into
# u1(x), u2(x), u3(x)
# and B gets turned into
# v1(x), v2(x), v3(x)
# Each of the u_i ... u_m are polynomials formed by taking a column from the matrix and running lagrange interpolation on it against x s = [1,2,3]. For example, u1(x) is computed as:
# u1 = lagrange([1,2,3], [9,8,7])
# Alice can turn the three polynomials into a single polynomial by doing:
# q(x) = u1(x) r1 + u2(x) r2 + u3(x) r3
# In the example above, v1 = 1, v2 = 3, v3 = 7. Now Alice has turned her matrix and vector into a single polynomial.
# Bob can compute a single polynomial in the same manner.
# They can then check that the polynomials created below are equal by using the Schwartz-Zippel Lemma as before:
# 1 * u1(x) + 3 * u2(x) + 7 * u3(x) = 1 * v1(x) + 3 * v2(x) + 7 * v3(x)
# Alice                              Bob
# Do not worry for now about whether they do their computations honestly.
# Write code that will accomplish this algorithm for arbitrary-sized matrices of reasonable size.

import galois
import numpy as np
import random

from py_ecc.bn128 import field_modulus
field_modulus = 1229

GF = galois.GF(field_modulus)

def lagrange_poly(xs, ys):
  return galois.lagrange_poly(xs, ys)

def is_same_matrix(A, B, v):
  row, col = A.shape

  if row != B.shape[0] or col != B.shape[1]:
    return False

  if len(v) != col:
    raise ValueError("v must have the same number of rows as A and B")

  xs = GF(np.arange(1, col + 1))

  p1 = [lagrange_poly(xs, A[i, :]) for i in range(row)]
  p2 = [lagrange_poly(xs, B[i, :]) for i in range(row)]

  u = GF(random.randint(0, field_modulus - 1))

  lhs = sum([p1[i](u) * v[i] for i in range(col)], GF(0))
  rhs = sum([p2[i](u) * v[i] for i in range(col)], GF(0))

  return lhs == rhs

# Test cases for is_same_matrix function
def test_is_same_matrix():
    print("Testing is_same_matrix function...")

    # Test 1: Same matrices should return True
    A = GF(np.array([[9, 4, 5], [8, 3, 4], [7, 9, 11]]))
    B = GF(np.array([[9, 4, 5], [8, 3, 4], [7, 9, 11]]))
    v = GF(np.array([1, 3, 7]))
    result = is_same_matrix(A, B, v)
    print(f"Test 1 - Same matrices: {result}")
    assert result == True, "Same matrices should return True"

    # Test 2: Different matrices should return False
    A = GF(np.array([[9, 4, 5], [8, 3, 4], [7, 9, 11]]))
    B = GF(np.array([[2, 4, 6], [1, 3, 5], [7, 9, 11]]))
    v = GF(np.array([1, 3, 7]))
    result = is_same_matrix(A, B, v)
    print(f"Test 2 - Different matrices: {result}")
    assert result == False, "Different matrices should return False"

    # Test 3: Different dimensions should return False
    A = GF(np.array([[9, 4, 5], [8, 3, 4], [7, 9, 11]]))
    B = GF(np.array([[9, 4], [8, 3], [7, 9]]))
    v = GF(np.array([1, 3, 7]))
    result = is_same_matrix(A, B, v)
    print(f"Test 3 - Different dimensions: {result}")
    assert result == False, "Different dimensions should return False"

    # Test 4: Vector length mismatch should raise ValueError
    A = GF(np.array([[9, 4, 5], [8, 3, 4], [7, 9, 11]]))
    B = GF(np.array([[9, 4, 5], [8, 3, 4], [7, 9, 11]]))
    v = GF(np.array([1, 3]))  # Wrong length
    try:
        result = is_same_matrix(A, B, v)
        print("Test 4 - Vector length mismatch: ERROR - should have raised ValueError")
        assert False, "Should have raised ValueError"
    except ValueError:
        print("Test 4 - Vector length mismatch: PASS - correctly raised ValueError")

    # Test 5: 2x2 matrices
    A = GF(np.array([[1, 2], [3, 4]]))
    B = GF(np.array([[1, 2], [3, 4]]))
    v = GF(np.array([5, 6]))
    result = is_same_matrix(A, B, v)
    print(f"Test 5 - 2x2 same matrices: {result}")
    assert result == True, "2x2 same matrices should return True"

    # Test 6: 2x2 different matrices
    A = GF(np.array([[1, 2], [3, 4]]))
    B = GF(np.array([[1, 2], [3, 5]]))
    v = GF(np.array([5, 6]))
    result = is_same_matrix(A, B, v)
    print(f"Test 6 - 2x2 different matrices: {result}")
    assert result == False, "2x2 different matrices should return False"

    # Test 7: 1x1 matrices
    A = GF(np.array([[42]]))
    B = GF(np.array([[42]]))
    v = GF(np.array([7]))
    result = is_same_matrix(A, B, v)
    print(f"Test 7 - 1x1 same matrices: {result}")
    assert result == True, "1x1 same matrices should return True"

    # Test 8: 1x1 different matrices
    A = GF(np.array([[42]]))
    B = GF(np.array([[43]]))
    v = GF(np.array([7]))
    result = is_same_matrix(A, B, v)
    print(f"Test 8 - 1x1 different matrices: {result}")
    assert result == False, "1x1 different matrices should return False"

    # Test 9: Zero matrices
    A = GF(np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]]))
    B = GF(np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]]))
    v = GF(np.array([1, 2, 3]))
    result = is_same_matrix(A, B, v)
    print(f"Test 9 - Zero matrices: {result}")
    assert result == True, "Zero matrices should return True"

    # Test 10: Zero vector
    A = GF(np.array([[9, 4, 5], [8, 3, 4], [7, 9, 11]]))
    B = GF(np.array([[9, 4, 5], [8, 3, 4], [7, 9, 11]]))
    v = GF(np.array([0, 0, 0]))
    result = is_same_matrix(A, B, v)
    print(f"Test 10 - Zero vector: {result}")
    assert result == True, "Zero vector should return True for same matrices"

    # Test 11: Large matrices (4x4)
    A = GF(np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]))
    B = GF(np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]))
    v = GF(np.array([1, 2, 3, 4]))
    result = is_same_matrix(A, B, v)
    print(f"Test 11 - 4x4 same matrices: {result}")
    assert result == True, "4x4 same matrices should return True"

    # Test 12: Large matrices with one difference
    A = GF(np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]))
    B = GF(np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 17]]))
    v = GF(np.array([1, 2, 3, 4]))
    result = is_same_matrix(A, B, v)
    print(f"Test 12 - 4x4 matrices with one difference: {result}")
    assert result == False, "4x4 matrices with one difference should return False"

    print("All tests passed! ✅")

# Run the tests
if __name__ == "__main__":
    test_is_same_matrix()