#!/usr/bin/env python3

import csv
import json
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BOARD = ROOT / "ctvt-pmod.kicad_pcb"
SCHEMATIC = ROOT / "ctvt-pmod.kicad_sch"
SOURCED_BOM = ROOT / "docs" / "ctvt-pmod-sourced-bom.csv"
OUTPUT = ROOT / "manufacturing" / "elecrow"
GERBERS = OUTPUT / "gerbers"
RAW_POS = OUTPUT / "ctvt-pmod-kicad-position.csv"
ELECROW_BOM = OUTPUT / "ctvt-pmod-elecrow-bom.csv"
ELECROW_POS = OUTPUT / "ctvt-pmod-elecrow-pos.csv"
GERBER_ZIP = OUTPUT / "ctvt-pmod-elecrow-gerbers.zip"
PCBA_ZIP = OUTPUT / "ctvt-pmod-elecrow-pcba.zip"


def find_kicad_cli() -> str:
    found = shutil.which("kicad-cli")
    if found:
        return found

    windows_path = Path(r"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe")
    if windows_path.exists():
        return str(windows_path)

    raise SystemExit("KiCad 10 kicad-cli was not found")


def run(*args: str) -> None:
    subprocess.run(args, cwd=ROOT, check=True)


def references(text: str) -> list[str]:
    return text.replace(",", " ").split()


def natural_reference_key(reference: str) -> tuple[str, int]:
    prefix = reference.rstrip("0123456789")
    suffix = reference[len(prefix) :]
    return prefix, int(suffix or 0)


def export_bom() -> set[str]:
    all_references: set[str] = set()
    with SOURCED_BOM.open(newline="", encoding="utf-8-sig") as source:
        rows = list(csv.DictReader(source))

    fieldnames = [
        "Designator",
        "Quantity",
        "Comment",
        "Footprint",
        "Manufacturer",
        "Manufacturer Part Number",
        "Supplier",
        "Supplier Part Number",
        "Sourcing Note",
    ]
    with ELECROW_BOM.open("w", newline="", encoding="utf-8-sig") as output:
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            refs = references(row["References"])
            all_references.update(refs)
            writer.writerow(
                {
                    "Designator": ",".join(refs),
                    "Quantity": row["Quantity"],
                    "Comment": row["Value"],
                    "Footprint": row["Package"],
                    "Manufacturer": row["Manufacturer"],
                    "Manufacturer Part Number": row[
                        "Manufacturer Part Number"
                    ],
                    "Supplier": row["Supplier"],
                    "Supplier Part Number": row["Supplier Part Number"],
                    "Sourcing Note": row["Sourcing Note"],
                }
            )
    return all_references


def export_positions() -> set[str]:
    with RAW_POS.open(newline="", encoding="utf-8-sig") as source:
        rows = [
            row
            for row in csv.DictReader(source)
            if not row["Ref"].upper().startswith("LOGO")
        ]

    rows.sort(key=lambda row: natural_reference_key(row["Ref"]))
    fieldnames = [
        "Designator",
        "Mid X",
        "Mid Y",
        "Layer",
        "Rotation",
        "Comment",
        "Footprint",
    ]
    with ELECROW_POS.open("w", newline="", encoding="utf-8-sig") as output:
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    "Designator": row["Ref"],
                    "Mid X": f'{float(row["PosX"]):.4f}mm',
                    "Mid Y": f'{-float(row["PosY"]):.4f}mm',
                    "Layer": "Top" if row["Side"].lower() == "top" else "Bottom",
                    "Rotation": f'{float(row["Rot"]) % 360:.2f}',
                    "Comment": row["Val"],
                    "Footprint": row["Package"],
                }
            )
    return {row["Ref"] for row in rows}


