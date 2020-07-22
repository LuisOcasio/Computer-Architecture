#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()

file_name = sys.argv[1]
cpu.load(file_name)

cpu.run()


# LS-8 has 8-bit addressing, so can address 256 bytes of RAM total.

# Execution Sequence

# 1. The instruction pointed to by the `PC` is fetched from RAM, decoded, and executed.
# 2. If the instruction does _not_ set the `PC` itself, the `PC` is advanced to point to the subsequent instruction.
# 3. If the CPU is not halted by a `HLT` instruction, go to step 1.

# INSTRUCTIONS TO IMPLEMENT

# A. `LDI` - Set the value of a register to an integer.

# B. `PRN`- Print numeric value stored in the given register.

# C. 'HLT' INSTRUCTION.('HALTED')
