# V2 technical requirements change register

This is a technical change register, not student-authored decisions/reflection or a Step6 answer. It records requirement IDs and implementation/verification obligations.

| Change | V1 evidence and classification | V2 spec/model impact | Implementation and verification | Remaining uncertainty |
| --- | --- | --- | --- | --- |
| V2-CR01 | RQ-01 / EV12,26; requirements insufficiency | FR-017 new, FR-002/007/010/012 revised; AS-18..20; G02-U supports G07, D10 refined | tripCondition(trip,now) and elapsed notice priority; V2E01/05; elapsed/equality/unknown/terminal tests | Future-but-stale age SLA and refresh responsibility U02/U03 remain unconfirmed. No numeric threshold invented. |
| V2-CR02 | RQ-02 / EV06,17; requirements ambiguity/insufficiency | FR-018 new, FR-003/015 revised; AS-21..23; G03 discovery and delivery evidence split, G08 dependency retained | noticeTiming, shared labeled attemptHistory, strict-before comparison; V2E02/06..10 and deadline tests | Channel-specific informed/understood success, escalation owner/timing U01/U04 remain open. Delivery is recorded evidence only. |
| V2-CR03 | ID-01 / EV20; implementation defect against existing focus requirement | FR-019 clarification, AS-24; G06 constraint preserved | Stable native ack control and aria-disabled guard; V2E03/04 focus JSON and actual next-Tab continuation | Full accessibility certification is not claimed; other unverified checks remain. |

V2-CR01 and V2-CR02 are meaningful requirements-level improvements driven by V1 evaluation; neither is merely a UI rename or a code fix. V2-CR03 is kept separately as correction of an already specified behavior. No additional stakeholder interview, approval, receipt comprehension or physical arrival has been invented. Revisited D03/04/05/08/10/12 and preserved conflicts/assumptions are in goal-model-v2.md and the revised spec.
