---
document_id: inc-conv-0001
title: CV-03 Belt Mistracking After Belt Replacement
document_type: incident_report
equipment_type: conveyor
machine_id: CV-03
alarm_code: CONV-2004
occurred_on: 2026-02-16
version: "1.0.0"
license: synthetic
---

# CV-03 Belt Mistracking After Belt Replacement

CV-03 had a new belt fitted by the belt contractor over the weekend and returned to production on the Monday morning shift.

## Symptoms

From 06:10 the belt kept wandering toward the operator side. The HMI logged six `CONV-2003` warnings in the first hour, all from the operator-side switch, and the crew acknowledged each one. At 10:12 the conveyor stopped on `CONV-2004`. The belt edge sat 48 mm off centre at the tail pulley and 31 mm at the drive pulley, with black rubber dust on the operator-side frame. Sheets had been reaching the CP-01 feeder about 20 mm off centre since start-up.

## Diagnosis

Belt speed and motor current were normal for the whole shift, at 0.60 m/s and 4.2 A, so the conveyor was not slipping or overloaded. The wander was worst at the tail pulley and started immediately after the belt change, which pointed to the tail pulley rather than the load.

Before the stop, the crew had turned the return-side training idler to steer the belt back. It **did not help**: the belt moved toward centre for about 15 minutes, then drifted back once heavy double-wall stacks arrived.

With CV-03 locked out, maintenance read the take-up scales: 52 mm on the operator side and 46 mm on the drive side. The shaft centre distance from tail pulley to drive pulley differed by 6 mm between the two sides. Pulley faces and return idlers were clean, and the new splice was square.

## Root Cause

The take-up screws had been tensioned unevenly when the new belt was installed, leaving the tail pulley **6 mm out of square**. The training idler adjustment had only masked the problem at light load.

## Resolution

**SAFETY:** CV-03 was locked out, zero energy was verified, and the tail pulley was blocked before the take-up screws were turned. Maintenance set both screws to 49 mm in 3 mm steps until the centre distances agreed within 1 mm, and returned the training idler to its scribe marks. The belt ran empty at 0.20 m/s for two full revolutions, then loaded at 0.60 m/s. The edge stayed within ±6 mm for the rest of the shift with no further `CONV-2003` warnings. The belt contractor's handover checklist now includes recording both take-up positions.
