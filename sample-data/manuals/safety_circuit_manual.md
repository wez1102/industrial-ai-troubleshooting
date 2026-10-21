---
document_id: safety-manual-v1
title: SG-30 Machine Safety Circuit Manual
document_type: manual
equipment_type: safety_circuit
manufacturer: "North Quay Training (fictional)"
model: SG-30
version: "1.0.0"
license: synthetic
---

# SG-30 Machine Safety Circuit Manual

The SG-30 is the machine safety circuit on CV-03, CP-01, and PL-01: emergency stops, the CV-03 pull-cord, guard interlocks, the safety controllers, and the stop devices they switch. This manual covers how the safety functions work, their alarms, fault isolation, and the routine function tests. It does not replace qualified maintenance personnel, plant lockout/tagout procedures, or the plant's safety validation records.

## Operating Guide

Each machine has its own safety controller that monitors its emergency stops and guard switches on two independent channels. When any input opens, the controller removes the enable to that machine's stop devices. CP-01 and CV-03 share an emergency stop zone, because CV-03 feeds sheets directly into the CP-01 feeder: an emergency stop or pull-cord on either machine stops both.

| Machine | Safety Inputs | Stop Devices | Stop Type |
| --- | --- | --- | --- |
| CV-03 | 2 emergency stop buttons; pull-cord switch along the full length | Two VFD supply contactors in series, with feedback contacts | Immediate removal of motor power |
| CP-01 | 6 emergency stop buttons; 8 coded non-contact guard switches on the feeder, die-cut, folding, and counter-ejector guards | Safe torque off (STO) on servo axes 1–4; pneumatic dump valve with pressure switch | Controlled stop, then STO after 1.0 s |
| PL-01 | 3 emergency stop buttons; cell access door with a guard-locking switch | STO on Axis 1 and Axis 2 with hoist brake applied; pneumatic dump valve with pressure switch | Controlled stop, then STO after 1.0 s |

**Two channels.** Every emergency stop button and guard switch has two contacts, channel A and channel B, wired separately to the controller. Both must open when the device is operated and both must close when it is restored. If the channels disagree for longer than 100 ms, the controller assumes a wiring or device fault and latches SAFE-5003 Channel Discrepancy.

**Coded guard switches.** CP-01 guard switches only accept the specific actuator they were paired with. A spare or loose actuator held against the switch is rejected and raises SAFE-5011. The switch is guaranteed to recognise its actuator within 5 mm of the switch face and guaranteed to open beyond 15 mm; between the two, recognition is not reliable. With the guard closed, the gap between actuator and switch face is set at 2–3 mm.

**Guard locking on PL-01.** The PL-01 cell door stays locked while the cell is running. A door-release request starts a stop; the lock opens only after the controller confirms both axes are at standstill and 8 s have passed. The lock reports its position to the controller, and the cell cannot start unless the door is closed and locked.

**Stop feedback.** The controller checks that each stop device actually acted. On CV-03, both contactors must open within 200 ms and their feedback contacts must confirm it before a restart is allowed. On CP-01 and PL-01, each servo drive confirms STO within 50 ms, and the dump valve pressure switch must show machine air below 0.5 bar within 3 s of a stop. A device that fails to confirm raises a feedback fault, and the machine cannot be reset until the fault is corrected.

**Reset.** After a safety stop, the machine restarts only after a deliberate reset. Each machine has a blue reset button outside its guarding, positioned so the operator can see into the guarded area. The reset acts on release of the button and is refused if the button is held for more than 5 s. A guard closing or an emergency stop being released never restarts the machine by itself.

| Item | Normal Reference | Alarm Criterion |
| --- | --- | --- |
| Channel discrepancy | Both channels switch within 100 ms | SAFE-5003 latched above 100 ms |
| Guard actuator gap, guard closed | 2–3 mm | Recognition guaranteed only within 5 mm; switch open beyond 15 mm |
| CV-03 contactor opening | Within 200 ms, both feedback contacts confirm | SAFE-5005 |
| Servo STO confirmation | Within 50 ms | SAFE-5006 |
| Dump valve exhaust | Below 0.5 bar within 3 s; typically 1.0–1.5 s | SAFE-5007 |
| PL-01 door unlock delay | Standstill confirmed plus 8 s | SAFE-5008 if lock position disagrees |
| Reset button | Press and release within 5 s | SAFE-5010 if held longer |

The safety circuit is never bypassed, jumpered, or defeated to keep a machine running or to make troubleshooting easier. That includes taping or tying actuators to switches, using spare actuators, bridging terminals, and holding a door lock open. Changes to safety wiring, devices, or the safety controller configuration are made only by the plant's authorized safety engineer and are revalidated before production resumes.

