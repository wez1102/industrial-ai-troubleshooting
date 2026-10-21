---
document_id: inc-pneu-0004
title: PL-01 Excessive Air Consumption From Hidden Leaks
document_type: incident_report
equipment_type: pneumatic_cylinder
machine_id: PL-01
alarm_code: PNEU-4007
occurred_on: 2026-08-19
version: "1.0.0"
license: synthetic
---

# PL-01 Excessive Air Consumption From Hidden Leaks

PL-01 had been running normally, but the energy report showed its air use rising month on month.

## Symptoms

At the 06:00 shift start, with PL-01 idle, the HMI logged `PNEU-4007` Excessive Air Consumption. Idle flow read **135 Nl/min** against a baseline of about 35 Nl/min. The monthly leak-down test took 2 minutes to fall from 5.5 to 4.5 bar, compared with 12 minutes in the spring. The bundle stop gate, PL-01 CYL3, had started drifting slightly open during long stops. No hiss could be heard over the plant noise.

## Diagnosis

Idle flow nearly four times baseline meant large leaks, not a single pinhole. The first check was a soapy-water test on the fittings that could be reached from outside the guarding. It **did not help**: no bubbles were found on any of them.

An ultrasonic leak detector was then used with the machine idle and pressurized, from outside the guarding. It picked up three sources: a cracked push-in elbow on the CYL4 clamp manifold, a hose rubbed through where it crossed the bundle turner frame, and air flowing steadily from the CYL3 valve's silencer with the valve at rest.

## Root Cause

Three **hidden leaks** together were wasting about 100 Nl/min: a cracked fitting, a hose worn through on a frame edge, and a worn seal in the CYL3 valve. The worn valve seal also let air reach the wrong side of CYL3, which is why the bundle stop drifted.

## Resolution

**SAFETY:** PL-01 was locked out, the pneumatic shut-off valve was closed and locked, 0 bar was confirmed, and the bundle stop gate was blocked before the fittings, hose, and valve were replaced. The cracked elbow and the worn hose were replaced, and the hose was rerouted through a protective sleeve. The CYL3 valve was exchanged. Idle flow fell to 38 Nl/min and leak-down time rose to 14 minutes. CYL3 no longer drifted during stops.
