
class SemanticStack:
    def __init__(self):
        self.stack = []

    def push(self, element):
        self.stack.append(element)

    def pop(self):
        return self.stack.pop()

    def pop(self, count):
        for i in range(count):
            self.stack.pop()

class CodeGen:
    def __init__(self):
        self.program_block = []
        self.temp_count = -1
        self.semantic_stack = SemanticStack()


    def code_gen(action):
        pass

    def get_temp(self):
        self.temp_count += 1
        return (self.temp_count * 4) + 3000 

    def find_addr(self, input):
        symbol_table = open('./symbol_table.txt', 'r')
        for line in symbol_table:
            if(line.split('\t')[1] == input):
                return line.split('.')[0]

    def pid(self):
        p = self.find_addr(input)
        self.semantic_stack.push(p)
        

    def assign(self):
        self.program_block.append(f'(ASSIGN, {self.semantic_stack.pop()}, {self.semantic_stack.pop()}, )')

    def mult(self):
        t = self.get_temp()
        self.program_block.append(f'(MULT, {self.semantic_stack.pop()}, {self.semantic_stack.pop()}, {t})')
        self.semantic_stack.push(t)

    def add(self):
        t = self.get_temp()
        self.program_block.append(f'(ADD, {self.semantic_stack.pop()}, {self.semantic_stack.pop()}, {t})')
        self.semantic_stack.push(t)

    def save(self):
        self.semantic_stack.append(len(self.program_block))
        self.program_block.append('')

    def label(self):
        self.semantic_stack.append(len(self.program_block))

    def jpf_save(self):
        self.program_block[self.semantic_stack.pop()] = f'(JPF, {self.semantic_stack.pop()}, {len(self.program_block) + 1}, )'
        self.semantic_stack.push(len(self.program_block))
        self.semantic_stack.append('')

    def jp(self):
        self.program_block[self.semantic_stack.pop()] = f'(JP, {len(self.program_block)}, , )'

    def jpf(self):
        self.program_block[self.semantic_stack.pop()] = f'(JPF, {self.semantic_stack.pop()}, {len(self.program_block)}, )'

    def write_to_output(self):
        output = open('output.txt', 'w')
        for line in self.program_block:
            output.write(line)
        output.close()