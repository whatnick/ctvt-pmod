# DigiKey BOM sourcing

The orderable BOM is in
[`ctvt-pmod-sourced-bom.csv`](ctvt-pmod-sourced-bom.csv). DigiKey parts were
checked through the Product Search API on 2026-09-22 using the Australian
locale, with in-stock and RoHS-compliant filters.

The selected parts preserve the schematic values and PCB footprints. In
particular, the 10 nF C0G capacitors use 0603 `GRM188` parts and the ferrite
bead uses a 0603 `MPZ1608` part; the earlier `GRM155` and `BLM15` MPNs were
0402 parts and did not match the board footprints.

R1 and R2 use TE Connectivity Holsworthy `RN73C2A6R49BTDF`, sourced from
[Mouser Australia](https://au.mouser.com/en/ProductDetail/TE-Connectivity-Holsworthy/RN73C2A6R49BTDF?qs=8G8kQhBkhGgsmDku%2FDmUNg%3D%3D).
It is a footprint-compatible 6.49 ohm, 0.1%, 0805 thin-film resistor with a
10 ppm/degree C temperature coefficient and a 0.1 W rating.

Stock and pricing change continuously. Recheck all DigiKey part numbers before
ordering, especially the ADC, connectors, D1, C7, and the precision resistors.