## Alarm and Fault Codes

The alarm table lists the `SAFE-5xxx` codes from the safety controllers. The HMI shows the machine and the device address with each code, such as `CP-01 GS4` for guard switch 4. Codes for a guard opening or an emergency stop pressed are normal stop events. Discrepancy and feedback codes are faults that latch and need the cause corrected before the machine can be reset.

| Code | Name | Severity | Description | Likely Causes | Action |
| --- | --- | --- | --- | --- | --- |
| SAFE-5001 | Guard Circuit Not Satisfied | MEDIUM | A guard switch reports open. | Guard open; guard sagging or misaligned; damaged actuator. | Close guard; if it persists, check actuator gap. |
| SAFE-5002 | Emergency Stop Pressed | HIGH | An emergency stop button reports operated. | Button pressed; button not fully released; contact block fault. | Find why it was pressed; release and reset from outside. |
| SAFE-5003 | Channel Discrepancy | HIGH | Channels A and B of one device disagree for more than 100 ms. | Loose contact block; damaged wire; misaligned guard switch. | Lock out; inspect the reported device and its wiring. |
| SAFE-5004 | Pull-Cord Stop | HIGH | CV-03 pull-cord switch operated or cord tension out of range. | Cord pulled; cord slack or over-tensioned; loose cord fixing. | Check cord tension window and fixings. |
| SAFE-5005 | Contactor Feedback Fault | CRITICAL | A CV-03 contactor did not confirm opening within 200 ms. | Welded contactor tips; feedback contact or wiring fault. | Lock out; do not reset until the contactor is checked. |
| SAFE-5006 | STO Feedback Fault | CRITICAL | A servo drive did not confirm STO within 50 ms. | STO wiring fault; drive fault. | Lock out; refer to the safety engineer. |
| SAFE-5007 | Dump Valve Feedback Fault | CRITICAL | Machine air did not fall below 0.5 bar within 3 s of a stop. | Clogged dump valve silencer; sticking valve; pressure switch fault. | Lock out; treat the machine as still pressurized. |
| SAFE-5008 | Guard Lock Fault | HIGH | PL-01 door lock position disagrees with the lock command. | Door misaligned with the lock; damaged lock; wiring fault. | Lock out; inspect door alignment and lock. |
| SAFE-5009 | Safety Controller Fault | CRITICAL | The safety controller reports an internal or configuration fault. | Hardware fault; configuration mismatch. | Refer to the safety engineer. |
| SAFE-5010 | Reset Button Fault | MEDIUM | Reset button held for more than 5 s or stuck closed. | Stuck button; held on purpose; wiring fault. | Check button operation; reset is refused until it releases. |
| SAFE-5011 | Coded Switch Mismatch | HIGH | A guard switch reads an actuator it is not paired with. | Wrong actuator fitted; actuators swapped between guards; spare actuator. | Fit the paired actuator; report any unexplained mismatch. |

## Troubleshooting

Safety circuit faults are diagnosed from the controller's device addresses and channel states, not by trial resets. A latched fault is the controller doing its job: it has found something it cannot trust.

**SAFETY:** Lock out the machine and verify zero energy before opening a guard, junction box, or control cabinet to work on a safety device. On CP-01 and CV-03, lock out both machines, because they share an emergency stop zone. Never bridge, jumper, or hold a safety input to test the rest of the circuit. After any repair to a safety device, a qualified person must function-test the affected safety function before the machine returns to production, and record the result. Record the machine, device address, alarm code, channel states, and any recent work on guards, doors, or wiring.

### Guard Circuit Not Satisfied

**What it means:** SAFE-5001 shows that a guard switch reports open. With the guard open, that is the correct response. The fault to troubleshoot is SAFE-5001 with the guard closed, or nuisance stops where the guard drops out for a moment while the machine runs.

**Symptoms:** The machine will not reset although every guard looks shut, or it stops briefly during running with SAFE-5001 on the same guard switch each time. Nuisance stops often get worse with vibration at higher speed or after a guard has been opened many times in a shift.

**Likely causes:** In ranked order: (1) a guard door sagging on its hinges so the actuator gap exceeds the 5 mm recognition distance under vibration; (2) a damaged, cracked, or loose actuator; (3) a guard that is not closing fully because of debris or a bent frame; (4) a damaged switch or cable; (5) the wrong actuator fitted after guard work, which shows as SAFE-5011.

**Checks:**

