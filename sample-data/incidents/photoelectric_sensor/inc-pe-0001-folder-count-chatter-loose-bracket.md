---
document_id: inc-pe-0001
title: CP-01 PE3 Output Chatter From Loose Bracket
document_type: incident_report
equipment_type: photoelectric_sensor
machine_id: CP-01
alarm_code: PE-3004
occurred_on: 2026-03-25
version: "1.0.0"
license: synthetic
---

# CP-01 PE3 Output Chatter From Loose Bracket

CP-01 had been running a regular slotted-container order at a higher folding-section speed since the start of the week.

## Symptoms

Shipping found pallets from CP-01 short of boxes even though the counter showed the full quantity. At 13:40 the HMI logged `PE-3004` Output Chatter on CP-01 PE3, followed by `PE-3009` Count Mismatch: CP-01 PE3 had counted **212 boxes** against **200 sheets** counted in by CV-03 PE1, with no rejects. The PE3 yellow LED flickered as each box passed instead of switching cleanly once.

## Diagnosis

The transition log showed some boxes producing six to eight output changes within 30 ms, so single boxes were being counted twice. Signal margin with the path clear was 22×, normal for the through-beam pair, so dirt and alignment were not the cause.

An operator suggested lengthening the controller input filter. Maintenance tried it on a test batch, raising the filter from 3 ms to 10 ms. It **did not help**: the count error fell, but two boxes running close together were merged into one, and the counts were still wrong.

With CP-01 locked out, the receiver bracket moved by hand. One of its two fasteners had backed off, and the bracket was vibrating against the guard frame at the higher folding speed.

## Root Cause

A **loose receiver bracket** let the beam shake across the box edge as each box passed. The extra vibration from the higher folding-section speed had loosened the fastener over the week.

## Resolution

**SAFETY:** CP-01 was locked out and zero energy verified before maintenance worked on the bracket inside the folding-section guarding. The bracket fasteners were replaced with locking fasteners, the alignment was centred, and the bracket position was paint-marked. The input filter was returned to 3 ms. The next 2,000 boxes counted within one of the CV-03 PE1 sheet count, and no further `PE-3004` alarms were logged.
