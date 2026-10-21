---
document_id: photoelectric-manual-v1
title: PE-40 Photoelectric Sensor Manual
document_type: manual
equipment_type: photoelectric_sensor
manufacturer: "North Quay Training (fictional)"
model: PE-40
version: "1.0.0"
license: synthetic
---

# PE-40 Photoelectric Sensor Manual

The PE-40 is the photoelectric sensor family used for sheet, box, and bundle detection on CV-03, CP-01, and PL-01. This manual covers the installed sensing modes, indicators, sensor alarms, fault isolation, cleaning, alignment, and teach-in. It does not replace qualified maintenance personnel or plant lockout/tagout procedures.

## Operating Guide

A PE-40 sends a pulsed red light beam and switches its output when the received light crosses a threshold. Three sensing modes are installed. In **through-beam** mode, a separate emitter and receiver face each other and an object is detected when it interrupts the beam. In **polarized retroreflective** mode, the sensor and a corner-cube reflector face each other across the product path; a polarizing filter rejects light from shiny surfaces, so glossy or film-wrapped board is not mistaken for the reflector. In **diffuse with background suppression** mode, the sensor detects light reflected from the object itself and ignores anything beyond a taught cut-off distance, so detection depends on distance rather than on board colour.

PE-40 sensors run from the 24 V control supply, which stays on when machine motion is locked out, so indicators can be read and sensors taught with the machine locked out. PE-40 sensors are process sensors only. They are not safety devices and are never used to protect people; guard and access monitoring is covered in the safety circuit manual.

| Sensor | Location | Mode | Range or Cut-Off | Purpose |
| --- | --- | --- | --- | --- |
| CV-03 PE1 | CV-03 discharge, across the belt | Polarized retroreflective, 80 mm reflector | 2.0 m to reflector | Sheet count and CONV-2008 jam timer |
| CP-01 PE2 | CP-01 feeder gate, looking down | Diffuse, background suppression | Cut-off 15 mm above feed table | Sheet present at the feeder |
| CP-01 PE3 | CP-01 folding section exit | Through-beam | 1.4 m emitter to receiver | Box count and registration check |
| PL-01 PE4 | PL-01 bundle infeed, side mounted | Diffuse, background suppression | Cut-off 600 mm | Bundle present before the turner |

Each PE-40 has two indicators. The **yellow output LED** is on when an object is detected. The **green stability LED** is steady when the received signal is clearly above or clearly below the switching threshold, and off when the signal sits in the uncertain band between them. A sensor that is switching with the green LED off is working without margin and will become unreliable as dust builds up.

The line controller reads each sensor's diagnostics over its IO-Link port: signal margin, ambient light warning, and supply voltage. **Signal margin** is the received signal divided by the switching threshold, measured in the light-received state: beam clear for through-beam and retroreflective sensors, object present for diffuse sensors. A margin of 1.0 is exactly at the threshold.

| Item | Normal Reference | Alarm Criterion |
| --- | --- | --- |
| Signal margin, through-beam (CP-01 PE3) | 20× or more when clean | PE-3003 below 1.5× for 10 s |
| Signal margin, retroreflective (CV-03 PE1) | 8–12× with a clean corner-cube reflector | PE-3003 below 1.5× for 10 s |
| Signal margin, diffuse (CP-01 PE2, PL-01 PE4) | 4× or more on the darkest board run | PE-3003 below 1.5× for 10 s |
| Stability LED | Steady green above 2.0× or below 0.5× | Off between 0.5× and 2.0× |
| Supply voltage | 23.0–25.0 V DC | PE-3007 below 20.4 V for 1 s |
| Output transitions per product | 2 (on, then off) | PE-3004 more than 4 within 50 ms |
| Response time | 0.5 ms | Controller input filter 3 ms |
| Operating temperature | −20 to 55 °C | None |

The controller cross-checks each sensor against the machine cycle. At points where the beam should be clear, such as the gap between sheets, it expects the sensor to report clear; at points where a product should be present, it expects a detection. Three wrong checks in a row raise PE-3001 or PE-3002. CV-03 PE1 and CP-01 PE3 together count sheets in and boxes out of CP-01, and PE-3009 compares the two counts.

Before changing a sensor setting after a fault, check the indicators and the HMI sensor page:

