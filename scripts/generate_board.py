from __future__ import annotations

from pathlib import Path

import pcbnew


ROOT = Path(__file__).resolve().parents[1]
BOARD_PATH = ROOT / "ctvt-pmod.kicad_pcb"
FOOTPRINTS = Path(r"C:\Program Files\KiCad\10.0\share\kicad\footprints")
LOCAL_FOOTPRINTS = ROOT / "ctvt-pmod.pretty"

BOARD_LEFT = 20.0
BOARD_TOP = 20.0
BOARD_RIGHT = 50.0
BOARD_BOTTOM = 90.0


def vmm(x: float, y: float) -> pcbnew.VECTOR2I:
    return pcbnew.VECTOR2I(pcbnew.FromMM(x), pcbnew.FromMM(y))


def net(board: pcbnew.BOARD, name: str) -> pcbnew.NETINFO_ITEM:
    existing = board.FindNet(name)
    if existing is not None:
        return existing
    created = pcbnew.NETINFO_ITEM(board, name)
    board.Add(created)
    return created


def load_footprint(library: str, name: str) -> pcbnew.FOOTPRINT:
    library_path = LOCAL_FOOTPRINTS if library == "ctvt-pmod" else FOOTPRINTS / f"{library}.pretty"
    footprint = pcbnew.FootprintLoad(str(library_path), name)
    if footprint is None:
        raise FileNotFoundError(f"{library}:{name}")
    return footprint


def add_footprint(
    board: pcbnew.BOARD,
    reference: str,
    value: str,
    library: str,
    name: str,
    x: float,
    y: float,
    rotation: float,
    nets: dict[str, str],
) -> pcbnew.FOOTPRINT:
    footprint = load_footprint(library, name)
    footprint.SetReference(reference)
    footprint.SetValue(value)
    footprint.SetPosition(vmm(x, y))
    footprint.SetOrientationDegrees(rotation)
    for pad in footprint.Pads():
        net_name = nets.get(pad.GetNumber())
        if net_name:
            pad.SetNet(net(board, net_name))
    board.Add(footprint)
    style_fields(footprint)
    return footprint


def style_fields(footprint: pcbnew.FOOTPRINT) -> None:
    reference = footprint.Reference()
    reference.SetLayer(pcbnew.F_SilkS)
    reference.SetVisible(True)
    reference.SetTextSize(vmm(0.8, 0.8))
    reference.SetTextThickness(pcbnew.FromMM(0.2))
    value = footprint.Value()
    value.SetLayer(pcbnew.F_Fab)
    value.SetVisible(True)


def place_reference(
    footprint: pcbnew.FOOTPRINT,
    x: float,
    y: float,
    rotation: float = 0.0,
) -> None:
    reference = footprint.Reference()
    reference.SetVisible(True)
    reference.SetPosition(vmm(x, y))
    reference.SetTextAngle(pcbnew.EDA_ANGLE(rotation, pcbnew.DEGREES_T))


def set_local_model(
    footprint: pcbnew.FOOTPRINT,
    filename: str,
    offset: tuple[float, float, float] = (0.0, 0.0, 0.0),
    rotation: tuple[float, float, float] = (0.0, 0.0, 0.0),
) -> None:
    models = footprint.Models()
    if len(models) != 1:
        raise RuntimeError(f"{footprint.GetReference()} expected one 3D model")
    models[0].m_Filename = f"${{KIPRJMOD}}/models/step/{filename}"
    models[0].m_Offset = pcbnew.VECTOR3D(*offset)
    models[0].m_Rotation = pcbnew.VECTOR3D(*rotation)


def renumber_pmod(footprint: pcbnew.FOOTPRINT) -> None:
    mapping = {
        "1": "1",
        "3": "2",
        "5": "3",
        "7": "4",
        "9": "5",
        "11": "6",
        "2": "7",
        "4": "8",
        "6": "9",
        "8": "10",
        "10": "11",
        "12": "12",
    }
    pads = list(footprint.Pads())
    for pad in pads:
        pad.SetNumber(f"tmp-{pad.GetNumber()}")
    for pad in pads:
        old = pad.GetNumber().removeprefix("tmp-")
        pad.SetNumber(mapping[old])


