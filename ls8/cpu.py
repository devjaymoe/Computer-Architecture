"""CPU functionality."""

import sys

SP = 7

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.pc = 0
        self.ram = [0] * 256
        self.branch_table = {}

        self.reg[SP] = 0xf4

    def load(self):
        """Load a program into memory."""

        address = 0

        if len(sys.argv) != 2:
            print("usage: comp.py filename")
            sys.exit(1)

        try:
            with open(sys.argv[1]) as f:
                for line in f:
                    try:
                        line = line.split('#',1)[0]
                        line = int(line, 2)  # int() is base 10 by default
                        self.ram[address] = line
                        address += 1
                    except ValueError:
                        pass

        except FileNotFoundError:
            print(f"Couldn't find file {sys.argv[1]}")
            sys.exit(1)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]    
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def ram_read(self, MAR):

        operand_a = self.ram[self.pc + 1]
        operand_b = self.ram[self.pc + 2]

        return self.ram[MAR]

    def ram_write(self, MDR, MAR):
        self.ram[MAR] = MDR

    def run(self):
        """Run the CPU."""

        running = True

        ops = {
            0b10000010: 'LDI',
            0b01000111: 'PRN',
            0b00000001: 'HLT',
            0b10100010: 'MUL',
            0b01000101: 'PUSH',
            0b01000110: 'POP'
        }
        # print("Ram: ", self.ram)
        # print("PC: ", self.pc)
        # print("Reg: ", self.reg)

        while running:
            # self.trace()

            instructions = self.ram_read(self.pc)

            if ops[instructions] == 'LDI': # LDI
                # set value of a register
                reg_num = self.ram[self.pc + 1]
                value = self.ram[self.pc + 2]

                self.reg[reg_num] = value

                self.pc += 3   

            elif ops[instructions] == 'PRN': # PRN
                # print register
                reg_num = self.ram[self.pc + 1]
                print(self.reg[reg_num])

                self.pc += 2

            elif ops[instructions] == 'HLT': # HLT
                # halt the cpu and exit em
                running = False

            elif ops[instructions] == 'MUL':
                reg_a = self.ram[self.pc + 1]
                reg_b = self.ram[self.pc + 2]

                self.alu('MUL', reg_a, reg_b)

                self.pc += 3

            elif ops[instructions] == 'PUSH':
                self.reg[SP] -= 1
                self.reg[SP] &= 0xff

                reg_num = self.ram[self.pc + 1]
                value = self.reg[reg_num]

                address_to_push = self.reg[SP]
                # print(address_to_push)
                self.ram[address_to_push] = value

                self.pc += 2

            elif ops[instructions] == 'POP':
                address_to_pop = self.reg[SP]
                value = self.ram[address_to_pop]

                reg_num = self.ram[self.pc + 1]
                self.reg[reg_num] = value
                
                self.reg[SP] += 1
                
                self.pc += 2

            else:
                print(f"Unknown instruction {instructions}")
            
            # print(self.reg)
