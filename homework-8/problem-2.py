# Write python code that takes an R1CS matrix A, B, and C and a witness vector w and
# verifies.

# *Aw* ⊙ *Bw* − *Cw* = 0

# Where ⊙ is the hadamard (element-wise) product.

# Use this to code to check your answer above is correct.

import numpy as np
import random

def verify_r1cs(A, B, C, w):
    result = np.matmul(C, w) == np.multiply(np.matmul(A, w), np.matmul(B, w))
    assert result.all(), "system contains an inequality"

def test_case_1():
    print("Test case 1: should pass")
    O = np.matrix([[0,1,0,0]])
    L = np.matrix([[0,0,1,0]])
    R = np.matrix([[0,0,0,1]])
    a = np.array([1, 4223, 41, 103])

    verify_r1cs(L, R, O, a)

def test_case_2():
    print("Test case 2: should fail")
    O = np.matrix([[0,1,0,0]])
    L = np.matrix([[0,0,1,0]])
    R = np.matrix([[0,0,0,1]])
    a = np.array([1, 4223, 41, 102])

    try:
        verify_r1cs(L, R, O, a)
    except AssertionError:
        print("Test case 2 failed")


def test_case_3():
    print("Test case 3: should pass")

    L = np.matrix([[0,0,1,0,0,0,0,0],
                   [0,0,0,0,1,0,0,0],
                   [0,0,0,0,0,0,1,0]])

    R = np.matrix([[0,0,0,1,0,0,0,0],
                   [0,0,0,0,0,1,0,0],
                   [0,0,0,0,0,0,0,1]])

    O = np.matrix([[0,0,0,0,0,0,1,0],
                   [0,0,0,0,0,0,0,1],
                   [0,1,0,0,0,0,0,0]])

    x = random.randint(1,1000)
    y = random.randint(1,1000)
    z = random.randint(1,1000)
    u = random.randint(1,1000)

    r = x * y * z * u
    v1 = x*y
    v2 = z*u

    a = np.array([1, r, x, y, z, u, v1, v2])

    verify_r1cs(L, R, O, a)

def test_case_4():
    print("Test case 4: should fail")

    L = np.matrix([[0,0,1,0,0,0,0,0],
                   [0,0,0,0,1,0,0,0],
                   [0,0,0,0,0,0,1,0]])

    R = np.matrix([[0,0,0,1,0,0,0,0],
                   [0,0,0,0,0,1,0,0],
                   [0,0,0,0,0,0,0,1]])

    O = np.matrix([[0,0,0,0,0,0,1,0],
                   [0,0,0,0,0,0,0,1],
                   [0,1,0,0,0,0,0,0]])

    x = random.randint(1,1000)
    y = random.randint(1,1000)
    z = random.randint(1,1000)
    u = random.randint(1,1000)

    r = x * y * z * u
    v1 = x*y
    v2 = z*u

    a = np.array([1, r + 1, x, y, z, u, v1, v2])

    try:
        verify_r1cs(L, R, O, a)
    except AssertionError:
        print("Test case 4 failed")

def test_case_5():
    print("Test case 5: should pass")

    L = np.matrix([[0,0,1,0]])
    R = np.matrix([[0,0,0,1]])
    O = np.matrix([[-2,1,0,0]])

    x = random.randint(1,1000)
    y = random.randint(1,1000)
    z = x * y + 2
    a = np.array([1, z, x, y])

    verify_r1cs(L, R, O, a)

def test_case_6():
    print("Test case 6: should pass")

    L = np.matrix([[0,0,2,0]])
    R = np.matrix([[0,0,1,0]])
    O = np.matrix([[0,1,0,-1]])

    x = random.randint(1,1000)
    y = random.randint(1,1000)
    v1 = x * x
    z = 2 * v1 + y
    a = np.array([1, z, x, y])

    verify_r1cs(L, R, O, a)

def test_case_7():
    print("Test case 7: should pass")

    L = np.array([[0,0,3,0,0,0],
                [0,0,0,0,1,0],
                [0,0,5,0,0,0]])

    R = np.array([[0,0,1,0,0,0],
                [0,0,0,1,0,0],
                [0,0,0,1,0,0]])

    O = np.array([[0,0,0,0,1,0],
                [0,0,0,0,0,1],
                [-3,1,1,2,0,-1]])

    x = random.randint(1,1000)
    y = random.randint(1,1000)

    out = 3 * x * x * y + 5 * x * y - x - 2 * y + 3
    v1 = 3*x*x
    v2 = v1 * y
    w = np.array([1, out, x, y, v1, v2])

if __name__ == "__main__":
    test_case_1()
    test_case_2()
    test_case_3()
    test_case_4()
    test_case_5()
    test_case_6()
    test_case_7()
