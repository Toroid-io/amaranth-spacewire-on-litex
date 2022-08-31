from litex.build.generic_platform import *

# SpaceWire pins definitions

_spw_node_pins = {
    "de0nano": [
        ("spw_node_se", 0,
            Subsignal("d_input", Pins("JP1:13")),
            Subsignal("s_input", Pins("JP1:15")),
            Subsignal("d_output", Pins("JP1:17")),
            Subsignal("s_output", Pins("JP1:19")),
            IOStandard("3.3-V LVTTL")
        ),
        ("uartbone", 0,
            Subsignal("tx", Pins("JP1:28")),
            Subsignal("rx", Pins("JP1:26")),
            IOStandard("3.3-V LVTTL")
        ),
    ],
    "tangnano4k": [
        ("spw_node_se", 0,
            Subsignal("d_input", Pins("40")),
            Subsignal("s_input", Pins("41")),
            Subsignal("d_output", Pins("42")),
            Subsignal("s_output", Pins("43")),
            IOStandard("LVCMOS33")
        ),
    ],
    "tangnano9k": [
        ("spw_node_lvds", 0,
            Subsignal("d_input_p", Pins("25")),
            Subsignal("d_input_n", Pins("26")),
            Subsignal("s_input_p", Pins("27")),
            Subsignal("s_input_n", Pins("28")),
            Subsignal("d_output_p", Pins("29")),
            Subsignal("d_output_n", Pins("30")),
            Subsignal("s_output_p", Pins("33")),
            Subsignal("s_output_n", Pins("34")),
            IOStandard("LVDS25")
        ),
        ("spw_node_se", 0,
            Subsignal("d_input", Pins("79")),
            Subsignal("s_input", Pins("80")),
            Subsignal("d_output", Pins("81")),
            Subsignal("s_output", Pins("82")),
            IOStandard("LVCMOS18")
        ),
    ]
}

