import os
import sys
import argparse

from migen import *

from litex.soc.integration.builder import Builder
from litex.soc.integration.soc_core import *
from litex.soc.integration.builder import *
from litex.soc.cores.uart import UARTWishboneBridge
from litex.build.generic_platform import *
from litex.build.io import DifferentialOutput, DifferentialInput

from litex_amaranth_spacewire import SpWNode

from spw_peripheral import _spw_node_pins

# Board definition----------------------------------------------------------------------------------

class Board:
    soc_kwargs = {"integrated_rom_size": 0x10000, "l2_size": 0}
    def __init__(self, soc_cls=None, soc_capabilities={}, bitstream_ext=""):
        self.soc_cls          = soc_cls
        self.soc_capabilities = soc_capabilities
        self.bitstream_ext    = bitstream_ext

    def load(self, filename):
        prog = self.platform.create_programmer()
        prog.load_bitstream(filename)

    def flash(self, filename):
        prog = self.platform.create_programmer()
        prog.flash(0, filename)

# De0Nano support ----------------------------------------------------------------------------------
class De0Nano(Board):
    soc_kwargs = {"uart_name": "serial", "cpu_variant": "standard+debug"}
    def __init__(self):
        from litex_boards.targets import terasic_de0nano
        Board.__init__(self, terasic_de0nano.BaseSoC, bitstream_ext=".sof")

# Tang Nano 4k support ----------------------------------------------------------------------------------
class TangNano4k(Board):
    soc_kwargs = {"with_video_terminal": False, "cpu_variant": "minimal", "uart_name": "serial"}
    def __init__(self):
        from litex_boards.targets import sipeed_tang_nano_4k
        Board.__init__(self, sipeed_tang_nano_4k.BaseSoC, bitstream_ext=".fs")

# Tang Nano 9k support ----------------------------------------------------------------------------------
class TangNano9k(Board):
    soc_kwargs = {"with_video_terminal": False, "cpu_variant": "standard+debug"}
    def __init__(self):
        from litex_boards.targets import sipeed_tang_nano_9k
        Board.__init__(self, sipeed_tang_nano_9k.BaseSoC, bitstream_ext=".fs")

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


def add_spw(args, soc):
    soc.platform.add_extension(_spw_node_pins[args.board])
    
    if args.lvds:
        class Object(object):
            pass

        spw_signals = Object()
        spw_signals.d_input = Signal()
        spw_signals.d_output = Signal()
        spw_signals.s_input = Signal()
        spw_signals.s_output = Signal()

        lvds = soc.platform.request("spw_node_lvds")

        soc.specials += DifferentialInput(lvds.d_input_p, lvds.d_input_n, spw_signals.d_input)
        soc.specials += DifferentialInput(lvds.s_input_p, lvds.s_input_n, spw_signals.s_input)
        soc.specials += DifferentialOutput(spw_signals.d_output, lvds.d_output_p, lvds.d_output_n)
        soc.specials += DifferentialOutput(spw_signals.s_output, lvds.s_output_p, lvds.s_output_n)

        soc.submodules.spw_node = SpWNode(soc.platform,
                pads=spw_signals,
                src_freq=int(float(args.sys_clk_freq)),
                reset_freq=int(float(args.reset_freq)),
                user_freq=int(float(args.user_freq)),
                time_master=args.time_master,
                rx_tokens=args.rx_tokens,
                tx_tokens=args.tx_tokens)
    else:
        soc.submodules.spw_node = SpWNode(soc.platform,
                pads=soc.platform.request("spw_node_se"),
                src_freq=int(float(args.sys_clk_freq)),
                reset_freq=int(float(args.reset_freq)),
                user_freq=int(float(args.user_freq)),
                time_master=args.time_master,
                rx_tokens=args.rx_tokens,
                tx_tokens=args.tx_tokens)


def de0nano_main(parser, target_group, soc_kwargs, builder_kwargs):
    args = parser.parse_args()
    
    board = De0Nano()

    soc = board.soc_cls(**soc_kwargs)

    if args.with_uartbone:
        soc.add_uartbone(name="uartbone")

    if args.with_jtagbone:
        soc.add_jtagbone()

    # SpaceWire peripheral ---------------------------------------------------------------------
    add_spw(args, soc)
    # ------------------------------------------------------------------------------------------

    # Build ------------------------------------------------------------------------------------
    builder = Builder(soc, **builder_kwargs)
    if args.build:
        builder.build()

    # Load FPGA bitstream ----------------------------------------------------------------------
    if args.load:
        board.load(filename=os.path.join(builder.gateware_dir, soc.build_name + board.bitstream_ext))

    # Flash bitstream/images (to SPI Flash) ----------------------------------------------------
    if args.flash:
        board.flash(filename=os.path.join(builder.gateware_dir, soc.build_name + board.bitstream_ext))

