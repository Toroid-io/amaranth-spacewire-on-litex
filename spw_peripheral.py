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
        ("uartbone", 0,
            Subsignal("tx", Pins("JP1:9")),
            Subsignal("rx", Pins("JP1:13")),
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
    ],
    "tangnano9k": [
        ("spw_node", 0,
            Subsignal("d_input", Pins("30")),
            Subsignal("s_input", Pins("33")),
            Subsignal("d_output", Pins("34")),
            Subsignal("s_output", Pins("40")),
            IOStandard("LVCMOS33")
        ),
    ]
}

