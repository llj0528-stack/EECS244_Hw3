from dd.autoref import BDD
import argparse

def example1(args):
    # Or gate
    bdd = BDD()

    # Create BDD variables
    bdd.declare('x', 'y')

    # | represents Boolean OR
    u = bdd.add_expr(r'x | y')

    # plot the BDD in file
    bdd.collect_garbage()  # optional
    bdd.dump(f"{args.filename}.pdf", roots = [u])

    # Get the number of nodes in the the list of BDDs
    print(f"BDD Size: {len(bdd)}")

    # Reorder the variable 
    my_order = dict(x=1, y=0)
    bdd.reorder(my_order)

    # Get the number of nodes in the the list of BDDs
    print(f"BDD Size: {len(bdd)}")

    # plot the BDD in file
    bdd.collect_garbage()  # optional
    bdd.dump(f"{args.filename}_reorder.pdf", roots = [u])

def example2(args):
    # And gate
    bdd = BDD()

    # Create BDD variables
    bdd.declare('x', 'y')

    # & represents Boolean And
    u = bdd.add_expr(r'x & y')

    # plot the BDD in file
    bdd.collect_garbage()  # optional
    bdd.dump(f"{args.filename}.pdf", roots = [u])

    # Get the number of nodes in the the list of BDDs
    print(f"BDD Size: {len(bdd)}")

    # Reorder the variable 
    my_order = dict(x=1, y=0)
    bdd.reorder(my_order)

    # Get the number of nodes in the the list of BDDs
    print(f"BDD Size: {len(bdd)}")

    # plot the BDD in file
    bdd.collect_garbage()  # optional
    bdd.dump(f"{args.filename}_reorder.pdf", roots = [u])


def example3(args):
    # XOR gate
    bdd = BDD()

    # Create BDD variables
    bdd.declare('x', 'y')

    # ^ represents Boolean And
    u = bdd.add_expr(r'x ^ y')

    # plot the BDD in file
    bdd.collect_garbage()  # optional
    bdd.dump(f"{args.filename}.pdf", roots = [u])

    # Get the number of nodes in the the list of BDDs
    print(f"BDD Size: {len(bdd)}")

    # Reorder the variable 
    my_order = dict(x=1, y=0)
    bdd.reorder(my_order)

    # Get the number of nodes in the the list of BDDs
    print(f"BDD Size: {len(bdd)}")

    # plot the BDD in file
    bdd.collect_garbage()  # optional
    bdd.dump(f"{args.filename}_reorder.pdf", roots = [u])

def example4(args):
    # 4-bit less than circuit
    # x < y where x = (x3,x2,x1,x0) and y = (y3,y2,y1,y0)
    bdd = BDD()

    # Create BDD variables
    bdd.declare('x3', 'x2', 'x1', 'x0', 'y3', 'y2', 'y1', 'y0')

    # | represents Boolean XOR
    u = bdd.add_expr(r"""(~ x3 & y3) | 
                     (~(x3 ^ y3) & (~x2 & y2)) |
                     (~(x3 ^ y3) & ~(x2 ^ y2) & (~x1 & y1)) |
                     (~(x3 ^ y3) & ~(x2 ^ y2) & ~(x1 ^ y1) & (~x0 & y0))""")

    # plot the BDD in file
    bdd.collect_garbage()  # optional
    bdd.dump(f"{args.filename}.pdf", roots = [u])

    # Get the number of nodes in the the list of BDDs
    print(f"BDD Size: {len(bdd)}")

    # Reorder the variable 
    my_order = dict(x3=0, y3=1, x2=2, y2=3, x1=4, y1=5, x0=6, y0=7)
    bdd.reorder(my_order)

    # Get the number of nodes in the the list of BDDs
    print(f"BDD Size: {len(bdd)}")

    # plot the BDD in file
    bdd.collect_garbage()  # optional
    bdd.dump(f"{args.filename}_reorder.pdf", roots = [u])


