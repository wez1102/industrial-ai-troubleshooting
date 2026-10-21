---
document_id: inc-conv-0005
title: CV-03 Zero Speed From Sheared Drive Pulley Key
document_type: incident_report
equipment_type: conveyor
machine_id: CV-03
alarm_code: CONV-2009
occurred_on: 2026-09-03
version: "1.0.0"
license: synthetic
---

# CV-03 Zero Speed From Sheared Drive Pulley Key

The previous afternoon, a dropped bundle had landed across CV-03 and tripped `CONV-2006` Motor Overload before it was cleared.

## Symptoms

At 07:31 the motor was still running but the belt had stopped, and sheets were piling up at the infeed. The HMI showed `CONV-2009` Zero Speed Detected. Operators reported the motor humming normally and the gearbox output turning. At the moment of the alarm, motor current had dropped from 4.3 A to 1.9 A while the VFD still showed 44 Hz.

## Diagnosis

The first suspicion was the speed sensor, because a loose sensor is the most common cause of a false zero-speed alarm. A technician checked the sensor indicator, but it was correct: the tail pulley really was stationary. The current drop to 1.9 A, the motor's no-load current, showed that the motor was no longer driving anything.

With CV-03 locked out, maintenance found the gearbox hollow shaft turned freely on the drive pulley shaft. The key between them had sheared, and the keyway on the pulley shaft showed wear marks from earlier movement.

## Root Cause

The **drive pulley shaft key had sheared**. The key had been working loose in a slightly worn keyway for some time, and the shock load from the dropped bundle the previous day cracked it. It failed completely on the first start of the next shift.

## Resolution

**SAFETY:** CV-03 was locked out, zero energy was verified, and the belt was clamped to stop it moving while the gearbox was eased off the pulley shaft. Maintenance dressed the keyway, fitted a new key of the material and size on the drive drawing, and tightened the gearbox retaining bolts to the drawing torque. The belt ran empty and then loaded for 30 minutes with motor current back at 4.2–4.4 A and belt speed tracking the reference. Any future `CONV-2006` trip from an impact load now triggers an inspection of the drive pulley key before the next shift.
