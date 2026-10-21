---
document_id: inc-pe-0005
title: CP-01 PE3 Short Circuit From Chafed Cable
document_type: incident_report
equipment_type: photoelectric_sensor
machine_id: CP-01
alarm_code: PE-3005
occurred_on: 2026-08-26
version: "1.0.0"
license: synthetic
---

# CP-01 PE3 Short Circuit From Chafed Cable

The CP-01 folding-section guard had been opened several times a shift that week for a run of glue-flap adjustments.

## Symptoms

At 10:52 CP-01 stopped and the HMI showed `PE-3005` Sensor Short Circuit on CP-01 PE3, followed by `PE-3006` Sensor Not Detected. Both indicators on the PE3 receiver were dark. Earlier that morning the box count had stopped for a second at a time on three occasions without an alarm.

## Diagnosis

The input card had switched off the PE3 channel to protect itself, which is why the sensor then disappeared. The earlier one-second dropouts suggested an intermittent fault before the hard short.

The first thought was a failed receiver, and the stores issued a new PE-40. Fitting it **did not help**: the new receiver tripped `PE-3005` as soon as the channel was reset.

With CP-01 locked out, maintenance followed the receiver cable from the sensor toward the junction box. Where it crossed the guard hinge, the jacket was worn through and the output conductor was rubbing on the hinge frame.

## Root Cause

The **receiver cable was chafed through at the guard hinge**. Each time the guard opened and closed, the hinge rubbed the cable, and it finally shorted the sensor output to the frame.

## Resolution

**SAFETY:** CP-01 was locked out and zero energy verified before the guard was opened and the cable handled. The damaged cable was replaced and rerouted through a protective sleeve away from the hinge, with a clamp on each side. The original receiver was refitted, tested, and kept; the new one went back to stores. After the channel was reset, PE3 showed its normal 22× margin and the count matched CV-03 PE1 for the rest of the shift.
