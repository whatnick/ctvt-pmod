from __future__ import annotations

from pathlib import Path

import pcbnew


ROOT = Path(__file__).resolve().parents[1]
BOARD_PATH = ROOT / "ctvt-pmod.kicad_pcb"
JACK_REFERENCE = "J2"
FINAL_POSITION = pcbnew.VECTOR2I_MM(28.0, 83.5)


def verify_stereo_jack_overhang(board: pcbnew.BOARD) -> None:
    jack = board.FindFootprintByReference(JACK_REFERENCE)
    if jack is None:
        raise RuntimeError(f"Could not find {JACK_REFERENCE}")
    if jack.GetPosition() != FINAL_POSITION:
        position = jack.GetPosition()
        raise RuntimeError(
            f"{JACK_REFERENCE} is at an unexpected position: "
            f"({pcbnew.ToMM(position.x):.3f}, {pcbnew.ToMM(position.y):.3f})"
        )


def main() -> None:
    board = pcbnew.LoadBoard(str(BOARD_PATH))
    verify_stereo_jack_overhang(board)
    pcbnew.ZONE_FILLER(board).Fill(board.Zones())
    pcbnew.SaveBoard(str(BOARD_PATH), board)
    print(f"Verified J2 mating-face overhang is 2.0 mm: {BOARD_PATH}")


if __name__ == "__main__":
    main()