def add_outline(board: pcbnew.BOARD) -> None:
    corners = [
        (BOARD_LEFT, BOARD_TOP),
        (BOARD_RIGHT, BOARD_TOP),
        (BOARD_RIGHT, BOARD_BOTTOM),
        (BOARD_LEFT, BOARD_BOTTOM),
        (BOARD_LEFT, BOARD_TOP),
    ]
    for start, end in zip(corners, corners[1:]):
        line = pcbnew.PCB_SHAPE(board)
        line.SetShape(pcbnew.SHAPE_T_SEGMENT)
        line.SetStart(vmm(*start))
        line.SetEnd(vmm(*end))
        line.SetLayer(pcbnew.Edge_Cuts)
        line.SetWidth(pcbnew.FromMM(0.15))
        board.Add(line)


def add_text(
    board: pcbnew.BOARD,
    text: str,
    x: float,
    y: float,
    size: float = 1.0,
    layer: int = pcbnew.F_SilkS,
    rotation: float = 0.0,
) -> None:
    item = pcbnew.PCB_TEXT(board)
    item.SetText(text)
    item.SetPosition(vmm(x, y))
    item.SetLayer(layer)
    item.SetTextSize(vmm(size, size))
    item.SetTextThickness(pcbnew.FromMM(0.2))
    item.SetTextAngle(pcbnew.EDA_ANGLE(rotation, pcbnew.DEGREES_T))
    if layer in (pcbnew.B_SilkS, pcbnew.B_Fab):
        item.SetMirrored(True)
    board.Add(item)


