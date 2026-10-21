---
document_id: conveyor-manual-v1
title: IC-600 Infeed Conveyor Manual
document_type: manual
equipment_type: conveyor
manufacturer: "North Quay Training (fictional)"
model: IC-600
version: "1.0.0"
license: synthetic
---

# IC-600 Infeed Conveyor Manual

The IC-600 is the flat-belt infeed conveyor installed as CV-03. It carries individual corrugated sheets from the stacker transfer to the feeder section of CP-01. This manual covers operation, conveyor alarm identification, fault isolation, and preventive maintenance for the belt, drive, and speed monitoring. It does not replace qualified maintenance personnel or plant lockout/tagout procedures.

## Operating Guide

CV-03 is a horizontal flat-belt conveyor with 8.4 m between pulley centres and a 1,600 mm wide belt. A 3.0 kW four-pole induction gearmotor at the discharge end drives a 200 mm lagged drive pulley through a 22.4:1 helical-bevel gearbox. The 160 mm tail pulley at the infeed end sits in a screw take-up with 150 mm of travel. The two take-up screws set belt tension and also hold the tail pulley square to the frame. Return idlers carry the belt underneath, and a self-aligning training idler sits on the return run 1.2 m from the tail pulley. Its mounting brackets carry scribed reference marks.

A variable-frequency drive (VFD) in the CV-03 control cabinet supplies the motor. The VFD receives a speed reference from the line controller and reports output frequency, motor current, and DC-bus voltage. Belt speed is measured separately by an inductive proximity sensor that counts eight steel targets on the tail pulley face. The tail pulley is turned only by the belt, so its speed is the true belt speed; the motor speed shows only what the drive pulley is doing. Two-stage belt-edge switches on each side of the carrying run report belt wander. The discharge photo-eye detects sheets leaving CV-03; its own indicators and alignment are covered in the photoelectric sensor manual.

The motor is totally enclosed and fan cooled. Its cooling fan is mounted on the motor shaft, so cooling airflow falls when the motor runs slower. Running CV-03 at reduced speed for long periods does not reduce motor heating in proportion, and it can raise winding temperature when the conveyor stays heavily loaded.

| Item | Normal Reference | Alarm Criterion |
| --- | --- | --- |
| Belt speed | 0.20–0.80 m/s; 0.60 m/s nominal at about 44 Hz | CONV-2001 if measured speed differs from reference by more than 5% for 2 s |
| Drive-to-belt speed difference | Below 2% | CONV-2002 above 8% for 3 s |
| Belt edge position | Within ±10 mm of centre | CONV-2003 at 25 mm for 2 s; CONV-2004 at 45 mm |
| Motor current (rated 6.2 A) | 3.8–4.6 A loaded at 0.60 m/s | CONV-2006 above 6.8 A for 60 s; CONV-2007 above 12.4 A for 50 ms |
| Motor winding temperature | 60–95 °C | CONV-2005 at 140 °C for 5 s |
| Gearbox housing temperature | 40–70 °C | CONV-2012 at 85 °C for 60 s |
| VFD heat sink | 35–60 °C | Reported by the VFD status page; no CONV alarm |
| VFD DC bus | 540–590 V | CONV-2011 below 425 V for 100 ms |
| Take-up travel | 30–110 mm | CONV-2010 at 135 mm |
| Discharge photo-eye blocked time | Under 2.4 s per sheet at 0.60 m/s | CONV-2008 above 6.0 s at 0.30 m/s or faster |
| Speed-sensor pulses | About 9.5 pulses/s at 0.60 m/s | CONV-2009 if none for 1.5 s with the run command active |

CONV-2009 is inhibited for the first 3 s after a start and whenever the speed reference is below 0.10 m/s.

The start-up check after maintenance or a long stop is:

