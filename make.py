#!/usr/bin/env python3

#
# This file is part of Linux-on-LiteX-VexRiscv
#
# Copyright (c) 2019-2021, Linux-on-LiteX-VexRiscv Developers
# SPDX-License-Identifier: BSD-2-Clause

import os
import sys
import argparse

from litex.soc.integration.builder import Builder

from litex_amaranth_spacewire import SpWNode

from spw_peripheral import _spw_node_pins

# Board definition----------------------------------------------------------------------------------

class Board:
    soc_kwargs = {"integrated_rom_size": 0x10000, "l2_size": 0}
    def __init__(self, soc_cls=None, soc_capabilities={}, soc_constants={}, bitstream_ext=""):
        self.soc_cls          = soc_cls
        self.soc_capabilities = soc_capabilities
        self.soc_constants    = soc_constants
        self.bitstream_ext    = bitstream_ext

    def load(self, filename):
        prog = self.platform.create_programmer()
        prog.load_bitstream(filename)

    def flash(self, filename):
        prog = self.platform.create_programmer()
        prog.flash(0, filename)

#---------------------------------------------------------------------------------------------------
# Intel Boards
#---------------------------------------------------------------------------------------------------

# De0Nano support ----------------------------------------------------------------------------------

class De0Nano(Board):
    soc_kwargs = {"uart_name": "jtag_uart", "l2_size" : 2048} # Use Wishbone and L2 for memory accesses.
    def __init__(self):
        #import target_de0nano as de0nano
        from litex_boards.targets import de0nano
        Board.__init__(self, de0nano.BaseSoC, soc_capabilities={
            # Communication
            "serial",
        }, bitstream_ext=".sof")

#---------------------------------------------------------------------------------------------------
# Gowin Boards
#---------------------------------------------------------------------------------------------------

# Tang Nano 4k support ----------------------------------------------------------------------------------

class TangNano4k(Board):
    soc_kwargs = {"with_video_terminal": False, "cpu_type": "gowin_emcu", "uart_name": "serial", "l2_size" : 2048} # Use Wishbone and L2 for memory accesses.
    def __init__(self):
        from litex_boards.targets import tang_nano_4k
        Board.__init__(self, tang_nano_4k.BaseSoC, soc_capabilities={
            # Communication
            "serial",
        }, bitstream_ext=".fs")

#---------------------------------------------------------------------------------------------------
# Build
#---------------------------------------------------------------------------------------------------

supported_boards = {
    # Altera/Intel
    "de0nano":          De0Nano,

    # Gowin Semi
    "tangnano4k":       TangNano4k
}

def main():
    description = "SpaceWire node\n\n"
    description += "Available boards:\n"
    for name in supported_boards.keys():
        description += "- " + name + "\n"
    parser = argparse.ArgumentParser(description=description, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--board",          required=True,            help="FPGA board")
    parser.add_argument("--device",         default=None,             help="FPGA device")
    parser.add_argument("--variant",        default=None,             help="FPGA board variant")
    parser.add_argument("--toolchain",      default=None,             help="Toolchain use to build")
    parser.add_argument("--build",          action="store_true",      help="Build bitstream")
    parser.add_argument("--load",           action="store_true",      help="Load bitstream (to SRAM)")
    parser.add_argument("--flash",          action="store_true",      help="Flash bitstream/images (to SPI Flash)")
    parser.add_argument("--doc",            action="store_true",      help="Build documentation")
    args = parser.parse_args()

    # Board(s) selection ---------------------------------------------------------------------------
    if args.board == "all":
        board_names = list(supported_boards.keys())
    else:
        args.board = args.board.lower()
        args.board = args.board.replace(" ", "_")
        board_names = [args.board]

    # Board(s) iteration ---------------------------------------------------------------------------
    for board_name in board_names:
        board = supported_boards[board_name]()
        soc_kwargs = Board.soc_kwargs
        soc_kwargs.update(board.soc_kwargs)

        # CPU parameters ---------------------------------------------------------------------------
        # Do memory accesses through Wishbone and L2 cache when L2 size is configured.
        args.with_wishbone_memory = soc_kwargs["l2_size"] != 0

        # SoC parameters ---------------------------------------------------------------------------
        if args.device is not None:
            soc_kwargs.update(device=args.device)
        if args.variant is not None:
            soc_kwargs.update(variant=args.variant)
        if args.toolchain is not None:
            soc_kwargs.update(toolchain=args.toolchain)
        if "crossover" in board.soc_capabilities:
            soc_kwargs.update(uart_name="crossover")
        if "usb_fifo" in board.soc_capabilities:
            soc_kwargs.update(uart_name="usb_fifo")
        if "usb_acm" in board.soc_capabilities:
            soc_kwargs.update(uart_name="usb_acm")

        # SoC creation -----------------------------------------------------------------------------
        soc = board.soc_cls(**soc_kwargs)

        board.platform = soc.platform

        # SoC constants ----------------------------------------------------------------------------
        for k, v in board.soc_constants.items():
            soc.add_constant(k, v)

        # SpaceWire peripheral ---------------------------------------------------------------------
        board.platform.add_extension(_spw_node_pins[board_name])
        soc.submodules.spw_node = SpWNode(soc.platform,
                pads=soc.platform.request("spw_node"), time_master=True)

        # Build ------------------------------------------------------------------------------------
        build_dir = os.path.join("build", board_name)
        builder   = Builder(soc,
            output_dir   = os.path.join("build", board_name),
            bios_options = ["TERM_MINI"],
            csr_json     = os.path.join(build_dir, "csr.json"),
            csr_csv      = os.path.join(build_dir, "csr.csv")
        )
        builder.build(run=args.build, build_name=board_name)

        # Load FPGA bitstream ----------------------------------------------------------------------
        if args.load:
            if board_name == "tangnano4k":
                board.load(filename=os.path.join(builder.gateware_dir, 'impl', 'pnr', 'project' + board.bitstream_ext))
            else:
                board.load(filename=os.path.join(builder.gateware_dir, soc.build_name + board.bitstream_ext))

        # Flash bitstream/images (to SPI Flash) ----------------------------------------------------
        if args.flash:
            board.flash(filename=os.path.join(builder.gateware_dir, soc.build_name + board.bitstream_ext))

        # Generate SoC documentation ---------------------------------------------------------------
        if args.doc:
            soc.generate_doc(board_name)

if __name__ == "__main__":
    main()
