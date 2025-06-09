def find_congruent(value, p):
  if value >= 0:
    return value % p

  while value < 0:
    value += p

  return value