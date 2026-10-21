---
document_id: inc-safe-0005
title: PL-01 Dump Valve Feedback Fault From Clogged Exhaust Silencer
document_type: incident_report
equipment_type: safety_circuit
machine_id: PL-01
alarm_code: SAFE-5007
occurred_on: 2026-10-06
version: "1.0.0"
license: synthetic
---

# PL-01 Dump Valve Feedback Fault From Clogged Exhaust Silencer

The quarterly stop feedback test on PL-01 in July had recorded a dump valve exhaust time of 2.6 s, inside the 3 s limit but above the 2.0 s replacement point.

## Symptoms

At 10:44 an operator pressed an emergency stop on PL-01 when a bundle tipped on the infeed. The cell stopped, but reset was refused and the HMI showed `SAFE-5007` Dump Valve Feedback Fault. Machine air had taken **4.8 s** to fall below 0.5 bar. Operators noticed the layer clamps still holding for several seconds after the stop.

## Diagnosis

The fault meant air was leaving PL-01 too slowly after a stop, so cylinders could hold pressure or move for longer than intended. The pressure trend showed a smooth but slow fall, which pointed to a restriction on the exhaust rather than a stuck valve.

The July test result had been recorded but no work order raised. The first response on the day was to press the emergency stop again and retest. It **did not help**: the exhaust took 4.9 s the second time, and the fault latched again.

With PL-01 locked out, the pneumatic shut-off valve closed and locked, 0 bar confirmed, and the layer clamps supported, maintenance removed the dump valve's exhaust silencer. It was packed with grey paper dust, the same build-up seen on the CYL4 valve silencers.

## Root Cause

**Paper dust had clogged the dump valve exhaust silencer**, slowing the release of machine air after a stop until it exceeded the 3 s limit. The rising exhaust time had been visible in the July test but not acted on.

## Resolution

**SAFETY:** PL-01 was locked out, the pneumatic shut-off valve was closed and locked, 0 bar was confirmed, and the layer clamps were supported before the silencer was removed. The silencer was replaced and the dump valve was inspected and found to operate freely. The stop feedback was then function-tested: an emergency stop dropped machine air below 0.5 bar in 1.2 s, the controller confirmed it, and PL-01 did not restart until reset was pressed. The result was recorded in the safety test log. An exhaust time above 2.0 s in the quarterly test now raises a work order automatically.
