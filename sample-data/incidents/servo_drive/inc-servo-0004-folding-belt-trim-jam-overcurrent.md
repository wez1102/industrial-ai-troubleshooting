---
document_id: inc-servo-0004
title: CP-01 Axis 3 Overcurrent From Trim Jam In Folding Belt
document_type: incident_report
equipment_type: servo_drive
machine_id: CP-01
alarm_code: SERVO-7023
occurred_on: 2026-06-02
version: "1.0.0"
license: synthetic
---

# CP-01 Axis 3 Overcurrent From Trim Jam In Folding Belt

CP-01 was running a die-cut order with heavy trim waste from the Axis 2 die-cut section.

## Symptoms

At 11:37 the left folding-belt trim axis stopped hard. The HMI showed `SERVO-7023` Power Stage Overcurrent with a **13.7 A** current spike, against about 4.5 A on the same recipe the day before. Axis 3 speed had been falling for the last 0.5 s before the trip while current climbed. Motor temperature was 46 °C. An operator reset the alarm and restarted, and the axis tripped again within 20 seconds at 13.1 A.

## Diagnosis

Current rising while speed fell is the pattern of a mechanical load, not a sudden electrical fault. The second trip at almost the same current confirmed that the cause was still there; the restart **did not help** and added a second high-current event on an unexplained load.

The mechanical specialist found a strip of die-cut trim, about 300 mm long, wedged between the left folding belt and its guide rail at the pulley entry. The belt surface was scored but not cut through. The electrical technician checked the Axis 3 motor cable and connections and found no damage.

## Root Cause

**Trim waste jammed the left folding belt.** The trim had escaped the waste-removal path because the stripping brush after the die-cut section was worn down and no longer pushed waste clear.

## Resolution

**SAFETY:** CP-01 was locked out, zero energy was verified, and the folding-belt tension was released and the belt section blocked before the trim was removed. Maintenance pulled out the trim, inspected the belt, and replaced the worn stripping brush. After restart, Axis 3 current held at 4.4–4.6 A over the next hour. The shift supervisor added a site rule: after a `SERVO-7023`, the axis is not restarted a second time until maintenance has inspected it.
