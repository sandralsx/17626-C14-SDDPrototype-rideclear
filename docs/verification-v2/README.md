# V2 technical verification — Step5

AI-assisted engineering record; no student Learning Log or Step6 answers. The original deployed-V1 evidence remains unchanged in [evaluation-v1](../evaluation-v1/README.md).

**Specification first:** revised spec/model/plan/tasks were committed as624261a5e9ffa702e174b44836994249b4593d14 before the implementation files changed. [Revised spec](../../specs/002-truthful-updates/spec.md), [plan](../../specs/002-truthful-updates/plan.md), [goal model](../goal-model-v2.md), [RTM](../traceability-v2.md).

## Automated checks

The existing17 domain/store tests plus8 new requirement-boundary tests pass: **25 passed,0 failed**, Node24.22.1, exit0. [Raw output](regression-output.txt). New cases cover elapsed estimate interpretation, exact ETA/terminal/unknown boundaries, no false recovery, late/exact-end delivery, deadline without evidence, early delivery/later acknowledgement, retry and deterministic fixtures. These test externally required outcomes, not the DOM implementation. Existing tests were adapted only to pass explicit demo time into the status query.

[Pre-implementation output](pre-implementation-test.txt) records an expected module import failure because the newly specified noticeTiming export did not yet exist. It does not claim8 individual red assertions were executed. Syntax check and static build also passed; only five application assets are public. The local preview initially timed out under sandbox networking; an elevated preview on4183 worked. This was an environment limitation, not an app defect.

## Actual browser verification

In-app browser, actual controls, explicit fictional Eastern service-day time. Fresh native accessibility captures and wall-clock UTC times appear in [records.json](evidence/records.json). Source/read-only DOM queries measured focus/layout; no hidden storage mutation or injected outcome was used.

| Evidence | Observed result / requirement |
| --- | --- |
| V2E01 | Return ETA17:15 at17:35 displays Estimate needs updating, Last recorded estimated arrival, as-of08:40 and arrival-not-confirmed/contact guidance. No fabricated arrival/history. FR-017. |
| V2E02 | Delay identified/sent16:50, delivered17:35: early discovery is separate from at/after-end delivery and manual follow-up. All timestamps labeled. FR-018. |
| V2E03/04 + focus JSON | Tab/Return acknowledgement keeps ack-N1 focused; label Update acknowledged, aria-disabled=true; repeated Return leaves revision3 unchanged; next Tab reaches contact-message. FR-019. |
| V2E05 | Revising delayed17:45 to past17:20 at17:35 creates an estimate-needs-update event and warning, not recovery. Revised FR-010. |
| V2E06 | Sent-only before17:30 deadline remains pending without claiming delivery. |
| V2E07 | At exact17:30 without delivery record, manual follow-up is shown. |
| V2E08 | Delivery exactly17:30 is at/after end, never before. Original sent16:50 retained. |
| V2E09 | Delivery17:20 stays before end after acknowledgement17:35. Distinct evidence/times retained. |
| V2E10 | Unreachable SMS attempt remains; retry uses current Phone preference and starts sent-only. |
| V2E11/12 | Peer update retains contact draft and focus; stale submission rejects without adding a request. |
| V2E13 | Reload retains V2 revised data/history and revision. |
| V2E14 | Requested375x812, but measured innerWidth1280/clientWidth1265/scrollWidth1265. No overflow at actual desktop width; **exact375px is unverified**. Screenshot filename is an attempted viewport check, not proof of mobile sizing. |

This is a technical repeat of the actual V1 failure paths, not stakeholder acceptance. No real SMS/phone/email, field ETA accuracy or transport punctuality was tested. Actual screen-reader speech,200% zoom, full contrast/WCAG certification and exact375px remain unverified. Future-but-old ETA remains a requirements question (U02/U03); recorded delivery does not prove understanding (U01/U04).

## Preservation and publication

V1 tag and source/spec/model remain independently preserved. V2 is a descendant in the same private GitHub repository and has a separate Site identity, URL and browser state keys. Only frontend assets are copied to the V2 hosting source; interview/model/PDF evidence is not part of public assets. Final publication provenance and deployed smoke evidence are recorded in [release-v2](../release-v2.md) when the native deployment completes.


## Published-page checks

Native deployment status succeeded at2026-11-08T02:50:27.915568Z. V2E15 confirms elapsed interpretation on the public URL; V2E16 confirms separate late-delivery timing; V2E17 focus JSON confirms the stable acknowledged control. V2E18 confirms V1 remains accessible and unchanged in title/observed state. Both URLs were read in the browser; V1 received no state-changing action. [Public V2 proof screenshot](evidence/V2E17-deployed-proof.jpg). The local preview was stopped after online checks.
