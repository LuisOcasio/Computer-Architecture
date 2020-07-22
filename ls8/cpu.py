"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""
    LDI = 0b10000010
    PRN = 0b01000111
    HLT = 0b00000001
    MUL = 0b10100010

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.running = True

    def ram_read(self, MDR):
        return self.ram[MDR]

    def ram_write(self, MAR, value):
        self.reg[MAR] = value

    def load(self, program=None):
        """Load a program into memory."""

        address = 0

        if len(sys.argv) < 2:
            print(
                "Please pass in a second filename: python3 in_and_out.py second_filename.py")
            sys.exit()
        try:
            address = 0
            with open(program) as file:
                for line in file:
                    split_line = line.split('#')[0]
                    command = split_line.strip()
                    if command == '':
                        continue
                    instruction = int(command, 2)
                    self.ram[address] = instruction
                    address += 1
        except FileNotFoundError:
            print(f'{sys.argv[0]}: {sys.argv[1]} file was not found')
            sys.exit()

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
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
                print(self.reg[reg_num])
                self.pc += 2
            elif ir == self.MUL:
                reg_num1 = self.ram_read(self.pc + 1)
                reg_num2 = self.ram_read(self.pc + 2)
                self.alu("MUL", reg_num1, reg_num2)
                self.pc += 3
# C. 'HLT' INSTRUCTION.('HALTED')
            elif ir == self.HLT:
                self.running = False

            else:
                print(f"Unknown instruction {ir}")
