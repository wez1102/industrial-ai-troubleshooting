---
document_id: servo-manual-v1
title: SD-200 Servo Drive Manual
document_type: manual
equipment_type: servo_drive
manufacturer: "North Quay Training (fictional)"
model: SD-200
version: "1.0.0"
license: synthetic
---

# SD-200 Servo Drive Manual

The SD-200 servo-drive designation covers the B&R ACOPOS-based motion axes on the BW Papersystems FlexPro finishing line at CP-01 and the palletizer at PL-01. This manual covers operation, alarm identification, fault isolation, and preventive maintenance. It does not replace qualified maintenance personnel or plant lockout/tagout procedures.

## Operating Guide

CP-01 retains the legacy plant tag Case Packer 01 and consists of the FlexPro flexo folder-gluer section. Axis 1 handles feeder registration, Axis 2 die-cutter phase, Axis 3 left folding-belt trim, and Axis 4 right folding-belt trim. PL-01 is the downstream palletizer with a separate servo group. When reviewing a fault, identify the machine and axis before comparing drive logs.

Each axis includes a motion controller, servo drive power stage, motor, encoder, and associated motor-power and feedback cables. The controller issues a position reference, compares encoder position with the command, and requests torque within configured limits. Some load-bearing axes have holding brakes. A holding brake alone cannot be relied on to restrain a suspended load. Drives are installed in ventilated electrical cabinets. Guarding and safety circuits operate separately from the normal motion-control status display.

The CP-01 and PL-01 maintenance reference settings are listed below. Record deviations against the configuration revision associated with the affected axis:

| Item | Normal Reference | Alarm Criterion |
| --- | --- | --- |
| Cabinet inlet air | 18–32 °C | Advisory above 36 °C for 30 s |
| Drive heat-sink reading | 28–65 °C | SERVO-7024 at 78 °C for 3 s |
| Motor winding estimate | 30–70 °C | SERVO-7025 at 82 °C for 5 s |
| Continuous axis current | At or below 6.0 A RMS | Investigate above 6.0 A for 10 s |
| Short peak current | At or below 12.0 A | SERVO-7023 above 12.0 A for 80 ms |
| Commanded acceleration | At or below 2.6 m/s² | Engineering review above 2.6 m/s² |
| Position following error | Below 1.0 mm | SERVO-7021 at 1.0 mm or more for 40 ms |
| Trace collection | 20 ms samples | Retain 4 s before and 2 s after an event |

The line HMI displays `NOT_READY`, `READY`, `RUN`, `FAULT`, or `LOCKED_OUT` along with the machine, axis, alarm code, and timestamp. Steady green indicates `READY`, animated green indicates `RUN`, and red indicates `FAULT` on the line HMI. A `READY` indication reflects drive state, not personnel protection or electrical isolation. The cabinet status indicators and controller history are reviewed independently when the HMI event sequence is unclear.

The start-up review is completed against the machine log and maintenance handover record:

1. **SAFETY:** Lock out the affected equipment, verify zero energy, and secure stored electrical, pneumatic, and mechanical energy before accessing cables, guards, brakes, or couplings.
2. Review the maintenance work order and verify the machine ID and axis. Read the first recorded `SERVO-7xxx` alarm and the subsequent HMI events in timestamp order.
3. Compare the production recipe with the recorded parameter revision. Axis 4 normally uses 2.2 m/s² acceleration; values above 2.6 m/s² require engineering review.
4. **SAFETY:** Keep the equipment isolated and the motion area secured when inspecting cabinet ventilation, motor connections, guards, or feedback cables.
5. Review logged `NOT_READY`, `READY`, `RUN`, and `FAULT` transitions. Confirm any stated isolation condition using the physical lockout record, not the HMI tile.
6. Record the handover authorization, unresolved faults, responsible technician, and results of any separately conducted operational checks.

During normal production, the drive heat sink typically reads 46–58 °C, cabinet inlet reads 24–30 °C, and Axis 4 following error stays below 0.35 mm. Both the 1.0 mm error limit and its 40 ms duration are required to trigger `SERVO-7021`. A hot cabinet with a comparatively cool motor suggests a different fault path from a motor that heats under sustained current. Compare the time trend, not only a single post-stop reading.

## Alarm and Fault Codes

The alarm table lists the `SERVO-7xxx` codes displayed for the CP-01 and PL-01 servo axes. The earliest alarm normally provides the most useful starting point; later alarms may be consequences of the original fault.

