---
document_id: inc-safe-0003
title: CP-01 Feeder Emergency Stop Discrepancy From Loose Contact Block
document_type: incident_report
equipment_type: safety_circuit
machine_id: CP-01
alarm_code: SAFE-5003
occurred_on: 2026-04-28
version: "1.0.0"
license: synthetic
---

# CP-01 Feeder Emergency Stop Discrepancy From Loose Contact Block

An operator had pressed the feeder emergency stop on CP-01 to clear a sheet jam, and released it once the jam was cleared.

## Symptoms

At 14:12 CP-01 would not reset after the feeder emergency stop `CP-01 ES2` was released. The HMI showed `SAFE-5003` Channel Discrepancy on ES2, with channel A closed and channel B still open. The same alarm had appeared once the previous week and had cleared after the safety controller was power-cycled.

## Diagnosis

A latched discrepancy on one device meant one of its two channels was not following the button. The previous week's fault on the same button pointed to a recurring problem at ES2, not a controller fault.

The shift lead power-cycled the safety controller again. It **did not help**: the fault cleared, then returned the next time ES2 was pressed and released. Running on after the first power cycle had left the button relying on one working channel.

With CP-01 and CV-03 locked out and zero energy verified, an electrician opened the ES2 enclosure. The channel B contact block had partly unclipped from the button body, so its contacts did not close reliably when the button was released. The enclosure was mounted on the feeder frame, which vibrates heavily.

## Root Cause

**Vibration had loosened the channel B contact block** on the feeder emergency stop. Channel B no longer followed the button, so the safety controller saw the two channels disagree.

## Resolution

**SAFETY:** CP-01 and CV-03 were locked out and zero energy verified before the enclosure was opened. The electrician replaced both contact blocks on ES2 with the same type, clipped them fully home, and fitted the enclosure on anti-vibration mounts. ES2 was then function-tested on both channels: pressing it stopped CP-01 and CV-03, both channels opened and closed together on the diagnostics page, and neither machine restarted until reset was pressed. The result was recorded in the safety test log. The plant now treats any repeat `SAFE-5003` on the same device as a mandatory repair before restart.
