# PlantAssist Synthetic Corpus

This folder contains synthetic maintenance and troubleshooting records for PlantAssist retrieval and evaluation. **Not for use on real equipment.** The plant, asset assignments, setpoints, events, measurements, outcomes, and procedures were written for this corpus; they were not taken from a former employer's or customer's internal documents. BW Papersystems, FlexPro, B&R Industrial Automation, and ACOPOS are real names used as public product context. No affiliation, certification, or verified knowledge of an actual FlexPro installation is claimed.

## Purpose

This corpus tests manual passage retrieval, informal technician wording, machine-specific fault matching, and answers to questions outside document coverage. The manuals and incident reports deliberately use realistic industrial language together with constructed site records. Operational limits and work steps in this corpus are not validated against physical equipment.

## Fictional Plant

The site is **North Quay Corrugated Test Plant**, a synthetic corrugated packaging facility. The finishing-line scenario is based conceptually on the BW Papersystems FlexPro flexo folder gluer and its publicly described feeder, die-cut, and folding sections. Asset names and axis allocation are constructed for evaluation, not verified BW Papersystems hardware configurations.

| Machine ID | Plant Asset Name | Equipment Contained | Synthetic Role |
| --- | --- | --- | --- |
| CP-01 | Case Packer 01 | Servo axes 1–4, photo-eyes, pneumatic cylinders, safety circuit | Legacy plant tag for the FlexPro-style finishing cell; the actual FlexPro product is a flexo folder gluer, not a conventional case packer |
| CV-03 | Infeed Conveyor 03 | Conveyor drive, photo-eyes | Feeds corrugated sheets toward CP-01 |
| PL-01 | Palletizer 01 | Servo axes, pneumatics, safety circuit | Handles completed bundles after the finishing cell |

In CP-01, Axis 1 is the feeder register, Axis 2 is bottom die-cutter synchronization, Axis 3 is the left folding-belt trim axis, and Axis 4 is the right folding-belt trim axis. In PL-01, Axis 1 is the bundle turner and Axis 2 is the layer hoist, the only vertical load-bearing axis with a holding brake. The drive designation is **SD-200**, with **B&R ACOPOS** as the public technology reference. SD-200 is not a B&R orderable model; manual metadata identifies **North Quay Training (fictional)** as the document manufacturer.

CV-03 is an **IC-600** flat-belt infeed conveyor that carries individual corrugated sheets to the CP-01 feeder. It has a VFD-driven 3.0 kW gearmotor, a screw take-up on the tail pulley, a tail-pulley speed sensor, belt-edge switches, and a discharge photo-eye. The IC-600 designation is fictional and does not refer to a real product.

Process photo-eyes use the fictional **PE-40** designation and are tagged by machine: `CV-03 PE1` (polarized retroreflective, CV-03 discharge), `CP-01 PE2` (diffuse with background suppression, feeder gate), `CP-01 PE3` (through-beam, folding-section exit count), and `PL-01 PE4` (diffuse with background suppression, bundle infeed). They are process sensors, not safety devices.

Pneumatic cylinders use the fictional **PC-63** system designation: `CP-01 CYL1` (feeder gate lift), `CP-01 CYL2` (counter-ejector bundle pusher), `PL-01 CYL3` (bundle stop gate), and `PL-01 CYL4` (layer squaring clamps). Each machine has its own shut-off valve, filter-regulator set to 5.5 bar, and a soft-start dump valve controlled by the safety circuit.

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

- The retrieval index includes every manual under `manuals/` and every incident report under `incidents/`; this README is for human review only and is excluded from ingestion.
- Manual front matter uses `document_id`, `title`, `document_type`, `equipment_type`, `manufacturer`, `model`, `version`, and `license`. Incident front matter uses `document_id`, `title`, `document_type`, `equipment_type`, `machine_id`, `alarm_code`, `occurred_on`, `version`, and `license`.
- Every `document_id` is unique. Versions are quoted semantic-version strings; dates use ISO `YYYY-MM-DD` notation. The license value `synthetic` is a corpus label, not an external legal license.
- All manual and Markdown-incident headings are unique within each file, unnumbered, in Title Case, and followed by meaningful prose. Preserve headings once evaluation questions use their chunk IDs.
- Manuals are named `<equipment_type>_manual.md` with a short `document_id` ending in `-manual-v1` (`servo-manual-v1`, `conveyor-manual-v1`, `photoelectric-manual-v1`, `pneumatic-manual-v1`). Incident filenames follow `inc-<prefix>-NNNN-short-kebab-description.md` or `.txt` inside `incidents/<equipment_type>/`, where the prefix is `servo`, `conv`, `pe`, `pneu`, or `safe`.
- Each equipment set includes at least one `.txt` incident with YAML front matter and a **plain-text body without Markdown headings** to exercise the TXT parser.
- Safety-critical steps in Markdown use the literal `**SAFETY:**` marker; TXT incidents use plain `SAFETY:`. Both represent `safetyCritical: true` after parsing. In manuals the marker introduces an instruction; in incident reports it introduces a past-tense record of the isolation that was applied.
- Every incident `alarm_code` appears in the alarm table of its equipment's manual.
- Values use metric units: current in A, voltage in V, power in kW, temperature in °C, distance in mm or m, speed in m/s, and time in s or ms. All operating numbers are constructed for evaluation.
- Records are historical examples, not universal repair advice. Resolving one incident does not prove another incident has the same cause.