| Code | Name | Severity | Description | Likely Causes | Action |
| --- | --- | --- | --- | --- | --- |
| SERVO-7021 | Following Error | HIGH | Command and feedback differ by 1.0 mm for 40 ms. | Binding; loose feedback; coupling alignment; motion profile. | Capture axis trace; inspect recent work under isolation. |
| SERVO-7022 | Encoder Feedback Loss | HIGH | Position stream has missing or invalid updates. | Connector; cable damage; encoder supply; electrical noise. | Preserve raw diagnostics; isolate and inspect feedback path. |
| SERVO-7023 | Power Stage Overcurrent | CRITICAL | Current exceeds 12.0 A for 80 ms. | Jam; damaged motor cable; load surge; power-stage fault. | Apply emergency/site isolation response; escalate. |
| SERVO-7024 | Drive Overtemperature | HIGH | Heat sink reaches 78 °C for 3 s. | Clogged filter; failed fan; high cabinet temperature. | Record thermal trend; inspect cooling under isolation. |
| SERVO-7025 | Motor Overtemperature | HIGH | Winding estimate reaches 82 °C for 5 s. | Excess duty; friction; brake drag; stalled load. | Review motor load and qualified service records. |
| SERVO-7026 | Peak Current Overload | HIGH | Current model exceeds its peak-duration budget. | Repeated acceleration; excessive load; tight mechanism. | Compare duty-cycle trace to approved baseline. |
| SERVO-7027 | Holding Brake Movement | HIGH | Brake-hold test records 1.8 mm unwanted movement. | Brake wear; incorrect adjustment; load imbalance. | Secure supported load and escalate brake assessment. |
| SERVO-7028 | DC Bus Overvoltage | HIGH | DC bus exceeds 710 V. | Supply disturbance; regenerative motion; control mismatch. | Record the first fault; refer to qualified electrical team. |
| SERVO-7029 | Positive Software Limit | MEDIUM | Position exceeds +425 mm envelope. | Recipe mismatch; lost reference; incorrect motion target. | Compare authorized recipe and position history. |
| SERVO-7030 | Axis Reference Missing | MEDIUM | Motion request arrives without recorded homing state. | Interrupted setup; invalid reference record. | Confirm reference history with controls engineer. |
| SERVO-7031 | Encoder Parity Warning | MEDIUM | Feedback monitor detects an invalid frame. | Connector intermittency; shielding degradation; interference. | Preserve event trace; plan isolated inspection. |
| SERVO-7032 | Drive Not Ready | MEDIUM | Motion requested while drive reports fault or inhibited state. | Earlier fault; incomplete initialization; site inhibit. | Investigate the preceding event before interpreting status. |

## Troubleshooting

Troubleshooting starts by preserving the event context, not by repeatedly clearing the fault.

**SAFETY:** Lock out the affected equipment, verify zero energy, and secure stored energy before opening a cabinet, unplugging feedback cables, touching couplings, inspecting holding brakes, or entering the motion area. Record machine ID, axis, `SERVO-7xxx` code, timestamp, production recipe, reference and feedback traces, ambient and drive temperatures, and recent maintenance. Check the first alarm before interpreting secondary alarms. Escalate conflicting evidence or work beyond the technician's qualifications.

### Following Error

**What it means:** `SERVO-7021` trips when position command and feedback differ by at least 1.0 mm for 40 ms. Axis 4's 0.20 s acceleration ramp normally produces less than 0.35 mm error. A 2.4 mm deviation with the motor at 48 °C is abnormal, but does not identify whether the root cause is mechanical resistance, encoder feedback, or tuning.

**Symptoms:** Axis 4 drops out as the folder speeds up, or right-side registration drifts before the section stops. Tracking at constant speed may remain normal. Low motor temperature makes immediate overheating less likely but does not clear a mechanical or feedback defect.

**Likely causes:** In ranked order after maintenance: (1) binding or added belt load; (2) loose encoder/feedback connector; (3) coupling misalignment; (4) position-loop gains too low for the load; (5) acceleration set too high. A missing feedback sample can imitate genuine mechanical lag.

**Checks:**

1. Compare archived command, feedback, motor current, and fault times over the 0.20 s ramp. Look for abrupt encoder jumps versus smooth lag.
2. Review belt, guard, connector, and coupling work completed during the past 48 h.
3. **SAFETY:** Lock out the axis, verify zero energy, and restrain the mechanism before checking feedback plug seating, latch, strain relief, and visible cable damage.
4. **SAFETY:** Keep the mechanism isolated and restrained while the mechanical specialist checks belt resistance and coupling alignment.
5. Compare gains and acceleration with the signed recipe baseline; never increase alarm limits to conceal an unresolved fault.

**Corrective action:** Record the confirmed defect and the completed repair. For a loose connector, record the original latch condition, corrected seating, and strain relief. Restore any parameter changes from the approved revision through controls-engineering change control. Retain a post-repair comparison trace in the maintenance record.

**When to escalate:** Escalate if traces remain inconsistent, the axis faults again after verified repair, connector damage is found, the coupling condition is uncertain, or safety-related events accompany the fault. A reset alone does not establish the cause.

### Encoder Feedback Loss

