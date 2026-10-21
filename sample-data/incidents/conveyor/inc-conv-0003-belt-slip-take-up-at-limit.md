---
document_id: inc-conv-0003
title: CV-03 Belt Slip With Take-Up At Its Limit
document_type: incident_report
equipment_type: conveyor
machine_id: CV-03
alarm_code: CONV-2002
occurred_on: 2026-07-29
version: "1.0.0"
license: synthetic
---

# CV-03 Belt Slip With Take-Up At Its Limit

The night shift was running heavy double-wall board on CV-03 for most of the shift.

## Symptoms

At 22:47 the belt hesitated every time a full stack landed on it, and the drive pulley squealed. The HMI logged `CONV-2001` Speed Deviation, followed about a second later by `CONV-2002` Belt Slip, which stopped the conveyor. The trend showed the drive pulley surface at 0.60 m/s while the belt dropped to 0.51 m/s, a 15% difference. Motor current only rose from 4.3 to 4.8 A. There was a smell of hot rubber at the discharge end.

## Diagnosis

The small current rise with a large speed loss meant the belt was slipping on the pulley rather than the motor being overloaded. The alarm history showed `CONV-2010` Take-Up Travel Limit had been acknowledged 37 times over the previous 16 days without a work order.

The first attempt was to take up the remaining travel: maintenance turned both screws from 141 mm to the 150 mm end stop. It **did not help** for long: slip came back within two hours on the next heavy stacks.

With CV-03 locked out, the drive pulley lagging grooves measured 0.5 mm deep in the centre of the face, against 4 mm when new, and the surface was glazed. The belt underside was clean and dry.

## Root Cause

The belt had **stretched beyond the take-up range**, so tension could no longer be restored, and the **worn, glazed lagging** gave too little grip to make up for it. The repeated `CONV-2010` acknowledgements had hidden the stretch for more than two weeks.

## Resolution

**SAFETY:** CV-03 was locked out, zero energy was verified, the tail pulley was blocked, and take-up tension was released before the belt was opened. The belt contractor removed 300 mm of belt and re-spliced it, and the drive pulley was re-lagged. Take-up was reset to 45 mm on both sides with centre distances within 1 mm. No slip occurred over the next three shifts of double-wall board. `CONV-2010` now raises a maintenance work order automatically instead of being acknowledged at the HMI.
