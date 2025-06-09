from mod_inverse import mod_inverse

##

# Find the elements that are congruent to a = 2/3, b = 1/2, and c = 1/3.

# Verify your answer by checking that a * b = c (in the finite field)

p = 71

multiplicative_inverse_of_3 = mod_inverse(3, p)
assert(multiplicative_inverse_of_3 == pow(3, -1, p))
a = (2 * multiplicative_inverse_of_3) % p
print(a)

multiplicative_inverse_of_2 = mod_inverse(2, p)
assert(multiplicative_inverse_of_2 == pow(2, -1, p))
b = (1 * multiplicative_inverse_of_2) % p
print(b)

c = (1 * multiplicative_inverse_of_3) % p
print(c)

assert((a * b) % p == c % p)