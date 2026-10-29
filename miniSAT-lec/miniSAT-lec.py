import argparse
import re
import subprocess




##############################################################################################
# Equivalence Check                                                                          #
##############################################################################################
def equivalence_checking(circuit, cnf_file_path, res_file_path):
    # Generate DIMACS CNF
    bench_to_cnf(circuit, cnf_file_path)
    # Call MiniSAT
    # NOTE, you *WILL* need to change the next line to match your system configuration.
    minisat_path = "/home/cc/ee144/fa26/class/ee144-aaj/minisat-releases-2.2.0/core/minisat"
    command = f"{minisat_path} {cnf_file_path} {res_file_path}"
    subprocess.run([minisat_path, cnf_file_path, res_file_path])

def bench_to_cnf(circuit, cnf_file_path):
    # Create a mapping from BENCH nodes to CNF indices
    node_map = {}
    counter = 1
    for input in circuit.inputs:
        node_map[input.node] = counter
        counter += 1
    for gate in circuit.gates:
        node_map[gate.node] = counter
        counter += 1

    # Need to store a list of clauses
    clauses = []

    # Encode each gate to CNF
    for gate in circuit.gates:
        if ((gate.type == "NOT1" and len(gate.fanins) != 1) or
            (gate.type == "BUFF1" and len(gate.fanins) != 1) or
            (gate.type != "NOT1" and  gate.type != "BUFF1" and len(gate.fanins) != 2)):
            print(f"Wrong number of fanin for node: {gate}") 
        elif gate.type == "NOT1":
            f0 = node_map[gate.fanins[0]] #fanin id
            fo = node_map[gate.node] # fanout id
            clauses.append(f"-{f0} -{fo} 0")
            clauses.append(f"{f0} {fo} 0")
        
        elif gate.type == "BUFF1":
            f0 = node_map[gate.fanins[0]]
            fo = node_map[gate.node]
            clauses.append(f"-{f0} {fo} 0")
            clauses.append(f"{f0} -{fo} 0")

        elif gate.type == "AND2":
            f0 = node_map[gate.fanins[0]]
            f1 = node_map[gate.fanins[1]]
            fo = node_map[gate.node]
            clauses.append(f"-{fo} {f0} 0")
            clauses.append(f"-{fo} {f1} 0")
            clauses.append(f"{fo} -{f0} -{f1} 0")

        elif gate.type == "OR2":
            f0 = node_map[gate.fanins[0]]
            f1 = node_map[gate.fanins[1]]
            fo = node_map[gate.node]
            clauses.append(f"{fo} -{f0} 0")
            clauses.append(f"{fo} -{f1} 0")
            clauses.append(f"-{fo} {f0} {f1} 0")

        elif gate.type == "XOR2":
            f0 = node_map[gate.fanins[0]]
            f1 = node_map[gate.fanins[1]]
            fo = node_map[gate.node]
            clauses.append(f"-{f0} -{f1} -{fo} 0")
            clauses.append(f"{f0} {f1} -{fo} 0")
            clauses.append(f"{f0} -{f1} {fo} 0")
            clauses.append(f"-{f0} {f1} {fo} 0")

        elif gate.type == "NAND2":
            f0 = node_map[gate.fanins[0]]
            f1 = node_map[gate.fanins[1]]
            fo = node_map[gate.node]
            clauses.append(f"{fo} {f0} 0")
            clauses.append(f"{fo} {f1} 0")
            clauses.append(f"-{fo} -{f0} -{f1} 0")

        elif gate.type == "NOR2":
            f0 = node_map[gate.fanins[0]]
            f1 = node_map[gate.fanins[1]]
            fo = node_map[gate.node]
            clauses.append(f"-{fo} -{f0} 0")
            clauses.append(f"-{fo} -{f1} 0")
            clauses.append(f"{fo} {f0} {f1} 0")

        elif gate.type == "XNOR2":
            f0 = node_map[gate.fanins[0]]
            f1 = node_map[gate.fanins[1]]
            fo = node_map[gate.node]
            clauses.append(f"-{f0} -{f1} {fo} 0")
            clauses.append(f"{f0} {f1} {fo} 0")
            clauses.append(f"{f0} -{f1} -{fo} 0")
            clauses.append(f"-{f0} {f1} -{fo} 0")


    # Encode output node
    fo = node_map[circuit.outputs[0].fanins[0]]
    clauses.append(f"{fo} 0")

    n_variables = len(circuit.gates) + len(circuit.inputs)
    n_clauses = len(clauses)

    # Write CNF
    with open(cnf_file_path, "w") as cnf_file:
        cnf_file.write(f"p cnf {n_variables} {n_clauses}\n")
        for clause in clauses:
            cnf_file.write(f"{clause}\n")

    return