1. Read the device address and channel states. Note whether both channels open together.
2. With the guard closed, check visually that the actuator lines up with the switch face.
3. **SAFETY:** Lock out the machine and verify zero energy. Measure the actuator gap with the guard closed; it should be 2–3 mm. Check the hinges, latch, and guard frame for sag or damage.
4. Inspect the actuator and switch for cracks, loose fasteners, and impact marks.
5. Check the switch cable for damage where the guard moves.

**Corrective action:** Adjust the hinges or latch so the guard closes square and the actuator gap returns to 2–3 mm. Replace a damaged actuator or switch with the same type; pairing a replacement actuator is done by the safety technician. Function-test the guard after the repair: with the machine running, opening the guard must stop it, and it must not restart until the guard is closed and reset is pressed.

**When to escalate:** Escalate if the gap is correct and the switch still drops out, if SAFE-5011 appears without an explained actuator change, or if the guard frame is distorted.

### Channel Discrepancy

**What it means:** SAFE-5003 latches when channels A and B of one device disagree for longer than 100 ms. Two channels exist so that one failed contact or wire cannot hide a demand to stop. A discrepancy means the controller can no longer trust that device.

**Symptoms:** The machine stops and cannot be reset after the device is restored. The HMI shows one channel closed and the other open for the same device. The fault may clear after a power cycle and then return within hours or days.

**Likely causes:** In ranked order: (1) a loose or cracked contact block on an emergency stop button, often from vibration; (2) a damaged conductor or loose terminal on one channel; (3) a guard switch mounted so the actuator sits at the edge of its range; (4) a worn emergency stop button mechanism; (5) a controller input fault.

**Checks:**

1. Note which channel is open and which device address is reported.
2. Check the history for earlier SAFE-5003 alarms on the same device.
3. **SAFETY:** Lock out the machine and verify zero energy. Inspect the contact blocks on the reported device for looseness, cracks, and correct seating.
4. **SAFETY:** Keep the machine locked out while checking terminals and wiring of the open channel between the device and the junction box.
5. For a guard switch, check the actuator gap and alignment.

**Corrective action:** Replace the loose or damaged contact block or device, re-terminate loose wiring, or realign the guard switch. Do not clear a discrepancy by power cycling the controller and running on; the fault will return, and until it is fixed the device has only one working channel. Function-test the device on both channels after the repair.

**When to escalate:** Escalate if the discrepancy returns after the device and wiring are repaired, or if it appears on several devices at once.

### Stop Feedback Faults

**What it means:** SAFE-5005, SAFE-5006, and SAFE-5007 mean a stop device did not confirm that it acted: a CV-03 contactor did not open, a servo drive did not confirm STO, or machine air did not exhaust. These are the most serious safety circuit faults, because the device that removes energy may not be working. The redundant device usually still stopped the machine, which is why the controller refuses to restart rather than letting the line run on one device.

**Symptoms:** The machine stopped normally, but reset is refused and the HMI shows a feedback fault for one device. For SAFE-5007, a cylinder may still hold position or move slowly after the stop because air is still in the machine. A welded contactor often follows a period of frequent emergency stops and restarts, or a high-current event.

**Likely causes:** For contactors: (1) main contacts welded after frequent switching or high current; (2) a failed feedback contact or wiring. For STO: (1) STO wiring fault; (2) drive fault. For the dump valve: (1) a clogged dump valve exhaust silencer; (2) a sticking dump valve; (3) a pressure switch fault.

**Checks:**

1. Read which device failed to confirm, and review alarms and current trends from just before the stop.
2. **SAFETY:** Lock out the machine at its main isolator and verify zero energy at the motor terminals or drive output before working on contactors or drives. Do not rely on the safety circuit stop for isolation while it has a feedback fault.
3. **SAFETY:** For SAFE-5007, treat the machine as pressurized. Close and lock the pneumatic shut-off valve, confirm 0 bar, and support any raised load before working near cylinders.
4. Inspect the contactor for welded contacts and check its feedback contact and wiring.
5. Inspect the dump valve exhaust silencer and time the exhaust after the repair.

**Corrective action:** Replace a welded contactor together with its partner and find out why it welded, such as frequent emergency stops used as routine stops. Replace a clogged dump valve silencer or a sticking valve. Refer STO faults and any fault you cannot trace to the safety engineer. Function-test the stop device and its feedback before the machine returns to production.

**When to escalate:** Escalate every STO fault, any repeat of a feedback fault, and any case where the cause of a welded contactor is not found.

### Emergency Stop and Pull-Cord Reset

**What it means:** SAFE-5002 and SAFE-5004 show that an emergency stop or the CV-03 pull-cord was operated. The first question is why it was operated. The fault to troubleshoot is a stop that will not reset after the device is released, or a pull-cord that trips with nobody pulling it.

