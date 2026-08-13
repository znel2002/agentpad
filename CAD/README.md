# CAD — AgentPad case

Two-part 3D-printed sandwich (top lid + bottom base), designed in **Autodesk Fusion**
around the exact PCB. The board is imported as STEP and every cutout is placed on the
real switch/encoder/OLED/mounting geometry.

## Files
- `agentpad-case.f3d` — Fusion source (editable), the case + inserted PCB reference.
- `agentpad_assembly.step` / `agentpad_assembly.3mf` — full assembly (case + real PCB).
- `agentpad-board.step` — the KiCad board export.
- `agentpad-board-origin.step` — the same board parked at the origin (used as the Fusion import reference).
- Printable parts live in [`../production/`](../production/): `top_plate.stl` (lid), `bottom_tray.stl` (base).

## Design
- **Outer size:** 120 × 100 mm (both parts match). Rounded corners R6.
- **Lid:** 3 mm plate + 4 mm raised bezel around a recessed key well. 9× 14 mm switch
  cutouts with chamfered mouths, Ø8.5 encoder hole, OLED window, 4× M3 clearance holes.
- **Base:** ~13 mm tall tray holding the PCB; USB-C slot in the side wall; `AgentPad`
  engraved on the front wall; 4 corner posts for the screws.
- **Assembly:** 4× M3 screws, lid → base corner posts.

## Print notes
- Both parts print flat, **no supports**.
- Print tolerance ~0.2 mm between mating parts.
- **Verify before printing** (physical modules): the OLED window and USB-C opening
  size/position, and the encoder hole diameter vs your knob.

## Hard limits
- Case ≤ **200 × 200 × 100 mm**, **3D-printed only** (no laser/acrylic parts). ✔