## Coverage Gaps

These topics are deliberately outside the manuals. They provide evaluation cases for insufficient-information answers.

Servo drive manual:

- Servo-drive firmware updates and upgrade or rollback procedures.
- Fieldbus and network communication faults, topology, addressing, and protocol diagnostics.
- Complete drive-unit replacement and commissioning after a replacement.
- Braking-resistor selection and sizing calculations.

Conveyor manual:

- Belt splicing and re-splicing procedures (the incidents mention a belt contractor doing the work, without the method).
- VFD parameter programming, VFD replacement, and VFD fault codes.
- Gearbox oil grade and quantity (the manual refers to the gearbox nameplate), and gearbox overhaul.
- Changing conveyor speed recipes or line controller logic.

Photoelectric sensor manual:

- IO-Link master configuration and writing sensor parameters over IO-Link (the manual covers reading diagnostics and button teach only).
- Sensor connector pin assignments and wiring diagrams.
- Safety light curtains and safety-rated sensors (PE-40 sensors are not safety devices).
- Choosing a sensor or sensing mode for a new application, and fibre-optic sensors.

Pneumatic cylinder manual:

- Compressor house, air dryers, and main header maintenance.
- Dump valve function testing (referred to the safety circuit manual).
- Cylinder seal replacement and cylinder rebuild procedures.
- Sizing cylinders, valves, or supply lines for new applications, and valve manifold network configuration.

Actual BW Papersystems wiring, connector pinouts, product-specific torque values, electrical test points, safety-validation methods, and B&R model/firmware applicability are outside the corpus. These details are not established by the synthetic records.

## Files

Servo drive (`SERVO-7xxx`):

- `manuals/servo_drive_manual.md`: SD-200 operating, alarm, troubleshooting, and maintenance guide.
- `incidents/servo_drive/inc-servo-0001-following-error-after-maintenance.md`: CP-01 Axis 4 loose encoder connector after maintenance.
- `incidents/servo_drive/inc-servo-0002-drive-overtemperature.txt`: PL-01 cabinet-filter obstruction and drive heat-sink overtemperature.
- `incidents/servo_drive/inc-servo-0003-feeder-encoder-loss-after-cleaning.md`: CP-01 Axis 1 feedback cable crushed by a cable tray cover.
- `incidents/servo_drive/inc-servo-0004-folding-belt-trim-jam-overcurrent.md`: CP-01 Axis 3 overcurrent from trim waste jammed in the folding belt.
- `incidents/servo_drive/inc-servo-0005-hoist-motor-overtemperature-brake-drag.md`: PL-01 Axis 2 motor overtemperature from a partly released holding brake.

Conveyor (`CONV-2xxx`):

- `manuals/conveyor_manual.md`: IC-600 operating, alarm, troubleshooting, and maintenance guide.
- `incidents/conveyor/inc-conv-0001-belt-mistracking-after-belt-change.md`: CV-03 tail pulley out of square after belt replacement.
- `incidents/conveyor/inc-conv-0002-motor-overtemperature-blocked-fan-cover.txt`: CV-03 motor fan cover blocked by dust and trim.
- `incidents/conveyor/inc-conv-0003-belt-slip-take-up-at-limit.md`: CV-03 belt stretched past take-up range with worn lagging.
- `incidents/conveyor/inc-conv-0004-false-jam-misaligned-reflector.md`: CV-03 false jam from a knocked and dusty photo-eye reflector.
- `incidents/conveyor/inc-conv-0005-zero-speed-sheared-pulley-key.md`: CV-03 motor running with the belt stopped after a drive pulley key sheared.

