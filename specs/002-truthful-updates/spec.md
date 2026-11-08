# Feature Specification: V2 truthful estimates and communication timing

**Branch:** codex/a3-v2 · **Date:** 2026-11-07 · **Status:** revised specification before implementation

Input: Step4 deployed-V1 findings RQ-01, RQ-02 and ID-01 in [findings](../../docs/evaluation-v1/findings.md). The original [V1 spec](../001-trip-status/spec.md) and immutable v1 tag remain preserved. This is an AI-assisted technical revision, not Learning Log authorship. No new stakeholder interview or approval is claimed.

## User Scenarios & Testing

### US-V2-1 — Know whether the recorded ETA is still usable (P1)

Janelle asks for live status and reliable updated return information (SJ31/34). V1 displayed ETA17:15 as Within pickup window at17:35 (EV26), and announced recovery to an elapsed17:20 ETA (EV12). Showing the last input is insufficient to imply current usability.

- **AS-18:** Given normal Return17:00–17:30, ETA17:15, last update08:40, when clock advances to17:35 and status is not arrived/completed, show **Estimate needs updating** and **Last recorded estimated arrival17:15** with the original as-of time/window. State that arrival is not confirmed and direct the rider to contact dispatch. Do not claim within-window arrival, guarantee a pickup, infer actual arrival or generate a backdated notice. Clock-only change derives presentation without fabricating an event.
- **AS-19:** At now17:35, changing delayed ETA17:45 to17:20 must create an estimate-needs-update event, never a recovery event. A usable17:25 ETA at now17:20 may produce recovery; original notice snapshots remain unchanged.
- **AS-20:** At now equal to ETA the estimate has not yet elapsed; at now greater than ETA it has. Unknown remains unknown. Arrived/completed take precedence and the old ETA remains explicitly historical. Each leg is evaluated independently, and a saved window is immutable.

### US-V2-2 — Distinguish early discovery from recorded delivery (P1)

SJ21 requests notice before the pickup window expires. SF25 asks to distinguish delivered and acknowledged communication. V1 N1 was created16:50 but delivered17:35 after17:30 end (EV06/17); its rider card displayed an unlabeled16:50 beside Delivered.

- **AS-21:** Create Return delay at16:50, window end17:30, mark delivered17:35. Show labeled **Identified16:50**, **Sent16:50**, **Delivered17:35**, **Acknowledged: not recorded** on rider and dispatch views. Display early discovery separately from **Delivery recorded after window end · follow-up needed**. The delivery result must not use creation time.
- **AS-22:** A sent-only delay before17:30 says delivery not yet recorded and deadline pending. At17:30 with no delivery record, say **No delivery recorded before window end · follow-up needed**. Delivery exactly at17:30 is not before the end. Do not invent received/acknowledged facts or automatically cancel/hold a ride.
- **AS-23:** Delivery17:20 followed by acknowledgement17:35 remains delivery recorded before end. Acknowledgement is independently timed and is not proof of comprehension. Sent alone is not delivery. Retry preserves the old unreachable attempt, its channel and timestamps; the new attempt uses the current preference. Both views expose the complete labeled attempt history and identical timing result.

### US-V2-3 — Keep keyboard context after acknowledgement (P1 defect correction)

SD25 and SJ34 support accessible independent use. Existing V1 AS-16 and UI contract already required preserved focus; ID-01 violates them.

- **AS-24:** Focus delivered-notice Acknowledge using Tab, activate Return. The action succeeds once, its stable control remains focusable and labeled **Update acknowledged**, marked aria-disabled=true. Focus stays on that same control. Re-activation makes no new write or timestamp; the next Tab continues to the next operable control. Announce success through the persistent polite status region. This corrects an existing implementation defect rather than claiming a new stakeholder need.
- **AS-25:** A same-origin update preserves an active contact draft/focus, and a stale submission is rejected. Existing V1 window, unknown, acceptance-gate, receipt, history, reload, temporary-mode and no-real-action requirements remain in force. V2 storage is separately named; V1 sessions, deployment and tag remain untouched.

## Requirements

Stable V1 FR-001..016 / R-01..08 and their acceptance scenarios remain applicable except the explicit changes below; the new rules take precedence where a V1 paragraph conflicts. V1 files are historical baseline, not the active V2 rules.

