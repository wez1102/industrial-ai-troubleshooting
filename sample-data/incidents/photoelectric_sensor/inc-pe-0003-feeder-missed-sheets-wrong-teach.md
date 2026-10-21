---
document_id: inc-pe-0003
title: CP-01 PE2 Missed Sheets After Teach On Product
document_type: incident_report
equipment_type: photoelectric_sensor
machine_id: CP-01
alarm_code: PE-3002
occurred_on: 2026-06-17
version: "1.0.0"
license: synthetic
---

# CP-01 PE2 Missed Sheets After Teach On Product

The CP-01 PE2 feeder sensor had been replaced on the previous night shift after its housing was cracked.

## Symptoms

At 08:05 CP-01 started an order of black full-coverage printed board and the feeder kept stopping with sheets sitting in the feed gate. The HMI showed `PE-3002` Missed Detection on CP-01 PE2. The feeder stopped eleven times in the first hour. The previous order, plain white-topped board, had run through the night without a stop after the replacement.

## Diagnosis

With CP-01 locked out and a black sheet held in the feed gate, the PE2 yellow LED stayed off, and lifting the corner of the sheet by a few millimetres made it come on. The margin on the black sheet read 1.1×. The sensor log showed the replacement had been taught with a white sheet lying on the feed table, not with the table alone.

The first attempt was to clean the lens, assuming dust from the night shift. It **did not help**: the lens was already clean and the margin did not change.

## Root Cause

Teaching on the sheet instead of the background put the **background-suppression cut-off just in front of the sheet surface**, instead of 15 mm in front of the feed table. White board returned enough light to switch the sensor right at the cut-off. Black board returned less, and with slight warp the sheets fell outside the sensing zone.

## Resolution

**SAFETY:** CP-01 was locked out and zero energy verified before maintenance cleared the feed gate and placed teach targets. PE2 was re-taught on the bare feed table, which set the cut-off 15 mm above the table. With a black sheet in the gate, the margin read 4.6× and the green LED was steady. The feeder ran the rest of the order without a `PE-3002` stop. The replacement-sensor checklist now states "teach on the background, then record the margin on the darkest board".