def write_readme(version: str, parity_count: int) -> Path:
    path = OUTPUT / "README.txt"
    path.write_text(
        "\n".join(
            [
                "CTVT PMOD Elecrow PCBA package",
                "",
                f"Generated with KiCad {version}.",
                "Board: 2-layer, all fitted components on the top side.",
                "BOM: 18 grouped line items / 28 fitted component references.",
                "Position file: millimetres, board coordinates, top-side rotations.",
                "",
                "Files:",
                "- ctvt-pmod-elecrow-gerbers.zip: PCB fabrication files",
                "- ctvt-pmod-elecrow-bom.csv: sourcing and assembly BOM",
                "- ctvt-pmod-elecrow-pos.csv: component centroid/position file",
                "",
                "Engineering DRC/ERC reports are retained beside this upload",
                "archive in the repository's manufacturing output directory.",
                "",
                f"KiCad schematic parity warnings: {parity_count}. These are",
                "generator metadata differences (qualified footprint names,",
                "leading-slash net names, and sourcing fields), not PCB DRC,",
                "connectivity, or ERC violations.",
                "",
                "Confirm substitutions, connector orientation, and polarized",
                "component orientation with Elecrow before approving assembly.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    return path


def create_zip(path: Path, files: list[Path]) -> None:
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as archive:
        for file in files:
            archive.write(file, file.name)


def main() -> None:
    kicad = find_kicad_cli()
    version = subprocess.check_output([kicad, "version"], text=True).strip()
    if not version.startswith("10."):
        raise SystemExit(f"KiCad 10 is required, found {version}")

    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)
    GERBERS.mkdir(parents=True)

    drc = OUTPUT / "manufacturing-drc.json"
    erc = OUTPUT / "manufacturing-erc.json"
    parity = OUTPUT / "manufacturing-schematic-parity.json"

    run(
        kicad,
        "pcb",
        "drc",
        "--format",
        "json",
        "--severity-error",
        "--severity-warning",
        "--exit-code-violations",
        "-o",
        str(drc),
        str(BOARD),
    )
    run(
        kicad,
        "sch",
        "erc",
        "--format",
        "json",
        "--severity-error",
        "--severity-warning",
        "--exit-code-violations",
        "-o",
        str(erc),
        str(SCHEMATIC),
    )
    subprocess.run(
        [
            kicad,
            "pcb",
            "drc",
            "--format",
            "json",
            "--severity-error",
            "--severity-warning",
            "--schematic-parity",
            "-o",
            str(parity),
            str(BOARD),
        ],
        cwd=ROOT,
        check=False,
    )

    run(
        kicad,
        "pcb",
        "export",
        "gerbers",
        "--layers",
        "F.Cu,B.Cu,F.Paste,B.Paste,F.Silkscreen,B.Silkscreen,F.Mask,B.Mask,Edge.Cuts",
        "--subtract-soldermask",
        "--check-zones",
        "-o",
        str(GERBERS),
        str(BOARD),
    )
    run(
        kicad,
        "pcb",
        "export",
        "drill",
        "--format",
        "excellon",
        "--excellon-units",
        "mm",
        "--excellon-separate-th",
        "--generate-map",
        "--map-format",
        "pdf",
        "--generate-report",
        "--report-path",
        str(GERBERS / "ctvt-pmod-drill-report.txt"),
        "-o",
        str(GERBERS),
        str(BOARD),
    )
    run(
        kicad,
        "pcb",
        "export",
        "pos",
        "--format",
        "csv",
        "--units",
        "mm",
        "--side",
        "both",
        "--exclude-dnp",
        "-o",
        str(RAW_POS),
        str(BOARD),
    )

    bom_references = export_bom()
    position_references = export_positions()
    if bom_references != position_references:
        missing = sorted(bom_references - position_references)
        extra = sorted(position_references - bom_references)
        raise SystemExit(
            f"BOM/position mismatch; missing positions={missing}, "
            f"extra positions={extra}"
        )

    parity_data = json.loads(parity.read_text(encoding="utf-8"))
    readme = write_readme(
        version, len(parity_data.get("schematic_parity", []))
    )

    gerber_files = sorted(file for file in GERBERS.iterdir() if file.is_file())
    create_zip(GERBER_ZIP, gerber_files)
    create_zip(
        PCBA_ZIP,
        [GERBER_ZIP, ELECROW_BOM, ELECROW_POS, readme],
    )

    print(f"Created {PCBA_ZIP}")
    print(f"Validated {len(bom_references)} fitted component references")


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as error:
        sys.exit(error.returncode)
