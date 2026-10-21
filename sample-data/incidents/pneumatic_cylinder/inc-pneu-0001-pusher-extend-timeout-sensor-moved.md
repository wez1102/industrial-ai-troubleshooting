---
document_id: inc-pneu-0001
title: CP-01 CYL2 Extend Timeout From Moved Position Sensor
document_type: incident_report
equipment_type: pneumatic_cylinder
machine_id: CP-01
alarm_code: PNEU-4001
occurred_on: 2026-02-24
version: "1.0.0"
license: synthetic
---

# CP-01 CYL2 Extend Timeout From Moved Position Sensor

The CP-01 counter-ejector had pushed out a collapsed bundle the previous evening, and part of it had caught on the pusher cylinder before it was cleared.

## Symptoms

From 06:40 the bundle pusher kept stopping the machine. Operators said the pusher went all the way out and then CP-01 faulted. The HMI showed `PNEU-4001` Cylinder Extend Timeout on CP-01 CYL2, seven times in the first two hours. Each time the rod was fully extended against its end stop, the valve coil LED was lit, and the extended sensor LED was off.

## Diagnosis

The cylinder was clearly reaching the end of its stroke, so the problem was the sensor not seeing it, not the cylinder failing to move. Machine pressure was normal at 5.5 bar static and 5.2 bar during the stroke.

Before maintenance arrived, the shift lead had turned the regulator up from 5.5 to 6.2 bar on the theory that the pusher was weak. It **did not help**: the timeouts continued, and `PNEU-4005` High Supply Pressure started appearing as well.

With CP-01 locked out, the shut-off valve closed and locked, and the cylinder exhausted, maintenance found the extended sensor 14 mm short of its paint mark. Its clamp screw was loose and the sensor body had a fresh scrape where the collapsed bundle had struck it.

## Root Cause

The collapsed bundle **knocked the extended position sensor along its slot**. The piston magnet no longer passed under it at the end of the stroke, so the sensor never switched and the controller timed out.

## Resolution

**SAFETY:** CP-01 was locked out, the pneumatic shut-off valve was closed and locked, 0 bar was confirmed, and CYL2 was exhausted before the sensor was handled. With the piston pushed to full extension by hand, the sensor was slid until its LED came on and then a further 2 mm, tightened by hand, and paint-marked. The regulator was returned to 5.5 bar and its lock ring engaged. A small deflector plate was fitted ahead of the sensor. CP-01 ran the rest of the week with no `PNEU-4001` alarms on CYL2.
