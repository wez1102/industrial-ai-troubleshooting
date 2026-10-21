---
document_id: pneumatic-manual-v1
title: PC-63 Pneumatic Cylinder System Manual
document_type: manual
equipment_type: pneumatic_cylinder
manufacturer: "North Quay Training (fictional)"
model: PC-63
version: "1.0.0"
license: synthetic
---

# PC-63 Pneumatic Cylinder System Manual

The PC-63 system covers the double-acting pneumatic cylinders, valves, and air preparation on CP-01 and PL-01. This manual covers operation, pneumatic alarms, fault isolation, and preventive maintenance for the cylinders, position sensors, valve manifolds, and filter-regulators. It does not replace qualified maintenance personnel or plant lockout/tagout procedures.

## Operating Guide

Plant compressed air arrives from the compressor house through the main header at 6.0–7.0 bar. Each machine takes air through a lockable shut-off valve, a filter-regulator with a 5 µm element and automatic condensate drain, and a soft-start dump valve. The regulator holds machine pressure at 5.5 bar. The dump valve is controlled by the safety circuit: it admits air slowly at start-up and exhausts the machine's air when a stop is demanded. Its function and testing are covered in the safety circuit manual.

Air then goes to a valve manifold with one 5/2 solenoid valve per cylinder. Each valve has a 24 V DC coil with an LED that lights when the coil is energized, and a manual override button. A 5/2 valve holds its last position when de-energized, so a cylinder stays where it is and its chambers stay pressurized until the air is exhausted. Meter-out flow control valves at each cylinder set the stroke speed, and adjustable cushions slow the piston over the last 15–20 mm of stroke. Exhaust air leaves each valve through a sintered silencer.

Each cylinder has a magnetic piston and two clamp-on position sensors in its profile slot, one for extended and one for retracted. A sensor LED lights when the piston magnet is under it. The controller times every stroke from the valve command to the end-position sensor and keeps a baseline from the last 500 normal strokes. A flow meter after each filter-regulator records air consumption, and a pressure transmitter reads machine pressure after the regulator.

| Cylinder | Function | Bore and Stroke | Baseline Stroke Time |
| --- | --- | --- | --- |
| CP-01 CYL1 | Feeder gate lift | 50 mm, 100 mm | 0.25 s each way |
| CP-01 CYL2 | Counter-ejector bundle pusher | 63 mm, 400 mm | 0.60 s extend, 0.50 s retract |
| PL-01 CYL3 | Bundle stop gate | 40 mm, 80 mm | 0.20 s each way |
| PL-01 CYL4 | Layer squaring clamps, two cylinders on one valve | 63 mm, 200 mm | 0.45 s each way |

| Item | Normal Reference | Alarm Criterion |
| --- | --- | --- |
| Header pressure | 6.0–7.0 bar | None at machine level |
| Machine pressure, static | 5.3–5.7 bar | PNEU-4004 below 4.8 bar for 2 s; PNEU-4005 above 6.5 bar for 10 s |
| Machine pressure, during CYL2 stroke | Dips to no lower than 5.0 bar | PNEU-4004 below 4.8 bar for 2 s |
| Filter pressure drop under flow | Below 0.3 bar | PNEU-4009 above 0.6 bar for 30 s |
| Stroke time | Within 15% of baseline | PNEU-4006 if the 20-stroke average is 30% over; PNEU-4001/4002 at 2.0× baseline |
| Idle air flow, CP-01 | About 40 Nl/min | PNEU-4007 above 80 Nl/min for 5 min while idle |
| Idle air flow, PL-01 | About 35 Nl/min | PNEU-4007 above 70 Nl/min for 5 min while idle |
| Leak-down, 5.5 to 4.5 bar with supply shut | 10 min or longer | No alarm; recorded in the monthly check |

Compressed air is stored energy. Closing the shut-off valve does not by itself make a cylinder safe to touch. Air stays trapped between a 5/2 valve and its cylinder, and a cylinder carrying a load, such as the feeder gate, can move when that air is released.

Before working on a cylinder or valve:

1. **SAFETY:** Lock out the machine, close and lock the pneumatic shut-off valve, and confirm the machine pressure gauge reads 0 bar.
2. **SAFETY:** Support or block any load a cylinder is holding up, then exhaust trapped air from both sides of the cylinder before loosening a fitting.
3. Read the alarm, the cylinder tag, and the last stroke times from the HMI cylinder page.
4. Check the valve coil LED and both position sensor LEDs against what the cylinder is actually doing.
5. Do not use a valve manual override while anyone is inside the guarding; the override moves the cylinder regardless of the machine logic.

