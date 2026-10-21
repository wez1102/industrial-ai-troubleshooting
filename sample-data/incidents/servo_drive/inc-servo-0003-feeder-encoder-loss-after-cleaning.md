---
document_id: inc-servo-0003
title: CP-01 Axis 1 Feeder Encoder Feedback Loss After Cleaning
document_type: incident_report
equipment_type: servo_drive
machine_id: CP-01
alarm_code: SERVO-7022
occurred_on: 2026-05-04
version: "1.0.0"
license: synthetic
---

# CP-01 Axis 1 Feeder Encoder Feedback Loss After Cleaning

CP-01 had a weekend deep clean of the feeder section, including removal and refitting of the cable tray cover beside Axis 1.

## Symptoms

At 06:15 on the Monday start-up the feeder stopped mid-index, and operators called it a jam. No board was stuck. The HMI showed `SERVO-7022` Encoder Feedback Loss first, then `SERVO-7021` Following Error 40 ms later. Axis 1 position froze at **168.3 mm** while the command kept moving to 171.9 mm. The axis faulted four times in 50 minutes, and the stops seemed to happen more often when the feeder side guard was opened and closed.

## Diagnosis

The alarm order mattered: `SERVO-7022` came first, so the following error was a consequence of lost feedback rather than mechanical lag. The 20 ms trace showed three consecutive missing encoder updates before each stop. The feeder turned freely with the axis locked out, and motor current was normal up to each fault.

After the CP-01 Axis 4 connector incident in March, the crew checked the Axis 1 encoder connector first. It was fully latched. Re-seating it anyway **did not help**; the next fault came 12 minutes later.

Following the cable back from the motor, maintenance found it pinched where it left the cable tray. The refitted tray cover was pressing on the cable at the bend, flattening the jacket and exposing the braided shield.

## Root Cause

The **feedback cable had been crushed by the tray cover** when it was refitted after cleaning. The damaged conductors lost contact intermittently under vibration and when the side guard moved the tray.

## Resolution

**SAFETY:** Axis 1 was locked out, zero energy was verified, and the feeder mechanism was secured before the cable was handled. Maintenance replaced the feedback cable with the part listed in the axis maintenance record, routed it clear of the tray cover edge, and fixed it in the strain-relief clamp. Controls engineering re-referenced Axis 1 and confirmed its home position. Over the next two shifts the trace showed no missing encoder updates. The cleaning checklist now includes checking cable routing before tray covers are refitted.
