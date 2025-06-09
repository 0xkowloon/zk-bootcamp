from mod_inverse import mod_inverse

# Find the elements that are congruent to a = 5/6, b = 11/12, and c = 21/12

# Verify your answer by checking that a + b = c (in the finite field)

# x / y is equivalent to x * y^-1, hence we can find the multiplicative inverse of y and multiply it by x

p = 71

multiplicative_inverse_of_6 = mod_inverse(6, p)
assert(multiplicative_inverse_of_6 == pow(6, -1, p))

a = (5 * multiplicative_inverse_of_6) % p
print(a)

multiplicative_inverse_of_12 = mod_inverse(12, p)
assert(multiplicative_inverse_of_12 == pow(12, -1, p))

b = (11 * multiplicative_inverse_of_12) % p
print(b)

c = (21 * multiplicative_inverse_of_12) % p
print(c)

assert((a + b) % p == c % p)