1. **SAFETY:** Confirm that every lock applied for the maintenance work has been removed by the person who applied it, that all guards are closed, and that no one is inside the conveyor guarding before the run command is given.
2. Review the CONV alarm list. Acknowledge only alarms whose cause is understood. An active CONV-2010 needs a work order, not repeated acknowledgement.
3. Start empty at 0.20 m/s and watch the belt edge at both pulleys for one full belt revolution, about 90 s at that speed.
4. Confirm that measured belt speed tracks the reference within 2% and that empty-belt current is 2.6–3.0 A.
5. Ramp to production speed and feed sheets centred on the belt. After belt or pulley work, record the edge position at both pulleys during the first hour.

During production at 0.60 m/s, motor current is typically 3.8–4.6 A, winding temperature 60–95 °C depending on ambient, gearbox housing 40–70 °C, and the belt edge within ±10 mm. Current and belt speed together point to the fault path. Current rising while belt speed falls points to load or drag. Normal current with falling belt speed points to slip. A sudden drop to about 1.9 A with the run command active is the motor's uncoupled no-load current: the motor is no longer driving the belt, because of a sheared key, a slipping coupling, or a broken belt.

## Alarm and Fault Codes

The alarm table lists the `CONV-2xxx` codes for CV-03. The earliest alarm is normally the best starting point. Some conditions raise a second alarm close behind the first: belt slip usually appears as CONV-2001 Speed Deviation about one second before CONV-2002 confirms it.

| Code | Name | Severity | Description | Likely Causes | Action |
| --- | --- | --- | --- | --- | --- |
| CONV-2001 | Conveyor Speed Deviation | MEDIUM | Measured belt speed differs from reference by more than 5% for 2 s. | Belt slip; heavy load; VFD current limit; speed-sensor gap. | Compare belt speed, current, and VFD frequency trends. |
| CONV-2002 | Belt Slip | HIGH | Drive pulley surface speed exceeds belt speed by more than 8% for 3 s. | Low tension; worn lagging; contaminated pulley; overload. | Stop feeding; check take-up and lagging under lockout. |
| CONV-2003 | Belt Mistracking Warning | MEDIUM | Belt edge reaches the 25 mm warning switch for 2 s. | Pulley out of square; build-up; off-centre feed; training idler moved. | Observe edge at both pulleys; plan a tracking check. |
| CONV-2004 | Belt Mistracking Trip | HIGH | Belt edge reaches the 45 mm trip switch. | Uncorrected wander; uneven take-up; damaged splice. | Lock out; inspect belt edge and frame contact. |
| CONV-2005 | Motor Overtemperature | HIGH | Winding temperature reaches 140 °C for 5 s. | Blocked fan cover; dirty fins; long low-speed running; overload. | Let the motor cool; inspect the cooling path under lockout. |
| CONV-2006 | Motor Overload | HIGH | Motor current above 6.8 A for 60 s. | Overfeeding; dragging bearing or idler; excess tension; gearbox fault. | Compare current with load; check rotating parts for drag. |
| CONV-2007 | Drive Overcurrent | CRITICAL | Motor current above 12.4 A for 50 ms. | Hard jam; seized gearbox; motor cable or winding fault. | Isolate; escalate to electrical and mechanical staff. |
| CONV-2008 | Product Jam | MEDIUM | Discharge photo-eye blocked for more than 6.0 s at 0.30 m/s or faster. | Sheet stuck at discharge; dirty or misaligned photo-eye; feeder stopped. | Check discharge area and photo-eye indicators. |
| CONV-2009 | Zero Speed Detected | HIGH | No speed-sensor pulse for 1.5 s with run command active. | Broken belt; sheared key or coupling; severe slip; sensor gap. | Compare motor current and belt movement before sensor checks. |
| CONV-2010 | Take-Up Travel Limit | MEDIUM | Tail pulley take-up reaches 135 mm of 150 mm travel. | Belt stretch; incorrect setting after belt work. | Raise a work order to re-tension or shorten the belt. |
| CONV-2011 | VFD DC Bus Undervoltage | MEDIUM | DC-bus voltage below 425 V for 100 ms. | Supply dip; loose supply terminal; input fuse fault. | Record the supply event; refer to the electrical team. |
| CONV-2012 | Gearbox Overtemperature | MEDIUM | Gearbox housing reaches 85 °C for 60 s. | Low oil level; overload; bearing wear; blocked airflow. | Check oil level cold; compare with motor current. |

