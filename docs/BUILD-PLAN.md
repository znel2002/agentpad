# AgentPad — Build Plan

The shortest path from here to a submitted Hackpad board. Design is locked in
[DESIGN-SPEC.md](DESIGN-SPEC.md). Check boxes as you go.

## Session 0 — admin (do first, runs in parallel with everything)
- [ ] Join **#hackpad** on Hack Club Slack.
- [ ] Post the confirmation message ([docs/hackpad-slack-message.md](hackpad-slack-message.md)):
      Germany shipping, current grant amounts, MX switch type.
- [ ] Note the answers back into DESIGN-SPEC.md §7.

## Session 1 — toolchain validation
- [ ] Install KiCad (stable — 8.x or 9.x, whatever the guide + care package target;
      confirm the version in #hackpad before committing to KiCad 10).
      `brew install --cask kicad`  *(may prompt for your password)*
- [ ] Grab Hack Club's footprint/symbol **care package** (XIAO RP2040 + SK6812)
      from the guide → drop into `PCB/`. Links in [PCB/README.md](../PCB/README.md).
- [ ] Build the official **3-key tutorial board** end to end (schematic → route →
      DRC 0 → gerbers). This proves the toolchain before the real layout.

## Session 2 — the AgentPad PCB
- [ ] Schematic: XIAO + 3×3 matrix (9 switches + 9 diodes) + encoder + OLED header +
      20× SK6812 chain, wired per the net map in [PCB/README.md](../PCB/README.md).
- [ ] Footprints: use care-package parts. **OLED pin order GND-VCC-SCL-SDA.**
      **All diodes same orientation (COL2ROW).**
- [ ] Route (2 layers, ≤100×100 mm), add `AgentPad` silkscreen.
- [ ] **DRC → 0 errors.** Do not order until this is clean.
- [ ] Export gerbers → `production/gerbers.zip`.
- [ ] **Order from JLCPCB the moment DRC is clean** so fab/ship overlaps case + firmware.

## Session 3 — firmware (can start before boards arrive)
- [ ] Flash CircuitPython to the XIAO RP2040.
- [ ] Copy KMK + libs + [Firmware/kmk/main.py](../Firmware/kmk/main.py) to CIRCUITPY.
      Setup in [Firmware/README.md](../Firmware/README.md).
- [ ] Breadboard-test the matrix scan + encoder + OLED + one LED before the PCB lands.
- [ ] Fill in the Codex / Cursor / shell per-layer keystroke tables.

## Session 4 — case
- [ ] Generate the switch plate with the ai03 plate generator (3×3, 19.05 mm).
- [ ] Fusion 360 sandwich case (top plate + body), 6× M3 + heatset bosses,
      `AgentPad` on the top plate, 0.2–0.25 mm mating tolerances, no-supports print.
- [ ] Export one STEP/3MF of the assembly → `CAD/`; per-part STL/STEP → `production/`.

## Session 5 — assemble + ship
- [ ] Solder (watch diode orientation), flash `firmware.uf2` → `production/`.
- [ ] README screenshots: full render + schematic + PCB + case-fit.
- [ ] Ship post in **#hackpad-ships** + submit the form.