1. Note which sensor raised the alarm and what the yellow and green LEDs show with no product in front of it.
2. Read the present signal margin and compare it with the value in the sensor log.
3. Check for ambient light warnings and supply voltage alarms at the same time.
4. **SAFETY:** Lock out the machine before reaching into the product path to clean optics, check a bracket, or hold a test target.
5. Change the teach or alignment only after the cause is understood, and record the new margin.

## Alarm and Fault Codes

The alarm table lists the `PE-3xxx` codes for all PE-40 sensors. The HMI shows the sensor tag with each code. A machine-level alarm, such as CONV-2008 Product Jam on CV-03, can be caused by a sensor problem without any PE alarm appearing, so check the sensor page whenever a jam or missed-product alarm makes no physical sense.

| Code | Name | Severity | Description | Likely Causes | Action |
| --- | --- | --- | --- | --- | --- |
| PE-3001 | Blocked Sensor | MEDIUM | Sensor reports blocked at three consecutive expected-clear checks. | Stuck product; dirty optics; misalignment; ambient light; wrong teach. | Check for product, then LEDs and margin. |
| PE-3002 | Missed Detection | MEDIUM | Sensor reports clear at three consecutive expected-present checks. | Cut-off too short; dark or warped board; misaligned beam; emitter fault. | Compare margin on product; check teach and alignment. |
| PE-3003 | Low Signal Margin | LOW | Margin below 1.5× for 10 s in the light-received state. | Dust on lens or reflector; misalignment; wrong reflector; ageing emitter. | Clean optics; check alignment and reflector type. |
| PE-3004 | Output Chatter | MEDIUM | Output changes state more than 4 times within 50 ms. | Loose or vibrating bracket; flaps or warped edges; margin near threshold. | Inspect bracket; watch the output during product passage. |
| PE-3005 | Sensor Short Circuit | HIGH | Input card reports output short circuit or overload. | Chafed cable; water in connector; wiring fault. | Lock out; inspect cable route and connector. |
| PE-3006 | Sensor Not Detected | HIGH | No sensor current or IO-Link response for 500 ms. | Unplugged or broken cable; blown sensor supply fuse; failed sensor. | Check connector, cable, and supply before replacing the sensor. |
| PE-3007 | Supply Voltage Low | MEDIUM | Sensor supply below 20.4 V for 1 s. | Overloaded 24 V supply; loose terminal; voltage drop on long cable. | Measure supply at the sensor connector; refer to electrical team. |
| PE-3008 | Ambient Light Interference | LOW | Sensor reports received light that is not its own pulsed beam. | Low sun through a door or window; another sensor's beam; strobe lighting. | Identify the light source and its timing; shield or re-aim. |
| PE-3009 | Count Mismatch | MEDIUM | CV-03 PE1 and CP-01 PE3 counts differ by more than 2 per 100, excluding rejects. | Chatter double counts; products too close together; missed detections. | Compare both sensors' transition logs for the batch. |

## Troubleshooting

Sensor faults are often reported by a machine alarm first. Start with what the sensor is actually seeing: compare the LED states and the HMI sensor page with the product in front of it, and look at the margin trend over the last two weeks, not just the present value.

**SAFETY:** Lock out the machine before reaching into the product path, across a conveyor belt, or into the folding or palletizer area to clean, align, or test a sensor. A sensor that reports clear does not mean the area is clear of people or moving parts. Record the sensor tag, the alarm code, the board grade, the LED states, the signal margin, and any recent bracket, guard, or reflector work.

### Low Signal Margin

**What it means:** PE-3003 warns when the signal margin stays below 1.5× for 10 s in the light-received state. The sensor still switches correctly at this point, but it is close to the threshold. Below 2.0× the green stability LED goes off. Margin normally falls slowly as dust builds up; a sudden drop points to something that changed.

**Symptoms:** PE-3003 warnings repeat and are acknowledged, the green LED is off or flickers, and the sensor occasionally reports blocked or missed products. On CV-03 PE1, a false CONV-2008 jam is often the first visible effect. The margin trend shows a steady slide over days, or a step on a particular date.

**Likely causes:** In ranked order: (1) paper dust on the lens or reflector; (2) a bracket knocked or loosened so the beam no longer hits the reflector or receiver squarely; (3) the wrong reflector, such as reflective tape in place of a corner-cube reflector on a polarized sensor; (4) a scratched or fogged lens; (5) an ageing emitter.

**Checks:**