## Alarm and Fault Codes

The alarm table lists the `PNEU-4xxx` codes for all PC-63 cylinders. The HMI shows the cylinder tag with each code. A timeout tells you only that the expected sensor did not switch in time; it does not say whether the cylinder failed to move or the sensor failed to see it.

| Code | Name | Severity | Description | Likely Causes | Action |
| --- | --- | --- | --- | --- | --- |
| PNEU-4001 | Cylinder Extend Timeout | MEDIUM | Extended sensor not made within 2.0× the baseline stroke time. | Sensor moved; obstruction; low pressure; valve not shifting. | Compare the cylinder position with the sensor LEDs. |
| PNEU-4002 | Cylinder Retract Timeout | MEDIUM | Retracted sensor not made within 2.0× the baseline stroke time. | Sensor moved; obstruction; low pressure; valve not shifting. | Compare the cylinder position with the sensor LEDs. |
| PNEU-4003 | Position Sensor Conflict | HIGH | Both end sensors on together, or both off for 2 s with the cylinder at rest. | Sensor slid into the wrong position; damaged sensor; magnet fault. | Lock out; check sensor positions and wiring. |
| PNEU-4004 | Low Supply Pressure | HIGH | Machine pressure below 4.8 bar for 2 s. | Header pressure low; blocked filter; restricted supply line; large leak. | Compare header and machine gauges; check the supply path. |
| PNEU-4005 | High Supply Pressure | MEDIUM | Machine pressure above 6.5 bar for 10 s. | Regulator set too high or failing. | Check the regulator setting and lock ring. |
| PNEU-4006 | Slow Stroke Warning | LOW | 20-stroke average stroke time 30% over baseline. | Clogged silencer; flow control moved; worn seals; low pressure; binding rod. | Check silencers and flow control marks. |
| PNEU-4007 | Excessive Air Consumption | LOW | Idle air flow above the machine limit for 5 min. | Leaking fittings, hoses, or valve seals; leaking cylinder seals. | Leak survey with the machine idle. |
| PNEU-4008 | Valve Coil Fault | HIGH | Valve manifold reports an open or shorted coil output. | Loose coil connector; burned coil; damaged cable. | Lock out; check the coil connector and resistance. |
| PNEU-4009 | Filter Restriction | MEDIUM | Pressure drop across the filter above 0.6 bar for 30 s. | Clogged filter element; oil or dust load from the header. | Replace the element; inspect the bowl. |
| PNEU-4010 | Condensate Level High | MEDIUM | Filter bowl float switch detects water above the drain level. | Automatic drain stuck; very wet header air. | Drain the bowl; clean or replace the drain. |

## Troubleshooting

Troubleshooting starts with what the cylinder is actually doing compared with what the sensors and valve report. Read the stroke-time trend, the machine pressure trend, and the idle flow before changing any regulator, flow control, or sensor position.

**SAFETY:** Lock out the machine, close and lock the pneumatic shut-off valve, and confirm 0 bar on the machine gauge before reaching into the guarding. Support any raised or loaded mechanism and exhaust trapped air from the cylinder before loosening a fitting, moving a sensor, or pushing a piston rod. Record the cylinder tag, the alarm, the machine pressure, the stroke times, and any recent work on the cylinder, its sensors, or the air supply.

### Cylinder Timeout

**What it means:** PNEU-4001 or PNEU-4002 trips when the end-position sensor does not switch within 2.0 times the baseline stroke time after the valve is commanded. Either the cylinder did not reach the end of its stroke, or it did and the sensor did not see it. The first job is to find out which.

**Symptoms:** The machine stops mid-cycle with the cylinder either fully out, part-way, or not moved at all. If the cylinder is fully at the end of its stroke and the sensor LED is off, the sensor is the problem. If the cylinder stopped part-way, look for something stopping it. If it never moved, look at the valve and air supply.

**Likely causes:** In ranked order: (1) a position sensor that has slid along its slot after being knocked or after the clamp screw loosened; (2) a sheet, bundle, or scrap blocking the stroke; (3) low machine pressure; (4) a valve that is not shifting because of a coil fault or a sticking spool; (5) a flow control closed too far; (6) worn piston seals letting air bypass.

**Checks:**

1. Compare the cylinder's actual position with both sensor LEDs and the valve coil LED.
2. Check the machine pressure at the time of the alarm.
3. **SAFETY:** Lock out the machine, close and lock the shut-off valve, support any load, and exhaust the cylinder. Look along the full stroke for obstructions.
4. With the cylinder exhausted, push the rod by hand to each end where it is small enough to move, and confirm each sensor LED switches at its end.
5. If the coil LED lights but the cylinder does not move with pressure restored, the valve spool is sticking; if the coil LED stays off, check the coil output and connector.

