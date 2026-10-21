---
document_id: inc-safe-0004
title: CV-03 Contactor Feedback Fault From Welded Contactor
document_type: incident_report
equipment_type: safety_circuit
machine_id: CV-03
alarm_code: SAFE-5005
occurred_on: 2026-05-27
version: "1.0.0"
license: synthetic
---

# CV-03 Contactor Feedback Fault From Welded Contactor

During the morning, a run of warped board kept jamming at the CV-03 discharge, and the crew used the emergency stop more than 30 times to stop the conveyor while clearing sheets.

## Symptoms

At 13:05 an operator pressed an emergency stop on CV-03 during a sheet change. The conveyor and CP-01 stopped normally. When the button was released, reset was refused and the HMI showed `SAFE-5005` Contactor Feedback Fault on contactor K2. The diagnostics page showed contactor K1 open and confirmed, and K2's feedback contact still reporting closed.

## Diagnosis

The feedback fault meant K2 had not confirmed opening within 200 ms. CV-03 had still stopped, because K1 opened and removed motor power on its own. That is what the two contactors in series are for, and it is also why the controller refused to restart: with K2 stuck, the conveyor had only one working stop device.

An operator asked whether the fault could be cleared with a reset and a power cycle so the line could run until the weekend. It was not tried; the controller will not accept a reset while a feedback contact disagrees, and running on one contactor is not permitted.

With CV-03 and CP-01 locked out at their main isolators and zero energy verified at the motor terminals, an electrician inspected K2. Its main contacts were pitted and welded closed. Each restart had switched the VFD's inrush current through the contactors, and the morning's repeated stops and restarts had been far more than they are rated to switch in a short period.

## Root Cause

**K2's main contacts welded** after repeated switching of the VFD inrush current during the morning's emergency stops and restarts. Because they could no longer open, its feedback contact stayed closed, and the safety controller correctly refused to restart CV-03.

## Resolution

**SAFETY:** CV-03 and CP-01 were locked out at their main isolators and zero energy was verified at the CV-03 motor terminals before the contactors were removed. The electrician replaced both K1 and K2 with the same type, as a pair. The stop feedback was then function-tested: an emergency stop opened both contactors within 200 ms with both feedback contacts confirming, and CV-03 did not restart until reset was pressed. The result was recorded in the safety test log. The discharge guides were adjusted for warped board, and crews were reminded to use the normal stop button, not the emergency stop, for routine jam clearing.
