from __future__ import annotations

import shutil
import subprocess
import tempfile
from dataclasses import dataclass, field
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "ctvt-pmod.kicad_sch"
SYMBOL_LIBRARY_OUTPUT = ROOT / "ctvt-pmod-cache.kicad_sym"
SYMBOL_TABLE_OUTPUT = ROOT / "sym-lib-table"
KICAD_CLI = Path(r"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe")
KICAD_REVIVE = (
    "git+https://github.com/mgyenik/kicad-revive.git"
    "@2847877af4a3114fd1e61ab2f660089fa3c27ecc"
)


CUSTOM_LIBRARY = r"""EESchema-LIBRARY Version 2.4
#encoding utf-8
#
# ADS131M02PW
#
DEF ADS131M02PW U 0 40 Y Y 1 F N
F0 "U" 0 1150 50 H V C CNN
F1 "ADS131M02PW" 0 1050 50 H V C CNN
F2 "" 0 0 50 H I C CNN
F3 "" 0 0 50 H I C CNN
DRAW
S -500 1000 500 -1300 0 1 12 f
X AVDD 1 -700 900 200 R 40 40 1 1 W
X ~RESET 11 700 -300 200 L 40 40 1 1 I
X ~CS 12 700 -100 200 L 40 40 1 1 I
X ~DRDY 13 700 100 200 L 40 40 1 1 O
X SCLK 14 700 300 200 L 40 40 1 1 I
X DOUT 15 700 500 200 L 40 40 1 1 O
X DIN 16 700 700 200 L 40 40 1 1 I
X CLKIN 17 700 900 200 L 40 40 1 1 I
X CAP 18 -700 0 200 R 40 40 1 1 w
X DGND 19 -700 -1000 200 R 40 40 1 1 W
X AGND 2 -700 700 200 R 40 40 1 1 W
X DVDD 20 -700 -1200 200 R 40 40 1 1 W
X AIN0P 3 -700 400 200 R 40 40 1 1 I
X AIN0N 4 -700 200 200 R 40 40 1 1 I
X AIN1N 5 -700 -400 200 R 40 40 1 1 I
X AIN1P 6 -700 -200 200 R 40 40 1 1 I
X NC 7 -700 -600 200 R 40 40 1 1 N
X NC 8 -700 -800 200 R 40 40 1 1 N
X NC 9 700 -800 200 L 40 40 1 1 N
X NC 10 700 -600 200 L 40 40 1 1 N
ENDDRAW
ENDDEF
#
# R
#
DEF R R 0 0 Y Y 1 F N
F0 "R" 0 80 50 H V C CNN
F1 "R" 0 0 50 H V C CNN
F2 "" 0 0 50 H I C CNN
F3 "" 0 0 50 H I C CNN
DRAW
S -100 50 100 -50 0 1 10 N
X 1 1 -300 0 200 R 40 40 1 1 P
X 2 2 300 0 200 L 40 40 1 1 P
ENDDRAW
ENDDEF
#
# C
#
DEF C C 0 0 Y Y 1 F N
F0 "C" 0 90 50 H V C CNN
F1 "C" 0 -90 50 H V C CNN
F2 "" 0 0 50 H I C CNN
F3 "" 0 0 50 H I C CNN
DRAW
P 2 0 1 12 -30 80 -30 -80 N
P 2 0 1 12 30 80 30 -80 N
X 1 1 -300 0 270 R 40 40 1 1 P
X 2 2 300 0 270 L 40 40 1 1 P
ENDDRAW
ENDDEF
#
# FB
#
DEF FB FB 0 0 Y Y 1 F N
F0 "FB" 0 90 50 H V C CNN
F1 "Ferrite" 0 -90 50 H V C CNN
F2 "" 0 0 50 H I C CNN
F3 "" 0 0 50 H I C CNN
DRAW
S -100 50 100 -50 0 1 10 N
P 2 0 1 10 -70 80 -20 30 N
P 2 0 1 10 20 -30 70 -80 N
X 1 1 -300 0 200 R 40 40 1 1 P
X 2 2 300 0 200 L 40 40 1 1 w
ENDDRAW
ENDDEF
#
# TVS
#
DEF TVS D 0 0 Y Y 1 F N
F0 "D" 0 100 50 H V C CNN
F1 "TVS" 0 -100 50 H V C CNN
F2 "" 0 0 50 H I C CNN
F3 "" 0 0 50 H I C CNN
DRAW
P 3 0 1 12 -60 -80 -60 80 70 0 N
P 4 0 1 12 70 -80 70 80 40 50 100 20 N
X 1 1 -300 0 240 R 40 40 1 1 P
X 2 2 300 0 230 L 40 40 1 1 P
ENDDRAW
ENDDEF
#
# AUDIO_JACK
#
DEF AUDIO_JACK J 0 40 Y Y 1 F N
F0 "J" 0 450 50 H V C CNN
F1 "CT stereo jack" 0 350 50 H V C CNN
F2 "" 0 0 50 H I C CNN
F3 "" 0 0 50 H I C CNN
DRAW
S -400 300 400 -300 0 1 12 f
X T T 600 200 200 L 40 40 1 1 P
X R R 600 0 200 L 40 40 1 1 P
X S S 600 -200 200 L 40 40 1 1 P
X TN TN -600 150 200 R 40 40 1 1 P
X RN RN -600 -150 200 R 40 40 1 1 P
ENDDRAW
ENDDEF
#
# BARREL_JACK
#
DEF BARREL_JACK J 0 40 Y Y 1 F N
F0 "J" 0 350 50 H V C CNN
F1 "AC-AC barrel jack" 0 250 50 H V C CNN
F2 "" 0 0 50 H I C CNN
F3 "" 0 0 50 H I C CNN
DRAW
S -400 200 400 -200 0 1 12 f
X CENTER 1 600 150 200 L 40 40 1 1 P
X SLEEVE 2 600 -50 200 L 40 40 1 1 P
X SWITCH 3 600 -150 200 L 40 40 1 1 P
ENDDRAW
ENDDEF
#
# PMOD
#
DEF PMOD J 0 40 Y Y 1 F N
F0 "J" 0 750 50 H V C CNN
F1 "Tiny Tapeout PMOD" 0 650 50 H V C CNN
F2 "" 0 0 50 H I C CNN
F3 "" 0 0 50 H I C CNN
DRAW
S -500 600 500 -600 0 1 12 f
X CS 1 -700 500 200 R 40 40 1 1 B
X MOSI 2 -700 300 200 R 40 40 1 1 B
X MISO 3 -700 100 200 R 40 40 1 1 B
X SCLK 4 -700 -100 200 R 40 40 1 1 B
X GND 5 -700 -300 200 R 40 40 1 1 w
X +3V3 6 -700 -500 200 R 40 40 1 1 w
X DRDY 7 700 500 200 L 40 40 1 1 B
X RESET 8 700 300 200 L 40 40 1 1 B
X CLKIN 9 700 100 200 L 40 40 1 1 B
X RESERVED 10 700 -100 200 L 40 40 1 1 B
X GND 11 700 -300 200 L 40 40 1 1 P
X +3V3 12 700 -500 200 L 40 40 1 1 P
ENDDRAW
ENDDEF
#
# PMOD_PASSIVE
#
DEF PMOD_PASSIVE J 0 40 Y Y 1 F N
F0 "J" 0 750 50 H V C CNN
F1 "PMOD pass-through" 0 650 50 H V C CNN
F2 "" 0 0 50 H I C CNN
F3 "" 0 0 50 H I C CNN
DRAW
S -500 600 500 -600 0 1 12 f
X CS 1 -700 500 200 R 40 40 1 1 P
X MOSI 2 -700 300 200 R 40 40 1 1 P
X MISO 3 -700 100 200 R 40 40 1 1 P
X SCLK 4 -700 -100 200 R 40 40 1 1 P
X GND 5 -700 -300 200 R 40 40 1 1 P
X +3V3 6 -700 -500 200 R 40 40 1 1 P
X DRDY 7 700 500 200 L 40 40 1 1 P
X RESET 8 700 300 200 L 40 40 1 1 P
X CLKIN 9 700 100 200 L 40 40 1 1 P
X RESERVED 10 700 -100 200 L 40 40 1 1 P
X GND 11 700 -300 200 L 40 40 1 1 P
X +3V3 12 700 -500 200 L 40 40 1 1 P
ENDDRAW
ENDDEF
#
# TP
#
DEF TP TP 0 0 Y Y 1 F N
F0 "TP" 0 180 50 H V C CNN
F1 "Test point" 0 80 50 H V C CNN
F2 "" 0 0 50 H I C CNN
F3 "" 0 0 50 H I C CNN
DRAW
C 0 0 70 0 1 12 N
X 1 1 -250 0 180 R 40 40 1 1 P
ENDDRAW
ENDDEF
#
#End Library
"""


