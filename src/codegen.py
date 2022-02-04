
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

class Stack:
    def __init__(self):
        self.stack = []

    def push(self, element):
        self.stack.append(element)

    def pop(self):
        return self.stack.pop()


class Parameter:
    def __init__(self, name, address):
        self.address = address
        self.name = name

class Function:
    def __init__(self, name, address):
        self.name = name
        self.address = address
        self.parameters = []


class Array:
    def __init__(self):
        pass


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
        self.semantic_stack = Stack()
        self.functions = []
        self.paramter_declration = False
        self.symbol_table = {}

        self.actions = {
            "#pnum": self.pnum,
            "#pid": self.pid,
            "#assign": self.assign,
            "#exec_op": self.exec_op,
            "#push_op": self.push_op,
            "#declare_id": self.declare_id
        }
        self.operators = {
            '+': 'ADD',
            '*': 'MULT',
            '-': 'SUB',
            '==': 'EQ',
            '<': 'LT'
        }

    def run(self, action_name, token=None):
        print(action_name, token)
        self.actions[action_name](token)
        print("program block:", self.program_block)
        print("semantic stack: ", self.semantic_stack.stack)

    def get_temp(self):
        self.temp_count += 1
        return (self.temp_count * 4) + 3000 
    
    def get_data_var(self):
        self.data_var_count += 1
        return (self.data_var_count * 4) + 500

    def find_addr(self, token):
        if(self.symbol_table.keys().__contains__(token)):
            return self.symbol_table[token]
        else:
            address = self.get_data_var()
            self.symbol_table[token] = address
            return address

    def pid(self, token):
        address = self.find_addr(token['value'])
        self.semantic_stack.push(address)

    def pnum(self, token):
        num = token['value']
        self.semantic_stack.push(f'#{num}')


    #declarations
    def declare_id(self, token):
        self.semantic_stack.pop(); #pop the pid that had pushed to stack
        address = self.get_data_var()
        self.symbol_table[token['value']] = address
        self.program_block.append(f'(ASSIGN, #0, {address}, )')

    def declare_func(self, token):
        function = Function('', len(self.program_block))
        self.functions.append(function)

    def declare_id_parameter(self, token):
        self.paramter_declration = True
        pid = self.semantic_stack.pop()
        parameter = Parameter(pid, self.get_data_var())
        self.functions[-1].parameters.append(parameter)

    def declare_array_parameter(self, token):
        pass


    def call_func(self, token):
        func_addr = self.semantic_stack.pop()


    def assign(self, token):
        self.program_block.append(f'(ASSIGN, {self.semantic_stack.pop()}, {self.semantic_stack.stack[-1]}, )')

    def push_op(self, token):
        self.semantic_stack.push(self.operators[token['value']])
        
    def exec_op(self, token):
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