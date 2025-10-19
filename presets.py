
try:
    from .model import CardGroup, TurnSpec
except Exception:
    from model import CardGroup, TurnSpec

# Common card groups
BBBAQ = CardGroup(3,1,1)
BBAAQ = CardGroup(2,2,1)
BAAAQ = CardGroup(1,3,1)
BAAQQ = CardGroup(1,2,2)
BBAQQ = CardGroup(2,1,2)
BAQQQ = CardGroup(1,1,3)

# Helper constructors for constraints
def need(**kwargs):
    # need(B=1,Q=1) -> {'B':1,'Q':1}
    return kwargs

def OR(*conjs):
    # OR(need(B=2), need(B=1,Q=1)) => [{'B':2},{'B':1,'Q':1}]
    return list(conjs)

# Example specs
T_BQ_or_BB = TurnSpec(any_of=OR(need(B=1,Q=1), need(B=2)))
T_has_A = TurnSpec(any_of=OR(need(A=1)))
T_has_Q = TurnSpec(any_of=OR(need(Q=1)))
