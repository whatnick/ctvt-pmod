from __future__ import annotations

from pathlib import Path

import pcbnew

from generate_board import add_mounting_holes, add_outline


ROOT = Path(__file__).resolve().parents[1]
BOARD_PATH = ROOT / "ctvt-pmod.kicad_pcb"
MOUNTING_REFERENCES = {"H1", "H2"}


def main() -> None:
    board = pcbnew.LoadBoard(str(BOARD_PATH))
    drawings = list(board.GetDrawings())
    footprints = list(board.GetFootprints())

    for drawing in drawings:
        if drawing.GetLayer() == pcbnew.Edge_Cuts:
            board.Remove(drawing)

    for footprint in footprints:
        if footprint.GetReference() in MOUNTING_REFERENCES:
            board.Remove(footprint)

    add_outline(board)
    add_mounting_holes(board)
    j1 = board.FindFootprintByReference("J1")
    j1.Reference().SetPosition(pcbnew.VECTOR2I_MM(25.0, 23.876))
    pcbnew.ZONE_FILLER(board).Fill(board.Zones())
    pcbnew.SaveBoard(str(BOARD_PATH), board)
    print(f"Applied rounded corners and M2 mounting holes: {BOARD_PATH}")


if __name__ == "__main__":
    main()
