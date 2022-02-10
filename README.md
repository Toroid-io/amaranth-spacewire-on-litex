# Introduction

This is a test repository to run the
[amaranth-spacewire](https://github.com/Toroid-io/amaranth-spacewire)
core in a [LiteX](https://github.com/enjoy-digital/litex/) SoC.

Documentation regarding the `amaranth-spacewire` core can be found in
its repository.

# Requirements

## LiteX

Refer to the install instructions in the LiteX repository. Once
installed, add the [toroid](https://github.com/toroid-io/litex) remote:
`git remote add toroid https://github.com/toroid-io/litex)` and `git
checkout toroid/amaranth_spacewire`.

This is necessary to have some handy BIOS commands for the SpaceWire
node.

## Toolchain

The FPGA toolchain for your board vendor.

## Amaranth HDL

[Amaranth](https://github.com/amaranth-lang/amaranth) HDL.

## RISC-V toolchain

A RISC-V toolchain.

# Building and loading

Once the all the tools are in the `PATH`, then:

`python make.py --board de0nano --build --load`

