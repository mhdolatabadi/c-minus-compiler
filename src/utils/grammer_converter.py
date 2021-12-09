input_file = open("c-minus_001.txt", "r")
output_file = open("result.txt", "w")
for i in input_file:
    if "|" in i:
        split_line = i.split("->")
        LHS = split_line[0].replace(" ", "")
        RHSs = split_line[1].split("|")
        for j in RHSs:
            j.replace(" ", "")
            output_file.write(f"{LHS} -> {j}\n")
    else:
        output_file.write(i)

input_file.close()
output_file.close()
