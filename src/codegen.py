
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

from array import ArrayType
from scanner import SymbolTable

class Stack:
    def __init__(self):
        self.stack = []

    def push(self, element):
        self.stack.append(element)

    def pop(self):
        return self.stack.pop()

    def get_stack(self):
        return self.stack


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
    def __init__(self, name, offset, length):
        self.name = name
        self.offset = offset
        self.length = length

class Variable:
    def __init__(self):
        pass

class Scope:
    def __init__(self):
        self.variables = []




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
        self.arrays = []
        self.scopes = []

        self.current_token = None
        self.current_scope = None

        self.actions = {
            "#pnum": self.pnum,
            "#pid": self.pid,
            "#assign": self.assign,
            "#exec_op": self.exec_op,
            "#push_op": self.push_op,
            "#declare_id": self.declare_id,
            "#declare_array": self.declare_array,
            "#declare_func": self.declare_func,
            "#declare_array_parameter": self.declare_array_parameter,
            "#declare_id_parameter": self.declare_id_parameter,
            "#scope_start": self.scope_start,
            "#scope_end": self.scope_end,
        }

        self.operators = {
            '+': 'ADD',
            '*': 'MULT',
            '-': 'SUB',
            '==': 'EQ',
            '<': 'LT'
        }


    #memory management

    def get_temp(self):
        self.temp_count += 1
        return (self.temp_count * 4) + 3000 
    
    def get_data_var(self):
        self.data_var_count += 1
        return (self.data_var_count * 4) + 500


    #declarations

    def declare_id(self):
        address = self.semantic_stack.pop()
        record = SymbolTable.get_record_by_address(address)
        record.type = 'Id'

    def declare_array(self):
        array_size = self.semantic_stack.pop()[1:]
        address = self.semantic_stack.pop()
        record = SymbolTable.get_record_by_address(address)
        record.type = 'Array'
        record.size = array_size
        array = Array(record.token, record.address, array_size)
        self.arrays.append(array)
        self.data_var_count += array_size - 1

    def declare_func(self):
        address = self.semantic_stack.pop()
        record = SymbolTable.get_record_by_address(address)
        record.type = 'Function'
        function = Function(record.token, record.address)
        self.functions.append(function)

    def declare_array_parameter(self):
        address = self.semantic_stack.pop()
        record = SymbolTable.get_record_by_address(address)
        parameter = Parameter(record.token, address)
        self.functions[-1].parameters.append(parameter)

    def declare_id_parameter(self):
        address = self.semantic_stack.pop()
        record = SymbolTable.get_record_by_address(address)
        parameter = Parameter(record.token, address)
        self.functions[-1].parameters.append(parameter)

    # scopes
    def scope_start(self):
        scope = Scope()
        self.scopes.append(scope)
        self.current_scope = scope

    def scope_end(self):
        pass

    def call_func(self):
        pass

    def pid(self):
        record = SymbolTable.get_record_by_name(self.current_token['value'])
        if not record.address or record.address == 0:
            address = self.get_data_var()
            record.address = address
        self.semantic_stack.push(record.address)
        
    def pnum(self):
        num = self.current_token['value']
        self.semantic_stack.push(f'#{num}')

    def assign(self):
        self.program_block.append(f'(ASSIGN, {self.semantic_stack.pop()}, {self.semantic_stack.stack[-1]}, )')

    def push_op(self):
        self.semantic_stack.push(self.operators[self.current_token['value']])
        
    def exec_op(self):
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

    def run(self, action_name, token=None):
        print(action_name, token)
        self.current_token = token
        self.actions[action_name]()
        print("program block:", self.program_block)
        print("semantic stack: ", self.semantic_stack.stack)