**Symptoms:** The emergency stop button is pulled out but SAFE-5002 stays active, or CV-03 and CP-01 stop on SAFE-5004 at random with no one near the cord. Pull-cord trips may follow temperature changes or work near the conveyor.

**Likely causes:** For emergency stops: (1) a button not fully released; (2) a contact block not seated. For the pull-cord: (1) cord tension outside the switch window because the cord stretched or contracted; (2) a loose eye bolt, pulley, or cord clamp; (3) something resting on or snagging the cord; (4) a damaged switch.

**Checks:**

1. Confirm with the crew why the device was operated, and that the reason has been dealt with.
2. Check that the button is fully released or that the pull-cord switch reset lever is in the run position.
3. Check the pull-cord tension indicator; the pointer must sit in the green window.
4. **SAFETY:** Lock out CV-03 and CP-01 and verify zero energy before walking the length of CV-03 to check cord fixings, pulleys, and supports.
5. Inspect the contact blocks on an emergency stop button that will not reset.

**Corrective action:** Re-tension the cord into the green window, tighten loose fixings, and remove snags. Replace a faulty button, contact block, or switch with the same type. Function-test after the repair: each emergency stop button, and the pull-cord pulled at both ends and the middle, must stop CV-03 and CP-01.

**When to escalate:** Escalate if the cord cannot be tensioned into the window, if a device fails its function test, or if the stops cannot be explained.

## Maintenance Procedure

The preventive schedule below covers function tests of emergency stops, the pull-cord, guard interlocks, and stop feedback, and inspection of safety devices and wiring. Every test result is recorded in the safety test log with the device address, the result, and the name of the person who did the test. A failed test takes the machine out of production until the device is repaired and passes.

**SAFETY:** Function tests are done by trained personnel with the area clear and the machine running empty or at its test speed. Lock out the machine and verify zero energy for any inspection or repair inside guarding or enclosures. Never bridge or hold a safety input during a test.

| Frequency | Preventive Task | Record To Keep |
| --- | --- | --- |
| Shift start | Operate one emergency stop per machine, rotating through all buttons. | Button address and result |
| Monthly | Function-test every emergency stop and the CV-03 pull-cord. | Each device address and result |
| Monthly | Function-test every guard switch and the PL-01 door lock. | Each device address and result |
| Quarterly | Test stop feedback: contactor opening, STO confirmation, dump valve exhaust time. | Measured times and results |
| Quarterly | Inspect safety devices, actuators, cables, and pull-cord fixings. | Damaged or loose items found |
| Annual | Full safety function validation by the safety engineer. | Signed validation record |

### Test Emergency Stops and Pull-Cord

Each emergency stop button is tested by pressing it with the machine running empty. The machine must stop, and it must not restart when the button is released until reset is pressed.

**SAFETY:** Clear the area before the test. Press each button in turn and confirm that the machine stops and that the HMI shows SAFE-5002 with the correct address. On CV-03, pull the cord at both ends and the middle and confirm that CV-03 and CP-01 both stop. Check the pull-cord tension pointer is in the green window. Record each device separately.

### Test Guard Interlocks

Each guard switch is tested by opening its guard with the machine running empty. The machine must stop before the opening is large enough to reach a hazard, and it must not restart when the guard closes until reset is pressed.

**SAFETY:** Clear the area before the test. Open each guard in turn and confirm the stop and the SAFE-5001 address. On PL-01, request door release and confirm the lock stays closed until standstill plus 8 s. Lock out the machine before measuring actuator gaps, then confirm 2–3 mm on each closed guard.

### Test Stop Feedback

Stop feedback tests prove that the devices that remove energy actually act, not just that the safety inputs work.

**SAFETY:** With the area clear, trigger a stop and read the confirmation times from the safety controller diagnostics: CV-03 contactors within 200 ms, servo STO within 50 ms, and dump valve exhaust below 0.5 bar within 3 s. Record each time. A dump valve exhaust time rising above 2.0 s calls for the dump valve silencer to be replaced before it reaches the alarm limit.

### Inspect Safety Devices and Wiring

Safety devices on guards and along conveyors get knocked, vibrated, and covered in dust like any other device, and a loose part shows up first as nuisance stops or discrepancies.

**SAFETY:** Lock out the machine and verify zero energy before inspecting inside guarding or opening enclosures. Check each switch, actuator, and emergency stop for cracks, loose fasteners, and impact marks. Follow safety cables at guard hinges and moving parts for chafing. Check pull-cord eye bolts, pulleys, and clamps. Report any device that looks tampered with, such as tape, ties, or a spare actuator near a switch, to the safety engineer.
