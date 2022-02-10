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

# Installing `litex-amaranth-spacewire`

```
$ git submodule update --init --recursive
$ cd litex-amaranth-spacewire && python setup.py develop --user && cd ..
```

# Building and loading

Once the all the tools are in the `PATH`, then:

`python make.py --board de0nano --build --load`

# Error `gw_sh: symbol lookup error: /usr/lib/libfontconfig.so.1: undefined symbol: FT_Done_MM_Var`

If you hit this error, you can try prefixing the build command with `LD_PRELOAD=/usr/lib/libfreetype.so`.
