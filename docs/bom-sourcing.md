# DigiKey BOM sourcing

The orderable BOM is in
[`ctvt-pmod-digikey-bom.csv`](ctvt-pmod-digikey-bom.csv). Parts were checked
through the DigiKey Product Search API on 2026-09-22 using the Australian
locale, with in-stock and RoHS-compliant filters.

The selected parts preserve the schematic values and PCB footprints. In
particular, the 10 nF C0G capacitors use 0603 `GRM188` parts and the ferrite
bead uses a 0603 `MPZ1608` part; the earlier `GRM155` and `BLM15` MPNs were
0402 parts and did not match the board footprints.

## Sourcing exception

The specified Vishay `TNPW08056R49BEEA` 6.49 ohm, 0.1%, 0805 burden resistor
was not listed by DigiKey when checked. DigiKey had exact-value 1% cut-tape
parts and an exact-value 0.1% TE Connectivity part only in reels of 1000.
Keep the Vishay part and source it elsewhere, or re-run gain calibration and
explicitly approve a tolerance change before fitting an alternative.

Stock and pricing change continuously. Recheck all DigiKey part numbers before
ordering, especially the ADC, connectors, D1, C7, and the precision resistors.
