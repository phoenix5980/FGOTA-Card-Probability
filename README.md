
# fgo-card-probability

A modular FGO card probability calculator supporting:
1. 3-player shuffle (independent turns): probability all specified turns succeed.
2. 2-player shuffle (independent turns).
3. 3-player fixed-order (no shuffle across 3 consecutive turns).
4. 2-player fixed-order (no shuffle across 2 consecutive turns).

## Install

```bash
python3 -m pip install -U pip
# no third-party deps required
```

## Run (examples)

### Example 3p fixed (no shuffle): T1 has A, T2 has Q, T3 has (B+Q or BB) for BBAQQ
```bash
python -m fgo_card_probability.main --mode 3p-fixed --group BBAQQ --turn-specs '[[{"A":1}], [{"Q":1}], [{"B":1,"Q":1}, {"B":2}]]'
```

### Example 3p shuffle: same per-turn constraints (all turns succeed)
```bash
python -m fgo_card_probability.main --mode 3p-shuffle --group BBAQQ --turn-specs '[[{"A":1}], [{"Q":1}], [{"B":1,"Q":1}, {"B":2}]]'
```

## API

See `model.py` and `solver_probability.py`. Constraints are expressed as OR-of-ANDs:
- `[[{"B":2}], [{"B":1,"Q":1}]]` means "BB or BQ".
- `[ [{"A":1}] ]` means "at least one A".

## Notes
- Cards are modeled by type only (B/A/Q), not by individual identity.
- For fixed modes, exact enumeration is used: C(N,5) choices for your 5 cards' positions
  times unique multiset permutations of your hand.