## Troubleshooting

Troubleshooting starts with the alarm sequence and the trends for belt speed, motor current, and temperatures from the 10 minutes before the stop, not with repeated restarts.

**SAFETY:** Lock out CV-03 and verify zero energy before reaching into the guarding, touching the belt or pulleys, or removing the motor fan cover. A stopped belt can still move when a sheet stack rests on it or when take-up tension is released. Record the machine ID, the first CONV alarm, the speed reference, the board grade being run, and any recent belt, pulley, or drive work.

### Belt Mistracking

**What it means:** CONV-2003 warns when the belt edge reaches the 25 mm switch for 2 s. CONV-2004 stops the conveyor at 45 mm, before the belt edge reaches the frame. In normal running the edge stays within ±10 mm of centre. The warning does not stop production, so a run of acknowledged warnings is the earliest sign of a tracking problem.

**Symptoms:** The belt runs consistently to one side, often the same side at both pulleys. The edge rubs the frame and leaves black rubber dust. Sheets arrive at the CP-01 feeder off-centre. Wander that started right after a belt replacement or take-up adjustment points to pulley alignment. Wander that changes with board grade or stack position points to loading.

**Likely causes:** In ranked order: (1) tail pulley out of square after belt work or tension adjustment; (2) starch and paper-dust build-up on pulley faces or return idlers; (3) sheets fed off-centre; (4) training idler moved from its scribed position; (5) belt splice not square, or belt camber.

**Checks:**

1. Review the alarm history and count CONV-2003 warnings since the last belt or pulley work, noting which side reported them.
2. From outside the guarding, watch the edge at 0.20 m/s for a full belt revolution. Note whether the belt leaves the tail pulley off-centre or drifts along the carrying run.
3. **SAFETY:** Lock out CV-03 and verify zero energy. Record both take-up screw positions, then measure the shaft centre distance from tail pulley to drive pulley on each side. The two distances should agree within 2 mm.
4. **SAFETY:** Keep CV-03 locked out while inspecting pulley faces, return idlers, and the training idler for build-up, seized rollers, and movement away from the scribe marks.
5. Inspect the splice for squareness and the belt edges for fraying or cuts.

**Corrective action:** Square the tail pulley by equalising the take-up screws until the centre distances agree within 2 mm. Clean build-up from pulleys and idlers, and return the training idler to its scribe marks. Adjust in steps of no more than 3 mm and watch a full belt revolution after each step. Do not steer the belt with the training idler to hide a pulley that is out of square; the wander returns under load.

**When to escalate:** Escalate for edge damage, a cracked or out-of-square splice, frame contact damage, a bent shaft or moving bearing housing, or tracking that does not settle after the tail pulley is squared.

### Belt Slip

**What it means:** CONV-2002 trips when the drive pulley surface speed, calculated from motor speed, exceeds the measured belt speed by more than 8% for 3 s. CONV-2001 Speed Deviation normally appears about one second earlier. In normal running the difference stays below 2%.

**Symptoms:** The belt hesitates at start or when heavy double-wall stacks arrive. The drive pulley squeals and there is a smell of hot rubber. Sheets arrive late at the CP-01 feeder. Motor current stays normal or rises only slightly while belt speed drops; in an overload, current climbs instead.

**Likely causes:** In ranked order: (1) belt tension too low, usually because belt stretch has used up the take-up travel; (2) worn or glazed drive pulley lagging; (3) starch, moisture, or dust on the pulley face or belt underside; (4) a feed heavier than the conveyor normally carries; (5) an acceleration ramp too short for the load.

**Checks:**

1. Compare belt speed, VFD output frequency, and motor current at the moment of slip.
2. Check the CONV-2010 history and the present take-up position. Repeated acknowledgements without a work order point to belt stretch.
3. **SAFETY:** Lock out CV-03 and verify zero energy before touching the belt or drive pulley. Inspect the lagging grooves, which are 4 mm deep when new, for wear and glazing, and the belt underside for contamination.
4. Compare the take-up position with the value recorded at the last belt installation.
5. Confirm the acceleration ramp is 3.0 s from stop to 0.60 m/s.

