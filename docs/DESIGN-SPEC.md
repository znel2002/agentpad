# AgentPad — Hardware & UX Design Spec (v1)

Status: **v1 PCB complete, DRC 0 errors.** This is the buildable design the PCB,
case, and firmware are cut from.

> **v1 ships without RGB LEDs.** The SK6812 reverse-mount footprint (with its
> built-in board cutout) could not pass edge-clearance DRC, and RGB is not
> required by Hackpad (the reference board barely used LEDs). v1 = 9 switches +
> encoder + OLED. **RGB (per-key / underglow) is deferred to v2** with a proper
> LED footprint.

---

## 1. Locked decisions

| Decision | Value | Why |
|---|---|---|
| Name (branding) | **AgentPad** | On PCB silkscreen + top plate (Hackpad requires it) |
| MCU | Seeed XIAO RP2040 | Required by Hackpad; **11 usable GPIO** is the binding constraint |
| Config | **9 keys (3×3) + 1 EC11 encoder + 0.91" OLED + SK6812 RGB** | Only kit-only config that keeps screen + dial + per-key RGB |
| Encoder | **1, turn-only** (effort/model dial, live-apply) | 2nd encoder would force dropping the OLED; click would cost the 9th key |
| Firmware | **KMK** (CircuitPython) first, QMK fallback | Fastest iteration for a Python dev; no compile step |
| Tool layers | **4**: Claude Code · Codex · Cursor · shell | Vendor-neutral is the whole differentiator |
| PCB | 2-layer, ≤100×100 mm, **green** soldermask | Cheapest/fastest fab; DRC must pass 0 errors |
| Legends | **RGB color-coding + printed legend card** | Kit ships blank DSA caps; color is the legend |
| Case | 3D-printed sandwich, 6× M3 into heatset inserts, ≤200×200×100 mm | Kit + rules |

---

## 2. Pin budget (all 11 GPIO used)

RGB chains on one data wire regardless of LED count, so it costs 1 pin for all
20 LEDs. The rest divides as:

| Function | Pins | XIAO pads |
|---|---|---|
| Key matrix 3×3 (3 rows + 3 cols) | 6 | rows D0/D1/D2 (GP26/27/28), cols D6/D7/D8 (GP0/1/2) |
| Encoder A/B | 2 | D9/D10 (GP4/GP3) |
| OLED I2C (SDA/SCL) | 2 | D4/D5 (GP6/GP7) |
| SK6812 RGB data | 1 | D3 (GP29) |
| **Total** | **11** | D0–D10 fully allocated |

