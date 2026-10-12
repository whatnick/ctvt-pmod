# Elecrow manufacturing package

Run the deterministic KiCad 10 export from the repository root:

```powershell
python scripts\export_elecrow.py
```

The script runs PCB DRC and schematic ERC, exports fresh Gerbers and separate
PTH/NPTH drill files, converts the reviewed sourced BOM and KiCad centroid data
to assembly CSV files, verifies that every fitted BOM reference has exactly one
position, and creates:

```text
manufacturing/elecrow/ctvt-pmod-elecrow-pcba.zip
```

The PCBA ZIP contains:

- `ctvt-pmod-elecrow-gerbers.zip`
- `ctvt-pmod-elecrow-bom.csv`
- `ctvt-pmod-elecrow-pos.csv`
- a package README

DRC, ERC, and schematic-parity JSON reports remain beside the upload archive
under `manufacturing/elecrow/` for engineering traceability.

The BOM has 18 grouped line items covering 28 fitted references. Test points
and artwork footprints are excluded from procurement and placement. All fitted
parts are on the top side; the position file includes the two through-hole
connectors because Elecrow must quote their manual or selective-solder assembly.

Before approving the order, confirm any proposed substitutions, the right-angle
orientation of `J1`, the socket orientation of `J4`, and the polarity/orientation
of `D1`, `D2`, and `U1`.