class Circuit:
    def __init__(self):
        self.inputs = []
        self.outputs = []
        self.gates = []

class Node:
    def __init__(self):
        self.node = None
        self.type = None
        self.fanins = None

    def __str__(self):
        if self.type == "INPUT":
            return f"{self.type} {self.node}"
        elif self.type == "SINK":
            return f"{self.type} {self.fanins[0]}"
        else:
            return f"{self.node}: {self.type}({self.fanins})"



def parse_circuit(bench_file_path):
    circuit = Circuit()
    id_counter = 0

    with open(bench_file_path, "r") as bench_file:
        for line in bench_file:
            node_pattern = r"([0-9a-zA-Z_\[\]]+)"
            gate_type_pattern = r"([a-zA-Z]+)"
            fanin_pattern = r"([0-9a-zA-Z_\[\]]+(?:,[0-9a-zA-Z_\[\]]+)*)"

            line = re.sub(r"\s", "", line)  # Remove all whitespace

            p = Node()

            if match := re.match(fr"^{node_pattern}={gate_type_pattern}\({fanin_pattern}\)", line):
                p.node = match.group(1)
                p.type = f"{match.group(2)}{len(match.group(3).split(','))}"  # Append # of inputs
                p.fanins = match.group(3).split(',')
                circuit.gates.append(p)


            elif match := re.match(fr"^INPUT\({node_pattern}\)", line):
                p.node = match.group(1)
                p.type = "INPUT"
                p.fanins = ["SOURCE"]

                circuit.inputs.append(p)

            elif match := re.match(fr"^OUTPUT\({node_pattern}\)", line):
                p.node = "SINK"
                p.type = "SINK"
                p.fanins = [match.group(1)]
                circuit.outputs.append(p)

            elif re.match(r"^\s*$|^#.*$", line):  # Empty or comment lines
                continue

            else:
                raise ValueError(f"\n\nCannot identify: ->{line}<- \n")

    print(f"Total number of gates    : {len(circuit.gates)}")
    print(f"Total number of inputs   : {len(circuit.inputs)}")
    print(f"Total number of outputs  : {len(circuit.outputs)}")

    # collect each type of gate
    gate_type_dict = {}
    for gate in circuit.gates:
        if gate.type not in gate_type_dict:
            gate_type_dict[gate.type] = 1
        else:
            gate_type_dict[gate.type] += 1

    print("Number of instances of each gate type")
    print(f"{'gate':<15} {'count':<10}")
    for gate_type, count in gate_type_dict.items():
        print(f"{gate_type:<15} {count:<10}")
    print(f"{'output':<15} {len(circuit.outputs):<10}")
        
    return circuit


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="HW4: SAT Package")
    parser.add_argument("--file", type=str, required = True, help = "BENCH file")
    parser.add_argument("--cnf", type=str, required = True, help = "CNF file")
    parser.add_argument("--res", type=str, required = True, help = "CNF result file")

    args = parser.parse_args()
    print(args.file, args.cnf, args.res)

    print(f"Circuit        :  {args.file}");

    circuit = parse_circuit(args.file)
    equivalence_checking(circuit=circuit, cnf_file_path=args.cnf, res_file_path=args.res)
