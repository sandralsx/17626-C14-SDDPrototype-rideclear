# V1 Implementation Map

This is a Step 3 engineering navigation aid. It is not a completed Step 4 RTM or a
claim that stakeholder goals have been fully satisfied. Student evaluation must
later record fully/partially/not satisfied based on actual interaction and evidence.

| Spec / candidate | Goal and checked interview | Implementation | Verification input |
| --- | --- | --- | --- |
| FR-001 / R-01 | A3-G01; S:G-7, Q:G-22; SJ31 | domain.js immutable window fields; app.js tripPanel/renderLegs | AS-01/02/04; fixture/window invariant tests |
| FR-002 / R-02 | A3-G02; S:G-8, J:G-15/16/20, Q:G-23; SJ31,34 | domain.js tripCondition/formatTime/updateTrip; app.js tripPanel/dispatchEditor | AS-01..04/08; unknown/equality/status tests |
| FR-003 / R-03 | A3-G03; S:G-9, J:G-17, Q:G-26; SJ18,21,34 | domain.js addNotice/updateTrip; app.js noticeBody/riderNotices | AS-05..08; early/late/no-op/recovery/snapshot tests |
| FR-004 / R-04 | A3-G04; S:G-10; SJ21,23 | domain.js contact/reviewRequest; app.js contactPanel/dispatchRequests | AS-13/14; length/snapshot/no-rescheduling tests |
| FR-005 / R-05 | A3-G05; S:G-23, J:G-29/32, partial Q:G-89; SF27,31,33 | store.js createStore/commit/storage listener; app.js subscribe/draft preservation | AS-02/15/17; stale/concurrent/write-failure/reload tests and dual-tab interaction |
| FR-006 / R-06 | A3-G06; S:G-31; SD25,SJ34 | semantic index.html; app.js labels/errors/live feedback/focus; styles.css responsive/focus/reduced-motion | AS-16; keyboard interaction, 375px checks, color contrast calculation |
| FR-007 / R-07 | A3-G07 SoftGoal; S:G-14, partial Q:G-6; SJ14,18,34 | separate return fixture, leg selection, early/late/unknown scenarios | AS-01/05/06; no physical ETA accuracy claim |
| FR-008 / R-08 | A3-G08; S:G-22/24; SF21,25,36 | domain.js sendChange/setOutcome/retryNotice; app.js outcome controls/history | AS-09..12; acceptance, delivery/ack and retry tests |

Paths above are relative to `frontend/` except tests under `tests/`. Full source
ID names, exact evidence files and CSV row convention remain in `goal-model.md`.

Engineering additions FR-009..016 operationalize the explicit assumptions and
boundaries in spec.md. They are not new stakeholder testimony. In particular:
browser sharing is scoped; numeric refresh SLA is not invented; delivery is mock;
contact does not approve changes; original conflicts are retained in the source model.
