# What is the modular square root of 12?

# Verify your answer by checking that x * x = 12 (mod 71)

# Use brute force to find the answer (in Python)

p = 71

for x in range(p):
  if (x * x) % p == 12:
    print(x)