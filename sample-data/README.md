# PlantAssist Synthetic Corpus

This folder contains synthetic maintenance and troubleshooting records for PlantAssist retrieval and evaluation. **Not for use on real equipment.** The plant, asset assignments, setpoints, events, measurements, outcomes, and procedures were written for this corpus; they were not taken from a former employer's or customer's internal documents. BW Papersystems, FlexPro, B&R Industrial Automation, and ACOPOS are real names used as public product context. No affiliation, certification, or verified knowledge of an actual FlexPro installation is claimed.

## Purpose

This corpus tests manual passage retrieval, informal technician wording, machine-specific fault matching, and answers to questions outside document coverage. The manual and incident reports deliberately use realistic industrial language together with constructed site records. Operational limits and work steps in this corpus are not validated against physical equipment.

## Fictional Plant

The site is **North Quay Corrugated Test Plant**, a synthetic corrugated packaging facility. The finishing-line scenario is based conceptually on the BW Papersystems FlexPro flexo folder gluer and its publicly described feeder, die-cut, and folding sections. Asset names and axis allocation are constructed for evaluation, not verified BW Papersystems hardware configurations.

| Machine ID | Plant Asset Name | Equipment Contained | Synthetic Role |
| --- | --- | --- | --- |
| CP-01 | Case Packer 01 | Servo axes 1–4, photo-eyes, pneumatic cylinders, safety circuit | Legacy plant tag for the FlexPro-style finishing cell; the actual FlexPro product is a flexo folder gluer, not a conventional case packer |
| CV-03 | Infeed Conveyor 03 | Conveyor drive, photo-eyes | Feeds corrugated sheets toward CP-01 |
| PL-01 | Palletizer 01 | Servo axes, pneumatics, safety circuit | Handles completed bundles after the finishing cell |

In CP-01, Axis 1 is the feeder register, Axis 2 is bottom die-cutter synchronization, Axis 3 is the left folding-belt trim axis, and Axis 4 is the right folding-belt trim axis. The drive designation is **SD-200**, with **B&R ACOPOS** as the public technology reference. SD-200 is not a B&R orderable model; manual metadata identifies **North Quay Training (fictional)** as the document manufacturer.

## Alarm Code Prefixes

These are PlantAssist corpus HMI alarm prefixes, not published BW Papersystems or B&R alarm identifiers.

| Prefix | Equipment Type | Example |
| --- | --- | --- |
| SERVO-7xxx | Servo drive and servo axis | SERVO-7021 Following Error |
| CONV-2xxx | Conveyor and its motor drive | CONV-2001 Conveyor Speed Deviation |
| PE-3xxx | Photo-eye and object sensing | PE-3001 Blocked Sensor |
| PNEU-4xxx | Pneumatic device or cylinder | PNEU-4001 Cylinder Extend Timeout |
| SAFE-5xxx | Safety-chain reporting | SAFE-5001 Guard Circuit Not Satisfied |

## Severity Levels

These four levels classify the documented event severity within the corpus:

| Level | Meaning | Example Documentation Focus |
| --- | --- | --- |
| LOW | Advisory with no current loss of process | Log the symptom and trend |
| MEDIUM | Degraded condition or interrupted setup | Identify the affected asset and record the sequence |
| HIGH | Stopped axis or possible equipment damage | Isolation status and maintenance escalation |
| CRITICAL | Immediate high-consequence electrical or motion hazard | Emergency response and energy isolation |

## Data Conventions

- The retrieval index includes the Markdown manual and both incident reports; this README is for human review only and is excluded from ingestion.
- Manual front matter uses `document_id`, `title`, `document_type`, `equipment_type`, `manufacturer`, `model`, `version`, and `license`. Incident front matter uses `document_id`, `title`, `document_type`, `equipment_type`, `machine_id`, `alarm_code`, `occurred_on`, `version`, and `license`.
- Every `document_id` is unique. Versions are quoted semantic-version strings; dates use ISO `YYYY-MM-DD` notation. The license value `synthetic` is a corpus label, not an external legal license.
- All manual and Markdown-incident headings are unique within each file, unnumbered, in Title Case, and followed by meaningful prose. Preserve headings once evaluation questions use their chunk IDs.
- Incident filenames follow `inc-servo-NNNN-short-kebab-description.md` or `.txt` inside `incidents/servo_drive/`.
- The second incident intentionally has YAML front matter and a **plain-text body without Markdown headings** to exercise the TXT parser.
- Safety-critical steps in Markdown use the literal `**SAFETY:**` marker; the TXT incident uses plain `SAFETY:`. Both represent `safetyCritical: true` after parsing.
- Values use metric units: current in A, temperature in °C, distance in mm, and time in s or ms. All operating numbers are constructed for evaluation.
- Records are historical examples, not universal repair advice. Resolving one incident does not prove another incident has the same cause.

## Coverage Gaps

These topics are deliberately outside the servo manual. They provide evaluation cases for insufficient-information answers:

- Servo-drive firmware updates and upgrade or rollback procedures.
- Fieldbus and network communication faults, topology, addressing, and protocol diagnostics.
- Complete drive-unit replacement and commissioning after a replacement.
- Braking-resistor selection and sizing calculations.

Actual BW Papersystems wiring, connector pinouts, product-specific torque values, electrical test points, safety-validation methods, and B&R model/firmware applicability are outside the corpus. These details are not established by the synthetic records.

## Files In This Set

- `manuals/servo_drive_manual.md`: synthetic SD-200 operating, alarm, troubleshooting, and maintenance guide.
- `incidents/servo_drive/inc-servo-0001-following-error-after-maintenance.md`: CP-01 Axis 4 loose encoder connector after maintenance.
- `incidents/servo_drive/inc-servo-0002-drive-overtemperature.txt`: PL-01 cabinet-filter obstruction and drive heat-sink overtemperature.

## Suggested Retrieval Checks

CP-01 Axis 4 dropping out during acceleration is associated with Following Error and incident 0001. PL-01 cabinet heat accompanied by `SERVO-7024` is associated with Drive Overtemperature and incident 0002. Firmware updating and braking-resistor sizing are intentional out-of-scope test questions.