| Spec ID | V2 rule / revision | Goal / evidence / finding | Acceptance |
| --- | --- | --- | --- |
| FR-001 | Retain immutable leg-specific window distinct from ETA. | G01; SJ31 | AS-01/02/04/20 |
| FR-002 revised | Show operational status, ETA/as-of and its usability using FR-017; elapsed estimate must not imply usable current pickup information. | G02; SJ31/34; RQ-01 | AS-18..20 |
| FR-003 revised | Keep distinct delay discovery notice; distinguish discovery-before-end from recorded-delivery-before-end via FR-018. AS-05's former identified/notified wording means discovery only, never proven rider receipt. | G03/G08; SJ21/SF25; RQ-02 | AS-05/06/21..23 |
| FR-004/005 | Retain mock contact/receipt, reviewed-only workflow, shared revisions and stale rejection. | G04/G05; SJ21/SF31 | AS-13..15/17/25 |
| FR-006 clarified | Correct existing focus preservation using FR-019; retain labels, text states, announcements and scoped accessibility checks. | G06; SD25/SJ34; ID-01 | AS-16/24/25 |
| FR-007 revised | Demonstrate reliable interpretation of Return information via G02 usable estimate and G03 honest delivery timing. No field prediction-accuracy claim. | G07; SJ14/34; RQ-01/02 | AS-18/21 |
| FR-008 | Retain mock preferred-channel acceptance, outcome separation and retry history. | G08; SF21/25/36 | AS-09..12/23 |
| FR-010 revised | No-op unchanged ETA/status. Changed ETA creates at most one event in priority: known-to-unknown unavailable; recorded ETA>end delay; other elapsed ETA estimate-needs-update; usable transition from delayed ETA recovery; otherwise accepted change. Never call an elapsed estimate recovered. Clock-only changes create no notice. | G02/G03/G08; D04/D05/D10 | AS-07/08/19 |
| FR-012 clarified | Keep valid service-day times, monotonic clock and1–500 trimmed contact limit. An ETA may be earlier than now but then is explicitly last-recorded/unusable under FR-017, never an actual arrival. | G02/G04; RQ-01 | AS-18..20 |
| FR-015 clarified | Retain snapshots and historical attempts. Timing presentation is derived from recorded event timestamps and current explicit demo clock; subsequent acknowledgement cannot rewrite delivery/discovery timing. | G03/G08; RQ-02 | AS-21..23 |
| **FR-017 new** | For nonterminal legs with known ETA, now>ETA means elapsed: show Estimate needs updating, last recorded ETA, as-of, arrival not confirmed and contact-dispatch direction. Do not display a current within-window/ahead/delayed prediction badge in place of this usability warning. Unknown/terminal retain their meanings. now=ETA is not elapsed. Do not infer a numeric freshness SLA. | G02 supports G07; SJ31/34; RQ-01 | AS-18..20 |
| **FR-018 new** | Label discovery/creation, every attempt's sent, delivered, acknowledged and unreachable times; absent timestamps say not recorded. For delay notices, strict <windowEnd is before. Separately derive early/late discovery and delivery recorded before/at-or-after end, or pending/no recorded before-deadline evidence. Missed deadline or unreachable requires manual follow-up, with no automatic ride decision. Both views use the same result. | G03 depends on G08 delivery evidence; SJ21/SF25; RQ-02 | AS-21..23 |
| **FR-019 clarification** | Acknowledge retains a stable, focusable named control after success; aria-disabled state prevents duplicate actions. Next keyboard navigation remains logical; persistent live region announces the result. | G06 constrains G03/G08; SD25/SJ34; ID-01 | AS-24 |

FR-009 fictional-only, FR-011 immutable snapshots, FR-013 manual decisions, FR-014 persistence/temporary warning and FR-016 preserved engineering chain remain unchanged. Nothing adds real providers, GPS prediction, automatic rescheduling, accounts or finance integrations.

## Assumptions, dependencies and unresolved questions

- **V2-PA-01 (engineering interpretation, unconfirmed):** elapsed means now>ETA for a nonterminal leg. No one-minute/five-minute age limit is invented. A future ETA may still be stale: numeric update-age SLA, confidence and refresh ownership remain **U02/U03**, unresolved. Always retain as-of. This revision handles elapsed estimates, not all freshness uncertainty.
- **V2-PA-02 (engineering interpretation, unconfirmed):** recorded delivery before the window end is a minimum observable delivery-evidence indicator, **not proof the person was informed or understood**. Acknowledgement remains separate. Exact operational success/receipt criteria by channel and escalation responsibilities remain **U01/U04** for stakeholder clarification. UI says recorded delivery rather than goal achieved.
- **V2-PA-03:** a missing delivery record at the deadline demands manual follow-up; it does not prove a real person did not receive something. Retry/history remain explicit mock events.
- **D03 reviewed:** a late discovery cannot be made early; preserve timestamps and expose missed communication evidence. **D04/D05:** viewing ETA is separate from notification, and delay does not wait for driver acceptance. **D08:** focus constrains the complete rider notice journey. **D10 revised:** rapidly displaying the last input alone is insufficient; usability and truthful history qualify interpretation. **D12:** contacting dispatch never approves a new schedule.
- Original model conflicts (including cost/scope and J:G-60 versus G-62), all source IDs, exclusions and U01..06 remain in the retained model. No conflict was silently deleted or stakeholder agreement fabricated.

## Success Criteria

- SC-V2-01: both recorded RQ-01 sequences display elapsed information and never false recovery; equality/unknown/terminal boundaries pass.
- SC-V2-02: early-send/late-delivery, sent-only at deadline, exact-end delivery, early-delivery/later-ack and retry all display truthful separate times/results in both views.
- SC-V2-03: keyboard acknowledgement retains focus and does not repeat writes; peer drafts remain intact and stale submissions reject.
- SC-V2-04: V1 remains independently accessible; V2 has separate URL and preserved Git tag/history, with source/spec/plan/model and evidence. Unverified accessibility or field-accuracy claims remain explicitly limited.
