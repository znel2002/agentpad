# AgentPad — KMK firmware skeleton
# 9-key (3x3) + 1 turn-only EC11 encoder + 0.91" OLED + 20x SK6812 RGB
# on a Seeed XIAO RP2040. Design: ../../docs/DESIGN-SPEC.md
#
# Copy to CIRCUITPY/main.py. See ../README.md for the KMK + library setup.
# This is a STARTING POINT: matrix/encoder/layers/RGB/OLED are wired up, but the
# per-tool keystrokes are placeholders you refine, and the layer-cycle key should
# be verified on your KMK version (note below).

import board

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC, make_key
from kmk.matrix import DiodeOrientation
from kmk.modules.layers import Layers
from kmk.modules.holdtap import HoldTap
from kmk.modules.encoder import EncoderHandler
from kmk.handlers.sequences import send_string

keyboard = KMKKeyboard()

# ----------------------------------------------------------------------------
# Matrix  (net map in ../../PCB/README.md)
# ----------------------------------------------------------------------------
keyboard.row_pins = (board.D0, board.D1, board.D2)          # ROW0..2 (GP26/27/28)
keyboard.col_pins = (board.D6, board.D7, board.D8)          # COL0..2 (GP0/1/2)
keyboard.diode_orientation = DiodeOrientation.COL2ROW       # match the PCB diodes

# ----------------------------------------------------------------------------
# Modules
# ----------------------------------------------------------------------------
keyboard.modules.append(Layers())
keyboard.modules.append(HoldTap())
encoder = EncoderHandler()
keyboard.modules.append(encoder)

# ----------------------------------------------------------------------------
# Tool layers: 0 Claude Code | 1 Codex | 2 Cursor | 3 shell | 4 FN (hold LAYER)
# ----------------------------------------------------------------------------
CLAUDE, CODEX, CURSOR, SHELL, FN = 0, 1, 2, 3, 4

# LAYER key: tap = cycle the active tool layer; hold = momentary FN.
# NOTE: cycling isn't a built-in KMK keycode, so it's a custom key that rewrites
# active_layers. If it misbehaves on your KMK build, replace CYCLE with KC.MO(FN)
# and put KC.TO(0..3) on four FN-layer keys instead (rock-solid fallback).
_tool = [CLAUDE]


def _cycle_tool(key, keyboard, *args, **kwargs):
    _tool[0] = (_tool[0] + 1) % 4
    keyboard.active_layers[:] = [_tool[0]]


CYCLE = make_key(names=("CYCLE",), on_press=_cycle_tool)
LAYER = KC.HT(CYCLE, KC.MO(FN))     # tap=cycle tool, hold=FN

# send_string sequences for typed commands
CC_NEW = send_string("/clear\n")
CC_COMPACT = send_string("/compact\n")
CC_RESUME = send_string("/resume\n")
RUN_CMD = send_string("npm test\n")  # <- your test/last command

# Keymap: 9 keys row-major (R1C1,R1C2,R1C3, R2C1..). One row per layer.
keyboard.keymap = [
    # Layer 0 — Claude Code
    [
        KC.ESC,   KC.ENTER, KC.N,       # STOP  YES   NO
        KC.LSFT(KC.TAB), CC_NEW, KC.SPACE,  # PLAN  NEW   TALK(hold)
        RUN_CMD,  CC_COMPACT, LAYER,     # RUN   COMPACT  LAYER
    ],
    # Layer 1 — Codex (TODO: confirm current Codex TUI keys)
    [
        KC.ESC,   KC.ENTER, KC.TAB,      # STOP  steer  queue
        KC.LSFT(KC.TAB), send_string("/new\n"), KC.SPACE,
        RUN_CMD,  send_string("/compact\n"), LAYER,
    ],
    # Layer 2 — Cursor (GUI; Cmd-based. TODO: confirm)
    [
        KC.LGUI(KC.BSPC), KC.LGUI(KC.ENTER), KC.ESC,   # stop  accept-all  reject
        KC.NO,    KC.LGUI(KC.N), KC.SPACE,             # (no plan-mode)  new-chat  talk
        RUN_CMD,  KC.NO, LAYER,
    ],
    # Layer 3 — shell / generic terminal
    [
        KC.LCTL(KC.C), KC.ENTER, KC.LCTL(KC.C),        # SIGINT  enter  SIGINT
        KC.NO,    send_string("clear\n"), KC.SPACE,
        send_string("!!\n"), KC.NO, LAYER,             # RUN = repeat last cmd
    ],
    # Layer 4 — FN (held via LAYER). Hold-LAYER secondaries.
    [
        KC.TRNS,  KC.ENTER,  KC.ESC,     # -      accept-edit  reject-edit
        KC.TRNS,  CC_RESUME, KC.TRNS,    # -      resume       -
        KC.LCTL(KC.B), KC.TRNS, KC.TRNS, # background  -  (LAYER held)
    ],
]

# ----------------------------------------------------------------------------
# Encoder — turn-only effort/model dial. Placeholder = arrow up/down; remap per
# tool to its effort/model control once finalized. (ccw, cw) per encoder, per layer.
# ----------------------------------------------------------------------------
encoder.pins = ((board.D9, board.D10, None),)   # A, B, no push button
encoder.map = [
    ((KC.DOWN, KC.UP),),   # Claude Code
    ((KC.DOWN, KC.UP),),   # Codex
    ((KC.DOWN, KC.UP),),   # Cursor
    ((KC.DOWN, KC.UP),),   # shell
    ((KC.TRNS, KC.TRNS),),  # FN
]

# ----------------------------------------------------------------------------
# RGB — static per-key function colors (the legend). Index order must match the
# SK6812 CHAIN order on the PCB; adjust once the layout is fixed. Driven directly
# via neopixel (not the KMK RGB extension) so colors are simple and static.
# Enhancement: hook the KMK loop for press-flash + active-layer underglow.
# ----------------------------------------------------------------------------
try:
    import neopixel

    KEY_COLORS = [
        (255, 0, 0),   (0, 255, 0),   (255, 120, 0),   # STOP  YES   NO
        (0, 0, 255),   (160, 0, 255), (0, 200, 255),   # PLAN  NEW   TALK
        (255, 255, 255), (0, 255, 180), (255, 150, 0), # RUN   COMPACT  LAYER
    ]
    pixels = neopixel.NeoPixel(board.D3, 20, brightness=0.3, auto_write=False)
    for i, color in enumerate(KEY_COLORS):
        pixels[i] = color
    # LEDs 9..19 = case underglow; leave as a dim wash for now
    for i in range(len(KEY_COLORS), 20):
        pixels[i] = (10, 10, 10)
    pixels.show()
except Exception as exc:  # noqa: BLE001 - don't let RGB kill the keyboard
    print("RGB init skipped:", exc)

# ----------------------------------------------------------------------------
# OLED — boot splash + status. Needs adafruit_displayio_ssd1306 in CIRCUITPY/lib.
# ----------------------------------------------------------------------------
try:
    from kmk.extensions.display import Display, TextEntry
    from kmk.extensions.display.ssd1306 import SSD1306

    display = Display(
        display=SSD1306(sda=board.SDA, scl=board.SCL, device_address=0x3C),
        entries=[
            TextEntry(text="AgentPad", x=0, y=0),
            TextEntry(text="CLAUDE CODE", x=0, y=12),
            TextEntry(text="effort: HIGH", x=0, y=24),
        ],
        width=128,
        height=32,
    )
    keyboard.extensions.append(display)
except Exception as exc:  # noqa: BLE001
    print("OLED init skipped:", exc)


if __name__ == "__main__":
    keyboard.go()
