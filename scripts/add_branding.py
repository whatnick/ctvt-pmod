from __future__ import annotations

from pathlib import Path

import pcbnew


ROOT = Path(__file__).resolve().parents[1]
BOARD_PATH = ROOT / "ctvt-pmod.kicad_pcb"
LOCAL_FOOTPRINTS = ROOT / "ctvt-pmod.pretty"
BRANDING_TEXT = "by Tisham Dhar\nhttps://whatnick.com\nRev 1.0 20/09/2026"
BRANDING_REFERENCES = {"LOGO1", "LOGO2"}


def vmm(x: float, y: float) -> pcbnew.VECTOR2I:
    return pcbnew.VECTOR2I(pcbnew.FromMM(x), pcbnew.FromMM(y))


def add_logo(
    board: pcbnew.BOARD,
    reference: str,
    footprint_name: str,
    x: float,
    y: float,
    rotation: float = 0.0,
    back: bool = False,
) -> None:
    footprint = pcbnew.FootprintLoad(str(LOCAL_FOOTPRINTS), footprint_name)
    if footprint is None:
        raise FileNotFoundError(f"ctvt-pmod:{footprint_name}")
    footprint.SetReference(reference)
    footprint.SetValue(footprint_name)
    footprint.Reference().SetVisible(False)
    footprint.Value().SetVisible(False)
    footprint.SetPosition(vmm(x, y))
    footprint.SetOrientationDegrees(rotation)
    board.Add(footprint)
    if back:
        footprint.Flip(footprint.GetPosition(), False)


def add_branding(board: pcbnew.BOARD) -> None:
    footprints = list(board.GetFootprints())
    drawings = list(board.GetDrawings())

    for footprint in footprints:
        if footprint.GetReference() in BRANDING_REFERENCES:
            board.Remove(footprint)

    for drawing in drawings:
        if isinstance(drawing, pcbnew.PCB_TEXT) and drawing.GetText() == BRANDING_TEXT:
            board.Remove(drawing)

    add_logo(board, "LOGO1", "OSHW-LOGO-M", 25.0, 81.0, back=True)
    add_logo(board, "LOGO2", "Whatnick_logo", 24.13, 58.674, rotation=90.0)

    text = pcbnew.PCB_TEXT(board)
    text.SetText(BRANDING_TEXT)
    text.SetLayer(pcbnew.B_SilkS)
    text.SetPosition(vmm(35.0, 69.0))
    text.SetTextSize(vmm(0.8, 0.8))
    text.SetTextThickness(pcbnew.FromMM(0.2))
    text.SetBold(True)
    text.SetMirrored(True)
    text.SetHorizJustify(pcbnew.GR_TEXT_H_ALIGN_CENTER)
    text.SetVertJustify(pcbnew.GR_TEXT_V_ALIGN_CENTER)
    board.Add(text)


def main() -> None:
    board = pcbnew.LoadBoard(str(BOARD_PATH))
    add_branding(board)
    pcbnew.SaveBoard(str(BOARD_PATH), board)
    print(f"Added front and rear silkscreen branding: {BOARD_PATH}")


if __name__ == "__main__":
    main()
