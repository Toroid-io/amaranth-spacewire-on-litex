from litex.build.generic_platform import *

# SpaceWire pins definitions

_spw_node_pins = {
    "de0nano": [
        ("spw_node", 0,
            Subsignal("d_input", Pins("JP1:1")),
            Subsignal("s_input", Pins("JP1:3")),
            Subsignal("d_output", Pins("JP1:5")),
            Subsignal("s_output", Pins("JP1:7")),
            IOStandard("3.3-V LVTTL")
        ),
    ],
    "tangnano4k": [
        ("spw_node", 0,
            Subsignal("d_input", Pins("40")),
            Subsignal("s_input", Pins("41")),
            Subsignal("d_output", Pins("42")),
            Subsignal("s_output", Pins("43")),
            IOStandard("LVCMOS33")
        ),
    ]
}

