firsts = open('firsts.txt', 'r')
codes = list()
i = 0
for line in firsts:
    split_line = line.split(' ')
    codes.append(f"{split_line[0]} = TransitionDiagram('{split_line[0]}', [")
    for j in range(1, len(split_line)):
        value = split_line[j].replace('\n', '')
        codes[i] += f"'{value}'"
        if j != len(split_line) - 1:
            codes[i] += ", "
    codes[i] += f"],"
    i += 1
firsts.close()

follows = open('follows.txt', 'r')
i = 0
for line in follows:
    split_line = line.split(' ')
    codes[i] += f"["
    for j in range(1, len(split_line)):
        value = split_line[j].replace('\n', '')
        codes[i] += f"'{value}'"
        if j != len(split_line) - 1:
            codes[i] += ", "
    codes[i] += f"])"
    i += 1

follows.close()

code_file = open('codes.txt', 'a')
for i in codes:
    code_file.write(f'{i}\n')
code_file.close()