@dataclass
class Component:
    symbol: str
    ref: str
    value: str
    footprint: str
    x: int
    y: int
    fields: dict[str, str] = field(default_factory=dict)


def component_block(component: Component, timestamp: int) -> str:
    fields = [
        f'F 0 "{component.ref}" H {component.x} {component.y - 100} 50  0000 C CNN',
        f'F 1 "{component.value}" H {component.x} {component.y + 100} 50  0000 C CNN',
        f'F 2 "{component.footprint}" H {component.x} {component.y} 50  0001 C CNN',
        f'F 3 "" H {component.x} {component.y} 50  0001 C CNN',
    ]
    for index, (name, value) in enumerate(component.fields.items(), start=4):
        fields.append(
            f'F {index} "{value}" H {component.x} {component.y} 50  0001 C CNN "{name}"'
        )
    return "\n".join(
        [
            "$Comp",
            f"L ctvt-pmod-cache:{component.symbol} {component.ref}",
            f"U 1 1 {timestamp:08X}",
            f"P {component.x} {component.y}",
            *fields,
            f"\t1    {component.x} {component.y}",
            "\t1    0    0    -1",
            "$EndComp",
        ]
    )


def wire_label(x: int, y: int, net: str, direction: int = 1) -> str:
    end_x = x + direction * 200
    justify = 0 if direction > 0 else 2
    return "\n".join(
        [
            f"Wire Wire Line",
            f"\t{x} {y} {end_x} {y}",
            f"Text Label {end_x} {y} {justify}    40   ~ 0",
            net,
        ]
    )


