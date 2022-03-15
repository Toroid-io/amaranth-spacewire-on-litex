import os
import sys
import argparse

from litex.soc.integration.builder import Builder
from litex.soc.integration.soc_core import *
from litex.soc.integration.builder import *
from litex.build.generic_platform import *
from litex.soc.cores.uart import UARTWishboneBridge

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

# De0Nano support ----------------------------------------------------------------------------------
class De0Nano(Board):
    soc_kwargs = {"uart_name": "serial", "cpu_variant": "standard+debug", "l2_size" : 2048} # Use Wishbone and L2 for memory accesses.
    def __init__(self):
        from litex_boards.targets import de0nano
        Board.__init__(self, de0nano.BaseSoC, bitstream_ext=".sof")

# Tang Nano 4k support ----------------------------------------------------------------------------------
class TangNano4k(Board):
    soc_kwargs = {"with_video_terminal": False, "cpu_variant": "minimal", "uart_name": "serial", "l2_size" : 2048} # Use Wishbone and L2 for memory accesses.
    def __init__(self):
        from litex_boards.targets import tang_nano_4k
        Board.__init__(self, tang_nano_4k.BaseSoC, bitstream_ext=".fs")

# Tang Nano 9k support ----------------------------------------------------------------------------------
class TangNano9k(Board):
    soc_kwargs = {"with_video_terminal": False, "cpu_variant": "standard+debug", "l2_size" : 2048} # Use Wishbone and L2 for memory accesses.
    def __init__(self):
        from litex_boards.targets import tang_nano_9k
        Board.__init__(self, tang_nano_9k.BaseSoC, bitstream_ext=".fs")

#---------------------------------------------------------------------------------------------------
# Build
#---------------------------------------------------------------------------------------------------

supported_boards = {
    # Altera/Intel
    "de0nano":          De0Nano,

    # Gowin Semi
    "tangnano4k":       TangNano4k,
    "tangnano9k":       TangNano9k
}

def main():
    description = "SpaceWire node\n\n"
    description += "Available boards:\n"
    for name in supported_boards.keys():
        description += "- " + name + "\n"
    parser = argparse.ArgumentParser(description=description, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--board",          required=True,            help="FPGA board")
    parser.add_argument("--build",          action="store_true",      help="Build bitstream")
    parser.add_argument("--load",           action="store_true",      help="Load bitstream (to SRAM)")
    parser.add_argument("--flash",          action="store_true",      help="Flash bitstream/images (to SPI Flash)")
    parser.add_argument("--with-uartbone",  action="store_true",      help="Add UARTBone to the board")
    parser.add_argument("--time-master",    action="store_true",      help="SpaceWire node is the time master")
    parser.add_argument("--rx-tokens",      type=int, default=7,      help="Number of RX tokens (fifo size / 8)")
    parser.add_argument("--tx-tokens",      type=int, default=7,      help="Number of TX tokens (fifo size / 8)")
    args = parser.parse_args()

    soc_kwargs             = {}
    builder_kwargs         = {}

    # Board selection ---------------------------------------------------------------------------
    args.board = args.board.lower()
    board_name = args.board

    board = supported_boards[board_name]()
    soc_kwargs.update(Board.soc_kwargs)
    soc_kwargs.update(board.soc_kwargs)

    # CPU parameters ---------------------------------------------------------------------------
    # Do memory accesses through Wishbone and L2 cache when L2 size is configured.
    args.with_wishbone_memory = soc_kwargs["l2_size"] != 0

    # SoC creation -----------------------------------------------------------------------------
    soc = board.soc_cls(**soc_kwargs)

    board.platform = soc.platform

    # SoC constants ----------------------------------------------------------------------------
    for k, v in board.soc_constants.items():
        soc.add_constant(k, v)

    # SpaceWire peripheral ---------------------------------------------------------------------
    board.platform.add_extension(_spw_node_pins[board_name])

    if args.with_uartbone:
        soc.add_uartbone(name="uartbone")

    soc.submodules.spw_node = SpWNode(soc.platform,
            pads=soc.platform.request("spw_node"),
            time_master=args.time_master,
            rx_tokens=args.rx_tokens,
            tx_tokens=args.tx_tokens)

    # Build ------------------------------------------------------------------------------------
    build_dir = os.path.join("build", board_name)
    builder_kwargs["csr_csv"] = os.path.join(build_dir, "csr.csv")
    builder_kwargs["csr_json"] = os.path.join(build_dir, "csr.json")
    builder_kwargs["output_dir"] = os.path.join("build", board_name)
    builder_kwargs["bios_options"] = ["TERM_MINI"]
    builder = Builder(soc, **builder_kwargs)

    builder.build(build_name=board_name, run=args.build)

    # Load FPGA bitstream ----------------------------------------------------------------------
    if args.load:
        if board_name == "tangnano4k":
            board.load(filename=os.path.join(builder.gateware_dir, 'impl', 'pnr', 'project' + board.bitstream_ext))
        elif board_name == "tangnano9k":
            board.load(filename=os.path.join(builder.gateware_dir, 'impl', 'pnr', 'project' + board.bitstream_ext))
        else:
            board.load(filename=os.path.join(builder.gateware_dir, soc.build_name + board.bitstream_ext))

    # Flash bitstream/images (to SPI Flash) ----------------------------------------------------
    if args.flash:
        board.flash(filename=os.path.join(builder.gateware_dir, soc.build_name + board.bitstream_ext))

if __name__ == "__main__":
    main()
