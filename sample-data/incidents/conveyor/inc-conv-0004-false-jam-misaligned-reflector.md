---
document_id: inc-conv-0004
title: CV-03 False Product Jam From Misaligned Reflector
document_type: incident_report
equipment_type: conveyor
machine_id: CV-03
alarm_code: CONV-2008
occurred_on: 2026-08-12
version: "1.0.0"
license: synthetic
---

# CV-03 False Product Jam From Misaligned Reflector

CV-03 had been running normally until a warped sheet hit the far-side discharge guide early in the shift.

## Symptoms

From 09:20 the conveyor kept stopping on a jam, but there was nothing jammed. `CONV-2008` Product Jam stopped CV-03 five times in 40 minutes. Each time, operators found the discharge clear and the CP-01 feeder still waiting for board. The discharge photo-eye's output indicator stayed on (blocked) with no sheet in front of it, and its green stability indicator was off.

## Diagnosis

The jam timer was working as designed: the photo-eye really did report a blocked beam for more than 6.0 s. The problem was the signal, not the sheets. An operator wiped the photo-eye lens with a glove after the third stop. It **did not help** for long: the conveyor ran for about 10 minutes and then stopped again.

With CV-03 and the CP-01 feeder locked out, maintenance found the retroreflector on the far side of the belt coated with a film of paper dust. Its bracket was bent about 4° downward where the warped sheet had struck it, so the beam was landing near the reflector's lower edge.

## Root Cause

The **reflector bracket had been knocked out of alignment** by the warped sheet, leaving the beam at the edge of the reflector. Dust on the reflector then reduced the returned light below the switching level, so the photo-eye intermittently reported blocked with no sheet present.

## Resolution

**SAFETY:** CV-03 and the CP-01 feeder were locked out and zero energy was verified before maintenance reached across the belt. The reflector bracket was straightened and the lens and reflector were cleaned with a lint-free cloth. With the photo-eye powered and the conveyor still locked out, the green stability indicator came on steadily and the output switched cleanly when a test sheet was held in the beam. CV-03 ran the rest of the shift without a `CONV-2008` stop. The jam timer was left at 6.0 s.