def no_connect(x: int, y: int) -> str:
    return f"NoConn ~ {x} {y}"


def note(x: int, y: int, text: str) -> str:
    return f'Text Notes {x} {y} 0    60   ~ 12\n{text}'


def build_legacy_schematic() -> str:
    components = [
        Component(
            "AUDIO_JACK",
            "J2",
            "SJ-3523-SMT-TR",
            "Connector_Audio:Jack_3.5mm_CUI_SJ-3523-SMT_Horizontal",
            1500,
            1800,
            {
                "Manufacturer": "Same Sky",
                "MPN": "SJ-3523-SMT-TR",
                "DigiKey PN": "CP-3523SJCT-ND",
                "Description": "3.5 mm stereo CT input jack",
            },
        ),
        Component(
            "TVS",
            "D1",
            "SMF3.3CA",
            "Diode_SMD:D_SOD-123F",
            2700,
            1500,
            {
                "Manufacturer": "Good-Ark Semiconductor",
                "MPN": "GSMF3.3CA",
                "DigiKey PN": "4786-GSMF3.3CACT-ND",
            },
        ),
        Component(
            "R",
            "R1",
            "6.49R 0.1%",
            "Resistor_SMD:R_0805_2012Metric",
            3000,
            1850,
            {
                "Manufacturer": "Vishay",
                "MPN": "TNPW08056R49BEEA",
                "Description": "CT split burden resistor, 25 ppm/K; source outside DigiKey",
            },
        ),
        Component(
            "R",
            "R2",
            "6.49R 0.1%",
            "Resistor_SMD:R_0805_2012Metric",
            3000,
            2150,
            {
                "Manufacturer": "Vishay",
                "MPN": "TNPW08056R49BEEA",
                "Description": "CT split burden resistor, 25 ppm/K; source outside DigiKey",
            },
        ),
        Component(
            "R",
            "R3",
            "1k 0.1%",
            "Resistor_SMD:R_0603_1608Metric",
            4200,
            1750,
            {
                "Manufacturer": "Susumu",
                "MPN": "RG1608P-102-B-T5",
                "DigiKey PN": "RG16P1.0KBCT-ND",
            },
        ),
        Component(
            "R",
            "R4",
            "1k 0.1%",
            "Resistor_SMD:R_0603_1608Metric",
            4200,
            2250,
            {
                "Manufacturer": "Susumu",
                "MPN": "RG1608P-102-B-T5",
                "DigiKey PN": "RG16P1.0KBCT-ND",
            },
        ),
        Component(
            "C",
            "C1",
            "10nF C0G",
            "Capacitor_SMD:C_0603_1608Metric",
            5200,
            2000,
            {
                "Manufacturer": "Murata",
                "MPN": "GRM1885C1H103JA01D",
                "DigiKey PN": "490-9666-1-ND",
                "Description": "Differential anti-alias capacitor",
            },
        ),
        Component(
            "BARREL_JACK",
            "J3",
            "PJ-002BH-SMT-TR",
            "ctvt-pmod:DC_BARREL_JACK_SMD_2MM",
            1500,
            4100,
            {
                "Manufacturer": "Same Sky",
                "MPN": "PJ-002BH-SMT-TR",
                "DigiKey PN": "CP-002BHPJCT-ND",
                "Description": "2.0 mm SMT barrel jack for isolated AC-AC transformer",
            },
        ),
        Component(
            "TVS",
            "D2",
            "SMBJ18CA",
            "Diode_SMD:D_SMB",
            2650,
            3800,
            {
                "Manufacturer": "Littelfuse",
                "MPN": "SMBJ18CA",
                "DigiKey PN": "SMBJ18CALFCT-ND",
            },
        ),
        Component(
            "R",
            "R5",
            "100k 0.1%",
            "Resistor_SMD:R_0805_2012Metric",
            3300,
            4050,
            {
                "Manufacturer": "Panasonic Industry",
                "MPN": "ERA-6AEB104V",
                "DigiKey PN": "P100KDACT-ND",
                "Description": "VT balanced high-side divider resistor",
            },
        ),
        Component(
            "R",
            "R6",
            "100k 0.1%",
            "Resistor_SMD:R_0805_2012Metric",
            3300,
            4550,
            {
                "Manufacturer": "Panasonic Industry",
                "MPN": "ERA-6AEB104V",
                "DigiKey PN": "P100KDACT-ND",
                "Description": "VT balanced high-side divider resistor",
            },
        ),
        Component(
            "R",
            "R7",
            "6.49k 0.1%",
            "Resistor_SMD:R_0805_2012Metric",
            4200,
            4200,
            {
                "Manufacturer": "Yageo",
                "MPN": "RT0805BRD076K49L",
                "DigiKey PN": "YAG1965CT-ND",
                "Description": "VT balanced low-side divider resistor",
            },
        ),
        Component(
            "R",
            "R8",
            "6.49k 0.1%",
            "Resistor_SMD:R_0805_2012Metric",
            4200,
            4500,
            {
                "Manufacturer": "Yageo",
                "MPN": "RT0805BRD076K49L",
                "DigiKey PN": "YAG1965CT-ND",
                "Description": "VT balanced low-side divider resistor",
            },
        ),
        Component(
            "R",
            "R9",
            "1k 0.1%",
            "Resistor_SMD:R_0603_1608Metric",
            5200,
            4050,
            {
                "Manufacturer": "Susumu",
                "MPN": "RG1608P-102-B-T5",
                "DigiKey PN": "RG16P1.0KBCT-ND",
            },
        ),
        Component(
            "R",
            "R10",
            "1k 0.1%",
            "Resistor_SMD:R_0603_1608Metric",
            5200,
            4550,
            {
                "Manufacturer": "Susumu",
                "MPN": "RG1608P-102-B-T5",
                "DigiKey PN": "RG16P1.0KBCT-ND",
            },
        ),
        Component(
            "C",
            "C2",
            "10nF C0G",
            "Capacitor_SMD:C_0603_1608Metric",
            6000,
            4300,
            {
                "Manufacturer": "Murata",
                "MPN": "GRM1885C1H103JA01D",
                "DigiKey PN": "490-9666-1-ND",
                "Description": "Differential anti-alias capacitor",
            },
        ),
        Component(
            "ADS131M02PW",
            "U1",
            "ADS131M02IPWR",
            "Package_SO:TSSOP-20_4.4x6.5mm_P0.65mm",
            7000,
            3000,
            {
                "Manufacturer": "Texas Instruments",
                "MPN": "ADS131M02IPWR",
                "DigiKey PN": "296-ADS131M02IPWRCT-ND",
                "Description": "Dual simultaneous-sampling 24-bit delta-sigma ADC",
            },
        ),
        Component(
            "FB",
            "FB1",
            "600R@100MHz",
            "Inductor_SMD:L_0603_1608Metric",
            5800,
            900,
            {
                "Manufacturer": "TDK",
                "MPN": "MPZ1608S601ATA00",
                "DigiKey PN": "445-MPZ1608S601ATA00CT-ND",
                "Description": "AVDD ferrite bead",
            },
        ),
        Component(
            "C",
            "C3",
            "1uF",
            "Capacitor_SMD:C_0603_1608Metric",
            6500,
            900,
            {
                "Manufacturer": "KEMET",
                "MPN": "C0603C105K4RACTU",
                "DigiKey PN": "399-C0603C105K4RACTUCT-ND",
            },
        ),
        Component(
            "C",
            "C4",
            "100nF",
            "Capacitor_SMD:C_0603_1608Metric",
            6500,
            1200,
            {
                "Manufacturer": "KEMET",
                "MPN": "C0603C104K5RACTU",
                "DigiKey PN": "399-C0603C104K5RACTUCT-ND",
            },
        ),
        Component(
            "C",
            "C5",
            "1uF",
            "Capacitor_SMD:C_0603_1608Metric",
            8500,
            900,
            {
                "Manufacturer": "KEMET",
                "MPN": "C0603C105K4RACTU",
                "DigiKey PN": "399-C0603C105K4RACTUCT-ND",
            },
        ),
        Component(
            "C",
            "C6",
            "100nF",
            "Capacitor_SMD:C_0603_1608Metric",
            8500,
            1200,
            {
                "Manufacturer": "KEMET",
                "MPN": "C0603C104K5RACTU",
                "DigiKey PN": "399-C0603C104K5RACTUCT-ND",
            },
        ),
        Component(
            "C",
            "C7",
            "220nF",
            "Capacitor_SMD:C_0603_1608Metric",
            7800,
            1700,
            {
                "Manufacturer": "KEMET",
                "MPN": "C0603C224K4RACTU",
                "DigiKey PN": "399-C0603C224K4RACTUCT-ND",
            },
        ),
        Component(
            "R",
            "R11",
            "10k",
            "Resistor_SMD:R_0603_1608Metric",
            8600,
            4400,
            {
                "Manufacturer": "Stackpole Electronics",
                "MPN": "RMCF0603FT10K0",
                "DigiKey PN": "RMCF0603FT10K0CT-ND",
            },
        ),
        Component(
            "R",
            "R12",
            "10k",
            "Resistor_SMD:R_0603_1608Metric",
            8600,
            4700,
            {
                "Manufacturer": "Stackpole Electronics",
                "MPN": "RMCF0603FT10K0",
                "DigiKey PN": "RMCF0603FT10K0CT-ND",
            },
        ),
        Component(
            "R",
            "R13",
            "33R",
            "Resistor_SMD:R_0603_1608Metric",
            8600,
            5000,
            {
                "Manufacturer": "Yageo",
                "MPN": "RC0603FR-0733RL",
                "DigiKey PN": "13-RC0603FR-0733RLCT-ND",
            },
        ),
        Component(
            "PMOD",
            "J1",
            "Tiny Tapeout PMOD",
            "Connector_PinHeader_2.54mm:PinHeader_2x06_P2.54mm_Horizontal",
            9800,
            3100,
            {
                "Manufacturer": "Samtec",
                "MPN": "TSW-106-08-G-D-RA",
                "DigiKey PN": "612-TSW-106-08-G-D-RA-ND",
                "Description": "Standards-correct 12-pin mixed-direction PMOD",
            },
        ),
        Component(
            "PMOD_PASSIVE",
            "J4",
            "613012243121",
            "ctvt-pmod:PinSocket_2x06_P2.54mm_PMODHost1A",
            9800,
            6200,
            {
                "Manufacturer": "Wurth Elektronik",
                "MPN": "613012243121",
                "DigiKey PN": "732-613012243121-ND",
                "Description": "Vertical female PMOD pass-through connector",
            },
        ),
        Component("TP", "TP1", "AIN0P", "TestPoint:TestPoint_Pad_D1.0mm", 6000, 5350),
        Component("TP", "TP2", "AIN0N", "TestPoint:TestPoint_Pad_D1.0mm", 7000, 5350),
        Component("TP", "TP3", "AIN1P", "TestPoint:TestPoint_Pad_D1.0mm", 8000, 5350),
        Component("TP", "TP4", "AIN1N", "TestPoint:TestPoint_Pad_D1.0mm", 9000, 5350),
        Component("TP", "TP5", "DRDY", "TestPoint:TestPoint_Pad_D1.0mm", 6000, 5800),
        Component("TP", "TP6", "+3V3", "TestPoint:TestPoint_Pad_D1.0mm", 7000, 5800),
        Component("TP", "TP7", "GND", "TestPoint:TestPoint_Pad_D1.0mm", 8000, 5800),
    ]

    blocks = [
        "EESchema Schematic File Version 4",
        "LIBS:ctvt-pmod-cache",
        "EELAYER 29 0",
        "EELAYER END",
        "$Descr A4 11693 8268",
        "encoding utf-8",
        "Sheet 1 1",
        'Title "CTVT Energy Monitor PMOD"',
        'Date "2026-09-20"',
        'Rev "1.0"',
        'Comp "Whatnick"',
        'Comment1 "ADS131M02 isolated CT and AC-AC transformer frontend"',
        'Comment2 "Never connect mains directly"',
        'Comment3 "CERN-OHL-S-2.0-or-later"',
        'Comment4 "Tiny Tapeout 3.3 V mixed-direction PMOD"',
        "$EndDescr",
    ]
    for index, comp in enumerate(components, start=1):
        blocks.append(component_block(comp, 0x66000000 + index))

    # Connector labels and no-connects.
    blocks += [
        wire_label(2100, 1600, "CT_P"),
        wire_label(2100, 1800, "GND"),
        wire_label(2100, 2000, "CT_N"),
        no_connect(900, 1650),
        no_connect(900, 1950),
        wire_label(2100, 3950, "VT_P"),
        wire_label(2100, 4150, "VT_N"),
        no_connect(2100, 4250),
        # Input protection.
        wire_label(2400, 1500, "CT_P", -1),
        wire_label(3000, 1500, "CT_N"),
        wire_label(2350, 3800, "VT_P", -1),
        wire_label(2950, 3800, "VT_N"),
        # CT split burden and filter.
        wire_label(2700, 1850, "CT_P", -1),
        wire_label(3300, 1850, "GND"),
        wire_label(2700, 2150, "CT_N", -1),
        wire_label(3300, 2150, "GND"),
        wire_label(3900, 1750, "CT_P", -1),
        wire_label(4500, 1750, "AIN0P"),
        wire_label(3900, 2250, "CT_N", -1),
        wire_label(4500, 2250, "AIN0N"),
        wire_label(4900, 2000, "AIN0P", -1),
        wire_label(5500, 2000, "AIN0N"),
        # VT balanced divider and filter.
        wire_label(3000, 4050, "VT_P", -1),
        wire_label(3600, 4050, "VT_DIV_P"),
        wire_label(3000, 4550, "VT_N", -1),
        wire_label(3600, 4550, "VT_DIV_N"),
        wire_label(3900, 4200, "VT_DIV_P", -1),
        wire_label(4500, 4200, "GND"),
        wire_label(3900, 4500, "VT_DIV_N", -1),
        wire_label(4500, 4500, "GND"),
        wire_label(4900, 4050, "VT_DIV_P", -1),
        wire_label(5500, 4050, "AIN1P"),
        wire_label(4900, 4550, "VT_DIV_N", -1),
        wire_label(5500, 4550, "AIN1N"),
        wire_label(5700, 4300, "AIN1P", -1),
        wire_label(6300, 4300, "AIN1N"),
        # ADC pins.
        wire_label(6300, 2100, "AVDD", -1),
        wire_label(6300, 2300, "GND", -1),
        wire_label(6300, 2600, "AIN0P", -1),
        wire_label(6300, 2800, "AIN0N", -1),
        wire_label(6300, 3200, "AIN1P", -1),
        wire_label(6300, 3400, "AIN1N", -1),
        no_connect(6300, 3600),
        no_connect(6300, 3800),
        wire_label(6300, 3000, "CAP", -1),
        wire_label(6300, 4000, "GND", -1),
        wire_label(6300, 4200, "+3V3", -1),
        wire_label(7700, 2100, "CLKIN"),
        wire_label(7700, 2300, "MOSI"),
        wire_label(7700, 2500, "MISO"),
        wire_label(7700, 2700, "SCLK"),
        wire_label(7700, 2900, "DRDY"),
        wire_label(7700, 3100, "CS"),
        wire_label(7700, 3300, "RESET"),
        no_connect(7700, 3600),
        no_connect(7700, 3800),
        # Supply filtering and decoupling.
        wire_label(5500, 900, "+3V3", -1),
        wire_label(6100, 900, "AVDD"),
        wire_label(6200, 900, "AVDD", -1),
        wire_label(6800, 900, "GND"),
        wire_label(6200, 1200, "AVDD", -1),
        wire_label(6800, 1200, "GND"),
        wire_label(8200, 900, "+3V3", -1),
        wire_label(8800, 900, "GND"),
        wire_label(8200, 1200, "+3V3", -1),
        wire_label(8800, 1200, "GND"),
        wire_label(7500, 1700, "CAP", -1),
        wire_label(8100, 1700, "GND"),
        # Pull-ups and clock damping.
        wire_label(8300, 4400, "+3V3", -1),
        wire_label(8900, 4400, "CS"),
        wire_label(8300, 4700, "+3V3", -1),
        wire_label(8900, 4700, "RESET"),
        wire_label(8300, 5000, "CLK_HOST", -1),
        wire_label(8900, 5000, "CLKIN"),
        # PMOD physical pin numbering: 1-4 and 7-10 signals, 5/11 GND, 6/12 3V3.
        wire_label(9100, 2600, "CS", -1),
        wire_label(9100, 2800, "MOSI", -1),
        wire_label(9100, 3000, "MISO", -1),
        wire_label(9100, 3200, "SCLK", -1),
        wire_label(9100, 3400, "GND", -1),
        wire_label(9100, 3600, "+3V3", -1),
        wire_label(10500, 2600, "DRDY"),
        wire_label(10500, 2800, "RESET"),
        wire_label(10500, 3000, "CLK_HOST"),
        wire_label(10500, 3200, "RESERVED"),
        wire_label(10500, 3400, "GND"),
        wire_label(10500, 3600, "+3V3"),
        # Female PMOD pass-through.
        wire_label(9100, 5700, "CS", -1),
        wire_label(9100, 5900, "MOSI", -1),
        wire_label(9100, 6100, "MISO", -1),
        wire_label(9100, 6300, "SCLK", -1),
        wire_label(9100, 6500, "GND", -1),
        wire_label(9100, 6700, "+3V3", -1),
        wire_label(10500, 5700, "DRDY"),
        wire_label(10500, 5900, "RESET"),
        wire_label(10500, 6100, "CLK_HOST"),
        wire_label(10500, 6300, "RESERVED"),
        wire_label(10500, 6500, "GND"),
        wire_label(10500, 6700, "+3V3"),
        # Test points.
        wire_label(5750, 5350, "AIN0P", -1),
        wire_label(6750, 5350, "AIN0N", -1),
        wire_label(7750, 5350, "AIN1P", -1),
        wire_label(8750, 5350, "AIN1N", -1),
        wire_label(5750, 5800, "DRDY", -1),
        wire_label(6750, 5800, "+3V3", -1),
        wire_label(7750, 5800, "GND", -1),
        note(900, 1050, "CT INPUT - 100 A : 50 mA CT, 12.98 ohm split burden"),
        note(900, 3350, "VT INPUT - isolated 9-12 VAC transformer only"),
        note(5600, 700, "POWER / DECOUPLING"),
        note(8800, 1900, "TINY TAPEOUT PMOD"),
        note(900, 7200, "SAFETY: ISOLATED CT AND CERTIFIED ISOLATED AC-AC TRANSFORMER ONLY. NEVER CONNECT MAINS DIRECTLY."),
        "$EndSCHEMATC",
    ]
    return "\n".join(blocks) + "\n"


