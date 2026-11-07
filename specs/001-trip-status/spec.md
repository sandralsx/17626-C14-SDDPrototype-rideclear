# Feature Specification: Trip Status, ETA and Delay Communication

**Feature Branch**: `codex/a3-v1` (preserved release: `v1`)

**Created**: 2026-11-07

**Status**: V1 specification, ready for planning

**Input**: Continue A3 Step 3 from `docs/goal-model.md`, preserving A3-G01..08,
R-01..08, D01..12 and the explicit prototype assumptions. This specification is
AI-assisted technical work; it is not the student-authored Learning Log.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Know when each ride is expected (Priority: P1)

A rider views outbound and return legs, the original scheduled window, current
vehicle/trip status, estimated arrival and the time that estimate was updated.

**Why this priority**: Janelle prioritized reliable pickup information, especially
the return trip (SJ rows 14, 18, 31, 34).

**Independent Test**: Load seeded trips without notifications. A rider can identify
the correct leg and distinguish its scheduled window from the current estimate.

**Acceptance Scenarios**:

1. **AS-01** Given two legs with different windows, when either leg is selected,
   then its direction, origin, destination, window, vehicle status, ETA and as-of
   time are shown together; selecting one never substitutes the other leg's data.
2. **AS-02** Given a saved window, when dispatch changes the ETA, then the original
   window remains unchanged and both views show the same revised estimate.
3. **AS-03** Given no available ETA, when the trip is viewed, then it says
   "Estimate unavailable" and does not label the trip on time.
4. **AS-04** Given ETA equal to the window end, then the estimate is within the
   window; an ETA before the start says "Ahead of pickup window", without changing
   the schedule. Completed or arrived trips display their actual status.

---

### User Story 2 - Learn about a delay and revised ETA (Priority: P1)

A rider receives a distinct notice when dispatch information predicts that pickup
will miss the original window. A late discovery is reported honestly.

**Why this priority**: SJ rows 18 and 21 describe the lack of notice and request an
update with ETA before the window expires.

**Independent Test**: Use an existing leg and one dispatcher update; no booking,
route reassignment or actual notification provider is needed.

**Acceptance Scenarios**:

1. **AS-05** Given return window 17:00-17:30 and clock 16:50, when ETA becomes 17:45,
   then a distinct delay notice identifies the return leg, original window and
   17:45 ETA. It is recorded as identified/notified before the window ended.
2. **AS-06** Given the same window and clock 17:35, when delay is first identified,
   then notice is generated now and marked as an early-notice miss. No earlier
   send or delivery timestamp is invented.
3. **AS-07** Given the same ETA/status is submitted again, then no duplicate notice
   or artificial new as-of time is generated. A materially different delayed ETA
   produces a new update; recovery into the window produces a recovery notice.
4. **AS-08** Given a known ETA becomes unavailable, then an estimate-unavailable
   update is created without inventing a replacement time. Arrived/completed legs
   do not produce new predicted-delay messages.

---

### User Story 3 - Know whether communication reached the rider (Priority: P2)

Dispatch uses the rider's preferred channel for accepted pickup-information changes
and sees delivery, acknowledgement and unreachable outcomes separately.

**Why this priority**: Frank explicitly requested channel preference and visibility
of delivery/acknowledgement/unreachable riders (SF rows 21, 25, 36).

**Independent Test**: Create a simulated accepted-change notice and explicitly
advance its mock delivery result. Delay detection is not required for this story.

**Acceptance Scenarios**:

1. **AS-09** Given a pickup-information change not accepted by the simulated driver,
   when change notice is requested, then it is rejected with explanation and no
   message. An independently predicted delay still generates its own delay notice.
2. **AS-10** Given driver acceptance and a preferred channel, when a change notice
   is created, then its type, trip, channel, creation time and sent outcome are
   recorded. Sent is not displayed as delivered or acknowledged.
3. **AS-11** Given a sent notice, when simulated delivery is marked delivered,
   then dispatch sees delivered. Only an explicit rider acknowledgement or
   simulated external acknowledgement changes it to acknowledged. Page viewing
   alone is never acknowledgement. A sent notice cannot be acknowledged before
   delivery has been recorded.
4. **AS-12** Given delivery is marked unreachable, then the attempt history remains,
   dispatch sees the need for follow-up, and no run is held, canceled or sanctioned.
   Explicit retry starts another sent attempt on the current preferred channel and
   keeps the previous unreachable attempt. Delivered/acknowledged are terminal for
   that attempt; only sent attempts can be marked delivered or unreachable.

---

### User Story 4 - Report that the revised ETA does not work (Priority: P2)

The rider can send a mock contact request linked to a selected trip. Dispatch sees
the request without automatically approving or applying a schedule change.

**Why this priority**: SJ row 21 asks for a way to contact dispatch or report an
unsuitable revised time.

**Independent Test**: Submit a contact request for an existing trip, then open the
dispatch view and review it without changing the ETA/window.

**Acceptance Scenarios**:

