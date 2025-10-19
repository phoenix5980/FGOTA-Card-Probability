import argparse, json
from typing import List
from math import gcd

# Support both package-style execution (python -m ...) and direct script (python main.py)
try:
    # Package-style imports
    from .model import CardGroup, TurnSpec
    from .presets import *
    from .solver_probability import (
        prob_across_turns_shuffle,
        prob_fixed,
        prob_across_turns_shuffle_counts,
        prob_fixed_counts,
    )
except Exception:  # ImportError when no package context
    # Script-style fallback
    from model import CardGroup, TurnSpec
    from presets import *
    from solver_probability import (
        prob_across_turns_shuffle,
        prob_fixed,
        prob_across_turns_shuffle_counts,
        prob_fixed_counts,
    )


def parse_turn_specs(specs_json: str) -> List[TurnSpec]:
    raw = json.loads(specs_json)
    # raw is list of list-of-dicts
    out = []
    for disj in raw:
        out.append(TurnSpec(any_of=disj))
    return out


def main():
    parser = argparse.ArgumentParser(description="FGO card probability calculator")
    parser.add_argument('--mode', choices=['3p-shuffle','2p-shuffle','3p-fixed','2p-fixed'], required=True)
    parser.add_argument('--group', type=str, default='BBAQQ', help='one of BBBAQ,BBAAQ,BAAAQ,BAAQQ,BBAQQ,BAQQQ or custom JSON like {"B":2,"A":1,"Q":2}')
    parser.add_argument('--turn-specs', type=str, required=True, help='JSON list: [[{"A":1}], [{"Q":1}], [{"B":1,"Q":1}, {"B":2}]]')
    parser.add_argument('--simplify', action='store_true', help='简化分数显示（默认打印未约分分式）')
    args = parser.parse_args()

    group_map = {'BBBAQ':BBBAQ,'BBAAQ':BBAAQ,'BAAAQ':BAAAQ,'BAAQQ':BAAQQ,'BBAQQ':BBAQQ,'BAQQQ':BAQQQ}
    if args.group in group_map:
        cg = group_map[args.group]
    else:
        g = json.loads(args.group)
        cg = CardGroup(g['B'], g['A'], g['Q'])

    specs = parse_turn_specs(args.turn_specs)

    if args.mode == '3p-shuffle':
        num, den = prob_across_turns_shuffle_counts(15, cg, specs, mode='all', simplify=False)
        if num is None:  # fallback for modes we didn't count explicitly
            p = prob_across_turns_shuffle(15, cg, specs, mode='all')
            print(f"Probability = {p:.6%}")
            return
    elif args.mode == '2p-shuffle':
        num, den = prob_across_turns_shuffle_counts(10, cg, specs, mode='all', simplify=False)
        if num is None:
            p = prob_across_turns_shuffle(10, cg, specs, mode='all')
            print(f"Probability = {p:.6%}")
            return
    elif args.mode == '3p-fixed':
        num, den = prob_fixed_counts(15, len(specs), cg, specs)
    else:
        num, den = prob_fixed_counts(10, len(specs), cg, specs)

    percent = (num/den) if den else 0.0
    g = gcd(num, den) if den else 1
    if den == 0:
        print("0/0 = 0.000000%")
    elif g > 1:
        print(f"{num}/{den} = {num//g}/{den//g} = {percent:.6%}")
    else:
        print(f"{num}/{den} = {percent:.6%}")


if __name__ == '__main__':
    main()