def main() -> None:
    if not KICAD_CLI.exists():
        raise FileNotFoundError(KICAD_CLI)

    with tempfile.TemporaryDirectory(prefix="ctvt-schematic-") as temp:
        temp_dir = Path(temp)
        legacy = temp_dir / "ctvt-pmod.sch"
        cache = temp_dir / "ctvt-pmod-cache.lib"
        modern_cache = temp_dir / "ctvt-pmod-cache.kicad_sym"
        legacy.write_text(build_legacy_schematic(), encoding="utf-8")
        cache.write_text(CUSTOM_LIBRARY, encoding="utf-8")
        subprocess.run(
            [
                str(KICAD_CLI),
                "sym",
                "upgrade",
                str(cache),
                "--output",
                str(modern_cache),
            ],
            check=True,
        )
        output_dir = temp_dir / "modern"
        subprocess.run(
            [
                "uvx",
                "--from",
                KICAD_REVIVE,
                "kicad-revive",
                "convert",
                str(legacy),
                "--cache",
                str(modern_cache),
                "--out-dir",
                str(output_dir),
                "--project-name",
                "ctvt-pmod",
                "--kicad-cli",
                str(KICAD_CLI),
                "--overwrite",
            ],
            check=True,
        )
        generated = output_dir / "ctvt-pmod.kicad_sch"
        if not generated.exists():
            raise RuntimeError("KiCad did not produce ctvt-pmod.kicad_sch")
        shutil.copy2(generated, OUTPUT)
        shutil.copy2(modern_cache, SYMBOL_LIBRARY_OUTPUT)
    SYMBOL_TABLE_OUTPUT.write_text(
        '(sym_lib_table\n'
        '  (version 7)\n'
        '  (lib (name "ctvt-pmod-cache")(type "KiCad")'
        '(uri "${KIPRJMOD}/ctvt-pmod-cache.kicad_sym")(options "")(descr ""))\n'
        ')\n',
        encoding="utf-8",
    )
    print(f"Generated {OUTPUT}")


if __name__ == "__main__":
    main()