def carry_lookahead_adder_4_bit(args, bdd):
    print("4-bit carry-lookahead adder")

    # Generates
    g0 = bdd.add_expr(r'x0 & y0')
    g1 = bdd.add_expr(r'x1 & y1')
    g2 = bdd.add_expr(r'x2 & y2')
    g3 = bdd.add_expr(r'x3 & y3')

    # Propagates
    p0 = bdd.add_expr(r'x0 | y0')
    p1 = bdd.add_expr(r'x1 | y1')
    p2 = bdd.add_expr(r'x2 | y2')
    p3 = bdd.add_expr(r'x3 | y3')

    # Carry bits
    c0 = bdd.add_expr(r'cin')
    c1 = bdd.add_expr(rf'{g0} | ({p0} & {c0})')
    c2 = bdd.add_expr(rf'{g1} | ({p1} & {g0}) | ({p1} & {p0} & {c0})')
    c3 = bdd.add_expr(rf'{g2} | ({p2} & {g1}) | ({p2} & {p1} & {g0}) | ({p2} & {p1} & {p0} & {c0})')
    c4 = bdd.add_expr(rf'{g3} | ({p3} & {g2}) | ({p3} & {p2} & {g1}) | ({p3} & {p2} & {p1} & {g0}) | ({p3} & {p2} & {p1} & {p0} & {c0})')

    # Sum bits
    s0 = bdd.add_expr(rf'x0 ^ y0 ^ {c0}')
    s1 = bdd.add_expr(rf'x1 ^ y1 ^ {c1}')
    s2 = bdd.add_expr(rf'x2 ^ y2 ^ {c2}')
    s3 = bdd.add_expr(rf'x3 ^ y3 ^ {c3}')

    adder_out = [s0, s1, s2, s3, c4]
    # plot the BDD in file
    bdd.collect_garbage()  # optional
    bdd.dump(f"{args.filename}_carry.pdf", roots = adder_out)
    return adder_out



def ripple_carry_4_bit(args, bdd):
    print("4-bit ripple carry adder")

    adder_out = []
    c = bdd.var('cin')

    for i in range(4):
        x = bdd.var(f'x{i}')
        y = bdd.var(f'y{i}')

        # Propagate: pi = xi XOR yi
        p = bdd.apply('xor', x, y)

        # Sum: si = pi XOR ci
        s = bdd.apply('xor', p, c)

        # Carry: ci+1 = xi*yi + pi*ci
        c = (x & y) | (p & c)

        adder_out.append(s)

    adder_out.append(c)

    bdd.collect_garbage()
    bdd.dump(f"{args.filename}_ripple.pdf", roots=adder_out)

    return adder_out



def equivalence_check(args, bdd, cla_sum, rc_sum):
    miter = bdd.true

    for cla, rc in zip(cla_sum, rc_sum):
        diff = bdd.apply('xor', cla, rc)
        miter = miter & ~diff

    print("Equivalent:", miter == bdd.true)

    bdd.collect_garbage()
    bdd.dump(f"{args.filename}.pdf", roots=[miter])



def multiplexer_4_to_1(args, bdd):
    # 4-to-1 MUX
    mux_4_to_1 = bdd.add_expr(
        r'(~x & ~y & a) | '
        r'(~x & y & b) | '
        r'(x & ~y & c) | '
        r'(x & y & d)'
    )

    # Optimal variable ordering
    best_order = dict(x=0, y=1, a=2, b=3, c=4, d=5)
    bdd.reorder(best_order)

    bdd.collect_garbage()

    print("Optimal order:", best_order)
    print("BDD size (including terminals):", len(bdd))

    # Plot BDD
    bdd.dump(f"{args.filename}.pdf", roots=[mux_4_to_1])



def exercise1(args):
    bdd = BDD()
    bdd.declare('x3', 'x2', 'x1', 'x0', 'y3', 'y2', 'y1', 'y0', 'cin')
    ripple_carry_4_bit(args, bdd)

def exercise2(args):
    bdd = BDD()
    bdd.declare('x3', 'x2', 'x1', 'x0', 'y3', 'y2', 'y1', 'y0', 'cin')
    cla_sum = carry_lookahead_adder_4_bit(args, bdd)
    rc_sum = ripple_carry_4_bit(args, bdd)
    equivalence_check(args, bdd, cla_sum, rc_sum)


def exercise3(args):
    bdd = BDD()
    bdd.declare('x', 'y', 'a', 'b', 'c', 'd')
    multiplexer_4_to_1(args, bdd)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="HW3: BDD practice with dd package"
    )
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--example", type=int, choices=[1, 2, 3, 4],
                       help="Example to run")
    group.add_argument("--exercise", type=int, choices=[1, 2, 3],
                       help="HW problem to run")
    
    parser.add_argument("--filename", type=str, default="output",
                        help="Dump PDF for the BDD [default: output]")
    
    args = parser.parse_args()

    examples = [example1, example2, example3, example4]
    exercises = [exercise1, exercise2, exercise3]

    if args.example is not None:
        id = args.example-1
        examples[id](args)
    elif args.exercise is not None:
        id = args.exercise-1
        exercises[id](args)
