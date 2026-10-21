---
document_id: inc-servo-0001
title: CP-01 Axis 4 Following Error After Maintenance
document_type: incident_report
equipment_type: servo_drive
machine_id: CP-01
alarm_code: SERVO-7021
occurred_on: 2026-03-14
version: "1.0.0"
license: synthetic
---

# CP-01 Axis 4 Following Error After Maintenance

At the start of the shift, CP-01 had returned from planned belt and guard maintenance.

## Symptoms

At 08:42 the right folder trim axis kept dropping out when the line sped up after yesterday's scheduled belt and guard work. CP-01 Axis 4 tripped `SERVO-7021` three times between 08:42 and 08:57. Following error peaked at **2.4 mm** against the **1.0 mm** plant limit during the **0.20 s** acceleration ramp. Motor temperature sat at **48 °C**, cabinet inlet was **27 °C**, and drive heat sink was **52 °C**. It tracked at steady speed but faulted during ramp-up.

## Diagnosis

We pulled the 20 ms trend and checked the first alarm instead of the final stop banner. Reference position rose smoothly, but encoder feedback had several sudden jumps; the last event showed a missing feedback update just before the following-error trip. The logged alarm was `SERVO-7021` on all three stops.

Guard work had disturbed the feedback cable the previous day; coupling and belt records did not explain the feedback gaps. Controls engineering tried restoring an earlier gain set; it **did not help**. The fault still occurred on acceleration.

## Root Cause

A technician found that the **Axis 4 encoder connector had been left partly unlatched after maintenance**. The plug could move slightly under vibration. It was not a hot motor, excessive product load, or weak tuning. The dropped samples had looked like poor tracking.

## Resolution

**SAFETY:** Lock out Axis 4, verify zero energy, and secure the mechanism before handling the encoder connector. Maintenance seated and latched the plug, checked the strain relief, and recorded the connector condition. The controls engineer restored the previous gain revision. A subsequent verification record showed **0.22 mm** peak following error on the same 0.20 s ramp and no recurring alarm during a **30 min** observation. The team closed the record with the loose connector as the confirmed cause.
