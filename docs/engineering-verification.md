# V1 Engineering Verification

Date: 2026-11-07. This records checks performed by the coding agent for Step 3.
It is not student-authored Prototype Evaluation, Learning Log or a Step 6 response.

## Automated behavior checks

The tests were written before domain/storage implementation. Initial run failed
because the modules did not yet exist. After implementation, `node --test` passed
**17 tests, 0 failures**. Cases cover:

- Distinct leg windows and service-day time validation.
- ETA equal to window end, earlier-than-window, unknown and terminal status.
- Pure transitions, immutable windows, invalid status/time, no-op updates.
- Early delay notice and at-end/late-discovery early-notice misses.
- Delayed ETA changes, recovery, unavailable estimate and preserved snapshots.
- No fabricated notice from advancing the clock or a terminal trip update.
- Driver acceptance for change notices, independent delay triggers.
- Explicit delivery then acknowledgement; rejected invalid lifecycle transitions.
- Unreachable retry history and future-only channel preference.
- Contact text limits, ETA snapshot and no trip changes on review.
- Deterministic normal/early/late/unknown fixtures.
- Reload persistence, stale write rejection, serialized concurrent commands.
- Monotonic revisions through reset, temporary fallback and durable-write failure.

`node --check frontend/app.js` passed. Static build copied only five app assets.
No interview/model/document file is included in the public application directory.

Token color calculations also passed: main text 10.73:1, muted text 5.98:1,
primary-button text 6.69:1, warning text 6.37:1, control boundaries 3.60:1 and
focus ring 5.96:1 against their specified backgrounds. Exact checked pairs are
in `contrast-checks.json`; this is not a whole-page conformance audit.

## Browser interaction performed

Chromium local preview was served over HTTP localhost after resolving sandbox
network isolation. Observed through visible DOM/accessibility state:

1. Return window remained 17:00-17:30 after ETA 17:45 at simulated 16:50. A distinct
   delay notice appeared with the correct snapshot and sent-only outcome.
2. Marking delivered displayed delivered-but-not-acknowledged. Explicit rider
   acknowledgement changed the record; merely viewing did not.
3. Blank contact produced an associated error and focused the textarea. A valid
   request submitted with Tab/Enter produced a correct-leg receipt and ETA snapshot.
   Dispatch review changed only the request status.
4. A second same-origin Chrome tab loaded the shared state. A subsequent ETA 17:55
   appeared in it while the contact draft and focus remained. Submitting its stale
   form was rejected without adding the request or overwriting newer data.
5. Marking unreachable and retrying preserved both attempts. An unaccepted
   change notice was rejected with an explanation.
6. Late-discovery fixture displayed 17:35 creation and an early-notice miss.
   Unknown fixture displayed Estimate unavailable, without an on-time claim.
7. Reload retained same-browser state and cleared transient UI feedback.
8. In the embedded browser's **actual 375 CSS px viewport**, rider and dispatch
   layouts had document width 360 px (scrollbar excluded), with no horizontal
   page overflow. Screenshots were inspected. Keyboard activation selected a leg;
   DOM focus remained on `leg-return` with a solid visible focus outline.

Chrome's viewport override and Ctrl-plus did not change its reported CSS viewport,
so those attempts are not counted as successful mobile/200% zoom tests. The embedded
browser supplied the verified 375px check. Full 200% zoom and real screen-reader,
voice-control or switch-access use were not independently verified in this run.
No full WCAG conformance claim is made. Temporary viewport overrides were reset.

## Limits

Browser-profile/origin scoped state, not server-wide dispatch. Mock delivery, no real
GPS or ETA accuracy measurement. No stakeholder confirmation of prototype thresholds,
no financial ROI validation, and no student V1 evaluation conclusions are asserted.
V1 is preserved before any requested Step 4/5 work; no V2 improvement was fabricated.
