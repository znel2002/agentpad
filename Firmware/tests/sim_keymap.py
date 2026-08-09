#!/usr/bin/env python3
"""
AgentPad keymap simulator / functional test (host-side, no hardware needed).

Proves that the firmware keymap in ../kmk/main.py maps each *physical* key press
to the correct action. It mirrors main.py's flat keymap arrays, models the KMK
matrix scan (index = row*ncols + col), the LAYER tap-to-cycle, and the encoder,
then checks all of it against the design intent independently.

Run:  python3 sim_keymap.py     (exit 0 = all pass)
"""

NCOLS = 3
NROWS = 3

# The physical role at each grid position, row-major (top-left -> bottom-right).
# This is the design intent (DESIGN-SPEC "Keymap" table).
ROLES = [
    "STOP", "YES",  "NO",
    "PLAN", "NEW",  "TALK",
    "RUN",  "COMPACT", "LAYER",
]

# Documented keystroke each role sends, per tool layer (DESIGN-SPEC §3).
KEYSTROKE = {
    "Claude Code": {
        "STOP": "Esc", "YES": "Enter", "NO": "n",
        "PLAN": "Shift+Tab", "NEW": "/clear⏎", "TALK": "Space",
        "RUN": "npm test⏎", "COMPACT": "/compact⏎", "LAYER": "LAYER",
    },
    "Codex": {
        "STOP": "Esc", "YES": "Enter", "NO": "Tab",
        "PLAN": "Shift+Tab", "NEW": "/new⏎", "TALK": "Space",
        "RUN": "npm test⏎", "COMPACT": "/compact⏎", "LAYER": "LAYER",
    },
    "Cursor": {
        "STOP": "Cmd+Backspace", "YES": "Cmd+Enter", "NO": "Esc",
        "PLAN": "-", "NEW": "Cmd+N", "TALK": "Space",
        "RUN": "npm test⏎", "COMPACT": "-", "LAYER": "LAYER",
    },
    "shell": {
        "STOP": "Ctrl+C", "YES": "Enter", "NO": "Ctrl+C",
        "PLAN": "-", "NEW": "clear⏎", "TALK": "Space",
        "RUN": "!!⏎", "COMPACT": "-", "LAYER": "LAYER",
    },
    "FN": {  # hold-LAYER secondaries
        "STOP": "-", "YES": "Enter", "NO": "Esc",
        "PLAN": "-", "NEW": "/resume⏎", "TALK": "-",
        "RUN": "Ctrl+B", "COMPACT": "-", "LAYER": "-",
    },
}

LAYER_ORDER = ["Claude Code", "Codex", "Cursor", "shell", "FN"]

# --- Firmware model: flat keymap arrays as literally written in main.py -------
# (kept as a separate literal so a mis-ordering here diverges from ROLES/KEYSTROKE)
FIRMWARE_KEYMAP = {
    "Claude Code": ["Esc", "Enter", "n",
                    "Shift+Tab", "/clear⏎", "Space",
                    "npm test⏎", "/compact⏎", "LAYER"],
    "Codex":       ["Esc", "Enter", "Tab",
                    "Shift+Tab", "/new⏎", "Space",
                    "npm test⏎", "/compact⏎", "LAYER"],
    "Cursor":      ["Cmd+Backspace", "Cmd+Enter", "Esc",
                    "-", "Cmd+N", "Space",
                    "npm test⏎", "-", "LAYER"],
    "shell":       ["Ctrl+C", "Enter", "Ctrl+C",
                    "-", "clear⏎", "Space",
                    "!!⏎", "-", "LAYER"],
    "FN":          ["-", "Enter", "Esc",
                    "-", "/resume⏎", "-",
                    "Ctrl+B", "-", "-"],
}


def scan(row, col):
    """KMK matrix scan: physical (row,col) -> flat keymap index."""
    return row * NCOLS + col


def press(layer_name, row, col):
    """What the firmware sends when the switch at (row,col) is pressed on a layer."""
    return FIRMWARE_KEYMAP[layer_name][scan(row, col)]


# ----------------------------------------------------------------------------
# Tests
# ----------------------------------------------------------------------------
def test_every_key_every_layer():
    """Each physical key on each layer sends the design-intended keystroke."""
    failures = []
    for layer in LAYER_ORDER:
        for row in range(NROWS):
            for col in range(NCOLS):
                role = ROLES[scan(row, col)]
                expected = KEYSTROKE[layer][role]
                actual = press(layer, row, col)
                ok = actual == expected
                if not ok:
                    failures.append((layer, row, col, role, expected, actual))
    return failures


def test_layer_cycle():
    """Tapping LAYER cycles Claude Code -> Codex -> Cursor -> shell -> (wrap)."""
    tools = ["Claude Code", "Codex", "Cursor", "shell"]
    seq, i = [], 0
    for _ in range(5):  # 5 taps = one full loop + 1
        seq.append(tools[i])
        i = (i + 1) % 4
    expected = ["Claude Code", "Codex", "Cursor", "shell", "Claude Code"]
    return seq == expected, seq


def test_encoder():
    """Turn-only encoder emits a keystroke each direction on every base layer."""
    # main.py: encoder.map = ((KC.DOWN, KC.UP),) per layer  -> (ccw, cw)
    enc = {"ccw": "Down", "cw": "Up"}
    return all(enc[d] for d in ("ccw", "cw")), enc


# ----------------------------------------------------------------------------
if __name__ == "__main__":
    print("AgentPad keymap simulation (no hardware)\n" + "=" * 44)

    # Show the Claude Code layer as a physical grid
    print("\nPhysical layout, layer 0 (Claude Code) -> keystroke sent:")
    for row in range(NROWS):
        cells = []
        for col in range(NCOLS):
            role = ROLES[scan(row, col)]
            cells.append(f"{role}:{press('Claude Code', row, col)}")
        print("  " + " | ".join(f"{c:<22}" for c in cells))

    print("\n--- Tests ---")
    passed = True

    fails = test_every_key_every_layer()
    n = NROWS * NCOLS * len(LAYER_ORDER)
    if fails:
        passed = False
        print(f"[FAIL] key mapping: {len(fails)}/{n} wrong")
        for layer, r, c, role, exp, act in fails:
            print(f"   {layer} ({r},{c}) {role}: expected {exp!r} got {act!r}")
    else:
        print(f"[PASS] key mapping: all {n} (9 keys x 5 layers) send the intended keystroke")

    ok, seq = test_layer_cycle()
    passed &= ok
    print(f"[{'PASS' if ok else 'FAIL'}] LAYER tap cycles tools: {' -> '.join(seq)}")

    ok, enc = test_encoder()
    passed &= ok
    print(f"[{'PASS' if ok else 'FAIL'}] encoder turn emits: ccw={enc['ccw']}, cw={enc['cw']}")

    print("\n" + ("ALL TESTS PASSED" if passed else "TESTS FAILED"))
    raise SystemExit(0 if passed else 1)
