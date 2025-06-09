# Find the elements in a finite field that are congruent to the following values:

# - -1
# - -4
# - -160
# - 500

from find_congruent import find_congruent

p = 71

number_congruent_to_minus_1 = -1 % p
print(number_congruent_to_minus_1)

number_congruent_to_minus_4 = -4 % p
print(number_congruent_to_minus_4)

number_congruent_to_minus_160 = -160 % p
print(number_congruent_to_minus_160)

number_congruent_to_500 = 500 % p
print(number_congruent_to_500)

assert(find_congruent(-1, p) == number_congruent_to_minus_1)
assert(find_congruent(-4, p) == number_congruent_to_minus_4)
assert(find_congruent(-160, p) == number_congruent_to_minus_160)
assert(find_congruent(500, p) == number_congruent_to_500)