def add_components(board: pcbnew.BOARD) -> None:
    pmod_nets = {
        "1": "CS",
        "2": "MOSI",
        "3": "MISO",
        "4": "SCLK",
        "5": "GND",
        "6": "+3V3",
        "7": "DRDY",
        "8": "RESET",
        "9": "CLK_HOST",
        "10": "RESERVED",
        "11": "GND",
        "12": "+3V3",
    }
    j1 = add_footprint(
        board,
        "J1",
        "Tiny Tapeout PMOD",
        "Connector_PinHeader_2.54mm",
        "PinHeader_2x06_P2.54mm_Horizontal",
        27.5,
        25.0,
        90.0,
        {},
    )
    renumber_pmod(j1)
    for pad in j1.Pads():
        if pad.GetNumber() in pmod_nets:
            pad.SetNet(net(board, pmod_nets[pad.GetNumber()]))
    j4 = add_footprint(
        board,
        "J4",
        "613012243121",
        "ctvt-pmod",
        "PinSocket_2x06_P2.54mm_PMODHost1A",
        40.2,
        31.5,
        270.0,
        pmod_nets,
    )

    j2 = add_footprint(
        board,
        "J2",
        "SJ-3523-SMT-TR",
        "Connector_Audio",
        "Jack_3.5mm_CUI_SJ-3523-SMT_Horizontal",
        28.0,
        80.9,
        180.0,
        {"T": "CT_P", "R": "GND", "S": "CT_N"},
    )
    set_local_model(
        j2,
        "CUI_SJ-3523.step",
        offset=(0.0, 2.5, 0.0),
        rotation=(0.0, 0.0, -90.0),
    )
    j3 = add_footprint(
        board,
        "J3",
        "PJ-002BH-SMT-TR",
        "ctvt-pmod",
        "DC_BARREL_JACK_SMD_2MM",
        42.7,
        82.7,
        0.0,
        {"1": "VT_P", "2": "VT_N"},
    )
    for connector in (j1, j2, j3):
        for graphic in connector.GraphicalItems():
            if graphic.GetLayer() == pcbnew.F_SilkS:
                graphic.SetLayer(pcbnew.F_Fab)
    add_footprint(
        board,
        "U1",
        "ADS131M02IPWR",
        "Package_SO",
        "TSSOP-20_4.4x6.5mm_P0.65mm",
        35.0,
        47.0,
        90.0,
        {
            "1": "AVDD",
            "2": "GND",
            "3": "AIN0P",
            "4": "AIN0N",
            "5": "AIN1N",
            "6": "AIN1P",
            "11": "RESET",
            "12": "CS",
            "13": "DRDY",
            "14": "SCLK",
            "15": "MISO",
            "16": "MOSI",
            "17": "CLKIN",
            "18": "CAP",
            "19": "GND",
            "20": "+3V3",
        },
    )

    resistor_0603 = ("Resistor_SMD", "R_0603_1608Metric")
    resistor_0805 = ("Resistor_SMD", "R_0805_2012Metric")
    capacitor_0603 = ("Capacitor_SMD", "C_0603_1608Metric")

    resistor_specs = [
        ("R1", "6.49R 0.1%", *resistor_0805, 26.0, 66.5, 0.0, {"1": "CT_P", "2": "GND"}),
        ("R2", "6.49R 0.1%", *resistor_0805, 30.0, 66.5, 0.0, {"1": "CT_N", "2": "GND"}),
        ("R3", "1k 0.1%", *resistor_0603, 29.0, 54.0, 90.0, {"1": "CT_P", "2": "AIN0P"}),
        ("R4", "1k 0.1%", *resistor_0603, 33.0, 54.0, 90.0, {"1": "CT_N", "2": "AIN0N"}),
        ("R5", "100k 0.1%", *resistor_0805, 39.0, 63.0, 0.0, {"1": "VT_P", "2": "VT_DIV_P"}),
        ("R6", "100k 0.1%", *resistor_0805, 43.0, 63.0, 0.0, {"1": "VT_N", "2": "VT_DIV_N"}),
        ("R7", "6.49k 0.1%", *resistor_0805, 39.0, 66.0, 0.0, {"1": "VT_DIV_P", "2": "GND"}),
        ("R8", "6.49k 0.1%", *resistor_0805, 43.0, 66.0, 0.0, {"1": "VT_DIV_N", "2": "GND"}),
        ("R9", "1k 0.1%", *resistor_0603, 41.0, 54.0, 90.0, {"1": "VT_DIV_P", "2": "AIN1P"}),
        ("R10", "1k 0.1%", *resistor_0603, 37.0, 54.0, 90.0, {"1": "VT_DIV_N", "2": "AIN1N"}),
        ("R11", "10k", *resistor_0603, 39.0, 39.0, 90.0, {"1": "+3V3", "2": "CS"}),
        ("R12", "10k", *resistor_0603, 43.0, 39.0, 90.0, {"1": "+3V3", "2": "RESET"}),
        ("R13", "33R", *resistor_0603, 33.0, 39.0, 0.0, {"1": "CLK_HOST", "2": "CLKIN"}),
    ]
    for ref, value, library, name, x, y, rotation, nets in resistor_specs:
        add_footprint(board, ref, value, library, name, x, y, rotation, nets)

    capacitor_specs = [
        ("C1", "10nF C0G", 31.0, 58.0, 0.0, {"1": "AIN0P", "2": "AIN0N"}),
        ("C2", "10nF C0G", 39.0, 58.0, 0.0, {"1": "AIN1P", "2": "AIN1N"}),
        ("C3", "1uF", 27.0, 48.5, 90.0, {"1": "AVDD", "2": "GND"}),
        ("C4", "100nF", 27.0, 51.5, 90.0, {"1": "AVDD", "2": "GND"}),
        ("C5", "1uF", 27.0, 39.5, 90.0, {"1": "+3V3", "2": "GND"}),
        ("C6", "100nF", 27.0, 42.5, 90.0, {"1": "+3V3", "2": "GND"}),
        ("C7", "220nF", 34.5, 41.5, 90.0, {"1": "CAP", "2": "GND"}),
    ]
    for ref, value, x, y, rotation, nets in capacitor_specs:
        add_footprint(board, ref, value, *capacitor_0603, x, y, rotation, nets)

    add_footprint(
        board,
        "FB1",
        "600R@100MHz",
        "Inductor_SMD",
        "L_0603_1608Metric",
        27.0,
        45.5,
        90.0,
        {"1": "+3V3", "2": "AVDD"},
    )
    add_footprint(
        board,
        "D1",
        "SMF3.3CA",
        "Diode_SMD",
        "D_SOD-123F",
        28.0,
        69.5,
        0.0,
        {"1": "CT_P", "2": "CT_N"},
    )
    add_footprint(
        board,
        "D2",
        "SMBJ18CA",
        "Diode_SMD",
        "D_SMB",
        43.0,
        71.0,
        0.0,
        {"1": "VT_P", "2": "VT_N"},
    )

    test_points = [
        ("TP1", "AIN0P", 48.0, 40.0),
        ("TP2", "AIN0N", 48.0, 45.0),
        ("TP3", "AIN1P", 48.0, 50.0),
        ("TP4", "AIN1N", 48.0, 55.0),
        ("TP5", "DRDY", 48.0, 60.0),
        ("TP6", "+3V3", 48.0, 65.0),
        ("TP7", "GND", 48.0, 70.0),
    ]
    for ref, net_name, x, y in test_points:
        add_footprint(
            board,
            ref,
            net_name,
            "TestPoint",
            "TestPoint_Pad_D1.0mm",
            x,
            y,
            0.0,
            {"1": net_name},
        )

    reference_positions = {
        "J1": (24.13, 23.876, 90.0),
        "J2": (22.0, 70.0, 90.0),
        "J3": (47.5, 73.0, 90.0),
        "J4": (43.0, 30.5, 90.0),
        "U1": (40.0, 47.0, 90.0),
        "R1": (26.0, 64.8, 0.0),
        "R2": (30.0, 64.8, 0.0),
        "R3": (28.956, 56.134, 0.0),
        "R4": (33.02, 56.261, 0.0),
        "R5": (39.0, 61.3, 0.0),
        "R6": (43.0, 61.3, 0.0),
        "R7": (39.0, 67.7, 0.0),
        "R8": (43.0, 67.7, 0.0),
        "R9": (41.0, 56.261, 0.0),
        "R10": (37.0, 56.134, 0.0),
        "R11": (39.0, 37.3, 0.0),
        "R12": (43.0, 37.3, 0.0),
        "R13": (33.0, 37.3, 0.0),
        "C1": (31.0, 59.7, 0.0),
        "C2": (35.5, 59.7, 0.0),
        "C3": (24.257, 48.514, 0.0),
        "C4": (24.384, 51.435, 0.0),
        "C5": (24.13, 39.497, 0.0),
        "C6": (24.13, 42.5, 0.0),
        "C7": (37.5, 41.5, 0.0),
        "FB1": (24.511, 45.466, 0.0),
        "D1": (34.0, 69.5, 0.0),
        "D2": (36.5, 73.0, 0.0),
    }
    for reference, (x, y, rotation) in reference_positions.items():
        place_reference(board.FindFootprintByReference(reference), x, y, rotation)