1. **AS-13** Given a selected trip and a nonblank message of 1-500 trimmed characters,
   when the rider submits, then a visible receipt confirms a simulated request,
   with the correct leg, current ETA snapshot and time. The message is shown as text.
2. **AS-14** Given blank or overlong text, then an associated error explains the
   limit; no request is added. Dispatch can mark a valid request reviewed, which
   does not modify the trip or imply that a new time was approved.

### Cross-cutting Scenarios

1. **AS-15** Given sequential commands in the same demo session, including two
   same-origin tabs, then rider and dispatch read the same revision and values.
   A stale editor cannot overwrite a newer revision; it receives a refresh prompt.
2. **AS-16** Using keyboard only, a rider can select a leg, read notices, acknowledge
   a delivered notice, and submit a contact request. Controls have labels, visible
   focus and non-color status text; significant updates are announced without
   moving focus away from a control. At 375 CSS px, primary content fits without
   horizontal page scrolling. At 200% zoom, controls remain operable.
3. **AS-17** Given a reload, the same browser profile retains demo state. Explicit
   reset restores fixtures. If durable storage is unavailable, an understandable
   warning identifies temporary/session-only mode; the app remains usable in its
   current tab and does not promise cross-tab persistence.

### Edge Cases

- ETA comparison uses each leg's own window; no universal 30-minute rule.
- Unknown ETA is not evidence of punctuality; historical notices retain their ETA
  snapshot after the current estimate changes.
- Discovery exactly at window end cannot meet "before"; early-notice miss is true.
- Simulation time is explicit, monotonic within a scenario and independent of the
  device clock. Loaded scenarios/reset may replace the synthetic session.
- Updating a terminal leg does not create a new delay notice. Status vocabulary is
  scheduled, en route, arrived and completed; the trip status is distinct from the
  estimate's relationship to the scheduled window.
- Invalid times, unsupported status/channel/outcome values and stale revisions
  cause understandable errors without a partial write or modified trip.
- Notification receipt history and contact requests are linked to a leg; they must
  not leak into the other leg's display. Both legs belong to one fictional rider.
- Storage unavailable, another tab's update and an unreachable contact outcome have
  explicit feedback. Production multi-user delivery/concurrency is out of scope.

## Requirements *(mandatory)*

### Functional Requirements

| Spec ID / original candidate | Required behavior | Goal / checked evidence | Acceptance |
| --- | --- | --- | --- |
| **FR-001 / R-01** | Show the immutable scheduled window separately from ETA for each trip leg. | A3-G01; S:G-7, Q:G-22; SJ31 | AS-01,02,04 |
| **FR-002 / R-02** | Show current trip/vehicle status, latest ETA and as-of; explicitly show unknown, ahead-of-window and delayed information. | A3-G02; S:G-8, J:G-15/16/20, Q:G-23; SJ31,34 | AS-01..04,08 |
| **FR-003 / R-03** | Generate a distinct delay notice when valid ETA exceeds saved window end; record whether discovery was before the end. | A3-G03; S:G-9, J:G-17, Q:G-26; SJ18,21,34 | AS-05..08 |
| **FR-004 / R-04** | Support mock contact requests with trip/ETA snapshot and visible receipt, without rescheduling. | A3-G04; S:G-10; SJ21,23 | AS-13,14 |
| **FR-005 / R-05** | Keep sequential rider/dispatch status and message views consistent in one browser demo session; reject stale overwrites. | A3-G05; S:G-23, J:G-29/32, partial Q:G-89; SF27,31,33 | AS-02,15,17 |
| **FR-006 / R-06** | Apply scoped accessible operation, labels, focus, announcements, contrast and non-color information to all rider interactions. | A3-G06; S:G-31, partial S:G-12/Q:G-12; SD25,SJ34 | AS-16 |
| **FR-007 / R-07** | Demonstrate distinct return-leg window, ETA and delay communication, without claiming real-world prediction accuracy. | A3-G07 SoftGoal; S:G-14, partial Q:G-6; SJ14,18,34 | AS-01,05,06 |
| **FR-008 / R-08** | Use preferred-channel mock communication for accepted changes and preserve sent/delivered/acknowledged/unreachable outcomes and retry attempts. | A3-G08; S:G-22/24; SF21,25,36 | AS-09..12 |

- **FR-009**: The system MUST identify all records and actions as fictional demo
  data and simulated channels. It MUST make no real-world send or transport action.
- **FR-010**: Submitted ETA/status identical to current values MUST be a no-op.
  Each changed delayed ETA MUST create one new delay/update notice; recovery MUST
  create a recovery notice; known-to-unknown MUST create an unavailable notice.
  Triggering delay and accepted-change notices in the same command is forbidden;
  the distinct delay/recovery/unavailable event takes precedence.
- **FR-011**: A notice MUST preserve trip, window, ETA and creation-time snapshots.
  Channel preference edits affect future notices/retries, not prior attempts.
