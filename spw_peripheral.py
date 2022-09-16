from litex.build.generic_platform import *

# SpaceWire pins definitions

_spw_node_pins = {
    "de0nano": [
        ("spw_node_se", 0,
            Subsignal("data_input", Pins("JP1:13")),
            Subsignal("strobe_input", Pins("JP1:15")),
            Subsignal("data_output", Pins("JP1:17")),
            Subsignal("strobe_output", Pins("JP1:19")),
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
            Subsignal("data_input", Pins("40")),
            Subsignal("strobe_input", Pins("41")),
            Subsignal("data_output", Pins("42")),
            Subsignal("strobe_output", Pins("43")),
            IOStandard("LVCMOS33")
        ),
    ],
    "tangnano9k": [
        ("spw_node_lvds", 0,
            Subsignal("data_input_p", Pins("25")),
            Subsignal("data_input_n", Pins("26")),
            Subsignal("strobe_input_p", Pins("27")),
            Subsignal("strobe_input_n", Pins("28")),
            Subsignal("data_output_p", Pins("29")),
            Subsignal("data_output_n", Pins("30")),
            Subsignal("strobe_output_p", Pins("33")),
            Subsignal("strobe_output_n", Pins("34")),
            IOStandard("LVDS25")
        ),
        ("spw_node_se", 0,
            Subsignal("data_input", Pins("25")),
            Subsignal("strobe_input", Pins("26")),
            Subsignal("data_output", Pins("27")),
            Subsignal("strobe_output", Pins("28")),
            IOStandard("LVCMOS33")
        ),
    ]
}

