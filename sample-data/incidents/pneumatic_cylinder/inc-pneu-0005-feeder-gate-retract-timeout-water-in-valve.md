---
document_id: inc-pneu-0005
title: CP-01 CYL1 Retract Timeout From Water In Valve Manifold
document_type: incident_report
equipment_type: pneumatic_cylinder
machine_id: CP-01
alarm_code: PNEU-4002
occurred_on: 2026-09-14
version: "1.0.0"
license: synthetic
---

# CP-01 CYL1 Retract Timeout From Water In Valve Manifold

CP-01 had been stopped over a warm, humid weekend and started up on Monday morning.

## Symptoms

At 06:20 CP-01 stopped with the feeder gate stuck up. The HMI showed `PNEU-4002` Cylinder Retract Timeout on CP-01 CYL1. The valve coil LED was lit, so the retract command was reaching the valve, but the cylinder did not move. After a few seconds it sometimes lowered sluggishly. The filter bowl on the CP-01 filter-regulator was more than half full of water, and the HMI also showed `PNEU-4010` Condensate Level High.

## Diagnosis

A lit coil LED with no movement meant the coil was energized but the valve spool was not shifting. Machine pressure was normal at 5.5 bar.

The night shift had assumed an electrical fault and replaced the CYL1 valve coil. It **did not help**: the new coil also lit and the gate still stuck, because the coil had never been the problem.

With CP-01 locked out, the shut-off valve closed and locked, 0 bar confirmed, and the feeder gate blocked in its raised position, maintenance opened the CYL1 valve. There was water and a milky residue around the spool. The automatic drain in the filter bowl was jammed with debris, so condensate from the humid weekend had collected in the bowl, overflowed past the filter, and reached the valve manifold.

## Root Cause

A **stuck automatic condensate drain** let water pass into the valve manifold. The wet residue made the CYL1 valve spool stick, so the valve did not shift when its coil was energized.

## Resolution

**SAFETY:** CP-01 was locked out, the pneumatic shut-off valve was closed and locked, 0 bar was confirmed, and the feeder gate was blocked in its raised position before the trapped air was released and the valve was removed. The bowl was drained and cleaned, the automatic drain was replaced, and the filter element was renewed. The CYL1 valve was exchanged, and the other valves on the manifold were inspected and found dry. After restart, CYL1 stroked in 0.25 s each way. The daily bowl check now includes pressing the drain's manual button to confirm it releases.