- **FR-012**: Contact text MUST contain 1-500 trimmed characters. Clock/ETA inputs
  MUST be valid service-day times (00:00..23:59); clock changes cannot go backwards
  within one scenario. The ETA may refer to an earlier time than now, but it MUST
  remain an estimate and not be rewritten as an actual arrival.
- **FR-013**: Unreachable MUST require manual follow-up; viewing, delivery failure
  or a contact request MUST NOT cancel/reschedule a trip, hold a run, or sanction.
- **FR-014**: The demo MUST support reload persistence when storage is available,
  a reset to fixtures, and a truthful temporary-mode warning otherwise.
- **FR-015**: Historical notices and attempts MUST remain visible through ETA
  changes until explicit reset/scenario replacement. A delivery attempt can advance
  only sent → delivered → acknowledged, or sent → unreachable → explicit retry.
  Acknowledgement never retroactively proves that a late notice was early.
- **FR-016**: The engineering package MUST preserve original goal-model context,
  this spec, plan, tasks and V1 source. No implementation satisfaction or student
  evaluation findings may be fabricated before actual observation.

### Key Entities *(include if feature involves data)*

- **Trip leg**: stable ID, outbound/return direction, origin/destination, immutable
  saved window, vehicle label, operational status, optional ETA and update time.
- **Communication notice**: leg ID, event kind, window/ETA snapshots, creation time,
  early-notice timing result when applicable, channel-specific attempt history.
- **Communication attempt**: channel, sent time, delivery/acknowledgement outcome
  and explicit transition timestamps. No real provider receipt is implied.
- **Contact request**: leg ID, ETA snapshot, text, submission time and reviewed flag.
- **Demo session**: fictional rider, channel preference, simulated clock, revision,
  selected scenario and the above records. View role is a demonstration selector,
  not a security or authorization boundary.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: In both seeded leg scenarios, a reviewer can distinguish scheduled
  window, ETA, direction and information timestamp without opening dispatch.
- **SC-002**: All defined early, late-discovery, equality and unknown-ETA scenarios
  yield the specified notice/status outcome with zero fabricated early timestamps.
- **SC-003**: Each tested delivered notice remains unacknowledged until an explicit
  acknowledgement; every unreachable/retry scenario preserves the failed attempt.
- **SC-004**: A valid contact appears once on the correct leg and dispatch queue;
  blank/overlong contact attempts add zero records and change zero trip fields.
- **SC-005**: Sequential same-session/tab updates produce matching rider/dispatch
  values; stale writes produce zero silent overwrites.
- **SC-006**: The four primary rider journeys in AS-16 can be completed by keyboard;
  status is never conveyed by color alone and the page has no horizontal overflow
  at 375 CSS px. These checks are a scoped target, not full WCAG certification.

## Assumptions

### Prototype working decisions, not new stakeholder confirmation

| ID | Working assumption / earlier model item | V1 treatment |
| --- | --- | --- |
| PA-01 | A01/A02, U01; latest valid ETA > saved end predicts delay | Generate notice when identified; before-end is strictly clock < end. Late discovery remains an early-notice miss. |
| PA-02 | A04, U02/U03; explicit demo time, no numeric freshness or error SLA | Display as-of and unknown; use fixed service date 2026-11-07, America/New_York, with local service-day times. No real GPS calculation. |
| PA-03 | A03/A05, U04; share communication mechanism while preserving triggers | Channels are mock SMS/phone/email. Sent never auto-advances. Driver acceptance gates change notices, not delay detection. |
| PA-04 | U05; changes/recovery/unavailable and duplicate policy | Apply FR-010/011; no minimum delay threshold, no silent notification history overwrite. |
| PA-05 | A06; contact does not approve a new time | One 1-500 character request with a snapshot; reviewing marks workflow state only. |
| PA-06 | A04/A05; bounded shared demo session | One browser profile/origin, sequential operations. Separate browsers/devices are independent sessions; no production accounts or server-wide dispatch. |
| PA-07 | U06, J:G-60↔G-62 | Limit prototype scope and use mock channels. No savings, ROI or budget sufficiency is asserted. |

### Dependencies and conflict/overlap decisions

G05 supports status, delay detection and communication records (D02). G01/G02 stay
separate (D01); reading ETA does not replace delay notification (D04). G03 and G08
share a mechanism with different triggers (D05). Contact never bypasses deferred
change approval (D12). G06 constrains all rider surfaces (D08); return information
is a quality specialization, not guaranteed punctual transport (D09). Original
cost/call-volume and scope-external conflicts remain in `docs/goal-model.md`.

### Explicit exclusions and evidence limits

No new booking, automatic reassignment, actual positioning/traffic ETA, physical
pickup guarantee, finance reporting, production access control, real SMS/phone/email,
or sanctions. Other team members' original transcripts remain unverified; their
unique numeric rules are not promoted to stakeholder facts. Mock fixtures demonstrate
behavior rather than validate actual arrival accuracy. Learning Log authorship is
excluded from AI assistance by the assignment.