1. Read the margin trend. A slow slide points to dirt; a step on one date points to a bracket, reflector, or sensor change on that date.
2. Compare the present margin with the value recorded at the last alignment.
3. **SAFETY:** Lock out the machine before cleaning. Clean the lens and reflector with a dry lint-free cloth and read the margin again.
4. If margin stays low after cleaning, check the bracket for bends and loose fasteners, and confirm the beam spot is centred on the reflector or receiver.
5. For CV-03 PE1, confirm the reflector is the 80 mm corner-cube reflector. A polarized sensor returns very little signal from reflective tape.

**Corrective action:** Clean the optics, restore alignment, or fit the correct reflector, then record the new margin. A clean, aligned CV-03 PE1 returns 8–12×. Re-teaching a sensor to accept a weak signal only moves the threshold closer to the noise and is not a fix.

**When to escalate:** Escalate if the margin stays below 4× after cleaning and alignment, the lens is scratched or fogged inside, or the margin of a new sensor is far below the reference for its mode.

### Blocked Without Product

**What it means:** PE-3001 trips when a sensor reports blocked at three consecutive points where the controller expects it clear. The sensor is telling the controller that something is there. Either an object really is in the beam, or the sensor is receiving too little light, or too much in the case of a diffuse sensor.

**Symptoms:** The yellow LED stays on with nothing in front of the sensor. The machine stops on PE-3001 or on a machine alarm such as CONV-2008. Clearing the area and restarting works for a few minutes, then the stop returns. Sometimes the false blocks happen only at certain times of day.

**Likely causes:** In ranked order: (1) a scrap, trim strip, or label stuck in the beam path or on the reflector; (2) a dirty or misaligned retroreflective or through-beam sensor, which reads a weak beam as blocked; (3) a diffuse sensor seeing a new object inside its cut-off, such as a guard panel or bracket moved closer; (4) ambient light, especially low sun or another sensor's beam; (5) a teach done with an object in the beam.

**Checks:**

1. **SAFETY:** Lock out the machine, then look along the full beam path for trim, scrap, or tape.
2. Check the stability LED and margin with the path clear. A margin below 1.0× on a retroreflective or through-beam sensor means it cannot see its reflector or emitter.
3. For diffuse sensors, check that nothing new sits closer than the taught cut-off.
4. Check the alarm times against the time of day and the PE-3008 history.
5. Ask whether anyone re-taught the sensor recently.

**Corrective action:** Remove the obstruction, clean and realign, or re-teach correctly as described in the maintenance procedure. Shield the sensor from a light source or move it away. Do not invert the output or bypass the sensor to keep running; the machine logic depends on it.

**When to escalate:** Escalate if the sensor stays blocked with a clean, aligned path and correct teach, or if two sensors interfere with each other and need relocating.

### Missed Detection

**What it means:** PE-3002 trips when a sensor reports clear at three consecutive points where the controller expects a product. The product went past without being seen. For diffuse sensors this usually means the product sat beyond the cut-off or returned too little light. For through-beam and retroreflective sensors it usually means the beam went around the product or through a gap.

**Symptoms:** The CP-01 feeder waits for a sheet that is already there, PL-01 waits for a bundle, or the counts drift and PE-3009 follows. Misses often start with a particular order: dark or heavily printed board, warped sheets, thinner board, or a new bundle height.

**Likely causes:** In ranked order: (1) a diffuse cut-off taught in the wrong place, too close to the product surface; (2) warped board lifting or dropping outside the sensing zone; (3) very dark, matte, or angled glossy surfaces returning less light; (4) a beam aimed through the gap between products or under a raised flap; (5) a failing emitter.

**Checks:**

1. Note the board grade, colour, and thickness of the order where misses started.
2. With a product held in position and the machine locked out, check whether the yellow LED comes on and the green LED is steady.
3. Read the margin with the darkest board in the order; diffuse sensors need 4× or more.
4. Check the sensor log for the last teach date and what it was taught on.
5. Confirm the beam spot hits the product at its centre height, not near an edge or flap.

**Corrective action:** Re-teach background-suppression sensors on the background, not on the product, so the cut-off sits 15 mm in front of the background. Adjust the beam height to the centre of the product. Record the margin on the darkest board. Do not lower the threshold until the background starts to switch the sensor.

**When to escalate:** Escalate if the margin on product stays below 2× after a correct teach, or if the product geometry needs a different sensing mode.

