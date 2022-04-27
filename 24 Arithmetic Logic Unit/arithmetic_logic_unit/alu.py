# https://adventofcode.com/2021/day/24


class ALU:
    def __init__(self):
        self.vars = {'w': 0, 'x': 0, 'y': 0, 'z': 0}
        self.funcs = {'inp': self._inp_, 'add': self._add_, 'mul': self._mul_,
                      'div': self._div_, 'mod': self._mod_, 'eql': self._eql_}
    
    def execute(self, instruction):
        func = self.funcs[instruction[0]]
        var = instruction[1]
        val = self.vars.get(instruction[2])
        if val is None:
            val = int(instruction[2])
        func(var, val)

    def get(self, var):
        return self.vars[var]

    def _inp_(self, var, val):
        self.vars[var] = val
    
    def _add_(self, var, val):
        self.vars[var] += val

    def _mul_(self, var, val):
        self.vars[var] *= val

    def _div_(self, var, val):
        if not val == 0:
            self.vars[var] //= val
    
    def _mod_(self, var, val):
        if not self.vars[var] < 0 or val <= 0:
            self.vars[var] %= val

    def _eql_(self, var, val):
        if self.vars[var] == val:
            self.vars[var] = 1
        else:
            self.vars[var] = 0


def negation(num):
    with open('arithmetic_logic_unit/negation.txt') as file:
        program = [line.strip().split() for line in file.readlines()]
    a = ALU()
    for line in program:
        if line[0] == 'inp':
            line.append(num)
        a.execute(line)
    return a.get('x')


def check_3x_equal(num1, num2):
    with open('arithmetic_logic_unit/check_3x_equal.txt') as file:
        program = [line.strip().split() for line in file.readlines()]
    a = ALU()
    curr_num = num1
    for line in program:
        if line[0] == 'inp':
            line.append(curr_num)
            curr_num = num2
        a.execute(line)
    return True if a.get('z') == 1 else False


def binary(num):
    with open('arithmetic_logic_unit/binary.txt') as file:
        program = [line.strip().split() for line in file.readlines()]
    a = ALU()
    for line in program:
        if line[0] == 'inp':
            line.append(num)
        a.execute(line)
    return f"{a.get('w')}{a.get('x')}{a.get('y')}{a.get('z')}"


def monad(num):
    """Check if submarine's model number is valid.

    Submarine model numbers are always fourteen-digit
    numbers consisting only of digits 1 through 9.
    The digit 0 cannot appear in a model number.
    """
    with open('real_input.txt') as file:
        monad_program = [line.strip().split() for line in file.readlines()]
    a = ALU()
    curr = 0
    num = str(num)
    for line in monad_program:
        if line[0] == 'inp':
            line.append(num[curr])
            curr += 1
        a.execute(line)
    if a.get('z') == 0:
        return True
    else:
        return False
