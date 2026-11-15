# Elecrow assembly approval

This note answers the assembly checks identified for the PCBA package used by
Elecrow supplier reference `20261010041126`. It is board-specific evidence, not
a replacement for the reusable supplier workflow.

The released source is commit `23b18e7`; the manufacturing package was added by
commit `8687adf` and merged by `b8f732a`. The BOM and position file specify 28
fitted references, all on the top side.

## Assembly check answers

### Are substitutions allowed?

No substitution is pre-approved. Build the exact manufacturer part numbers in
`manufacturing/elecrow/ctvt-pmod-elecrow-bom.csv`. If any exact part is
unavailable, provide the proposed manufacturer, MPN, package, electrical
specifications, and affected references for approval before fitting it.

### How should J1 be fitted?

- Reference: `J1`
- Exact part: Samtec `TSW-106-08-G-D-RA`
- Type: 2x6, 2.54 mm, right-angle male header
- Side: top
- Position/rotation: `(28.65 mm, 25.00 mm)`, `90 degrees`
- Pin 1: square pad at `(28.65 mm, 25.00 mm)`, net `CS`

The right-angle mating pins point outward beyond the rounded top edge. The
plastic body and through-hole tails match the board fabrication and top render.

### How should J4 be fitted?

- Reference: `J4`
- Exact part: Wurth Elektronik `61301221821`
- Type: 2x6, 2.54 mm, vertical female socket
- Side: top
- Position/rotation: `(41.35 mm, 31.50 mm)`, `270 degrees`
- Pin 1: square pad at `(28.65 mm, 31.50 mm)`, net `CS`

J4 is vertical, not right-angle. Its opening faces upward. Pin numbering is
one-to-one with J1, and pin 1 is the leftmost pad in the top board view.

### What polarity should D1 and D2 use?

Both parts are bidirectional `CA` TVS devices and therefore have no functional
polarity:

| Reference | Exact part | Package | Position/rotation |
| --- | --- | --- | --- |
| `D1` | Good-Ark `GSMF3.3CA` | SOD-123F | `(28.00 mm, 69.50 mm)`, `0 degrees` |
| `D2` | Littelfuse `SMBJ18CA` | DO-214AA SMB | `(43.00 mm, 71.00 mm)`, `0 degrees` |

Fit the exact MPN and package. Either end-to-end electrical orientation is
valid; following the fabrication drawing orientation is preferred for visual
consistency.

### How should U1 be fitted?

- Reference: `U1`
- Exact part: Texas Instruments `ADS131M02IPWR`
- Package: TSSOP-20
- Side: top
- Position/rotation: `(35.00 mm, 47.00 mm)`, `90 degrees`
- Pin 1 pad: `(32.075 mm, 49.8625 mm)`, net `AVDD`

Align the package pin-1 dot/chamfer with the PCB pin-1 triangle and pad. In the
top board view, pin 1 is the lower-left package pin.

## Supplier-ready response

> Please proceed using the exact BOM with no substitutions unless we approve a
> proposed replacement in writing.
>
> J1 is Samtec TSW-106-08-G-D-RA, fitted on the top side as a right-angle male
> header with the mating pins pointing outward beyond the rounded board edge.
> J4 is Wurth 61301221821, fitted on the top side as a vertical female socket
> with its opening facing upward. Align both connectors to their square pin-1
> pads.
>
> D1 GSMF3.3CA and D2 SMBJ18CA are bidirectional CA TVS devices, so they have no
> functional polarity. Fit the exact listed packages in the fabrication
> drawing orientation.
>
> U1 is ADS131M02IPWR in TSSOP-20. Align the package pin-1 dot/chamfer with the
> PCB pin-1 triangle; pin 1 is the lower-left pin in the top board view.
>
> Before assembling the remaining boards, please send one clear first-article
> top-side photograph showing J1, J4, D1, D2, and U1.

## Verification

The saved board was rechecked with KiCad 10 before preparing this response:

- PCB DRC: zero violations and zero unconnected items.
- Schematic ERC: zero violations.
- BOM and CPL entries match the saved board references, sides, positions, and
  rotations listed above.
- `docs/images/ctvt-pmod-top.png` and
  `docs/images/ctvt-pmod-isometric.png` show the intended fitted geometry.

