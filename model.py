
from dataclasses import dataclass
from typing import Dict, List, Tuple

@dataclass(frozen=True)
class CardGroup:
    B: int
    A: int
    Q: int
    def to_list(self) -> List[str]:
        return ['B']*self.B + ['A']*self.A + ['Q']*self.Q
    @property
    def total(self) -> int:
        return self.B + self.A + self.Q

# A "conjunctive" constraint is like {'B':1,'Q':1} meaning at least 1 B and 1 Q in that segment.
# A "disjunctive" (OR) constraint is a list of conjunctive constraints: [{'B':2}, {'B':1,'Q':1}]
Constraint = List[Dict[str,int]]  # OR of ANDs

@dataclass(frozen=True)
class TurnSpec:
    # A per-turn OR-of-ANDs constraint, e.g. [{'B':2}, {'B':1,'Q':1}] stands for 'BB or BQ'
    any_of: Constraint

def eval_segment(segment: list, spec: TurnSpec) -> bool:
    # segment is a list like ['Other','B','A',...] length 5
    # spec.any_of is a list of dicts; True if any dict is satisfied (each dict is "at least" check)
    counts = {'B': segment.count('B'), 'A': segment.count('A'), 'Q': segment.count('Q')}
    for conj in spec.any_of:
        ok = True
        for k, need in conj.items():
            if counts.get(k, 0) < need:
                ok = False
                break
        if ok:
            return True
    return False
