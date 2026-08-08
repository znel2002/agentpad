# PCB — AgentPad

KiCad source for the AgentPad board. Design locked in
[../docs/DESIGN-SPEC.md](../docs/DESIGN-SPEC.md).

## Before you start
1. KiCad **10.0.5** is installed. Its libraries are forward-compatible, so the
   care package (authored on an older version) loads fine — no version issue.
2. Download + install the libraries here:
   - **Care package** (XIAO symbol + footprints): https://github.com/hackclub/hackpad/releases/tag/v0.1-bugfix → `kicad_care_package.zip`
   - XIAO footprints (backup): https://github.com/Seeed-Studio/OPL_Kicad_Library
   - MX switch footprints: https://github.com/ai03-2725/MX_V2
   - Rotary encoder: https://kicad.github.io/footprints/Rotary_Encoder
   - 0.91" OLED (4-pin): https://github.com/gorbachev/KiCad-SSD1306-0.91-OLED-4pin-128x32.pretty
   - The `.sym` files are symbol libs; the `.pretty` folders are footprint libs
     (Preferences → Manage Symbol/Footprint Libraries → add).
3. **Reference board** — the guide author's macropad (OLED + encoder + matrix +
   SK6812, closest to ours): https://github.com/hackclub/hackpad/tree/clean/extras/orpheuspad
4. Learn the flow: ai03's PCB guide https://wiki.ai03.com/books/pcb-design
5. Build the 3-key tutorial board first (XIAO symbol = `MODULE-SEEEDUINO-XIAO`,
   switches = `SW_Push`) to validate the toolchain, then extend to this net map.

## Net map — XIAO RP2040 pad → net (all 11 GPIO used)

| Pad | GPIO | Net |
|---|---|---|
| D0 | GP26 | ROW0 |
| D1 | GP27 | ROW1 |
| D2 | GP28 | ROW2 |
| D3 | GP29 | LED_DIN (SK6812 chain data-in) |
| D4 | GP6 | OLED_SDA (I2C) |
| D5 | GP7 | OLED_SCL (I2C) |
| D6 | GP0 | COL0 |
| D7 | GP1 | COL1 |
| D8 | GP2 | COL2 |
| D9 | GP4 | ENC_A |
| D10 | GP3 | ENC_B |
| 3V3 | — | OLED VCC |
| **5V** | — | **all SK6812 VCC** (the LEDs are 5V parts, per the Hackpad add-components page) |
| GND | — | matrix/encoder commons, OLED GND, all SK6812 GND |

> Data logic stays at the XIAO's 3.3V; SK6812 run their VCC at 5V (the XIAO's 5V/USB
> pad). This is how the kit is designed — do not put SK6812 VCC on 3V3.

## Exact symbols / footprints (confirmed on hackpad.hackclub.com/add-components)

| Part | Symbol | Footprint |
|---|---|---|
| XIAO RP2040 | `MODULE-SEEEDUINO-XIAO` (care package) | care-package XIAO footprint |
| MX switch | `SW_Push` | care package / `ai03-2725/MX_V2` |
| Diode 1N4148 | `D` | `Diode_THT:D_DO-35_SOD27_P7.62mm_Horizontal` (don't go shorter) |
| EC11 encoder | `RotaryEncoder_Switch` | `RotaryEncoder_Alps_EC11E-Switch_Vertical_H20mm` |
| SK6812 MINI-E | `SK6812MINI-E` (care package) | `SK6812MINI-E` (**not** SK6812MINI) |
| 0.91" OLED | 4-pin header | 2.54 mm 4-pin header footprint |

No pull-up resistors anywhere — the RP2040 has internal pull-ups (kit relies on this).

## Matrix (3×3, 9 keys)
- One **1N4148** (onsemi) per key, all the **same orientation (COL2ROW)**. Wrong
  diode direction is the #1 beginner failure — verify against the KMK config
  (`Firmware/kmk/main.py`, `diode_orientation = COL2ROW`). The physical diode has
  a **black bar** marking the cathode.
- Footprint `Diode_THT:D_DO-35_SOD27_P7.62mm_Horizontal`.
- Keys map row-major to the keymap: R1C1..R1C3, R2C1..R2C3, R3C1..R3C3.

## Encoder (EC11E, 20 mm D-shaft)
- Symbol `RotaryEncoder_Switch`, footprint `RotaryEncoder_Alps_EC11E-Switch_Vertical_H20mm`.
- A → ENC_A (D9), B → ENC_B (D10), common → GND. No pull-ups needed.
- **Turn-only config:** the footprint includes the push-switch pins — leave them
  **unconnected**. Keeping the pads means an 8-key clickable variant is possible
  later without a respin.

## OLED (0.91" 128×32 SSD1306, I2C @ 0x3C)
- Footprint = plain **2.54 mm 4-pin header** (the module has a standard header;
  no special footprint needed).
- **Pin order GND-VCC-SCL-SDA** — match it exactly (online pinouts vary).
- SDA→D4, SCL→D5, VCC→3V3, GND→GND. No pull-ups needed.

## SK6812 MINI-E chain (20 LEDs, 1 data line)
- Footprint `SK6812MINI-E` from the care package (**not** `SK6812MINI`; symbol +
  both footprints must say MINI-E).
- 4 pins: VCC (**5V**), GND, DIN, DOUT. D3 → LED1 DIN; each DOUT → next DIN; chain all 20.
- **Orientation: the notch/cut is on the bottom-right corner** — wrong rotation and
  the LEDs won't light. Keep every LED the same way.
- 9 per-key (under each switch) + up to 11 case underglow.
- Keep the data trace from the XIAO to LED1 short.

## Mounting holes (from the Hackpad resources page)
- Use KiCad's **M3 mounting-hole footprint** — NOT Edge.Cuts.
- 6 holes to match the 6× M3 screws / heatset inserts.
- For the OLED, a plain **4-pin header footprint** is fine (order GND-VCC-SCL-SDA).

## Routing tips (from the resources page)
- Try to route everything on **one layer** first; only drop to the 2nd layer to
  avoid a big loop. Keeps the board clean.
- After routing: **Tools → Cleanup Tracks & Vias** (press "Build changes" twice).
- Export the PCB to PDF and print 1:1 to sanity-check physical measurements.

## Preflight before ordering
- [ ] Board ≤ 100 × 100 mm, **2 layers**.
- [ ] `AgentPad` on the silkscreen.
- [ ] 6× M3 mounting-hole footprints placed.
- [ ] **DRC → 0 errors** (reviewers check this).
- [ ] Export gerbers → `../production/gerbers.zip`.
- [ ] Order JLCPCB immediately after DRC is clean.