**Corrective action:** Reset a moved sensor: with the piston at the end of stroke, slide the sensor until its LED comes on, then a further 2 mm toward the end position, and tighten the clamp screw by hand. Paint-mark the final position. Clear obstructions and find where they came from. Replace a sticking valve rather than freeing it with spray lubricant. Do not raise the regulator to force a cylinder through a timeout; the cause is rarely pressure alone.

**When to escalate:** Escalate if the cylinder moves part-way with full pressure and no obstruction, which points to worn seals or a bent rod, or if the same sensor moves again after being reset.

### Slow Cylinder Movement

**What it means:** PNEU-4006 warns when the average of the last 20 strokes runs 30% over the baseline. A slow cylinder upsets machine timing long before it causes a timeout, so the warning is worth acting on.

**Symptoms:** The cylinder takes visibly longer to stroke, sometimes in only one direction. The machine cycle slows or a downstream station waits. A cylinder that slows in one direction only points to the exhaust side of that stroke, because the meter-out flow control and silencer on the exhaust side set the speed.

**Likely causes:** In ranked order: (1) an exhaust silencer clogged with paper dust; (2) a flow control valve turned in from its marked setting; (3) low or dipping machine pressure; (4) worn piston seals; (5) a bent rod or misaligned mounting causing binding; (6) cushions screwed in too far, slowing the end of the stroke.

**Checks:**

1. Compare extend and retract times against the baseline to see which direction is slow.
2. Check the machine pressure trend during the stroke.
3. Inspect the exhaust silencers on that valve for dust build-up.
4. Compare each flow control and cushion screw with its paint mark.
5. **SAFETY:** Lock out the machine, close and lock the shut-off valve, support any load, and exhaust the cylinder before checking the rod for scoring or bending and the mounting for misalignment.

**Corrective action:** Replace clogged silencers rather than blowing them out. Return flow controls and cushions to their marked settings. Correct any binding or mounting misalignment. Do not open the flow controls to make up for a clogged silencer; when the silencer is replaced, the cylinder will slam into its end stop.

**When to escalate:** Escalate if the cylinder stays slow with clean silencers, correct settings, and normal pressure, which points to worn seals or internal leakage.

### Low Supply Pressure

**What it means:** PNEU-4004 trips when machine pressure stays below 4.8 bar for 2 s. Static pressure is normally 5.3–5.7 bar, and it should not dip below 5.0 bar even during a CP-01 CYL2 bundle pusher stroke, the largest air user on the line. Every cylinder slows and loses force at low pressure.

**Symptoms:** Several cylinders slow at once, timeouts appear on different cylinders, and the pressure trend dips with each large stroke. If static pressure is normal but it drops during strokes, the supply cannot deliver enough flow. If static pressure is low as well, the header or regulator is the problem.

**Likely causes:** In ranked order: (1) a restriction in the supply path, such as a clogged filter element, a partly closed shut-off valve, or a hose or fitting smaller than specified; (2) low header pressure from the compressor house; (3) a regulator set low or failing; (4) a large leak; (5) more cylinders moving at once than the supply was sized for.

**Checks:**

1. Compare the header gauge before the shut-off valve with the machine gauge after the regulator, both at rest and during a CYL2 stroke.
2. Check the PNEU-4009 history and the filter pressure drop.
3. Confirm the shut-off valve is fully open.
4. **SAFETY:** Lock out the machine, close and lock the shut-off valve, and confirm 0 bar before inspecting the supply hose and fittings. The supply line from the shut-off valve to the filter-regulator is 12 mm bore; check that no section has been replaced with smaller hose.
5. Check idle air flow for a large leak.

**Corrective action:** Remove the restriction: replace the filter element, restore full-bore hose and fittings, or repair the leak. If header pressure is low, report it to the compressor house. Do not raise the machine regulator above 5.5 bar to make up for a supply restriction; static pressure rises but the dips during flow remain.

**When to escalate:** Escalate if header pressure is below 6.0 bar, or if pressure still dips below 5.0 bar during strokes with a clean filter and a full-bore supply.

### Air Leaks

**What it means:** PNEU-4007 warns when idle air flow stays above the machine limit for 5 minutes. With the machine idle and all cylinders at rest, the only air used is leakage, so idle flow is a direct measure of leaks. Leaks waste compressor energy, lower pressure, and slow cylinders.

