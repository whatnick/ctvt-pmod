from __future__ import annotations

from pathlib import Path

import pcbnew


ROOT = Path(__file__).resolve().parents[1]
BOARD_PATH = ROOT / "ctvt-pmod.kicad_pcb"
JACK_REFERENCE = "J2"
ROUTED_POSITION = pcbnew.VECTOR2I_MM(28.0, 80.9)
FINAL_POSITION = pcbnew.VECTOR2I_MM(28.0, 83.5)


def move_stereo_jack(board: pcbnew.BOARD) -> None:
    jack = board.FindFootprintByReference(JACK_REFERENCE)
    if jack is None:
        raise RuntimeError(f"Could not find {JACK_REFERENCE}")
    if jack.GetPosition() == FINAL_POSITION:
        return
    if jack.GetPosition() != ROUTED_POSITION:
        position = jack.GetPosition()
        raise RuntimeError(
            f"{JACK_REFERENCE} is at an unexpected position: "
            f"({pcbnew.ToMM(position.x):.3f}, {pcbnew.ToMM(position.y):.3f})"
        )

    reference_position = jack.Reference().GetPosition()
    old_pad_positions = {
        pad.GetNumber(): pad.GetPosition()
        for pad in jack.Pads()
        if pad.GetNumber()
    }
    jack.SetPosition(FINAL_POSITION)
    jack.Reference().SetPosition(reference_position)

    for pad in jack.Pads():
        pad_number = pad.GetNumber()
        if not pad_number:
            continue
        old_position = old_pad_positions[pad_number]
        new_position = pad.GetPosition()
        adjusted_endpoints = 0
        for track in board.GetTracks():
            if isinstance(track, pcbnew.PCB_VIA) or track.GetNetCode() != pad.GetNetCode():
                continue
            if track.GetStart() == old_position:
                track.SetStart(new_position)
                adjusted_endpoints += 1
            if track.GetEnd() == old_position:
                track.SetEnd(new_position)
                adjusted_endpoints += 1
        if adjusted_endpoints != 1:
            raise RuntimeError(
                f"Expected one routed endpoint at {JACK_REFERENCE} pad {pad_number}, "
                f"found {adjusted_endpoints}"
            )


def main() -> None:
    board = pcbnew.LoadBoard(str(BOARD_PATH))
    move_stereo_jack(board)
    pcbnew.ZONE_FILLER(board).Fill(board.Zones())
    pcbnew.SaveBoard(str(BOARD_PATH), board)
    print(f"Moved J2 so its mating face overhangs the PCB by 2.0 mm: {BOARD_PATH}")


if __name__ == "__main__":
    main()
