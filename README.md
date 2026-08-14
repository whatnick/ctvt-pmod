# CTVT PMOD

An open hardware PMOD for safely acquiring current-transformer (CT) and
voltage-transformer (VT) waveforms for Tiny Tapeout energy-monitoring
experiments.

This repository is an independent KiCad 10 project. It has no template
project, submodules, or external project-library dependencies.

## Status

Initial placeholder design. The PCB establishes a 33.0 mm x 20.3 mm PMOD
outline and labels the intended functional areas. The analog frontend,
converter, protection network, connectors, and final routing are not yet
implemented and must not be used for measurement.

## Proposed architecture

```text
CT input -> burden/protection -> differential anti-alias filter --+
                                                                  |
VT input -> protection/scale -> differential anti-alias filter ---+-> ADS131M02
                                                                       |
3.3 V PMOD <---------------- SPI, DRDY, RESET --------------------------+
```

The proposed converter is the TI ADS131M02, providing two simultaneous
24-bit delta-sigma channels suitable for phase-coherent voltage and current
sampling.

## Proposed PMOD interface

| Pin | Signal | Direction | Purpose |
|---:|---|---|---|
| 1 | CS | Input | SPI chip select |
| 2 | MOSI | Input | SPI data to ADC |
| 3 | MISO | Output | SPI data from ADC |
| 4 | SCLK | Input | SPI clock |
| 5 | DRDY | Output | Conversion-ready interrupt |
| 6 | RESET | Input | ADC reset |
| 7-8 | Reserved | - | Optional clock, gain, or calibration control |
| 9-10 | GND | Power | Digital ground |
| 11-12 | 3V3 | Power | Regulated 3.3 V input |

## Design goals

- Simultaneous CT and VT sampling for RMS, phase, power-factor, and real/reactive-power tests
- Transformer-isolated field inputs
- Input clamps, burden/scale selection, and differential RC anti-alias filtering
- 3.3 V PMOD-compatible digital interface
- Test points and calibration-source injection
- Clear analog/digital partitioning and manufacturable Elecrow outputs

## Safety

This design is intended only for isolated CTs and certified isolated AC/AC
voltage transformers. **Never connect mains voltage directly to this PMOD.**
Transformer ratings, creepage, clearance, fusing, enclosure, and applicable
safety standards remain the responsibility of the final implementation.

## Files

- `ctvt-pmod.kicad_pro` - KiCad 10 project
- `ctvt-pmod.kicad_sch` - initial empty schematic sheet
- `ctvt-pmod.kicad_pcb` - PMOD-sized placeholder board

Open the project in KiCad 10 before beginning schematic capture.