**Symptoms:** Idle flow climbs over weeks. Pressure falls quickly after the supply is shut off. A hiss is sometimes audible on a quiet machine, but plant noise usually hides it. Cylinders that hold position by pressure may drift slowly.

**Likely causes:** In ranked order: (1) cracked push-in fittings or hoses not fully inserted; (2) hoses rubbed through on guards or moving parts; (3) leaking valve seals, often blowing out of a silencer with the valve at rest; (4) worn cylinder rod or piston seals; (5) a filter bowl seal or automatic drain stuck open.

**Checks:**

1. Record idle flow and compare it with the machine baseline.
2. Do a leak-down test: with the machine idle, close the shut-off valve and time the pressure fall from 5.5 to 4.5 bar. Ten minutes or longer is normal.
3. With the machine idle and still pressurized, survey fittings, hoses, valves, and silencers from outside the guarding with an ultrasonic leak detector.
4. Listen at each silencer; air flowing from a silencer with the valve at rest points to a leaking valve or cylinder seal.
5. **SAFETY:** Lock out the machine, close and lock the shut-off valve, and confirm 0 bar before touching any fitting or applying leak-detection fluid inside the guarding.

**Corrective action:** Replace cracked fittings and damaged hoses, reroute hoses away from rub points with sleeves and clamps, and replace leaking valves. Record idle flow and leak-down time after the repair.

**When to escalate:** Escalate if leaks come from cylinder seals, which need a cylinder exchange, or if idle flow remains above baseline with no external leak found.

## Maintenance Procedure

The preventive schedule below covers air preparation, silencers, position sensors, hoses and fittings, and leak checks. Record the cylinder or machine tag, the readings, and the technician for each task.

**SAFETY:** Lock out the machine, close and lock the pneumatic shut-off valve, and confirm 0 bar before any task inside the guarding or on a pressurized component. Support raised or loaded mechanisms, such as the CP-01 feeder gate, and exhaust trapped air before loosening fittings.

| Frequency | Preventive Task | Record To Keep |
| --- | --- | --- |
| Daily | Check machine pressure and filter bowl condensate level. | Static pressure and bowl state |
| Weekly | Check stroke-time trends for all cylinders. | Any cylinder more than 15% over baseline |
| Monthly | Inspect and replace exhaust silencers on CP-01 CYL2 and PL-01 CYL4. | Silencers replaced |
| Monthly | Leak-down test and idle flow reading on each machine. | Leak-down time and idle flow |
| Quarterly | Replace filter elements and test automatic drains. | Element date and drain function |
| Quarterly | Inspect hoses, fittings, sensor positions, and paint marks. | Damaged items and moved sensors |

### Service Filter-Regulators and Drains

Check the filter bowl daily and the element pressure drop weekly. An element that loads quickly points to oil or dust carryover from the header, which should be reported to the compressor house.

**SAFETY:** Lock out the machine, close and lock the shut-off valve, and confirm 0 bar before opening a filter bowl; a pressurized bowl can blow off when unlocked. Replace the element, clean the bowl, and check that the automatic drain float moves freely. Confirm the regulator holds 5.5 bar after air is restored and that its lock ring is engaged.

### Replace Exhaust Silencers

Paper dust clogs sintered silencers on the busiest valves within a few months. A clogged silencer slows the stroke in one direction.

**SAFETY:** Lock out the machine, close and lock the shut-off valve, and confirm 0 bar before removing silencers. Replace them with new ones rather than blowing them out, which pushes dust deeper into the sinter. After replacement, check that stroke times return to baseline without changing the flow control settings.

### Set Position Sensors

A position sensor must switch reliably at the end of stroke even with cushion bounce, so it is set slightly past the point where it first switches.

**SAFETY:** Lock out the machine, close and lock the shut-off valve, support any load, and exhaust the cylinder before moving its piston by hand. With the piston at the end of stroke, slide the sensor until its LED comes on, then move it a further 2 mm toward the end position. Tighten the clamp screw by hand; over-tightening cracks the sensor housing. Paint-mark the sensor position on the cylinder profile.

### Check Hoses, Fittings, and Leak-Down

Monthly idle-flow and leak-down readings show leaks building up before they cause slow strokes or low-pressure alarms.

**SAFETY:** Run the leak-down test with the machine idle and the guards closed. Close the shut-off valve and time the pressure fall from 5.5 to 4.5 bar. Then lock out the machine, close and lock the shut-off valve, and confirm 0 bar before inspecting hoses and fittings inside the guarding. Look for rub marks at guard hinges and moving parts, and check that every hose is fully inserted in its push-in fitting.
