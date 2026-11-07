# Tasks: Trip Status, ETA and Delay Communication

**Input**: spec.md, plan.md, research.md, data-model.md, contracts/ui-and-state.md.
**Prerequisites**: Spec and built-in quality checklist completed before planning.
**Tests**: Behavioral verification is explicitly required by the plan/constitution.
**Organization**: Four user stories with independently seeded validation scenarios.

## Phase 1: Setup

- [x] T001 Create no-dependency commands and asset build/preview in package.json, scripts/build.mjs and scripts/serve.mjs.
- [x] T002 Preserve source model/evidence inputs and project ignore rules in docs/, sources/ and .gitignore.

## Phase 2: Foundational

- [x] T003 Write domain fixture/time/status boundary tests in tests/domain.test.js before frontend/domain.js; enforce integer minutes 0..1439 and immutable windows.
- [x] T004 Implement common fixtures, pure command validation and status derivation in frontend/domain.js.
- [x] T005 Write stale revision, persistence failure and shared-update tests in tests/store.test.js before frontend/store.js.
- [x] T006 Implement Web Lock/revision persistence, storage events and explicit temporary fallback in frontend/store.js.

## Phase 3: User Story 1 - Know pickup information (P1, MVP)

Independent test: both seeded legs show distinct window/ETA/as-of; unknown and
equality cases are correct. No notice or contact feature is required to inspect them.

- [x] T007 [US1] Implement leg selection, separate window/ETA/status panels and per-tab view state in frontend/index.html and frontend/app.js.
- [x] T008 [US1] Implement responsive transport-sign typography and original-window/current-estimate layout in frontend/styles.css.

## Phase 4: User Story 2 - Delay information (P1)

Independent test: one changed ETA on an existing leg creates the specified notice;
early/late discovery and duplicate rules can be exercised without booking/reassignment.

- [x] T009 [US2] Write early/late/equality/unknown/recovery/no-op and terminal-state cases in tests/domain.test.js before notification transitions.
- [x] T010 [US2] Implement snapshot notices and one-event-per-update precedence in frontend/domain.js.
- [x] T011 [US2] Implement dispatcher ETA/status/time editor, scenario controls and rider delay notices in frontend/app.js.

## Phase 5: User Story 3 - Communication outcomes (P2)

Independent test: create accepted-change notice on an existing leg, then explicitly
advance mock delivery/acknowledgement; preserve unreachable attempt through retry.

- [x] T012 [US3] Write acceptance-gating, delivery/ack/retry and immutable-attempt tests in tests/domain.test.js before lifecycle transitions.
- [x] T013 [US3] Implement channel enums sms/phone/email and sent → delivered → acknowledged or sent → unreachable → retry transitions in frontend/domain.js.
- [x] T014 [US3] Implement communication history, explicit acknowledgement and dispatcher outcome actions in frontend/app.js.

## Phase 6: User Story 4 - Contact dispatch (P2)

Independent test: submit one valid contact, inspect its correct-leg receipt and
review it in dispatch; trip/ETA/window remain unchanged.

- [x] T015 [US4] Write contact validation and trip-invariance tests in tests/domain.test.js; enforce "1-500 trimmed characters" before contact implementation.
- [x] T016 [US4] Implement request snapshots/review in frontend/domain.js and labeled form/queue feedback in frontend/app.js.

## Phase 7: Polish and Preservation

- [x] T017 Add persistent live feedback, labels, errors, focus preservation and reduced-motion styles in frontend/index.html, frontend/app.js and frontend/styles.css.
- [x] T018 Run behavior tests/build and browser keyboard, narrow-screen and tab-sync checks; record actual evidence in docs/engineering-verification.md.
- [x] T019 [P] Record Spec Kit provenance, implementation mappings and V1 run instructions in docs/workflow-receipt.md, docs/implementation-map.md and README.md.
- [ ] T020 Preserve the model/spec/plan/tasks/source in a private GitHub repository and v1 Git reference, deploy the separate V1 URL, and record verified links in README.md and docs/release-v1.md.

## Dependencies & Execution Order

Setup → foundation → US1 → US2 → US3 → US4 → verification/preservation.
US2/US3/US4 are independently demonstrable from fixtures, but their changes share
frontend/domain.js and frontend/app.js and are executed sequentially here.
Within each story, scenario tests precede the corresponding transitions. A failed
check is resolved before advancing. T020 depends on completed code/build and access
to GitHub/hosting; do not mark it complete based only on a local ZIP or Site source repo.

## Parallel Opportunities

T019 can run alongside browser verification once all interfaces stabilize. Styling
can be reviewed separately from domain tests. No concurrent edits to shared source
files are needed; [P] is optional work independence, not a requirement for delegation.
For US1 compare seeded windows while styling; for US2 review timing fixtures while
reading notification copy; for US3 review attempt history alongside channel labels;
for US4 review validation messages alongside the queue.

## Implementation Strategy

First establish US1 as the smallest useful slice, then add delay, outcomes and
contact without widening the eight-goal scope. Validate the complete V1 before
tagging. Do not start V2 or author student evaluation/reflection during Step 3.
