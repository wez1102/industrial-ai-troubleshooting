---
document_id: inc-servo-0005
title: PL-01 Hoist Motor Overtemperature From Brake Drag
document_type: incident_report
equipment_type: servo_drive
machine_id: PL-01
alarm_code: SERVO-7025
occurred_on: 2026-07-15
version: "1.0.0"
license: synthetic
---

# PL-01 Hoist Motor Overtemperature From Brake Drag

PL-01 Axis 2, the layer hoist, is the palletizer's only vertical load-bearing axis and has a holding brake.

## Symptoms

At 16:02 the hoist stopped between layers and the HMI showed `SERVO-7025` Motor Overtemperature. The winding estimate had reached **84 °C**, above the 82 °C alarm point. The drive heat sink read 51 °C and the cabinet inlet 26 °C, both normal. Continuous current had risen to **5.6 A** over the afternoon, against a typical 3.9 A for the same layer pattern. Operators heard a faint scraping sound from the hoist motor on every move.

## Diagnosis

This was the reverse of the April cabinet case: a hot motor with a cool drive. The current trend showed the increase on both up and down moves. A heavier load would raise current mainly when lifting, so an equal rise in both directions pointed to drag.

The first assumption was overloaded layers. The crew lightened the layer pattern and slowed the cycle by 15%. It **did not help**: the winding temperature kept rising at the same rate.

With the carriage supported and the axis locked out, the brake housing measured 71 °C, much warmer than the motor end shield. The electrical technician found a loose terminal on the brake supply, and the trace showed only **19.8 V** at the brake during moves against the nominal 24 V.

## Root Cause

A **loose brake supply terminal** dropped the release voltage, so the holding brake only partly released and dragged on every move. The extra friction raised motor current and heated the winding.

## Resolution

**SAFETY:** The hoist carriage was lowered onto its mechanical rest stops and independently supported, and Axis 2 was locked out with zero energy verified, before the brake terminal was handled. The electrical technician re-terminated the brake supply and tightened the terminal to the drawing value; release voltage measured 24.1 V. A qualified team then assessed the brake against the axis brake specification and recorded the result. After restart, current returned to 3.9–4.1 A, and the winding settled at 64 °C after two hours. The scraping sound was gone.
