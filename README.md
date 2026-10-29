# Problem 8

- 8(a): Implemented a 4-bit ripple-carry adder.
- 8(b): Ripple-carry and carry-lookahead adders are equivalent.
- 8(c): Optimal variable ordering: x, y, a, b, c, d. Minimum BDD size: 7 nonterminal nodes.

# Problem 9

- 9(a–c): UNSAT. All four equivalences hold.
- 9(d):
problem2a.bench: UNSAT
problem2b.bench: SAT

- 9(e): SAT. The stuck-at-1 fault at h is detectable.
Counterexample: a=0, b=0, c=1, d=0.
Normal output f=0, faulty output f=1.