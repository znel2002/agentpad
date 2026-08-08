# Firmware — AgentPad (KMK)

KMK (CircuitPython) firmware. Keymap + pin map locked in
[../docs/DESIGN-SPEC.md](../docs/DESIGN-SPEC.md). Entry point: [kmk/main.py](kmk/main.py).

## Flash setup (XIAO RP2040)
1. **CircuitPython:** double-tap the XIAO reset to enter bootloader (RPI-RP2
   drive), drop the CircuitPython `.uf2` for the Seeed XIAO RP2040
   (https://circuitpython.org/board/seeeduino_xiao_rp2040/). It reboots as a
   `CIRCUITPY` drive.
2. **KMK:** clone https://github.com/KMKfw/kmk_firmware and copy its `kmk/`
   folder to `CIRCUITPY/`.
3. **Libraries** (into `CIRCUITPY/lib/`, from the Adafruit CircuitPython bundle):
   - `neopixel.mpy` — per-key RGB
   - `adafruit_displayio_ssd1306.mpy` + `adafruit_display_text/` — OLED
     (displayio is built into CircuitPython on RP2040)
4. Copy [kmk/main.py](kmk/main.py) to `CIRCUITPY/main.py`. It runs on boot.

## Test order (before the PCB arrives)
Breadboard the XIAO and validate incrementally — comment out blocks in `main.py`:
1. Matrix scan (press a key across a row/col jumper → keystroke appears).
2. Encoder turn.
3. One SK6812 lights.
4. OLED prints text.

## Status
- Matrix, encoder, layers, hold-LAYER FN, static per-key RGB, OLED splash: scaffolded.
- **TODO:** finalize Codex / Cursor / shell keystrokes; verify the layer-cycle key
  on your KMK version (see the comment in `main.py`); optional live LED feedback.
