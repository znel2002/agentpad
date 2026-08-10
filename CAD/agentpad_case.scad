// ============================================================================
// AgentPad — parametric 3D-printed sandwich case (OpenSCAD)
// Generated from the KiCad board geometry (95 x 95 mm, holes/switches/encoder/
// OLED extracted from agentpad.kicad_pcb). Two printed parts: top plate + bottom
// tray. PCB sits between them; 6x M3 screws from the top thread into heatset
// inserts in the bottom bosses.
//
// USAGE:  set `part` below, then Render (F6) and Export as STL.
//   part = "plate"     -> top_plate.stl        (print flat, no supports)
//   part = "bottom"    -> bottom_tray.stl      (print open-side up, no supports)
//   part = "assembly"  -> visual check (plate + PCB placeholder + tray)
//
// Coordinates are board-local mm with (0,0) at the board's min corner, Y flipped
// so this top view matches the KiCad top view (encoder/OLED along the top edge).
// ============================================================================

part = "assembly";           // "plate" | "bottom" | "assembly"
explode = 0;                 // assembled fit view; set >0 (e.g. 16) to explode the stack

/* ---- board geometry (fixed — from the PCB) -------------------------------- */
board_w = 95;                // X
board_d = 95;                // Y
pcb_t   = 1.6;

// 6 mounting holes [x,y]  (H1,H4 top corners; H3,H2,H6 bottom; H5 mid-right)
holes = [[5,90],[90,90],[90,47],[90,5],[47.5,5],[5,5]];

// 3x3 switch centers: X {40, 59.05, 78.1}  Y {26.9, 45.95, 65}
sw_x = [40, 59.05, 78.1];
sw_y = [26.9, 45.95, 65];

// KiCad footprint origins are at pin 1 / a corner, NOT the component center.
// These offsets move each cutout onto the true center (already Y-flipped for OpenSCAD).
sw_off = [-2.54, -5.08];     // MX origin is at pin 1; the stem (keycap center) is here
enc  = [37.0, 79.5];          // encoder shaft = origin(29.5,82) + mounting-post midpoint (7.5,-2.5)
// OLED: J1 is a 4-pin header on the module's short edge; the module extends to one side.
oled_pin = [48.32, 81.02];   // header pin-row center (computed from J1)
oled_dir = 1;                // +1 = module extends +X (right, away from encoder); -1 = left  [VERIFY]

/* ---- tunables ------------------------------------------------------------ */
wall     = 2.5;              // outer wall thickness
plate_t  = 3;               // top plate thickness
floor_t  = 2;               // bottom floor thickness
pcb_gap  = 0.2;             // clearance around the PCB (print tolerance)
comp_gap = 5;               // clearance UNDER the PCB for the XIAO (on the back)
boss_d   = 8;               // heatset boss diameter
heatset_d= 4.7;             // heatset insert hole (4.7 x 4 deep, per Hackpad)
heatset_h= 4;
screw_d  = 3.4;             // M3 clearance hole through the plate
sw_cut   = 14;              // MX switch cutout (standard plate cut)
corner_r = 6;               // outer case corner radius (rounder = fancier)
bezel_h  = 4;               // raised rim above the recessed key well (Hackpad-v5 bezel look)
rim_w    = 3.5;             // bezel rim width
$fn = 64;

// ---- module cutouts (VERIFY against the physical modules + KiCad 3D view) --
enc_d    = 8;               // VERIFY: EC11 bushing pass-through (~7 mm)
oled_len = 38; oled_wid = 13; // 0.91" module ~38x12mm (incl tol); window spans the module  [VERIFY]
usb_edge = "top";           // XIAO USB-C faces NORTH (top edge) — pins are vertical columns
usb_pos  = 16;              // X of the port along the top edge (XIAO center: KiCad 76 - 60)
usb_w    = 12; usb_h = 7;   // USB-C cutout width x height (spans the under-PCB gap)
usb_depth= 13;              // reach INWARD from the edge (port is recessed ~9 mm) -> a channel

/* ---- derived Z levels ---------------------------------------------------- */
pcb_z    = floor_t + comp_gap;      // PCB bottom sits here (on the bosses)
plate_z  = pcb_z + pcb_t;           // plate sits on the PCB top
wall_h   = plate_z;                 // tray walls rise to the PCB top
out_off  = wall + pcb_gap;          // how far the outer shell is beyond the board
out_w    = board_w + 2*out_off;
out_d    = board_d + 2*out_off;

// rounded rectangle helper
module rrect(w, d, h, r) {
    linear_extrude(h)
        offset(r) offset(-r) square([w, d]);
}

/* ---- top plate ----------------------------------------------------------- */
module top_plate() {
    H = plate_t + bezel_h;      // full height at the bezel rim
    difference() {
        union() {
            // recessed floor (holds the switch cutouts)
            translate([-out_off, -out_off, 0]) rrect(out_w, out_d, plate_t, corner_r);
            // raised perimeter bezel enclosing a recessed key well
            difference() {
                translate([-out_off, -out_off, 0]) rrect(out_w, out_d, H, corner_r);
                translate([-out_off + rim_w, -out_off + rim_w, plate_t])
                    rrect(out_w - 2*rim_w, out_d - 2*rim_w, bezel_h + 2, max(corner_r - rim_w, 1));
            }
        }
        // 9 switch cutouts (through the floor)
        for (x = sw_x, y = sw_y)
            translate([x + sw_off[0] - sw_cut/2, y + sw_off[1] - sw_cut/2, -1])
                cube([sw_cut, sw_cut, H + 2]);
        // encoder bushing hole
        translate([enc[0], enc[1], -1]) cylinder(d = enc_d, h = H + 2);
        // OLED window (recessed screen area)
        let (ox0 = (oled_dir > 0) ? oled_pin[0] - 2 : oled_pin[0] - oled_len)
            translate([ox0, oled_pin[1] - oled_wid/2, -1])
                cube([oled_len + 2, oled_wid, H + 2]);
        // 6 screw clearance holes
        for (h = holes)
            translate([h[0], h[1], -1]) cylinder(d = screw_d, h = H + 2);
        // soften the top outer edge (small chamfer ring)
        translate([-out_off, -out_off, H - 1])
            difference() {
                rrect(out_w, out_d, 1.2, corner_r);
                translate([1, 1, -0.5]) rrect(out_w - 2, out_d - 2, 2, corner_r);
            }
    }
}

