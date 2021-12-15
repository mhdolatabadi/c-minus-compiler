grammer_file = open("grammer.txt", "r")
code_file = open("generated.txt", "w")
for line in grammer_file:
    split_line = line.split("->")
    LHS = split_line[0].replace(" ", "")
    code_file.write(f"{LHS} = TransitionDiagram()\n")
    RHSs = split_line[1]
    is_nodes_created = False
    for rhs in RHSs.split("|"):
        if not is_nodes_created:
            for i in range(len(rhs.split(" ")) - 1):
                token = rhs.split(" ")[i]
                if i == 0:
                    code_file.write(f"{LHS}.add_node(0)\n")
                elif i == len(rhs.split(" ")) - 2:
                    code_file.write(f"{LHS}.add_node({i}, False, True)\n")
                else:
                    code_file.write(f"{LHS}.add_node({i}, False)\n")
        is_nodes_created = True
        j = 0
        for i in range(len(rhs.split(" "))):
            token = rhs.split(" ")[i]
            if not token or token == " ":
                continue
            code_file.write(f"{LHS}.add_edge({j}, {j+1}, {token})\n")
            j += 1

grammer_file.close()
code_file.close()