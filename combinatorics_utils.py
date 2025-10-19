
from math import comb, factorial
from functools import lru_cache

def C(n:int, k:int) -> int:
    if k < 0 or k > n: 
        return 0
    return comb(n, k)

@lru_cache(maxsize=None)
def multiset_perm_count(b:int, a:int, q:int) -> int:
    n = b + a + q
    return factorial(n) // (factorial(b) * factorial(a) * factorial(q))