/* ---- bottom tray --------------------------------------------------------- */
module usb_cutout() {
    // carve a CHANNEL through the wall + inward to the recessed port.
    // The XIAO sits on the PCB back, so the USB port is in the under-PCB gap.
    z = floor_t - 0.5;
    L = usb_depth + wall + 2;   // channel length (edge -> port + through the wall)
    if (usb_edge == "left")
        translate([-out_off - 1, usb_pos - usb_w/2, z]) cube([L, usb_w, usb_h]);
    else if (usb_edge == "right")
        translate([board_w + pcb_gap + wall + 1 - L, usb_pos - usb_w/2, z]) cube([L, usb_w, usb_h]);
    else if (usb_edge == "top")
        translate([usb_pos - usb_w/2, board_d + pcb_gap + wall + 1 - L, z]) cube([usb_w, L, usb_h]);
    else // bottom
        translate([usb_pos - usb_w/2, -out_off - 1, z]) cube([usb_w, L, usb_h]);
}

module bosses() {
    for (h = holes)
        translate([h[0], h[1], floor_t]) difference() {
            cylinder(d = boss_d, h = comp_gap);              // rises to PCB rest
            translate([0, 0, comp_gap - heatset_h])
                cylinder(d = heatset_d, h = heatset_h + 1);  // heatset hole from top
        }
}

module bottom_tray() {
    difference() {
        union() {
            // outer shell (solid up to the PCB top)
            translate([-out_off, -out_off, 0]) rrect(out_w, out_d, wall_h, corner_r);
        }
        // inner pocket (open top) housing the PCB + components under it
        translate([-pcb_gap, -pcb_gap, floor_t])
            cube([board_w + 2*pcb_gap, board_d + 2*pcb_gap, wall_h]);
        usb_cutout();
        // branding recessed into the underside (mirrored so it reads when flipped over)
        translate([board_w/2, board_d/2, -0.5])
            linear_extrude(1.2) mirror([1, 0, 0])
                text("AgentPad", size = 9, halign = "center", valign = "center",
                     font = "Liberation Sans:style=Bold");
    }
    bosses();
}

/* ---- realistic PCB + components (assembly fit view) ---------------------- */
sw_body_h = 11; cap = 18; cap_h = 6;

module switches_3d() {
    for (x = sw_x, y = sw_y) {
        color("#222222") translate([x + sw_off[0] - 7, y + sw_off[1] - 7, pcb_z + pcb_t]) cube([14, 14, sw_body_h]);
        color("#f2f2f2") translate([x + sw_off[0] - cap/2, y + sw_off[1] - cap/2, pcb_z + pcb_t + sw_body_h]) cube([cap, cap, cap_h]);
    }
}
module encoder_3d() {
    color("#444444") translate([enc[0], enc[1], pcb_z + pcb_t]) cylinder(d = 12, h = 6);
    color("silver")  translate([enc[0], enc[1], pcb_z + pcb_t + 6]) cylinder(d = 6, h = 9);
}
module oled_3d() {   // OLED module sitting in the window (extends oled_dir from the header)
    let (ox0 = (oled_dir > 0) ? oled_pin[0] : oled_pin[0] - oled_len)
        color("#111111") translate([ox0, oled_pin[1] - oled_wid/2, plate_z - 1]) cube([oled_len, oled_wid, 2.5]);
}
module xiao_3d() {  // on the PCB BACK, in the component gap; USB-C toward the top edge
    color("#333333") translate([16 - 8.9, 75 - 10.5, pcb_z - 1.4]) cube([17.8, 21, 1.4]);
    color("silver")  translate([16 - 4.5, 75 + 10.5 - 1, pcb_z - 4.6]) cube([9, 8, 3.2]);
}
module pcb() {
    color("green") difference() {
        translate([0, 0, pcb_z]) rrect(board_w, board_d, pcb_t, corner_r);
        for (h = holes) translate([h[0], h[1], pcb_z - 1]) cylinder(d = 3.2, h = pcb_t + 2);
    }
    switches_3d(); encoder_3d(); oled_3d(); xiao_3d();
}

/* ---- render (two-tone: red plate + black base, Hackpad-v5 style) --------- */
plate_col = "#d1272e";   // red top plate
base_col  = "#1b1b1b";   // black bottom tray

if (part == "plate")   color(plate_col) top_plate();
else if (part == "bottom") color(base_col) bottom_tray();
else if (part == "realfit") {            // REAL KiCad board (STL) inside the case
    color(base_col) bottom_tray();
    // STEP export negates Y (matches our flip) -> just translate: X-60, Y+165, Z+7
    translate([-60, 165, 7]) import("agentpad-board.stl", convexity = 10);
    translate([0, 0, plate_z + explode]) color([0.82, 0.15, 0.18, 0.85]) top_plate();
}
else {                                   // assembly (styled, keycaps on -> no exposed PCB)
    color(base_col) bottom_tray();
    pcb();
    translate([0, 0, plate_z + explode]) color(plate_col) top_plate();
}