**What it means:** `SERVO-7022` records missing or invalid encoder feedback for 60 ms. The controller may continue to receive a changing position request while the measured position remains stale. This discrepancy can trigger a following-error alarm after the initial feedback-loss event.

**Symptoms:** A position reading freezes at 168.3 mm, an axis reference becomes inconsistent, or a following-error banner appears after the feedback stream fails. The commanded position may continue changing after the last valid encoder sample. Operators sometimes describe the symptom as a jam even when the problem is measurement quality.

**Likely causes:** Ranked possibilities are (1) partly latched feedback connector, (2) cable strain at a bend, (3) damaged conductor or shielding, (4) unstable encoder supply, and (5) encoder failure or incorrect stored configuration. Confirm the encoder type from the axis maintenance record before selecting an inspection method.

**Checks:**

1. Save the original alarm sequence, missing-update count, and last valid position timestamp.
2. Compare the alarm with maintenance and wash-down history, especially work near the encoder cable.
3. **SAFETY:** Lock out the axis, verify zero energy, and restrain the load before examining the connector latch, plug seating, visible cable jacket, gland, and shield routing.
4. Review archived encoder-value quality, recorded reference state, and prior fault frequency without probing live conductors.
5. **SAFETY:** Keep the circuit isolated during any continuity check; qualified electrical staff use the axis wiring drawings and the encoder interface specification.

**Corrective action:** Record the identified connector, cable, or configuration defect and the correction in the maintenance log. Do not substitute an estimated position for missing feedback or bypass feedback-loss monitoring. Retain the original trace and repair details for comparison.

**When to escalate:** Escalate if the feedback reference is untrustworthy, possible unobserved motion occurred, the encoder type is uncertain, or a corrected connector is followed by further dropouts. Controls engineering reviews the axis reference before additional motion troubleshooting.

### Overcurrent Fault

**What it means:** `SERVO-7023` records current above 12.0 A for 80 ms. `SERVO-7026` records excessive accumulated peak-current duty. A short current spike and a repeated overload pattern require different reviews of the motor current, axis speed, and production load.

**Symptoms:** A servo axis stops during a load increase, with a recorded 13.7 A spike compared with 4.5 A on the last normal recipe. Jammed machinery may produce increasing current while speed falls. A sudden power-stage event may lack that gradual mechanical pattern. The motor can still be at normal temperature.

**Likely causes:** Ranked cases are (1) jammed scrap or tight folder belts, (2) unexpected load or recipe change, (3) motor or power-cable defect, (4) brake drag, and (5) power-stage damage or incorrect recorded motor data. This fault is classified `CRITICAL` because dangerous electrical or mechanical energy may be involved.

**Checks:**

1. **SAFETY:** Stop physical intervention, lock out the affected equipment, verify zero energy, and restrain gravity-driven or mechanically stored loads before access.
2. Preserve the earliest `SERVO-7xxx` alarm and traces for current, acceleration, speed, and last complete cycle.
3. Ask the mechanical specialist to review the last material position, scrap path, load history, and recent intervention records.
4. **SAFETY:** Keep motor circuits isolated while qualified electrical staff inspect the power connections, cable insulation, and brake components using the axis drawings.
5. Compare the approved motor and recipe records. Do not raise current limits or repeatedly test under the same unexplained load.

**Corrective action:** Route the verified jam, cable defect, or configuration discrepancy through approved repair and change control. A software adjustment must not substitute for an unresolved electrical condition. Record who independently reviewed and accepted the work.

**When to escalate:** Escalate immediately for an unclear fault origin, damaged insulation, visible heating, repeated current events, or coincident safety alarms. Lack of a detailed trace does not justify downgrading this `CRITICAL` alarm.

### Drive Overtemperature

**What it means:** `SERVO-7024` records a drive heat-sink temperature of at least 78 °C for 3 s. The heat sink can overheat even while motor temperature and axis current remain within their normal ranges. Review the cabinet inlet temperature and airflow before attributing the event to motor load.

**Symptoms:** On PL-01 a palletizer axis stops after several bundle groups while the cabinet feels hotter than usual. One event trace shows the heat sink climbing from 57 °C to 81 °C over 27 min, with the motor at 51 °C and the cabinet inlet at 39 °C. The mismatch between cabinet and motor readings suggests reduced cabinet cooling rather than motor overheating.

**Likely causes:** Ranked possibilities are (1) filter blocked by corrugated dust, (2) obstructed cabinet airflow, (3) failed fan, (4) hot surrounding air, and (5) heavy duty cycle or unreliable temperature reading. A cool motor does not disprove a hot drive heat sink.

**Checks:**

