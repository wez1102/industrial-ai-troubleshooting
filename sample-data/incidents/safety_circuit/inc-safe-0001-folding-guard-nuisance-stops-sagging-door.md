---
document_id: inc-safe-0001
title: CP-01 Folding Guard Nuisance Stops From Sagging Door
document_type: incident_report
equipment_type: safety_circuit
machine_id: CP-01
alarm_code: SAFE-5001
occurred_on: 2026-03-10
version: "1.0.0"
license: synthetic
---

# CP-01 Folding Guard Nuisance Stops From Sagging Door

The CP-01 folding-section guard had been opened many times a shift for several weeks during glue-flap setup changes.

## Symptoms

From 09:30 CP-01 kept stopping with the folding guard closed. The HMI showed `SAFE-5001` Guard Circuit Not Satisfied on `CP-01 GS5`, the folding-section guard switch, eight times in two hours. Each stop happened while the machine was running at full folding speed, and the guard was shut every time the operators checked. A reset worked straight away, then the next stop came within 10 to 20 minutes.

## Diagnosis

Both channels of GS5 opened together on every stop, so the switch was seeing the actuator move away rather than a wiring fault on one channel. The stops only happened at full speed, which pointed to vibration moving the guard.

The night shift had replaced the GS5 switch, suspecting a failing switch. It **did not help**: the new switch dropped out the same way, and the safety technician had to pair it to the existing actuator.

With CP-01 and CV-03 locked out and zero energy verified, maintenance measured the actuator gap with the guard closed: **7 mm**, against the 2–3 mm setting. The guard door had dropped on its hinges, and the latch was holding it slightly open at the bottom. At 7 mm the actuator sat outside the 5 mm range where the switch is guaranteed to recognise it, so vibration was enough to make the switch drop out for an instant.

## Root Cause

Repeated opening had worn the hinge pins and let the **folding guard door sag**. The actuator sat too far from the switch, so normal machine vibration was enough to drop the guard circuit.

## Resolution

**SAFETY:** CP-01 and CV-03 were locked out and zero energy verified before the guard door was removed. Maintenance replaced the hinge pins, re-hung the door square, and adjusted the latch. The actuator gap measured 2 mm with the guard closed. The guard was then function-tested with CP-01 running empty: opening it stopped the machine, and the machine did not restart until the guard was closed and reset was pressed. The result was recorded in the safety test log. No further `SAFE-5001` nuisance stops occurred.
