#!/usr/bin/env bash

set -e

# Create bin file
riscv64-unknown-elf-objcopy $1 -O binary $1.bin

# Program FPGA
litex_term --kernel $1.bin $2
