# Introduction

This is a test repository to run the
[amaranth-spacewire](https://github.com/Toroid-io/amaranth-spacewire)
core in a [LiteX](https://github.com/enjoy-digital/litex/) SoC.

Documentation regarding the `amaranth-spacewire` core can be found in
its repository.

# Requirements

## LiteX

Refer to the install instructions in the
[LiteX](https://github.com/enjoy-digital/litex/) repository.

## Toolchain

The FPGA toolchain for your board vendor.

## Amaranth HDL

[Amaranth](https://github.com/amaranth-lang/amaranth) HDL.

## RISC-V toolchain

A RISC-V toolchain. It can be installed at the same time that you
install LiteX.

# Installing `litex-amaranth-spacewire`

```
$ git submodule update --init --recursive
$ cd litex-amaranth-spacewire && python setup.py develop --user && cd ..
```

# Building and loading

## Terasic `de0nano`

1. Add the RISCV toolchain and the FPGA toolchain to the PATH

```shell
$ export PATH=/path/to/toolchain/riscv64-unknown-elf-gcc-xxxx/bin:$PATH
$ export PATH=/path/to/toolchain/XX.X/quartus/bin
$ export QUARTUS_ROOTDIR=/path/to/toolchain/XX.X/quartus/bin
```
2. Build the bitstream

```shell
$ python make.py --board de0nano --build`
```

## SiPeed `tangnano4k`

1. Add the RISCV toolchain and the FPGA toolchain to the PATH

```shell
$ export PATH=/path/to/toolchain/riscv64-unknown-elf-gcc-xxxx/bin:$PATH
$ export PATH=/path/to/toolchain/IDE/bin:$PATH
```

2. Build the bitstream

```shell
$ python make.py --board tangnano4k --build --rx-tokens 4 --tx-tokens 4
```

The `--rx-tokens` and `--tx-tokens` flags are added to correctly fit the
design in the FPGA.

# Building the demo app

The demo app will activate the SpaceWire IP and show the link status. It
can be found under the `app` directory.

In order to be built you need to add the RISCV toolchain to the path,
and export the `BUILD_DIR` variable. Assuming that this repository is
placed in `REPO_PATH`, and that you built for the board `BOARD`, then
you should:

```shell
$ export BUILD_DIR=REPO_PATH/build/BOARD
```

Then run `make` in the app directory. This will generate the
`spw_app.bin` binary. It can be uploaded to your board with `litex_term`
with the following command:

```shell
$ litex_term --kernel=spw_app.bin --serial-boot {SERIALPORT}
```

# Troubleshooting

## undefined symbol: `FT_Done_MM_Var`

If you hit the error

```
Error gw_sh: symbol lookup error: /usr/lib/libfontconfig.so.1: undefined symbol: FT_Done_MM_Var
```

you can try prefixing the build command with `LD_PRELOAD=/usr/lib/libfreetype.so`.
