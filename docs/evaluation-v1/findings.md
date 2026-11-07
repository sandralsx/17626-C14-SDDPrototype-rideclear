# V1 technical findings — Step 4

AI-authored technical findings supported by actual deployed interactions. This document is not a personal reflection, Learning Log, or a response to Step6 questions. Classification follows assignment Step4: an implementation defect violates an already clear V1 requirement; a requirements issue exposes missing/ambiguous/insufficient specification needed for the stakeholder goal. Proposed next actions have not been performed.

## ID-01 — Acknowledgement removes keyboard focus

**Classification: Implementation defect.** Affects FR-006 / A3-G06; supporting stakeholder evidence SD25 and SJ34. Existing AS-16 requires updates without moving focus away from a control. The frozen UI contract explicitly says “Updates preserve active control and unsent form fields.” The requirement already exists; discovering this does not create a new requirement.

**Reproduction observed:** create/deliver a notice in dispatch, switch to Rider, click Rider to set a known focus origin, press Tab four times until ack-N7 is active, then press Return. The acknowledgement succeeds, the button disappears and activeElement becomes BODY with an empty ID. [Before/after focus JSON](evidence/EV20-focus.json) and [fresh resulting AX tree](evidence/EV20-keyboard-focus-confirmed.txt) preserve the actual transition. EV07 independently showed the same loss for N1. Draft focus survives a different-tab update in EV23, so the defect is specifically meaningful when the active control is removed.

**Code:** frontend/app.js L62–66 conditionally removes the acknowledgement control; render L93–106 replaces content; restoreFocus L27–30 returns if the prior ID no longer exists. There is no focus destination in that path. This source explanation is consistent with the observation; no general WCAG failure certification is inferred.

**Required correction:** in a later code revision, preserve a stable acknowledgement element/state or assign focus to an appropriate persistent control after completion. Verify keyboard continuation and announcement without resetting to BODY. Existing spec is sufficient to require correction; clarify fallback behavior in its acceptance scenario if needed. Do not relabel this as a requirements-only finding.

## RQ-01 — Elapsed or stale ETA can still imply usable current information

**Classification: Requirements issue (insufficient freshness/elapsed-estimate semantics).** Affects FR-002/FR-007 and A3-G02/G07; SJ31 asks for live status/updated ETA, SJ34 prioritizes reliable accurate return information. D10 and U02/U03 already preserve uncertainty; evaluation now demonstrates its consequence.

**Reproduction observed:** reset normal trips; set service clock to17:35; select Return without publishing a new ETA. Page shows Latest estimated arrival17:15, Estimate updated at08:40, Scheduled, and Within pickup window despite the17:00–17:30 window already having ended. [EV26](evidence/EV26-stale-without-update.txt). A second path changed a delayed ETA to17:20 at17:35: the page issued “Your estimate is back within the window.” [EV12 text](evidence/EV12-recovery-past-estimate.txt), [screenshot](evidence/EV12-recovery-past-estimate.jpg). This is not proof a vehicle actually arrived late or that the rider interpreted the screen in a particular way.

**Why requirements-level:** tripCondition (domain.js L25–31) only compares saved ETA with window bounds, as V1 specifies. FR-012 expressly allows an ETA earlier than now, and PA-02 defines no numeric freshness SLA. Neither rule says when the displayed estimate stops being usable or how a recovery must account for elapsed time. Adding a new age threshold and calling the old code defective would invent a rule after testing.

**Needed spec change before code:** distinguish last recorded estimate, estimate usability, operational status and window compliance. Specify what happens when now exceeds an unfulfilled ETA, and when estimate age is excessive; prevent a recovery message from implying a usable future pickup if the estimate has elapsed. Retain the original window and last recorded time; do not silently turn an estimate into an actual arrival.

**Stakeholder clarification:** agree the acceptable age/refresh expectation, treatment of uncertainty and rider/dispatcher follow-up responsibility. No arbitrary one-minute or five-minute SLA is established here. A deterministic elapsed-time case can be specified separately from an unconfirmed numeric age threshold. Later validation should repeat EV26/EV12 and check boundaries/terminal states; this is a Step5 candidate, not an implemented revision.

## RQ-02 — Early discovery and timely delivery lack a common success definition

**Classification: Requirements issue (ambiguity/insufficient timing outcome).** Affects FR-003, A3-G03 and its dependency on G08. SJ21 requests an update before the pickup window expires; SF25 distinguishes delivered/acknowledged communication.

**Reproduction observed:** Return window17:00–17:30; at16:50 save ETA17:45. N1 is created/sent by Email. Advance clock to17:35 and mark delivered. Rider card shows Delivered adjacent to16:50 and says identified before window end. Dispatch history separately records sent16:50, delivered17:35, acknowledged17:35 after the explicit action. [EV06 rider text](evidence/EV06-delivery-after-window.txt), [screenshot](evidence/EV06-delivery-after-window.jpg), [EV17 dispatch history](evidence/EV17-change-confirmed.txt). Thus delivery is late in this synthetic sequence, even though discovery was early. The UI does not claim the rider acknowledged at16:50; the problem is ambiguous timing presentation and missing goal-level deadline result.

**Why requirements-level:** AS-05 says “identified/notified before the window ended”; FR-003 and PA-01 operationalize the early flag using discovery time, while FR-015 says acknowledgement cannot retroactively make a late notice early. The spec preserves individual outcomes but does not define which event establishes success for the before-window stakeholder goal, or require an explicit delivery-deadline result. domain.js addNotice L58–63 and app.js noticeBody L56–60 implement that discovery interpretation. riderNotices L66 places creation time beside the latest outcome; dispatchCommunications L86 shows the separate actual times. These rules are implemented, but remain insufficient/ambiguous for the traced goal. This is not an invented real-provider failure.

**Needed spec change before code:** label identified/sent/delivered/acknowledged times explicitly; define separate discovery-before-deadline and communication-before-deadline outcomes. An unreceived sent message must not count as proven timely rider receipt. Show unknown/pending and late delivery honestly, preserving original timestamps and history. Clarify a manual follow-up/escalation responsibility when the deadline is missed.

**Stakeholder clarification:** for each mock/real channel, determine the minimum event that counts as having informed the rider (provider delivery versus explicit acknowledgement), and any escalation deadline. Delivery is not necessarily comprehension. No new automatic hold/cancel rule is authorized. Later tests should include early send/late delivery, sent-only at the deadline, early delivery/later acknowledgement and late discovery. Step5 must revise the spec first.

## Findings not asserted

Mocks, a same-browser scope, manual ETA input and lack of real booking/route/finance integration were deliberate declared boundaries, not newly discovered bugs. No physical ETA accuracy score is claimed. Exact375px,200% zoom and assistive-technology checks remain unverified coverage items, not fabricated observed failures. The 17 passing domain/store tests do not cover the disappearing-control focus path.