1. Capture machine ID, the earliest code, heat-sink and cabinet temperatures, current, workload, and filter-service date.
2. Confirm PL-01 and the affected drive sensor. Compare the drive, motor, and cabinet inlet temperature histories for the same time window.
3. **SAFETY:** Lock out the cabinet, verify zero energy and stored-energy discharge, and secure fan motion before opening the door or touching the filter.
4. **SAFETY:** Keep the cabinet isolated while qualified staff inspect the filter, fan assembly, intake clearance, and outlet condition; record dust coverage by percentage.
5. Compare archived sensor history for plausible temperature behavior. Implausible readings require specialist evaluation, not a guessed sensor replacement.

**Corrective action:** A confirmed filter or ventilation problem is corrected only through approved maintenance using authorized consumables. Record the prior blockage, completed work, and any subsequently authorized temperature trend; one cooler reading does not validate all cabinet conditions.

**When to escalate:** Escalate if `SERVO-7024` recurs, temperatures remain excessive after airflow correction, a temperature sensor appears unreliable, electrical damage is suspected, or ventilation differs from the cabinet drawing. Never bypass thermal protection.

## Maintenance Procedure

The preventive schedule below covers routine inspections, cooling-system cleanliness, mechanical connections, holding-brake records, and parameter backups. Record actual completion dates, observations, and maintenance personnel for each affected machine.

For every completed task, close the maintenance record with the original fault, evidence collected, corrective work, changed parts or settings, and the responsible maintenance reviewer.

**SAFETY:** Locked out the affected equipment, verified zero energy and DC-bus discharge, relieved pneumatic pressure, and restrained gravity-loaded or spring-loaded mechanisms before performing physical maintenance. Isolated adjacent machinery that could move into the work area. Did not rely on the HMI LOCKED_OUT tile as evidence of physical isolation.

| Frequency | Preventive Task | Record To Keep |
| --- | --- | --- |
| Daily | Review prior-shift fault log and cabinet temperature trend. | 24 h alarm export and hottest drive reading |
| Weekly | Inspect external cable routing and visible enclosure condition. | Photo or written observation and machine ID |
| Monthly | Check isolated cabinet filter and fan assembly. | Dust coverage, cleaning date, and filter condition |
| Monthly | Review approved parameter backup status. | Backup checksum and revision identifier |
| Quarterly | Inspect isolated feedback connectors and strain relief. | Plug ID, lock condition, visible damage notes |
| Quarterly | Review coupling and set-screw inspection records. | Authorized torque specification reference and result |
| Annual | Plan qualified holding-brake verification if applicable. | Work permit, load-restraint reference, test report |
| Annual | Compare approved drive parameter images and event trends. | Signed configuration comparison and deviation log |

### Inspect Cables and Connectors

Review the machine isolation record and the previous maintenance entries.

**SAFETY:** Lock out the affected circuit, verify zero energy, and restrain the mechanism before handling a motor or feedback connector. Record connector name, visible latch condition, cable bend support, jacket abrasion, dust intrusion, and whether recent work disturbed the cable path. A partly unlatched connector on CP-01 Axis 4 is a defect even when electrical symptoms appear intermittent. Do not probe energized connector contacts.

### Clean Cabinet Filter and Fans

Review heat-sink and cabinet-inlet temperature trends first.

**SAFETY:** Lock out the cabinet and verify zero energy before opening its door, removing a filter, or inspecting fan blades. Do not defeat a fan guard or operate with the intake uncovered. Record filter coverage at 0%, 25%, 50%, 75%, or 100%, fan movement while isolated, visible deposits, and door-seal condition. Record the replacement filter identifier and service date. Compare later temperature logs against the pre-service trend.

### Check Coupling and Set-Screw Torque

Compare prior service entries with the coupling drawing and fastening specification associated with the axis.

**SAFETY:** Lock out the axis, verify zero energy, and restrain all movable sections before touching the coupling, shaft, timing belt, or set screws. Record measured alignment offset, coupling condition, fastener identification, and torque-check results. A past Axis 4 inspection recorded a 0.35 mm alignment offset. Do not substitute that historical reading for the required mechanical tolerance or a fastener torque value.

### Test the Holding Brake

Review the brake inspection schedule and the load-support plan for the affected axis.

**SAFETY:** Install independent load support, isolate hazardous motion, and secure access before a qualified test team performs a brake assessment. Record the completed test method, brake command state, measured movement, and acceptance criterion from the axis brake specification. The `SERVO-7027` log threshold is 1.8 mm of unwanted movement; it is an alarm condition, not an acceptance allowance. Escalate a brake concern rather than repeating trials.

### Back Up Drive Parameters

Export a configuration snapshot through the maintenance configuration-management workflow and compare it with the recorded baseline. Log the machine and axis, software release identifier, file timestamp, checksum, and reviewer. Changes to gain, acceleration, motor data, or encoder settings require a controls engineer's signed review. Preserve both the prior and current revisions so troubleshooting can establish which settings were active when an alarm occurred.
