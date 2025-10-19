from itertools import combinations, permutations
from typing import List, Dict, Optional
from math import comb, gcd
try:
    from .model import CardGroup, TurnSpec, eval_segment
    from .combinatorics_utils import C, multiset_perm_count
except Exception:
    from model import CardGroup, TurnSpec, eval_segment
    from combinatorics_utils import C, multiset_perm_count

# Utility: simplify a fraction
def _simplify(n: int, d: int):
    if d == 0:
        return n, d
    g = gcd(n, d)
    return n // g, d // g

# ---------- Shuffle modes (each turn independent) ----------

def prob_single_turn_shuffle_counts(total_cards:int, cg: CardGroup, turn_req: TurnSpec) -> tuple[int,int]:
    total_hands = C(total_cards, 5)
    acc = 0
    for b in range(0, min(5, cg.B)+1):
        for a in range(0, min(5-b, cg.A)+1):
            for q in range(0, min(5-b-a, cg.Q)+1):
                other = 5 - b - a - q
                if other < 0:
                    continue
                ways = C(cg.B, b) * C(cg.A, a) * C(cg.Q, q) * C(total_cards - cg.total, other)
                segment = ['B']*b + ['A']*a + ['Q']*q + ['Other']*other
                if eval_segment(segment, turn_req):
                    acc += ways
    return acc, total_hands

def prob_single_turn_shuffle(total_cards:int, cg: CardGroup, turn_req: TurnSpec) -> float:
    num, den = prob_single_turn_shuffle_counts(total_cards, cg, turn_req)
    return num / den

def prob_across_turns_shuffle_counts(total_cards:int, cg: CardGroup, turn_specs: List[TurnSpec], mode:str='all', simplify: bool=False):
    nums = []
    dens = []
    for ts in turn_specs:
        n, d = prob_single_turn_shuffle_counts(total_cards, cg, ts)  # 这个函数你已有，返回单回合的未约分
        nums.append(n); dens.append(d)
    if mode == 'all':
        num = 1
        den = 1
        for i in range(len(nums)):
            num *= nums[i]; den *= dens[i]   # 保持未约分
        return _simplify(num, den) if simplify else (num, den)
    elif mode == 'any':
        # 'any' 的精确计数需要做跨回合容斥；当前用不到就先不返回分子/分母
        return (None, None)
    else:
        num = 1
        den = 1
        for i in range(len(nums)):
            num *= nums[i]; den *= dens[i]
        return _simplify(num, den) if simplify else (num, den)

def prob_across_turns_shuffle(total_cards:int, cg: CardGroup, turn_specs: List[TurnSpec], mode:str='all') -> float:
    # mode: 'all' (all turns succeed), 'any' (at least one), or 'independent_product' list mapping if specs identical.
    ps = [prob_single_turn_shuffle(total_cards, cg, ts) for ts in turn_specs]
    if mode == 'all':
        p = 1.0
        for x in ps: p *= x
        return p
    elif mode == 'any':
        p_not = 1.0
        for x in ps: p_not *= (1-x)
        return 1 - p_not
    else:
        # default: product
        p = 1.0
        for x in ps: p *= x
        return p

# ---------- Fixed (no-shuffle) modes ----------

def prob_fixed_counts(total_cards:int, num_turns:int, cg: CardGroup, turn_specs: List[TurnSpec]) -> tuple[int,int]:
    assert len(turn_specs) == num_turns, "turn_specs length must equal num_turns"
    perms = set(permutations(cg.to_list()))
    assert len(perms) == multiset_perm_count(cg.B, cg.A, cg.Q)
    total = 0
    valid = 0
    for pos_combo in combinations(range(total_cards), 5):
        pos = sorted(pos_combo)
        for tup in perms:
            board = ['Other'] * total_cards
            for i in range(5):
                board[pos[i]] = tup[i]
            ok = True
            for t in range(num_turns):
                seg = board[t*5:(t+1)*5]
                if not eval_segment(seg, turn_specs[t]):
                    ok = False
                    break
            total += 1
            if ok:
                valid += 1
    return valid, total

def prob_fixed(total_cards:int, num_turns:int, cg: CardGroup, turn_specs: List[TurnSpec]) -> float:
    num, den = prob_fixed_counts(total_cards, num_turns, cg, turn_specs)
    return num / den
