# ADC PMOD comparative analysis

This document compares CTVT PMOD with the 17 commercial expansion boards in
[`expansion_boards__daughter_cards.csv`](expansion_boards__daughter_cards.csv).
The source list is a DigiKey Australia snapshot, so stock and prices should be
rechecked before making purchasing or product-positioning decisions.

## Executive comparison

CTVT PMOD is not a generic ADC evaluation board. It is a complete low-voltage,
isolated-sensor analog front end for phase-coherent current and voltage
measurement:

- two simultaneously sampled 24-bit delta-sigma channels;
- dedicated CT burden and isolated AC/AC transformer input networks;
- precision dividers, differential filtering, and transient protection;
- direct Tiny Tapeout and FabricFox PMOD pin mapping;
- a pass-through PMOD socket for probing or chaining; and
- companion open FPGA and GF180 ASIC DSP for RMS, active power, and energy.

Most boards in the comparison instead demonstrate one ADC IC with a generic
analog input. Eleven are single-channel SAR ADC boards optimized for higher
sample rate. Two provide isolated single-channel measurement front ends, two
provide configurable mixed ADC/DAC/GPIO, and one is a precision multiplexed
delta-sigma sensor ADC.

The `EVAL-AD7124-8-PMDZ` is the closest alternative by converter architecture
and low-noise measurement intent. It is not a direct energy-metrology
alternative, however, because its many inputs share a multiplexer and are not
sampled simultaneously.

## Product-family summary

| Family | Boards in the CSV | Architecture | Best use | Comparison with CTVT |
|---|---:|---|---|---|
| PulSAR single-channel ADC | 11 | 14-, 16-, or 18-bit SAR; 100 kSPS to 1.33 MSPS | Fast control, transient capture, and general data acquisition | Much faster per channel, but a second board does not provide inherently simultaneous or phase-matched voltage/current capture |
| AD7124-8 precision ADC | 1 | 24-bit delta-sigma with an input multiplexer | Low-bandwidth precision sensors and many slowly changing inputs | Closest precision alternative, but multiplexed rather than simultaneous |
| CN0335/CN0336 isolated acquisition | 2 | AD7091R SAR ADC, amplifier, and ADuM5401 isolation | Isolated industrial signal acquisition | Adds digital/power isolation absent from CTVT, but remains a single-channel 12-bit measurement path rather than a coherent metrology pair |
| AD5592R/AD5593R mixed signal | 2 | Configurable 12-bit ADC, DAC, and GPIO channels | Flexible control and housekeeping I/O | More flexible, but substantially less specialized for precision waveform and power measurement |
| MAX1240 peripheral module | 1 | Single-channel 12-bit SAR | Basic SPI ADC evaluation | Simple and easy to drive, but limited resolution, channel count, and metrology-specific conditioning |

## Closest products

