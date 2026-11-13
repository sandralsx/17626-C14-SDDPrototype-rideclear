# V2 requirements traceability — Step5

AI-assisted technical assessment, not a student Learning Log. The same eight selected requirements retain interview/original-goal provenance from [V1 RTM](traceability-v1.md), [checked excerpts](evaluation-v1/interview-evidence.csv) and [source crosswalk](source-crosswalk.csv). CSV record numbering uses header=1. All original evidence is private and preserved; other members' original transcripts remain unavailable, as stated in V1. No new stakeholder facts are asserted.

**Goal satisfaction** below remains broader than literal mock-spec conformance. Four selected goals are Fully satisfied in bounded scope and four Partially satisfied because remaining stakeholder/quality evidence is unresolved. This does not conceal the V2 improvements: the three revised technical behaviors are separately verified below. [Spec](../specs/002-truthful-updates/spec.md), [model](goal-model-v2.md), [change register](v2-requirements-change-register.md), [verification](verification-v2/README.md), [CSV](traceability-v2.csv).

| Requirement | Goal / original IDs | Interview support | Active V2 spec | Code component / behavior | Actual verification | Goal satisfaction | Scope / unresolved limits |
| --- | --- | --- | --- | --- | --- | --- | --- |
| FR-001/R-01 | A3-G01; S:G-7,Q:G-22 | SJ31;2026-10-27T14:03:08.818Z | FR-001 retained; AS-01/02/20 | frontend/app.js renderLegs/tripPanel; domain updateTrip | V1 EV01..04; V2E01/05/11; immutable-window regression | Fully satisfied | Original window retained through elapsed/delay/peer updates. |
| FR-002/R-02 + FR-017 | A3-G02; S:G-8,J:G-15/16/20,Q:G-23 | SJ31/34; SJ34 timestamp2026-10-27T14:04:06.720Z | FR-002/012 revised, FR-017; AS-18..20 | domain tripCondition(trip,now); app tripPanel | V2E01/05; elapsed/equality/unknown/terminal tests | Partially satisfied | Elapsed-case insufficiency addressed and revised rules verified. Future-estimate age SLA/U02/U03 remains open; no true GPS accuracy evidence. |
| FR-003/R-03 + FR-018 | A3-G03; S:G-9,J:G-17,Q:G-26/27 | SJ21;2026-10-27T14:00:39.816Z; SF25 | FR-003/010/015 revised, FR-018; AS-19/21..23 | domain noticeTiming/updateTrip; app noticeBody/attemptHistory | V2E02/05..09; strict-deadline tests | Partially satisfied | Discovery and recorded-delivery timing now independent; no false early receipt claim. Stakeholder-informed/understood/channel SLA U01/U04 unconfirmed. |
| FR-004/R-04 | A3-G04; S:G-10 | SJ21/23; SJ23 timestamp2026-10-27T14:01:17.258Z | FR-004 retained; AS-13/14/25 | domain contact/reviewRequest; app contactPanel/dispatchRequests | V1 EV08..10; retained domain validation tests; V2E12 | Fully satisfied | Mock receipt/review/no-reschedule behavior retained; stale request rejected. |
| FR-005/R-05 | A3-G05; S:G-23,J:G-29/31/32..35,partial Q:G-89 | SF27/31/33; SF31 timestamp2026-10-28T09:18:24.415Z | FR-005/014 retained; AS-15/17/25 | store createStore/commit; app subscription/drafts | V2E11..13; existing storage/stale/failure tests | Fully satisfied | Shared origin/profile scope retained, draft/focus preserved, stale overwrite prevented, reload persists. Production sync remains excluded. |
| FR-006/R-06 + FR-019 | A3-G06; S:G-31,partial S:G-12/Q:G-12 | SD25;2026-10-28T09:31:53.662Z; SJ34 | FR-006 clarified, FR-019; AS-16/24 | app riderNotices/restoreFocus and guarded acknowledgement | V2E03/04 focus JSON, V2E11; V2E14 viewport limitation | Partially satisfied | Observed acknowledgement defect corrected; same control retains focus and no-op reactivation. Exact375px,200% zoom/screen-reader/full contrast unverified. |
| FR-007/R-07 | A3-G07 softgoal; S:G-14,partial Q:G-6 | SJ14/18/34; SJ14 timestamp2026-10-27T13:59:32.222Z | FR-007 revised; AS-18/21 | Return fixture; tripCondition; noticeTiming and leg-filtered UI | V2E01/02/05/09 | Partially satisfied | Return usability/timing improved by both requirements changes; fictional inputs do not validate real prediction accuracy or punctuality. |
| FR-008/R-08 | A3-G08; S:G-22/24 | SF21/25/36; SF25 timestamp2026-10-28T09:17:02.911Z | FR-008 retained, FR-018; AS-09..12/23 | domain sendChange/setOutcome/retryNotice; shared attemptHistory | V1 EV15/17..20; V2E02/03/09/10; acceptance/outcome tests | Fully satisfied | Preferred-channel mock attempts retain separate sent/delivered/ack/unreachable times and retry history; no real-channel claim. |

