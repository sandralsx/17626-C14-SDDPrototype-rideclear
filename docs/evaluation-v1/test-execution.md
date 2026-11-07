# V1 execution record and coverage

Test date2026-11-07; deployed public V1, in-app browser. Test inputs are fictional. Full capture paths/actions/UTC timestamps are in [records.json](evidence/records.json). Initial EV01/02 have no recorded UTC timestamp and are not assigned one retrospectively. Simulated times below are Eastern. UI captures are read-only accessibility/DOM evidence, not hidden-state exports.

| Evidence | Action and actual outcome |
| --- | --- |
| EV01–02 | Normal outbound09:00–09:20/ETA09:10 and Return17:00–17:30/ETA17:15 appear separately with as-of08:40. |
| EV03 | At16:50, ETA17:30 equality stays within saved Return window; no new notice, revision2. |
| EV04–05 | Email preference then ETA17:45 creates N1 before driver acceptance; repeat identical save retains one notice/revision4. |
| EV06–07 | At17:35 N1 explicitly delivered, still not acknowledged until Return action; creation16:50 shown beside outcome. First focus-loss observation. |
| EV08–10 | Blank contact rejected; valid Return R2 records17:45 ETA; marking reviewed does not reschedule or approve a time. |
| EV11–13 | Changed delay17:55 preserves N1 snapshot17:45; recovery17:20 at17:35 produces recovery message; clearing ETA creates unavailable notice and unknown current state. |
| EV14 | Early DOM snapshot retained previous render; **not used as saved-terminal evidence**. |
| EV15 | Sending change without acceptance yields explanation, no accepted-change notice. |
| EV16 | Capture retained prior DOM render; success feedback alone is insufficient. Confirmed by EV17. |
| EV17 | Fresh AX tree: N7 accepted-change sent Email, N6 late-discovery delay, six notices; original N1 timestamps preserved. |
| EV18–19 | N7 Email marked unreachable, follow-up needed; change preference to Phone then retry retains failed Email and adds Phone sent. |
| EV20 | Deliver Phone attempt; Tab sequence reaches ack-N7; Return changes to acknowledged and focus becomes BODY (JSON proof). |
| EV21 | Editor held stale draft; save rejected and revision20 unchanged. **Not a successful terminal save.** |
| EV22 | Refresh form then save arrived with ETA18:10; Return says Vehicle arrived, revision21; six notices remain, no new predicted delay. |
| EV23–24 | Peer Return draft remains focused/intact through main ETA18:15 update (revision22); stale contact submit rejected with no request added. |
| EV25 | Peer reload retains revision22 and updated Return values/history. |
| EV26 | Reset normal trips, advance clock17:35 with no ETA update: Return ETA17:15/as-of08:40 still Within pickup window; revision24. |
| EV27–28 | Requested375x812 then427x864 outer viewport, but both measured innerWidth323/document308. No observed horizontal overflow at measured width; exact375 remains unverified. Native viewport screenshots retained; full-page screenshot tool failed on these later captures. |

Every EVxx above links to its full filename through records.json. EV14/16 remain intact to avoid editing away capture limitations. EV17 onward uses fresh native AX trees rather than potentially lagging DOM snapshots.

## Acceptance scenario coverage

| Scenario | Evidence / disposition |
| --- | --- |
| AS-01 | EV01/02/26 leg details observed. |
| AS-02 | EV03/04/22/23 immutable window and same-revision update observed. |
| AS-03 | EV13 unknown state observed, not labeled on time. |
| AS-04 | Equality EV03, arrived EV22; ahead/completed supplemented by existing domain tests. |
| AS-05 | EV04 early discovery/creation observed; timely receipt remains RQ-02. |
| AS-06 | EV11/17 late-discovery notice preserves actual creation time, no backdating. Exactly-at-end supplemented by domain test. |
| AS-07 | EV05 no-op; EV11 changed delay; EV12 recovery observed but exposes RQ-01. |
| AS-08 | EV13 unavailable; EV22 terminal no new delay. Completed case unit-tested. |
| AS-09 | EV15 rejection, EV04 delay independent of acceptance. |
| AS-10 | EV17 accepted-change event Email/sent. |
| AS-11 | EV06/07/20 delivery versus explicit acknowledgement. Invalid transition supplemented by domain test. |
| AS-12 | EV18/19 unreachable/retry history, channel switch, no automatic ride change. |
| AS-13 | EV09/10/17 valid request and review; visible receipt/snapshot. |
| AS-14 | Blank UI EV08; overlong and1/500 boundary supplemented by domain test, not manually pasted beyond maxlength. |
| AS-15 | EV23/24 same-origin update/draft/stale rejection, EV21 stale editor rejection. |
| AS-16 | **Partially satisfied:** keyboard acknowledgement/focus defect EV20; draft focus EV23; labels/text/polite region present. Exact375px,200% zoom, screen-reader announcements and full contrast unverified. |
| AS-17 | EV25 reload, EV26 reset. Storage/locks failure warning behavior unit-tested only. |

## Supplementary automated checks

The unchanged V1 suite was re-run with bundled Node24.22.1 using `node --test`: **17 passed,0 failed**, exit0. [Raw output](regression-output.txt). No new implementation-mirroring tests were written. These are local source behavior tests, not an assertion that every deployed UI requirement passes. In particular, all tests can pass while ID-01 still exists.

## Reproduce the three findings without hidden-state access

Use Demo controls → Reset normal trips between independent sequences. Dispatch controls explicitly edit simulated time, selected leg, ETA and delivery outcome. Original schedule remains fixed.

1. RQ-01: set clock17:35, select Return/Rider. Read ETA17:15/as-of08:40 and Within pickup window.
2. RQ-02: reset, set clock16:50, select Return, save ETA17:45/en-route; set clock17:35, mark the delay delivered; compare Rider card and Dispatch attempt timestamps.
3. ID-01: from a delivered notice open Rider; focus Rider selector, Tab through Dispatch and both leg controls to Acknowledge; Return. Observe keyboard focus after acknowledgement. The exact recorded sequence and element IDs are in EV20-focus.json.

If a form shows a stale-data prompt, refresh it before a new intended save. A rejected stale action is not a successful trip update. Browser automation timeouts or failed screenshot capture are tool limitations and are not classified as app defects.