- Matrix diode direction: one 1N4148 per key (9 used of 20). Pick **COL2ROW** and
  keep every diode the same orientation (the #1 beginner failure). Confirm the
  direction against the KMK/QMK matrix config before ordering.
- OLED footprint pin order is **GND-VCC-SCL-SDA** (kit spec) — the PCB must match.
- Encoder is turn-only in this config (no matrix node free for the push). A
  clickable encoder is available only by dropping to 8 keys.

---

## 3. Keymap

9 physical keys in a fixed 3×3 grid. Each **layer** = one tool profile; the same
key sends that tool's equivalent keystroke. The Claude Code column is the
reference binding; the other three fill the same slots (finalized against each
tool's current shortcuts at firmware time).

| Pos | Key | Purpose | Claude Code keystroke |
|---|---|---|---|
| R1C1 | **STOP** | Interrupt the run, don't kill the session | `Esc` |
| R1C2 | **YES** | Approve / accept the pending prompt | `Enter` |
| R1C3 | **NO** | Reject / decline | `n` |
| R2C1 | **PLAN** | Cycle permission / plan mode | `Shift+Tab` |
| R2C2 | **NEW** | Clear context, fresh session | `/clear⏎` |
| R2C3 | **TALK** | Push-to-talk dictation (momentary, active while held) | hold `Space` |
| R3C1 | **RUN** | Fire test / last command | `npm test⏎` (configurable) |
| R3C2 | **COMPACT** | Compact the context window | `/compact⏎` |
| R3C3 | **LAYER** | **Tap** = cycle tool profile · **Hold** = FN modifier | — |

**Encoder:** turn = reasoning-effort / model dial, applies live; OLED shows the
new level.

**Hold-LAYER secondary actions** (recover the Tier-2/3 actions without more keys):
- Hold LAYER + **YES** = accept edit/diff
- Hold LAYER + **NO** = reject edit/diff
- Hold LAYER + **NEW** = resume session (`/resume⏎`)
- Hold LAYER + **RUN** = background task

Per-layer keystroke tables (Codex / Cursor / shell) → firmware appendix, TBD.

---

## 4. RGB scheme (20× SK6812, 1 data pin)

9 per-key LEDs + up to 11 case-underglow LEDs on the same chain (0 extra pins).

**Static per-key function color** (the legend):

| STOP 🔴 red | YES 🟢 green | NO 🟠 amber |
|---|---|---|
| **PLAN 🔵 blue** | **NEW 🟣 purple** | **TALK 🩵 cyan** (brightens while held) |
| **RUN ⚪ white** | **COMPACT teal** | **LAYER = active-tool color** |

**Layer identity** (LAYER key + underglow wash): Claude Code = amber · Codex =
green · Cursor = blue · shell = white.

**Feedback:** brief flash on key press.

Offline note: RGB encodes *local* state (layer, function, press). Live agent
status (idle/thinking/waiting) needs optional USB-serial feedback from the host —
**parked as a post-submission stretch.**

---

## 5. OLED (0.91", 128×32, SSD1306)

- Line 1: active tool profile — `CLAUDE CODE`
- Line 2: effort + mode — `effort: HIGH  ·  PLAN`
- Boot splash: `AgentPad` + logo.

Same offline caveat: the mode field tracks local PLAN/effort presses, it does not
read the host.

---

## 6. Physical layout

- 3×3 key grid on **19.05 mm** MX spacing. OLED top-left, encoder top-right on the
  strip above the grid. Estimated footprint ~70×90 mm (inside 100×100 mm).
- MX switches are **solder-in** (no hotswap sockets in kit).
- Sandwich case: top plate + PCB + bottom, 6× M3×16 screws into M3 heatset inserts.
- `AgentPad` branding on the top plate (recessed/embossed) **and** PCB silkscreen.
- Printed legend card / plate silkscreen keying the RGB colors to functions.

---

## 7. Open items before layout
- [ ] **Germany shipping** — ships from Burlington VT; the site never addresses
      international shipping. Confirm in #hackpad (the one real unknown).
- [ ] **Grant amount conflict** — the submitting page says **$15** for the PCB, the
      FAQ says **$10**. Confirm the current number in #hackpad. (Iron grant is $18,
      non-transferrable, both pages agree.)
- [ ] Confirm the kit's MX switch type (tactile vs linear) in #hackpad.
- [ ] Finalize Codex / Cursor / shell per-layer keystroke tables.
- [ ] Decide 9-key-turn-only vs 8-key-clickable-encoder (default: 9-key).
- [ ] Case color (decide at print time with Printing Legion).

---

## 8. Bill of materials (from the free kit)

| Part | Qty used / kit | Notes |
|---|---|---|
| Seeed XIAO RP2040 | 1 / 1 | |
| 1N4148 diode | 9 / 20 | one per key, COL2ROW |
| MX-style switch | 9 / 16 | solder-in |
| EC11 encoder | 1 / 2 | 2nd = solder backup |
| 0.91" OLED (SSD1306) | 1 / 1 | GND-VCC-SCL-SDA |
| SK6812 MINI-E LED | up to 20 / 20 | 9 per-key + underglow |
| DSA blank keycap | 9 / 16 | color-coded |
| M3×16 screw | 6 / 6 | |
| M3 heatset insert | 6 / 6 | |