**Corrective action:** Restore tension within the take-up range. If the take-up is already at or beyond 135 mm, the belt has to be shortened and re-spliced by the belt contractor. Re-lag the drive pulley when groove depth falls below 1 mm. Clean any contamination and remove its source. Do not over-tension the belt to compensate for worn lagging; excess tension overloads the pulley bearings and shafts.

**When to escalate:** Escalate if the take-up is at the end of its travel, lagging is loose or detached, the belt cover is burned, or slip returns after tension and lagging are corrected.

### Motor Overtemperature

**What it means:** CONV-2005 trips when the motor winding reaches 140 °C for 5 s. In normal running the winding stays between 60 and 95 °C. The VFD heat sink is measured separately in the control cabinet. A hot motor with a normal VFD heat sink points to the motor or its cooling, not to the drive.

**Symptoms:** CV-03 stops after a long run, often on hot afternoons. The motor frame is too hot to touch and smells hot. Winding temperature climbs steadily over one or two hours, and motor current may stay in its normal range.

**Likely causes:** In ranked order: (1) fan cover grille or cooling fins blocked by corrugated dust or trim; (2) long periods at reduced speed under load, which slows the shaft-mounted fan; (3) mechanical drag from a bearing, idler, or gearbox, which raises current; (4) ambient air near the motor above 40 °C; (5) supply imbalance or a winding fault.

**Checks:**

1. Compare winding temperature, motor current, belt speed, and ambient temperature over the hours before the trip. Normal current with rising temperature points to cooling.
2. Check how long CV-03 ran below 0.40 m/s before the trip.
3. **SAFETY:** Lock out CV-03, verify zero energy, and let the motor cool below 50 °C before removing the fan cover or touching the frame.
4. **SAFETY:** Keep the motor locked out while inspecting the grille, fan blades, and fins. Record the blocked area as a percentage.
5. If current was high, check gearbox oil level, drive pulley bearings, and return idlers for drag.

**Corrective action:** Clean the cooling path and remove the source of debris, such as a bent trim deflector or an open dust chute. Return CV-03 to normal speed rather than running slower to protect the motor. Correct any mechanical drag found. Never raise the CONV-2005 threshold or bypass the winding sensor.

**When to escalate:** Escalate for a burnt-insulation smell that persists after cooling, repeated trips after the cooling path is clean, phase currents that differ by more than 5%, bearing noise, or a discoloured terminal box.

### Product Jam

**What it means:** CONV-2008 trips when the discharge photo-eye stays blocked for more than 6.0 s with the belt at 0.30 m/s or faster. The longest sheet, 1,400 mm, passes the photo-eye in 2.4 s at 0.60 m/s and 4.7 s at 0.30 m/s. The alarm reports a blocked beam; it does not confirm that a sheet is physically stuck.

**Symptoms:** In a real jam, sheets pile up or skew at the discharge and the CP-01 feeder runs out of board. In a false jam, the belt is clear but the alarm repeats, and the photo-eye output indicator shows blocked with no sheet in front of it.

**Likely causes:** In ranked order: (1) a sheet caught on the discharge transfer plate or a side guide; (2) warped board lifting at the discharge; (3) a dirty photo-eye lens or reflector; (4) the photo-eye or reflector bracket knocked out of alignment; (5) the CP-01 feeder stopped while CV-03 kept running.

**Checks:**

1. From outside the guarding, check whether a sheet is actually present at the discharge.
2. Compare the photo-eye output and stability indicators with the photoelectric sensor manual.
3. **SAFETY:** Lock out CV-03 and the CP-01 feeder before reaching across the belt to clear sheets or clean optics.
4. Inspect the transfer plate edge and side guides for burrs, bent sections, or glue build-up.
5. Check the CP-01 feeder status at the time of the alarm.

**Corrective action:** Remove the stuck sheet and repair the transfer plate or guide that caught it. For a false jam, clean the lens and reflector and restore the bracket alignment. Do not lengthen the jam timer to hide false alarms; a longer timer also delays detection of a real jam.

