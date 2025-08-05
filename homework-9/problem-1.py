# Alice and Bob have two vectors, and they want to test if they are the same vector. Assume that they evaluate their polynomials honestly. Write the code they would use to turn their vector into a polynomial over a finite field.

import galois
import numpy as np
import random
from py_ecc.bn128 import field_modulus

GF = galois.GF(field_modulus)

def to_polynomial(xs, v):
  return galois.lagrange_poly(GF(xs), GF(v))

def is_same_vector(v1, v2):
  if len(v1) == 0:
    return False

  if len(v1) != len(v2):
    return False

  xs = np.arange(1, len(v1) + 1)

  p1 = to_polynomial(xs, v1)
  p2 = to_polynomial(xs, v2)

  u = random.randint(0, field_modulus - 1)

  lhs = p1(u)
  rhs = p2(u)

  return lhs == rhs

# Test cases for is_same_vector function
def test_is_same_vector():
    print("Testing is_same_vector function...")

    # Test 1: Same vectors should return True
    v1 = np.array([4, 8, 19])
    v2 = np.array([4, 8, 19])
    result = is_same_vector(v1, v2)
    print(f"Test 1 - Same vectors [4,8,19]: {result}")
    assert result == True, "Same vectors should return True"

    # Test 2: Different vectors should return False
    v1 = np.array([4, 8, 19])
    v2 = np.array([4, 8, 20])
    result = is_same_vector(v1, v2)
    print(f"Test 2 - Different vectors [4,8,19] vs [4,8,20]: {result}")
    assert result == False, "Different vectors should return False"

    # Test 3: Different length vectors should return False
    v1 = np.array([4, 8, 19])
    v2 = np.array([4, 8])
    result = is_same_vector(v1, v2)
    print(f"Test 3 - Different lengths [4,8,19] vs [4,8]: {result}")
    assert result == False, "Different length vectors should return False"

    # Test 4: Empty vectors should return False
    v1 = np.array([])
    v2 = np.array([])
    result = is_same_vector(v1, v2)
    print(f"Test 4 - Empty vectors: {result}")
    assert result == False, "Empty vectors should return False"

    # Test 5: One empty vector should return False
    v1 = np.array([4, 8, 19])
    v2 = np.array([])
    result = is_same_vector(v1, v2)
    print(f"Test 5 - One empty vector: {result}")
    assert result == False, "One empty vector should return False"

    # Test 6: Single element vectors
    v1 = np.array([42])
    v2 = np.array([42])
    result = is_same_vector(v1, v2)
    print(f"Test 6 - Single element same [42]: {result}")
    assert result == True, "Single element same vectors should return True"

    # Test 7: Single element different vectors
    v1 = np.array([42])
    v2 = np.array([43])
    result = is_same_vector(v1, v2)
    print(f"Test 7 - Single element different [42] vs [43]: {result}")
    assert result == False, "Single element different vectors should return False"

    # Test 8: Large vectors
    v1 = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    v2 = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    result = is_same_vector(v1, v2)
    print(f"Test 8 - Large same vectors: {result}")
    assert result == True, "Large same vectors should return True"

    # Test 9: Large vectors with one difference
    v1 = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    v2 = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 11])
    result = is_same_vector(v1, v2)
    print(f"Test 9 - Large vectors with one difference: {result}")
    assert result == False, "Large vectors with one difference should return False"

    # Test 10: Zero vectors
    v1 = np.array([0, 0, 0])
    v2 = np.array([0, 0, 0])
    result = is_same_vector(v1, v2)
    print(f"Test 10 - Zero vectors [0,0,0]: {result}")
    assert result == True, "Zero vectors should return True"

    print("All tests passed! ✅")

# Run the tests
if __name__ == "__main__":
    test_is_same_vector()