Photoelectric sensor (`PE-3xxx`):

- `manuals/photoelectric_sensor_manual.md`: PE-40 sensing modes, indicators, alarms, troubleshooting, cleaning, alignment, and teach-in.
- `incidents/photoelectric_sensor/inc-pe-0001-folder-count-chatter-loose-bracket.md`: CP-01 PE3 double counts from a vibrating bracket.
- `incidents/photoelectric_sensor/inc-pe-0002-low-margin-tape-reflector.txt`: CV-03 PE1 low margin after reflective tape replaced the corner-cube reflector.
- `incidents/photoelectric_sensor/inc-pe-0003-feeder-missed-sheets-wrong-teach.md`: CP-01 PE2 missed black sheets after a teach on the product.
- `incidents/photoelectric_sensor/inc-pe-0004-bundle-sensor-low-sun-interference.md`: PL-01 PE4 false detections from low afternoon sun.
- `incidents/photoelectric_sensor/inc-pe-0005-folder-sensor-cable-chafed-short-circuit.md`: CP-01 PE3 cable chafed through at a guard hinge.

Pneumatic cylinder (`PNEU-4xxx`):

- `manuals/pneumatic_cylinder_manual.md`: PC-63 air preparation, valves, position sensors, alarms, troubleshooting, and maintenance.
- `incidents/pneumatic_cylinder/inc-pneu-0001-pusher-extend-timeout-sensor-moved.md`: CP-01 CYL2 timeout with the cylinder fully out; the sensor had been knocked along its slot.
- `incidents/pneumatic_cylinder/inc-pneu-0002-layer-clamps-slow-clogged-silencers.txt`: PL-01 CYL4 slow retract from a dust-clogged exhaust silencer.
- `incidents/pneumatic_cylinder/inc-pneu-0003-low-pressure-undersized-supply-hose.md`: CP-01 pressure dips from an 8 mm replacement supply hose.
- `incidents/pneumatic_cylinder/inc-pneu-0004-excess-air-consumption-hidden-leaks.md`: PL-01 idle flow nearly four times baseline from three hidden leaks.
- `incidents/pneumatic_cylinder/inc-pneu-0005-feeder-gate-retract-timeout-water-in-valve.md`: CP-01 CYL1 valve spool stuck by water from a jammed condensate drain.

## Suggested Retrieval Checks

- CP-01 Axis 4 dropping out during acceleration → Following Error and incident servo-0001.
- PL-01 cabinet heat accompanied by `SERVO-7024` → Drive Overtemperature and incident servo-0002.
- A feeder "jam" with no board stuck and the position frozen → Encoder Feedback Loss and incident servo-0003, not a mechanical jam.
- Deliberate overlaps, where the right equipment must rank first:
  - Overheating caused by dust: a hot servo drive heat sink with a cool motor (servo-0002) vs a hot conveyor motor with a normal VFD heat sink (conv-0002).
  - Motor overheating: servo hoist brake drag with raised current (servo-0005) vs conveyor motor cooling with normal current (conv-0002).
  - Alarms that blame the wrong thing: `SERVO-7021` raised after feedback loss (servo-0003), and `CONV-2008` Product Jam raised by a misaligned reflector (conv-0004).
  - The same sensor, two causes: CV-03 PE1 false jams from a knocked, dusty reflector (conv-0004) vs a tape reflector with low margin (pe-0002).
  - Fixes that did not help: lengthening an input filter (pe-0001), cleaning a clean lens (pe-0003), re-teaching a correctly taught sensor (pe-0004), replacing a healthy sensor (pe-0005), raising the regulator (pneu-0001, pneu-0003), opening flow controls (pneu-0002), replacing a healthy valve coil (pneu-0005).
  - Sensors knocked out of position: a photo-eye bracket (pe-0001, conv-0004) vs a cylinder position sensor (pneu-0001).
  - Dust slowing things down: a clogged exhaust silencer (pneu-0002) vs blocked cooling (servo-0002, conv-0002).
- Answerable only from an alarm table row, with no troubleshooting section: for example `SERVO-7028` DC Bus Overvoltage, `CONV-2011` VFD DC Bus Undervoltage, `CONV-2012` Gearbox Overtemperature.
- Out of scope: SD-200 firmware updates, braking-resistor sizing, CV-03 belt splicing method, VFD parameter programming, gearbox oil grade, IO-Link parameter writing, sensor pinouts, safety light curtains, compressor and dryer maintenance, cylinder seal replacement.