def configure_board(board: pcbnew.BOARD) -> None:
    title = board.GetTitleBlock()
    title.SetTitle("CTVT Energy Monitor PMOD")
    title.SetDate("2026-09-20")
    title.SetRevision("1.0")
    title.SetCompany("Whatnick")
    title.SetComment(0, "ADS131M02, isolated CT and AC-AC transformer inputs")
    title.SetComment(1, "CERN-OHL-S-2.0-or-later")

    settings = board.GetDesignSettings()
    settings.m_MinClearance = pcbnew.FromMM(0.15)
    settings.m_CopperEdgeClearance = pcbnew.FromMM(0.25)


def add_markings(board: pcbnew.BOARD) -> None:
    add_text(board, "CTVT PMOD", 46.482, 30.353, 0.8, rotation=90)
    add_text(board, "CT", 28.0, 88.0, 0.8)
    add_text(board, "AC-AC ONLY", 47.0, 80.0, 0.8, pcbnew.B_SilkS, rotation=90)
    add_text(board, "Made for\nTiny Tapeout", 23.114, 31.623, 0.8, rotation=90)
    add_text(board, "REV 1.0 | CERN-OHL-S-2.0+", 35.0, 36.0, 0.8, pcbnew.B_SilkS)
    add_text(board, "NO DIRECT MAINS", 35.0, 39.0, 0.8, pcbnew.B_SilkS)


def main() -> None:
    board = pcbnew.BOARD()
    configure_board(board)
    add_outline(board)
    add_components(board)
    add_markings(board)
    pcbnew.SaveBoard(str(BOARD_PATH), board)
    print(f"Generated {BOARD_PATH}")


if __name__ == "__main__":
    main()
