N = 2 ** 32
class riscv_simulator:
    def __init__(self) -> None:
        self.registers = [0]*32
        self.stack = [0] * 1024
        self.symbol_table = {}
        self.instruction_dict = {
            "add": self.add_func,
            "addi": self.addi_func,
            "sub": self.sub_func,
            "subi": self.subi_func,
            "mul": self.mul_func,
            "div": self.div_func,
            "li": self.li_func,
            "lw": self.lw_func,
            "sw": self.sw_func,
            "beq": self.beq_func,
            "bne": self.bne_func,
            "blt": self.blt_func,
            "bgt": self.bgt_func,
            "bge": self.bge_func,
            "jal": self.jal_func,
            "ret": self.ret_func
        }
        self.pc = 0
        self.is_debugging = False

    def load_program(self, path):
        try:
            with open(path, "r") as f:
                self.lines = [line.strip() for line in f.readlines()]
                self.lines = [line for line in self.lines if len(line) > 0]
                self.program_lines = [line for line in self.lines if line[0] != '.']
        except:
            print("The file you are trying to open does not exist")
    
    def print_registers(self):
        for i in range(32):
            print(f"x{i:<2d}: {self.registers[i]}")
    
    def print_stack(self, n = 16):
        for i in range(n):
            print(f"{i:<4d}: {self.stack[i]}")
    
    def stack_push(self, value):
        assert type(value) == int and value < N//2 and value >= -N//2, "Must be an integer of 32 bits"
        self.stack.append(value)
    
    def stack_pop(self):
        return self.stack.pop()

    def execute_program(self):
        self.preprocess()
        while self.pc < len(self.program_lines):
            # if self.is_debugging:
            #     print(f"Executing line {self.pc}: {self.program_lines[self.pc]}")
            self.execute_line(self.program_lines[self.pc])
            self.pc += 1
    
    def preprocess(self):
        gp = 0
        for line in self.lines:
            tokens = line.split(" ")
            if tokens[0][0] == '.':
                self.symbol_table[tokens[0]] = gp
                continue
            else:
                gp += 1
        return 
    
    def execute_line(self, line):
        tokens = line.split(" ")
        instruction_name = tokens[0]
        instruction_func = self.instruction_dict[instruction_name]
        instruction_func(*tokens[1:])

    def add_func(self, rd, rs1, rs2):
        self.registers[int(rd[1:])] = self.registers[int(rs1[1:])] + self.registers[int(rs2[1:])] % N
    
    def addi_func(self, rd, rs1, imm):
        self.registers[int(rd[1:])] = self.registers[int(rs1[1:])] + int(imm) % N

    def sub_func(self, rd, rs1, rs2):
        self.registers[int(rd[1:])] = self.registers[int(rs1[1:])] - self.registers[int(rs2[1:])] % N
    
    def subi_func(self, rd, rs1, imm):
        self.registers[int(rd[1:])] = self.registers[int(rs1[1:])] - int(imm) % N
    
    def mul_func(self, rd, rs1, rs2):
        self.registers[int(rd[1:])] = self.registers[int(rs1[1:])] * self.registers[int(rs2[1:])] % N
    
    def div_func(self, rd, rs1, rs2):
        assert self.registers[int(rs2[1:])] != 0, "Division by zero"
        self.registers[int(rd[1:])] = self.registers[int(rs1[1:])] // self.registers[int(rs2[1:])] % N
    
    def li_func(self, rd, imm):
        self.registers[int(rd[1:])] = int(imm)
    
    def lw_func(self, rd, address):
        offset, rs1 = address.split("(")
        self.registers[int(rd[1:])] = self.stack[self.registers[int(rs1[1:-1])] + int(offset)]
    
    def sw_func(self, rd, address):
        offset, rs1 = address.split("(")
        self.stack[self.registers[int(rs1[1:-1])] + int(offset)] = self.registers[int(rd[1:])]
    
    def beq_func(self, rs1, rs2, label):
        if self.registers[int(rs1[1:])] == self.registers[int(rs2[1:])]:
            self.pc = self.symbol_table[label] - 1
    
    def bne_func(self, rs1, rs2, label):
        if self.registers[int(rs1[1:])] != self.registers[int(rs2[1:])]:
            self.pc = self.symbol_table[label] - 1

    def blt_func(self, rs1, rs2, label):
        if self.registers[int(rs1[1:])] < self.registers[int(rs2[1:])]:
            self.pc = self.symbol_table[label] - 1
    
    def bgt_func(self, rs1, rs2, label):
        if self.registers[int(rs1[1:])] > self.registers[int(rs2[1:])]:
            self.pc = self.symbol_table[label] - 1
    
    def bge_func(self, rs1, rs2, label):
        if self.registers[int(rs1[1:])] >= self.registers[int(rs2[1:])]:
            self.pc = self.symbol_table[label] - 1
    
    def jal_func(self, rd, label):
        self.registers[int(rd[1:])] = self.pc
        self.pc = self.symbol_table[label] - 1

    def ret_func(self):
        self.pc = self.registers[1]


simulator = riscv_simulator()
simulator.load_program("test.txt")
simulator.is_debugging = False
simulator.preprocess()
simulator.execute_program()

simulator.print_stack(32)
simulator.print_registers()