# Step 4 — Evaluate frozen V1

The deployed V1 was actually exercised on 2026-11-07. The resulting technical package contains the required Interview → Goal → Spec → Code/behavior → Satisfaction trace and distinguishes implementation defects from requirements issues.

**Outcome:** four of eight selected requirements are Fully satisfied and four Partially satisfied against their traced goals. Three material findings were observed: one implementation defect and two requirements issues. The existing 17 automated tests passed; they do not cover or invalidate the observed UI focus defect.

- [RTM, all eight selected requirements and derived safeguards](../traceability-v1.md) · [CSV](../traceability-v1.csv)
- [Actual execution record and acceptance coverage](test-execution.md)
- [Technical findings and required next actions](findings.md)
- [Checked interview references](interview-evidence.csv)
- [Frozen baseline and asset hashes](baseline.json)
- [Evidence catalog](evidence-index.md) · [raw capture records](evidence/records.json) · [regression output](regression-output.txt)

## Scope and method

Evaluation used the publicly deployed RideClear V1 in the ChatGPT in-app browser, interacting with actual controls. Only fictional browser-local trips/messages were changed. Both rider and dispatcher views were used; a second same-origin tab tested shared revision/draft behavior. Keyboard Tab/Return was used to reproduce acknowledgement focus loss. Source inspection and existing Node tests supplement those UI observations.

All example times in observations are explicit **simulated Eastern service-day times** on2026-11-07. records.json timestamps are wall-clock UTC capture times. Neither represents a real passenger or provider event.

The evaluated tag resolves to4e3997c26cfd9792dcdb0e12a1c659b1cb3e0df0; the deployment build source is3b3a21755bdc5bef8946f289d26e4f6c7099896a. Step4 adds documentation/evidence only. Model, V1 spec, plan/tasks, app, v1 tag and deployment remain unchanged. A reset at the end restored fictional fixtures, then advanced the clock to17:35 to leave the stale-ETA observation reproducible; it did not change application code.

## Evidence limits

These are agent-executed technical observations, not a stakeholder usability study or confirmation. No real delivery, ETA prediction accuracy, transport punctuality, multi-device synchronization, GPS or production integration was evaluated. Temporary-storage behavior and several boundaries were checked through existing unit tests rather than simulated browser failure.

The browser viewport override requested375px, but the actual measured innerWidth was323px (document/body308px). A second outer request did not change this measurement. The observed narrow page did not overflow horizontally, but **the exact375px acceptance check is not verified**. 200% browser zoom, actual screen-reader speech, voice/switch operation and full contrast/WCAG compliance were not verified. They are not counted as passes.

Some early DOM snapshots retained older accessible heading names, and EV14/EV16 captured a previous render. They are retained as raw records but are not independent evidence of terminal-state or accepted-change success. Fresh native accessibility captures EV17 and EV22 confirm those outcomes. EV21 records a stale-form rejection, not a saved terminal state. Evidence integrity takes precedence over the intended action notes.

## Authorship boundary

This package is AI-authored technical work for Step4. The assignment PDF p5 permits AI assistance except Learning Log authorship and requires Step6 examples/answers without AI assistance. No learning-log.md, personal learning narrative or Step6 answers have been written. The student must independently inspect the prototype and form/write their own evaluation and reflection. This package does not complete the whole assignment or Step5.

Baseline hashes record working-copy bytes and canonical LF text separately. Git archive can normalize tracked text line endings; that conversion is not a V1 source edit. Raw browser evidence is preserved byte-for-byte with scoped Git attributes.