def tangnano9k_main(parser, target_group, soc_kwargs, builder_kwargs):
    target_group.add_argument("--bios-flash-offset",    default="0x0",            help="BIOS offset in SPI Flash.")
    target_group.add_argument("--with-spi-sdcard",      action="store_true",      help="Enable SPI-mode SDCard support.")
    target_group.add_argument("--with-video-terminal",  action="store_true",      help="Enable Video Terminal (HDMI).")
    target_group.add_argument("--prog-kit",             default="openfpgaloader", help="Programmer select from Gowin/openFPGALoader.")

    args = parser.parse_args()

    board = TangNano9k()

    soc_kwargs["sys_clk_freq"] = int(float(args.sys_clk_freq))
    soc_kwargs["bios_flash_offset"] = int(args.bios_flash_offset, 0)
    soc_kwargs["with_video_terminal"] = args.with_video_terminal
    soc = board.soc_cls(**soc_kwargs)
    
    if args.with_uartbone:
        soc.add_uartbone(name="uartbone")

    if args.with_jtagbone:
        soc.add_jtagbone()

    # SpaceWire peripheral ---------------------------------------------------------------------
    add_spw(args, soc)
    # ------------------------------------------------------------------------------------------

    if args.with_spi_sdcard:
        soc.add_spi_sdcard()

    import os
    os.environ['LD_PRELOAD'] = "/usr/lib/libfreetype.so"
    builder = Builder(soc, **builder_kwargs)

    if args.build:
        builder.build()

    if args.load:
        prog = soc.platform.create_programmer(kit=args.prog_kit)
        prog.load_bitstream(builder.get_bitstream_filename(mode="sram"))

    if args.flash:
        prog = soc.platform.create_programmer(kit=args.prog_kit)
        prog.flash(0, builder.get_bitstream_filename(mode="flash", ext=".fs")) # FIXME
        # Axternal SPI programming not supported by gowin 'programmer_cli' now!
        # if needed, use openFPGALoader or Gowin programmer GUI
        if args.prog_kit == "openfpgaloader":
            prog.flash(int(args.bios_flash_offset, 0), builder.get_bios_filename(), external=True)


if __name__ == "__main__":
    description = "SpaceWire node\n\n"
    description += "Available boards:\n"

    for name in supported_boards.keys():
        description += "- " + name + "\n"

    from litex.soc.integration.soc import LiteXSoCArgumentParser
    parser = LiteXSoCArgumentParser(description=description)

    spw_group = parser.add_argument_group(title="SpaceWire options")
    spw_group.add_argument("--board",           required=True,            help="FPGA board")
    spw_group.add_argument("--time-master",     action="store_true",      help="SpaceWire node is the time master")
    spw_group.add_argument("--rx-tokens",       type=int, default=7,      help="Number of RX tokens (fifo size / 8)")
    spw_group.add_argument("--tx-tokens",       type=int, default=7,      help="Number of TX tokens (fifo size / 8)")
    spw_group.add_argument("--with-uartbone",   action="store_true",      help="Add UARTBone to the board")
    spw_group.add_argument("--with-jtagbone",   action="store_true",      help="Add JTAGBone to the board")
    spw_group.add_argument("--reset-freq",      default=10e6,             help="Reset frequency.")
    spw_group.add_argument("--user-freq",       default=10e6,             help="User frequency.")
    spw_group.add_argument("--lvds",            action="store_true",      help="Use LVDS outputs")

    target_group = parser.add_argument_group(title="Target options")
    target_group.add_argument("--build",                action="store_true",      help="Build design.")
    target_group.add_argument("--load",                 action="store_true",      help="Load bitstream.")
    target_group.add_argument("--flash",                action="store_true",      help="Flash Bitstream.")
    target_group.add_argument("--sys-clk-freq",         default=27e6,             help="System clock frequency.")

    builder_args(parser)
    soc_core_args(parser)

    args = parser.parse_known_args()[0]

    board = supported_boards[args.board]()

    soc_kwargs = {}
    soc_kwargs.update(**soc_core_argdict(args))
    soc_kwargs.update(Board.soc_kwargs)
    soc_kwargs.update(board.soc_kwargs)

    builder_kwargs = {}
    builder_kwargs.update(**builder_argdict(args))
    build_dir = os.path.join("build", args.board)
    builder_kwargs["csr_svd"] = os.path.join(build_dir, "csr.svd")
    builder_kwargs["csr_csv"] = os.path.join(build_dir, "csr.csv")
    builder_kwargs["csr_json"] = os.path.join(build_dir, "csr.json")
    builder_kwargs["output_dir"] = build_dir
    builder_kwargs["bios_options"] = ["TERM_MINI"]

    if args.board == "tangnano4k":
        None#board.load(filename=os.path.join(builder.gateware_dir, 'impl', 'pnr', 'project' + board.bitstream_ext))
    elif args.board == "tangnano9k":
        tangnano9k_main(parser, target_group, soc_kwargs, builder_kwargs)
    else:
        de0nano_main(parser, target_group, soc_kwargs, builder_kwargs)
