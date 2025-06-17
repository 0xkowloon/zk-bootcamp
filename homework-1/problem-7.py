# Find a polynomial f(x) that crosses the points (10, 15), (23, 29).

# Since these are two points, the polynomial will be of degree 1 and be the equation for a line (y = ax + b).

# Verify your answer by checking that f(10) = 15 and f(23) = 29.

# The slope is (29 - 15) / (23 - 10) = 14 / 13
# The multiplicative inverse of 13 mod 71 is 11
# Therefore the slope is 14 * 11 = 154 = 12 mod 71

# The intercept is 15 - 12 * 10
# -120 is congruent to 22 mod 71
# So the intercept is 15 + 22 = 37 mod 71

import galois

# 1. Define the field
GF = galois.GF(71)

# 2. Define the points
x1, y1 = GF(10), GF(15)
x2, y2 = GF(23), GF(29)

# 3. Compute the slope (a)
slope = (y2 - y1) / (x2 - x1)  # Uses modular division in GF(71)

# 4. Compute the intercept (b)
intercept = y1 - slope * x1

# 5. Display the result
print(f"f(x) = {int(slope)}x + {int(intercept)} mod 71")

def f(x):
    return slope * x + intercept

assert f(10) == 15
assert f(23) == 29