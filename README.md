# AgentPad *(working name — not final)*

A purpose-built macropad for driving AI coding agents (Claude Code · Codex CLI · Cursor).
Twelve keys mapped to the actions you hit dozens of times an hour — Stop / Yes / No /
Plan-mode / New session / push-to-talk / Accept-edit / Reject-edit / Run / Compact /
Resume / Layer — plus a rotary encoder for model/reasoning-effort and a 0.91" OLED
showing the active tool profile and permission mode.

Built for **Hack Club Hackpad**. Firmware-native (no host daemon for core actions);
per-tool **LAYER** switching instead of app-detection.

> **Status:** design locked, pre-layout. Next: install KiCad → 3-key tutorial → this board.
>
> - **Design spec (locked):** [docs/DESIGN-SPEC.md](docs/DESIGN-SPEC.md)
> - **Build plan / checklist:** [docs/BUILD-PLAN.md](docs/BUILD-PLAN.md)
> - **PCB net map + KiCad steps:** [PCB/README.md](PCB/README.md)
> - **Firmware setup + KMK skeleton:** [Firmware/README.md](Firmware/README.md)
> - **#hackpad message to send:** [docs/hackpad-slack-message.md](docs/hackpad-slack-message.md)

## Hardware (locked — Config A, kit-only)
- **MCU:** Seeed XIAO RP2040 (11 usable GPIO — the binding constraint)
- **Keys:** 9 MX switches in a 3×3 matrix  ·  **Encoder:** 1× EC11 (turn-only)  ·  **Display:** 1× 0.91" OLED  ·  **RGB:** 20× SK6812 (9 per-key + underglow, one data line)
- **Firmware:** KMK (CircuitPython) — QMK as fallback
- **Layers:** 4 tool profiles — Claude Code · Codex · Cursor · shell

## Layout (3×3)
| Row | Keys |
| --- | --- |
| 1 | STOP · YES · NO |
| 2 | PLAN · NEW · TALK |
| 3 | RUN · COMPACT · LAYER |
| Encoder | turn = model/effort dial (live-apply) |
| OLED | active tool profile + effort/mode |

Secondary actions (accept-edit / reject-edit / resume / background) live on
**hold-LAYER**. Full keymap: [docs/DESIGN-SPEC.md](docs/DESIGN-SPEC.md).

## Repo structure
- `CAD/` — Fusion 360 sources; one STEP/3MF of the full assembly
- `PCB/` — KiCad project (schematic, board, care-package libs)
- `Firmware/` — KMK source (QMK fallback)
- `production/` — `gerbers.zip`, per-part case STL/STEP, compiled `firmware.uf2`
- `docs/` — working notes and screenshots

## Renders & proof *(to be added)*
- [ ] Full 3D render of the assembly
- [ ] Schematic screenshot
- [ ] PCB (routed, front/back) screenshot
- [ ] Case-fit / cross-section screenshot
- [ ] DRC report: **0 errors**

## BOM
*(to be added — mirrors the free Hackpad kit)*

## License
TBD
