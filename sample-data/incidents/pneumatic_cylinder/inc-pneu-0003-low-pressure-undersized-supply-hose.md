---
document_id: inc-pneu-0003
title: CP-01 Low Supply Pressure From Undersized Replacement Hose
document_type: incident_report
equipment_type: pneumatic_cylinder
machine_id: CP-01
alarm_code: PNEU-4004
occurred_on: 2026-07-08
version: "1.0.0"
license: synthetic
---

# CP-01 Low Supply Pressure From Undersized Replacement Hose

A forklift had damaged the CP-01 air supply hose on the night shift, and it was replaced before the morning shift started.

## Symptoms

From 07:15 CP-01 kept stopping on `PNEU-4004` Low Supply Pressure, always during a counter-ejector bundle push. The machine pressure trend dipped from 5.5 to 4.6 bar every time CP-01 CYL2 extended, then recovered within a second. The feeder gate and other cylinders also logged occasional timeouts. Static pressure at rest was normal.

## Diagnosis

The header gauge before the shut-off valve read 6.5 bar throughout, so the compressor house was delivering. Static pressure was normal and the dips only came with flow, which pointed to a restriction between the header and the regulator. The filter pressure drop was 0.2 bar and there was no `PNEU-4009` alarm, so the filter element was not the restriction.

The first fix tried was raising the regulator from 5.5 to 6.0 bar. It **did not help**: static pressure rose, but the pressure still dipped to 4.7 bar on each push and the alarm continued.

With CP-01 locked out, the shut-off valve closed and locked, and 0 bar confirmed, maintenance followed the supply line from the shut-off valve. The 2 m section replaced overnight was 8 mm bore hose with 8 mm push-in fittings, instead of the specified 12 mm.

## Root Cause

The **replacement supply hose was too small**. An 8 mm bore could hold static pressure but could not deliver the flow CYL2 needs during a bundle push, so machine pressure collapsed on every stroke.

## Resolution

**SAFETY:** CP-01 was locked out, the pneumatic shut-off valve was closed and locked, and 0 bar was confirmed before the hose was removed. The 8 mm section was replaced with 12 mm bore hose and fittings and clamped clear of the forklift aisle. The regulator was returned to 5.5 bar. During bundle pushes the pressure now dipped only to 5.2 bar, and no further `PNEU-4004` alarms were logged. Spare 12 mm supply hose is now kept at the machine.
