
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
        self.stack = []

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
        self.data_var_count = -1
        self.semantic_stack = SemanticStack()
        self.symbol_table = {}
        self.argument_pointer = 0
        self.functions_address = {}
        self.actions = {
            "#pnum": self.pnum,
            "#pid": self.pid,
            "#assign": self.assign,
            "#exec_op": self.exec_op,
            "#push_op": self.push_op,
        }
        self.operators = {
            '+': 'ADD',
            '*': 'MULT',
            '-': 'SUB',
            '==': 'EQ',
            '<': 'LT'
        }

    def run(self, action_name, lexeme=None):
        print(action_name, lexeme)
        self.actions[action_name](lexeme)
        print("program block:" ,self.program_block)
        print("semantic stack: ", self.semantic_stack.stack)

    def get_temp(self):
        self.temp_count += 1
        return (self.temp_count * 4) + 3000 
    
    def get_data_var(self):
        self.data_var_count += 1
        return (self.data_var_count * 4) + 500

    def find_addr(self, lexeme):
        if(self.symbol_table.keys().__contains__(lexeme)):
            return self.symbol_table[lexeme]
        else:
            address = self.get_data_var()
            self.symbol_table[lexeme] = address
            return address

    def pid(self, lexeme):
        address = self.find_addr(lexeme['value'])
        self.semantic_stack.push(address)

    def pnum(self, lexeme):
        num = lexeme['value']
        self.semantic_stack.push(f'#{num}')
        
    def assign(self, lexeme):
        self.program_block.append(f'(ASSIGN, {self.semantic_stack.pop()}, {self.semantic_stack.stack[-1]}, )')

    def push_op(self, lexeme):
        self.semantic_stack.push(self.operators[lexeme['value']])
        
    def exec_op(self, lexeme):
        second_operand = self.semantic_stack.pop()
        operator = self.semantic_stack.pop()
        first_operand = self.semantic_stack.pop()
        result_temp = self.get_temp()
        self.program_block.append(f'({operator}, {first_operand}, {second_operand}, {result_temp})')
        self.semantic_stack.push(result_temp)

    def write_to_output(self):
        output = open('output.txt', 'w')
        for line in self.program_block:
            output.write(line + '\n')
        output.close()