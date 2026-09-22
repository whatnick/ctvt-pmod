from __future__ import annotations

from pathlib import Path

import pcbnew

from add_branding import add_branding
from adjust_stereo_jack import verify_stereo_jack_overhang
from generate_board import TRACK_WIDTH


ROOT = Path(__file__).resolve().parents[1]
BOARD_PATH = ROOT / "ctvt-pmod.kicad_pcb"
SESSION_PATH = ROOT / "routing" / "ctvt-pmod.ses"


def add_ground_zone(board: pcbnew.BOARD, layer: int) -> None:
    zone = pcbnew.ZONE(board)
    zone.SetLayer(layer)
    zone.SetNet(board.FindNet("GND"))
    zone.SetPadConnection(pcbnew.ZONE_CONNECTION_FULL)
    zone.SetLocalClearance(pcbnew.FromMM(0.25))
    zone.SetMinThickness(pcbnew.FromMM(0.20))
    outline = zone.Outline()
    outline.NewOutline()
    for x, y in ((20.3, 20.3), (49.7, 20.3), (49.7, 89.7), (20.3, 89.7)):
        outline.Append(pcbnew.FromMM(x), pcbnew.FromMM(y))
    board.Add(zone)


def main() -> None:
    board = pcbnew.LoadBoard(str(BOARD_PATH))

    if board.GetTracks() or board.Zones():
        raise RuntimeError(
            "Run generate_board.py before finalize_route.py; the input board must be unrouted."
        )

    if not pcbnew.ImportSpecctraSES(board, str(SESSION_PATH)):
        raise RuntimeError(f"Could not import {SESSION_PATH}")

    minimum_width = pcbnew.FromMM(TRACK_WIDTH)
    for item in board.GetTracks():
        if not isinstance(item, pcbnew.PCB_VIA) and item.GetWidth() < minimum_width:
            item.SetWidth(minimum_width)

    add_ground_zone(board, pcbnew.F_Cu)
    add_ground_zone(board, pcbnew.B_Cu)
    verify_stereo_jack_overhang(board)
    add_branding(board)
    pcbnew.ZONE_FILLER(board).Fill(board.Zones())
    pcbnew.SaveBoard(str(BOARD_PATH), board)
    print(f"Finalized routed board: {BOARD_PATH}")


if __name__ == "__main__":
    main()
