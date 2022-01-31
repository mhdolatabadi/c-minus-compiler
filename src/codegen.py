
# Available 3-addrress codes:
# ADD A1 A2 R => R = A1 + A2
# MULT A1 A2 R => R = A1 * A2
# SUB A1 A2 R => R = A1 - A2
# EQ A1 A2 R
# LT A1 A2 R
# ASSIGN A R
# JPF A L
# JP L
# PRINT A

class SemanticStack:
    def __init__(self):
        self.stack = [1,2,3,4,5]

    def push(self, element):
        self.stack.append(element)

    def pop(self):
        return self.stack.pop()


class CodeGen:
    operators = {
        '+': 'ADD',
        '-': 'SUB',
        '*': 'MULT',
        '<': 'LT',
        '==': 'EQ'
    }
    def __init__(self):
        self.program_block = []
        self.temp_count = -1
        self.semantic_stack = SemanticStack()
        self.actions = {
            "#pnum": self.pnum,
            "#pid": self.pid,
            "#assign": self.assign,
            "#exec_op": self.exec_op,
            "#push_op": self.push_op,
            "#label": self.label,
        }
        self.operators = {
            '+': 'ADD',
            '*': 'MULT',
            '-': 'SUB',
            '==': 'EQ',
            '<': 'LT'
        }


    def run(self, action_name, lexeme=None):
        self.actions[action_name](lexeme)

    def get_temp(self):
        self.temp_count += 1
        return (self.temp_count * 4) + 3000 

    def find_addr(self, lexeme):
        symbol_table = open('./symbol_table.txt', 'r')
        for line in symbol_table:
            if(line.split('\t')[1] == lexeme):
                return line.split('.')[0]

    def pid(self, lexeme):
        address = self.find_addr(lexeme)
        self.semantic_stack.push(address)

    def pnum(self, lexeme):
        num = lexeme['value']
        self.semantic_stack.push(f'#{num}')
        

    def assign(self, lexeme):
        self.program_block.append(f'(ASSIGN, {self.semantic_stack.pop()}, {self.semantic_stack.stack[-1]}, )')

    def label(self):
        self.semantic_stack.push(len(self.program_block))

    def jpf_save(self):
        self.program_block[self.semantic_stack.pop()] = f'(JPF, {self.semantic_stack.pop()}, {len(self.program_block) + 1}, )'
        self.semantic_stack.push(len(self.program_block))
        self.semantic_stack.push('')

    def jp(self):
        self.program_block[self.semantic_stack.pop()] = f'(JP, {len(self.program_block)}, , )'

    def jpf(self):
        self.program_block[self.semantic_stack.pop()] = f'(JPF, {self.semantic_stack.pop()}, {len(self.program_block)}, )'

    def push_op(self, lexeme):
        print(lexeme['value'])
        self.semantic_stack.push(self.operators[lexeme['value']])
        
    def exec_op(self, lexeme):
        second_operand = self.semantic_stack.pop()
        operator = self.semantic_stack.pop()
        first_operand = self.semantic_stack.pop()
        result_temp = self.get_temp()
        self.program_block.append(f'({operator}, {first_operand}, {second_operand}, {result_temp})')
        self.semantic_stack.push(result_temp)
    
    def pop(self, lexeme):
        self.semantic_stack.pop()



    def write_to_output(self):
        output = open('output.txt', 'w')
        for line in self.program_block:
            output.write(line + '\n')
        output.close()