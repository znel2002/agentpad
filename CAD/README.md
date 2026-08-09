# CAD — AgentPad case

3D-printed sandwich case, built parametrically in **OpenSCAD**: [agentpad_case.scad](agentpad_case.scad).
It's generated from the exact PCB geometry (95×95 mm, hole/switch/encoder/OLED
positions). Two printed parts — top plate + bottom tray — plus a PCB placeholder
for the assembly view.

**Render (OpenSCAD → File → Export):**
- `part = "plate"`  → `../production/top_plate.stl`
- `part = "bottom"` → `../production/bottom_tray.stl`
- `part = "assembly"` → `agentpad_assembly.3mf` (the single assembly file Hackpad wants)

**Verify before printing** (flagged `VERIFY` in the .scad): the encoder hole, OLED
window, and USB-C cutout — their size/orientation depend on the physical modules.
Check the USB edge/offset in KiCad's **3D Viewer** and set `usb_edge`/`usb_pos`.
Note: the kit's **M3×16 screws are long** for a thin macropad — trim them or bump
`comp_gap` so they don't bottom out.

## Hard limits
- Case ≤ **200 × 200 × 100 mm**, **3D-printed only** (no acrylic/laser parts).
- Designed to print **without supports**.

## Exact dimensions (from the Hackpad guide + resources page)
- **Switch spacing:** 19.05 mm center-to-center (3×3 grid).
- **Print tolerance:** 0.2 mm gap between mating 3D-printed parts. Draw the PCB
  cutout at PCB size **+0.4 mm per side**.
- **Heatset insert hole:** 4.7 mm diameter, 4 mm deep (6×, for the M3 inserts).
  - (Screwing straight into plastic instead: 2.9 mm. Screw pass-through: 3.4 mm.)
- **Plate:** generate with ai03's plate generator (https://kbplate.ai03.com),
  download DXF, import to Fusion, center it, extrude 3 mm.
- **Bottom:** base extrude ~3 mm, walls ~10 mm (≈13 mm total) — tune to component
  height + the XIAO + USB-C port clearance.
- Add a **USB-C cutout** aligned to the XIAO position.

## Branding
- `AgentPad` on the top plate (recessed/embossed). Tip from the guide: text/graphics
  in CAD is fiddly — design the overlay in Figma and import it.

## Deliverables
- `CAD/agentpad-assembly.step` (or `.3mf`) — the full assembly, one file.
- `../production/` — each printable part as its own STL + STEP.

## References
- Keyboard mounting styles: https://www.keyboard.university/200-courses/keyboard-mounting-styles-4lpp7
- Joe Scotto case tutorial: https://www.youtube.com/watch?v=7azQkSu0m_U
- EC11 knob / keycap 3D models: search grabcad.com, sort by popular.