| Product | Converter and interface | Sampling relationship | Input/front end | CSV price | CTVT comparison |
|---|---|---|---|---:|---|
| **CTVT PMOD** | TI ADS131M02, dual 24-bit delta-sigma, SPI plus DRDY/reset/clock | **Two simultaneous channels** | CT burden and protection; balanced isolated-transformer divider and protection; differential filters | Project BOM rather than retail price | Purpose-built open energy-metrology front end with FPGA/ASIC DSP |
| [EVAL-AD7124-8-PMDZ](https://www.analog.com/en/products/ad7124-8.html) | AD7124-8, 24-bit delta-sigma, SPI, up to 19.2 kSPS IC output rate | Up to 8 differential or 15 pseudo-differential inputs through one multiplexer | Generic precision sensor inputs; programmable gain, references, excitation currents, and digital filters | A$67.63 | Better for many low-speed precision sensors; worse for coherent voltage/current phase measurement |
| [EVAL-CN0335-PMDZ](https://www.analog.com/en/resources/reference-designs/circuits-from-the-lab/cn0335.html) | AD7091R 12-bit SAR with AD8606 and ADuM5401 | Single conversion channel | Conditioned and galvanically isolated industrial acquisition circuit | A$92.47 | Stronger isolation boundary; lower resolution and no simultaneous current/voltage pair |
| [EVAL-CN0336-PMDZ](https://www.analog.com/en/resources/reference-designs/circuits-from-the-lab/cn0336.html) | AD7091R 12-bit SAR with AD8606 and ADuM5401 | Single conversion channel | Alternate conditioned and galvanically isolated industrial acquisition circuit | A$92.47 | Same broad tradeoff as CN0335; consult the circuit notes for their differing input conditioning |
| [EVAL-AD7690-PMDZ](https://www.analog.com/en/products/ad7690.html) | AD7690, 18-bit SAR, SPI-compatible, 400 kSPS | Single channel | Generic ADC evaluation input | A$76.09 | Higher bandwidth; lacks the second coherent channel and metrology input networks |
| [EVAL-AD7984-PMDZ](https://www.analog.com/en/products/ad7984.html) | AD7984, 18-bit SAR, 1.33 MSPS | Single channel | Generic ADC evaluation input | A$66.50 | Best suited to fast acquisition rather than line-frequency energy integration |
| [EVAL-AD5592R-PMDZ](https://www.analog.com/en/products/ad5592r.html) | AD5592R, configurable 12-bit ADC/DAC/GPIO, SPI | Multiplexed configurable channels | General mixed-signal I/O | A$58.55 | Wins on flexibility; CTVT wins on resolution, simultaneity, front-end accuracy, and metrology purpose |

Nominal converter bits are not equivalent to noise-free or effective
resolution. Board layout, reference noise, input source impedance, converter
data rate, gain, digital filter, clock quality, and calibration all affect
usable performance.

## Complete CSV classification

| Board | Nominal conversion capability | Classification |
|---|---|---|
| `MAX1240PMB#` | MAX1240, single-channel 12-bit SAR, up to 73 kSPS | Basic SPI ADC |
| `EVAL-CN0335-PMDZ` | AD7091R-based isolated 12-bit acquisition path; listed at 300 kSPS board throughput | Isolated industrial ADC |
| `EVAL-CN0336-PMDZ` | AD7091R-based isolated 12-bit acquisition path; listed at 300 kSPS board throughput | Isolated industrial ADC |
| `EVAL-AD7690-PMDZ` | Single-channel 18-bit SAR, 400 kSPS | Precision high-speed SAR |
| `EVAL-AD7124-8-PMDZ` | 24-bit delta-sigma, up to 8 differential multiplexed inputs, up to 19.2 kSPS | Precision sensor ADC |
| `EVAL-AD7693-PMDZ` | Single-channel 16-bit SAR, 500 kSPS | Precision high-speed SAR |
| `EVAL-AD7984-PMDZ` | Single-channel 18-bit SAR, 1.33 MSPS | Precision high-speed SAR |
| `EVAL-AD7982-PMDZ` | Single-channel 18-bit SAR, 1 MSPS | Precision high-speed SAR |
| `EVAL-AD7688-PMDZ` | Single-channel 16-bit SAR, 500 kSPS | Precision high-speed SAR |
| `EVAL-AD5592R-PMDZ` | Eight configurable 12-bit ADC, DAC, or GPIO pins; SPI | Mixed-signal control |
| `EVAL-AD5593R-PMDZ` | Eight configurable 12-bit ADC, DAC, or GPIO pins; I2C | Mixed-signal control |
| `EVAL-AD7686-PMDZ` | Single-channel 16-bit SAR, 500 kSPS | Precision high-speed SAR |
| `EVAL-AD7983-PMDZ` | Single-channel 16-bit SAR, 1.33 MSPS | Precision high-speed SAR |
| `EVAL-AD7980-PMDZ` | Single-channel 16-bit SAR, 1 MSPS | Precision high-speed SAR |
| `EVAL-AD7946-PMDZ` | Single-channel 14-bit SAR, 500 kSPS | High-speed SAR |
| `EVAL-AD7988-5-PMDZ` | Single-channel 16-bit SAR, 500 kSPS | Precision SAR |
| `EVAL-AD7988-1-PMDZ` | Single-channel 16-bit SAR, 100 kSPS | Precision SAR |

The CSV descriptions and linked manufacturer documents are the source of the
headline rates in this table. Actual usable rates can be lower because of
interface timing, isolation, settling, filtering, or host limitations.

## Why simultaneous sampling matters

Energy measurement depends on the instantaneous product of voltage and
current:

```text
p[n] = v[n] * i[n]
```

If the voltage and current samples are taken at different times, the sampling
offset appears as phase error. At 50 or 60 Hz this can materially affect active
power when the load has a low power factor. A multiplexed ADC can compensate
for a stable timing offset in software, but the correction depends on frequency,
filter delay, source settling, and the selected channel sequence.

The ADS131M02 converts both CTVT channels together and applies matched digital
filtering. This is more valuable for power measurement than the much higher
sample rate of a single-channel SAR PMOD. The SAR boards are preferable when
the application instead needs wide signal bandwidth, low conversion latency,
or transient capture.

## AD7124-8 versus ADS131M02

The two devices share a nominal 24-bit delta-sigma architecture, but target
different systems.

| Property | AD7124-8 PMOD | CTVT ADS131M02 PMOD |
|---|---|---|
| Input strategy | Many inputs through a multiplexer | Two dedicated simultaneous channels |
| Primary strength | Flexible, low-noise precision sensor interface | Phase-coherent waveform acquisition |
| Integrated features | PGA, reference options, sensor excitation, flexible filters and diagnostics | Matched dual conversion paths, metrology-oriented data interface and channel timing |
| External conditioning | Application-dependent | Included CT and isolated-transformer networks |
| Energy calculations | Host must supply all processing | Open FPGA/GF180 companion implementation |
| Best fit | RTD, thermocouple, bridge, pressure, and laboratory sensor acquisition | Current, voltage, active power, RMS, and energy experiments |

The AD7124-8 is a better general laboratory sensor ADC. CTVT is the better
starting point when relative phase and a reproducible energy-measurement signal
chain matter more than channel count.

## Isolation comparison

The ADuM5401 used by CN0335 and CN0336 combines digital isolation with an
isolated power converter. It separates the measurement-side circuitry from the
host-side PMOD signals. CTVT does not contain a board-level galvanic isolation
barrier. Instead, its intended sensors provide isolation:

- the current input requires an isolated current transformer; and
- the voltage input requires a certified isolated AC/AC transformer.

This keeps CTVT inexpensive and directly compatible with a 3.3 V PMOD host,
but it makes correct sensor selection part of the safety architecture. An
isolated digital interface could be useful in a future laboratory variant, but
it would increase cost, board area, emissions, power demand, and clock/data
complexity. It would not by itself make the product safe or certified for a
direct mains connection.

## Price and positioning

The 17-board CSV snapshot ranges from **A$47.10 to A$182.84**:

- median: **A$64.24**;
- arithmetic mean: **A$71.10**; and
- most Analog Devices PMOD boards: approximately **A$48 to A$76**.

The unusually high `MAX1240PMB#` price and low stock should not be treated as a
normal market anchor. The strongest retail reference for CTVT is the A$58-A$93
group containing the mixed-signal, precision delta-sigma, and isolated
acquisition boards.

CTVT can justify a price in that group only if it is sold as more than an ADC
breakout. The value proposition is:

1. a complete and documented CT/voltage-transformer front end;
2. coherent dual-channel capture;
3. open FPGA and ASIC processing;
4. reproducible KiCad and manufacturing sources; and
5. calibration and reference-measurement examples.

Conversely, CTVT should not claim that nominal 24-bit conversion makes it more
accurate than the SAR boards or the AD7124-8. Accuracy must be demonstrated
over input amplitude, phase angle, frequency, temperature, supply variation,
and component tolerance.

## Lessons for CTVT

The commercial boards suggest several improvements to documentation and future
revisions:

1. **Publish measured performance.** Include noise histograms, effective
   resolution, gain error, phase error, crosstalk, and power-error plots rather
   than relying on nominal ADC resolution.
2. **State the operating configuration.** Document ADC clock, output data rate,
   oversampling ratio, gain, filter mode, reference arrangement, and frame
   format.
3. **Document input limits.** Give normal, full-scale, and protected transient
   input ranges for supported CT and transformer combinations.
4. **Provide calibration data.** Supply a repeatable voltage, current, phase,
   and offset calibration procedure with uncertainty and temperature results.
5. **Add host examples.** Commercial evaluation boards reduce adoption friction
   with drivers and demonstrations. CTVT should provide FPGA, RP2040/RP2350,
   and Python capture examples using one documented register protocol.
6. **Separate safety from converter isolation.** Clearly retain the requirement
   for isolated sensors and avoid implying that protection components provide
   a certified mains isolation barrier.
7. **Consider an isolation variant only for a defined need.** A digitally
   isolated laboratory PMOD could compete with CN0335/CN0336, but should not
   displace the smaller and less expensive standard version without user
   evidence.

## Recommended positioning

Describe CTVT as an **open, phase-coherent energy-metrology PMOD**, not as a
generic 24-bit ADC PMOD:

> CTVT PMOD provides a complete isolated-sensor current and voltage front end,
> simultaneous 24-bit conversion, and open FPGA-to-GF180 metrology processing
> for power-measurement research and education.

This separates it from the high-speed SAR PMODs, which sell conversion
bandwidth, and from the AD7124-8 PMOD, which sells flexible precision sensor
acquisition. CTVT's defensible product is the integrated measurement workflow:
sensor connector to calibrated samples to inspectable power and energy
algorithms.
