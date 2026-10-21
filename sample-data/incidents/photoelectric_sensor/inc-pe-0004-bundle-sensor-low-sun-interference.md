---
document_id: inc-pe-0004
title: PL-01 PE4 False Bundle Detection From Low Sun
document_type: incident_report
equipment_type: photoelectric_sensor
machine_id: PL-01
alarm_code: PE-3008
occurred_on: 2026-09-29
version: "1.0.0"
license: synthetic
---

# PL-01 PE4 False Bundle Detection From Low Sun

The shipping dock door beside PL-01 had been left open on warm afternoons to cool the area.

## Symptoms

For a week, PL-01 stopped in the late afternoon with the bundle infeed empty. The HMI logged `PE-3001` Blocked Sensor on PL-01 PE4 together with `PE-3008` Ambient Light Interference. All the stops happened between 16:10 and 16:55. Mornings and night shift had none. The PE4 yellow LED flickered on with no bundle in front of the sensor.

## Diagnosis

The timing pointed to light, not dirt. Margin with a bundle present was normal at 6×, and the lens was clean. At 16:30 a technician watched from outside the guarding and saw low sun coming through the open dock door and shining across the infeed directly into the PE4 lens.

The first response had been to re-teach PE4 on the afternoon of the second stop. It **did not help**: the teach was correct, and the next afternoon's stops happened at the same times.

## Root Cause

In late September, the **low afternoon sun** came through the open dock door at an angle that reached the PE4 lens. The sensor received light that was not its own pulsed beam, reported ambient light interference, and occasionally switched as if a bundle were present.

## Resolution

**SAFETY:** PL-01 was locked out and zero energy verified before maintenance worked at the bundle infeed. A sun hood was fitted over PE4, and the sensor was turned 10° downward and re-taught so its cut-off stayed 15 mm in front of the far guide rail. The dock door now stays closed while PL-01 runs. Over the next two weeks of afternoons, no `PE-3008` or `PE-3001` alarms were logged on PE4.
