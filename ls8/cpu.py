"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""
    LDI = 0b10000010
    PRN = 0b01000111
    HLT = 0b00000001

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.running = True

    def ram_read(self, MDR):
        return self.ram[MDR]

    def ram_write(self, MAR, value):
        self.ram[MAR] = value

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010,  # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111,  # PRN R0
            0b00000000,
            0b00000001,  # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()
# pc === program counter, index of the current instruction
# ir === Instruction register

    def run(self):
        """Run the CPU."""
        while self.running:
            # read the current index
            ir = self.ram_read(self.pc)
# A. `LDI` - Set the value of a register to an integer.
            # curr index set 'integer'
            if ir == self.LDI:
                # registered number
                reg_num = self.ram_read(self.pc + 1)
                # value in register
                value = self.ram_read(self.pc + 2)
                # store our values
                self.ram_write(reg_num, value)
                # 3 bit instruction, move pointer
                self.pc += 3
# B. `PRN`- Print numeric value stored in the given register.
            # Print numeric value stored in the given register.
            elif ir == self.PRN:
                reg_num = self.ram[self.pc + 1]
                print(self.ram[reg_num])
                self.pc += 2
# C. 'HLT' INSTRUCTION.('HALTED')
            elif ir == self.HLT:
                self.running = False

            else:
                print(f"Unknown instruction {ir}")
