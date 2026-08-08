# PCB — AgentPad

KiCad source for the AgentPad board. Design locked in
[../docs/DESIGN-SPEC.md](../docs/DESIGN-SPEC.md).

## Before you start
1. Install KiCad (stable 8.x/9.x — confirm the version against the Hackpad guide +
   care package in #hackpad first).
2. Drop Hack Club's footprint/symbol **care package** here (XIAO RP2040 + SK6812).
   - Guide: https://hackpad.hackclub.com/guide
   - Repo + reference boards: https://github.com/hackclub/hackpad
3. Build the 3-key tutorial board first to validate the toolchain.

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
| 3V3 | — | OLED VCC, all SK6812 VDD |
| GND | — | matrix/encoder commons, OLED GND, all SK6812 GND |

## Matrix (3×3, 9 keys)
- One 1N4148 **per key**, all the **same orientation (COL2ROW)**. Wrong diode
  direction is the #1 beginner failure — verify against the KMK config
  (`Firmware/kmk/main.py`, `diode_orientation = COL2ROW`).
- Keys map row-major to the keymap: R1C1..R1C3, R2C1..R2C3, R3C1..R3C3.

## Encoder (EC11)
- A → ENC_A (D9), B → ENC_B (D10), common → GND.
- **Turn-only config:** the encoder's push-switch pins are left unconnected (no
  free GPIO / matrix node). Add a pad footprint anyway so an 8-key clickable
  variant stays possible without a respin.

## OLED (0.91" SSD1306, I2C @ 0x3C)
- **Footprint pin order is GND-VCC-SCL-SDA** (kit spec) — match it exactly.
- SDA→D4, SCL→D5, VCC→3V3, GND→GND.

## SK6812 chain (20 LEDs, 1 data line)
- D3 → LED1 DIN; each LED DOUT → next LED DIN; chain all 20.
- 9 per-key (under each switch) + up to 11 case underglow.
- Kit ships no caps/resistors; per-LED decoupling is optional for a chain this
  small. Keep the data trace short from the XIAO to LED1.

## Preflight before ordering
- [ ] Board ≤ 100 × 100 mm, **2 layers**.
- [ ] `AgentPad` on the silkscreen.
- [ ] **DRC → 0 errors** (reviewers check this).
- [ ] Export gerbers → `../production/gerbers.zip`.
- [ ] Order JLCPCB immediately after DRC is clean.