## Revised technical requirements

| ID | Finding trace → requirement → implementation → actual result | Revised-spec satisfaction |
| --- | --- | --- |
| FR-017 | RQ-01/EV12,26 → AS-18..20 → tripCondition/elapsed event → V2E01/05 and boundary tests: elapsed warning, last ETA/as-of retained, no false recovery | Fully satisfied for explicit elapsed rule; age-SLA uncertainty is retained rather than claimed solved. |
| FR-018 | RQ-02/EV06,17 → AS-21..23 → noticeTiming/shared attemptHistory → V2E02/06..10: early discovery/late delivery, exact-end, missing record, early delivery/later ack and retry all distinguish event times | Fully satisfied for truthful recorded timing; actual informed/understood goal is not asserted. |
| FR-019 | ID-01/EV20 → existing focus contract clarified AS-24 → stable ack control/guard → V2E03/04: focus stays ack-N1, next Tab contact-message, repeat Return revision unchanged | Fully satisfied for observed keyboard defect correction; not a new requirements-level improvement by itself. |

FR-009/011/013/014/016 retain fictional-only operation, immutable snapshots, manual decisions, labeled storage mode and preservation. Existing25 passing tests cover the inherited domain/store invariants together with new requirements; live UI evidence supplements those tests. V1 Step4 results are historical and are not overwritten with V2 satisfaction.

## Immutable V2 implementation anchors

- [export function tripCondition](https://github.com/sandralsx/17626-C14-SDDPrototype-rideclear/blob/89d49042a599c1c1ef0eb2ae0b4c8a41976468ce/frontend/domain.js#L25)
- [export function noticeTiming](https://github.com/sandralsx/17626-C14-SDDPrototype-rideclear/blob/89d49042a599c1c1ef0eb2ae0b4c8a41976468ce/frontend/domain.js#L36)
- [export function applyCommand](https://github.com/sandralsx/17626-C14-SDDPrototype-rideclear/blob/89d49042a599c1c1ef0eb2ae0b4c8a41976468ce/frontend/domain.js#L93)
- [function tripPanel](https://github.com/sandralsx/17626-C14-SDDPrototype-rideclear/blob/89d49042a599c1c1ef0eb2ae0b4c8a41976468ce/frontend/app.js#L47)
- [function noticeBody](https://github.com/sandralsx/17626-C14-SDDPrototype-rideclear/blob/89d49042a599c1c1ef0eb2ae0b4c8a41976468ce/frontend/app.js#L57)
- [function attemptHistory](https://github.com/sandralsx/17626-C14-SDDPrototype-rideclear/blob/89d49042a599c1c1ef0eb2ae0b4c8a41976468ce/frontend/app.js#L69)
- [function riderNotices](https://github.com/sandralsx/17626-C14-SDDPrototype-rideclear/blob/89d49042a599c1c1ef0eb2ae0b4c8a41976468ce/frontend/app.js#L73)
- [function restoreFocus](https://github.com/sandralsx/17626-C14-SDDPrototype-rideclear/blob/89d49042a599c1c1ef0eb2ae0b4c8a41976468ce/frontend/app.js#L27)
- [export function createStore](https://github.com/sandralsx/17626-C14-SDDPrototype-rideclear/blob/89d49042a599c1c1ef0eb2ae0b4c8a41976468ce/frontend/store.js#L14)

Public-deployment evidence V2E15..17 repeats the elapsed/timing/focus paths; V2E18 confirms the preserved V1 page. These supplement the local V2E01..14 records.