### Output Chatter

**What it means:** PE-3004 trips when the output changes state more than four times within 50 ms. A clean detection produces two transitions per product. Chatter makes one product look like several and inflates counts, which leads to PE-3009 Count Mismatch.

**Symptoms:** Counts at CP-01 PE3 run higher than sheets fed. The yellow LED flickers as each product passes. Chatter gets worse at higher line speeds or after the machine has been running a while.

**Likely causes:** In ranked order: (1) a loose or vibrating bracket; (2) box flaps, die-cut edges, or warped corners crossing the beam edge; (3) a margin sitting near the threshold so small changes cross it; (4) products too close together, with gaps narrower than the beam spot; (5) electrical noise on the sensor cable.

**Checks:**

1. Compare the count on CV-03 PE1 with CP-01 PE3 for the same batch.
2. **SAFETY:** Lock out the machine, then check the bracket for loose fasteners and test whether it moves by hand.
3. Check where the beam crosses the product. A beam at flap height sees every flap edge.
4. Read the margin with the path clear; a low margin makes chatter more likely.
5. Check that the sensor cable is routed away from motor power cables.

**Corrective action:** Tighten or stiffen the bracket, move the beam to the solid body of the product, and restore a healthy margin. Do not lengthen the controller input filter to hide chatter; a longer filter can also merge two real products.

**When to escalate:** Escalate if chatter continues with a rigid bracket and a clean beam path, or if product spacing is too tight for single-product detection.

## Maintenance Procedure

The preventive schedule below covers optics cleaning, alignment and signal margin, brackets and cables, and sensor replacement. Record the sensor tag, the margin before and after the work, and the technician.

**SAFETY:** Lock out the machine before reaching into a product path or across a belt to work on a sensor or reflector. Treat every sensor as a process signal only; never use a sensor indicator as evidence that an area is safe to enter.

| Frequency | Preventive Task | Record To Keep |
| --- | --- | --- |
| Weekly | Clean lenses and reflectors on CV-03 PE1 and CP-01 PE2. | Margin before and after cleaning |
| Monthly | Clean CP-01 PE3 and PL-01 PE4 optics. | Margin before and after cleaning |
| Monthly | Review the margin trend for every sensor. | Lowest margin and any step changes |
| Quarterly | Check brackets, fasteners, and cable routing. | Loose or damaged items found |
| After any sensor or reflector change | Teach and record the new margin. | Teach target, date, and margin |

### Clean Lenses and Reflectors

Paper dust settles on lenses and reflectors faster near the CV-03 discharge and the CP-01 feeder than anywhere else on the line.

**SAFETY:** Lock out the machine before cleaning. Wipe the lens and reflector with a dry lint-free cloth. Use a cloth slightly dampened with water for starch film; do not use solvents, which fog the lens. Read the margin before and after cleaning. A margin that does not recover after cleaning points to alignment or a damaged reflector.

### Check Alignment and Signal Margin

Alignment is correct when the beam spot sits in the centre of the reflector or receiver, not just when the sensor switches. Move the sensor slowly in each direction until the margin starts to drop, then set it halfway between the two edges.

**SAFETY:** Lock out the machine before adjusting brackets inside the product path. Compare the margin with the reference for the sensing mode. Record the final margin and mark the bracket position with paint so a knocked bracket is easy to spot.

### Inspect Brackets and Cables

Brackets near product paths get hit by warped sheets and falling scrap. A bent bracket changes alignment, and a loose one causes chatter.

**SAFETY:** Lock out the machine before handling brackets or cables. Check fasteners, paint marks, and whether the bracket moves by hand. Follow each cable to the junction box and look for chafing at guard hinges, sharp edges, and moving parts. Replace damaged cables rather than taping them.

### Teach a Replacement Sensor

A replacement PE-40 must be taught before use. Teach on the background, not on the product, so the result does not depend on the board being run.

**SAFETY:** Lock out the machine before mounting the sensor and placing teach targets. Then teach as follows. For through-beam and retroreflective sensors, clear the beam path and hold the teach button for 3 s until the yellow LED flashes. For background-suppression sensors, leave only the background in view, such as the feed table or the far guide rail, and hold the teach button for 3 s; the sensor sets its cut-off 15 mm in front of the background. Two green flashes confirm the teach. Fast yellow flashing means the margin is too low; clean and realign, then teach again. Record the margin with the darkest board expected.