**When to escalate:** Escalate if false jams continue after cleaning and alignment, the transfer plate is damaged, or the CV-03 and CP-01 feeder states disagree.

## Maintenance Procedure

The preventive schedule below covers belt tracking, tension, motor cooling, pulleys and idlers, and the gearbox. Record the completion date, readings, and technician for each task.

**SAFETY:** Lock out CV-03 and verify zero energy before any task that needs access inside the guarding. Release take-up tension only when the task requires it, and block the tail pulley before turning the take-up screws. Isolate the CP-01 feeder when working at the discharge end.

| Frequency | Preventive Task | Record To Keep |
| --- | --- | --- |
| Daily | Check belt edge position at both pulleys and listen for noisy idlers. | Edge offset in mm and any noisy roller position |
| Daily | Review the CONV alarm history. | Count of CONV-2003 and CONV-2010 acknowledgements |
| Weekly | Inspect the motor fan cover and fins for dust. | Blocked area percentage and cleaning date |
| Weekly | Clean the discharge photo-eye lens and reflector. | Stability indicator state after cleaning |
| Monthly | Record take-up position on both sides. | Left and right screw positions in mm |
| Monthly | Inspect drive pulley lagging and pulley faces. | Groove depth and build-up notes |
| Quarterly | Check gearbox oil level and housing for leaks. | Level reading and leak observations |
| Quarterly | Inspect return idlers and pulley bearings. | Seized or noisy roller positions; bearing temperature |
| Annual | Inspect the splice and the full belt length. | Splice condition, edge damage, cover wear |

### Inspect Belt Tracking and Edge Condition

Check tracking while the conveyor runs, from outside the guarding, before any locked-out inspection. Record the edge offset at the tail and drive pulleys and the side it favours. An offset that has grown since the last record matters more than a single reading.

**SAFETY:** Lock out CV-03 before touching the belt edge. Inspect both edges for fraying, cuts, and frame rub marks, and check that the training idler is still on its scribe marks. Clean starch and dust build-up from the return idlers that the belt edge passes over.

### Check Belt Tension and Take-Up

Read both take-up screw positions against the scale on the take-up frame. Both sides should match within 2 mm, and the travel should sit between 30 and 110 mm. A reading that rises month after month shows belt stretch and lets the replacement or re-splice be planned before CONV-2010 appears.

**SAFETY:** Lock out CV-03 and block the tail pulley before turning a take-up screw. Turn both screws by the same amount, no more than 3 mm per step, and recheck the shaft centre distances after adjustment.

### Clean Motor Fan Cover and Cooling Fins

Corrugated dust and edge trim collect on the fan cover grille and between the motor fins, especially near trim chutes. A partly blocked grille raises winding temperature long before CONV-2005 trips.

**SAFETY:** Lock out CV-03, verify zero energy, and let the motor cool below 50 °C before removing the fan cover. Brush or vacuum the grille, fan blades, and fins; do not blow dust into the motor terminal box. Record the blocked area before cleaning and check that the fan turns freely by hand with the motor locked out.

### Inspect Pulleys, Lagging, and Idlers

Measure drive pulley lagging groove depth at three points across the face; new lagging has 4 mm grooves. Note glazing, cracks, and any loose lagging edge. Check pulley faces and return idlers for build-up that changes the effective diameter and steers the belt.

**SAFETY:** Keep CV-03 locked out and the belt stationary while turning idlers by hand. Mark any roller that is seized, rough, or noisy, and replace it from the approved spares list. Compare pulley bearing housing temperatures recorded during running; a bearing more than 15 °C warmer than its neighbour needs investigation.

### Check Gearbox Oil Level

Check the oil level through the sight glass with the conveyor stopped and the gearbox cold, at least 2 hours after running. The level should sit at the centre of the sight glass. Look for oil on the housing, the output seal, and the floor beneath.

**SAFETY:** Lock out CV-03 before removing a fill plug. Top up only with the oil grade shown on the gearbox nameplate and record the quantity added. A gearbox that needs repeated top-ups has a leak that must be found and repaired.
