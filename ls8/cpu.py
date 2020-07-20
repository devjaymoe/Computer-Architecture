"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.pc = 0
        self.ram = [0] * 256
        self.cache = [0] * 8

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
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
            0b00000001: 'HLT'
        }

        while running:

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

            else:
                print(f"Unknown instruction {instructions}")

