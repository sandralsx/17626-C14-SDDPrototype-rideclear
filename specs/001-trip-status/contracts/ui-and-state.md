# UI and State Contract

The app has no external HTTP API. This contract covers UI commands and observable
state. Domain commands return a new state or throw an understandable validation
error without mutating their input. No-op commands return the unchanged state.

| Command | Inputs | Effect / errors |
| --- | --- | --- |
| `updateTrip` | tripId, eta (null or 0..1439), status enum, acceptedChange boolean | Validate leg/time/status; unchanged ETA/status is a no-op. Distinct delay/recovery/unavailable event wins over change. A change-only notice requires acceptance. Window immutable. Use sendChange for an explicit accepted-change event without an ETA/status edit. |
| `sendChange` | tripId, accepted boolean | Reject unaccepted change; accepted creates a change snapshot notice. Does not edit route/schedule. |
| `setClock` | minute 0..1439 | Cannot move backwards; updates demo now, does not fabricate newly inferred messages by itself. |
| `setChannel` | sms/phone/email | Updates preferred channel only for future attempts. |
| `setOutcome` | noticeId, delivered/unreachable/acknowledged | Only allowed transitions described in data-model.md; invalid transition rejects without mutation. |
| `retryNotice` | noticeId | Only latest unreachable attempt can retry; preserve all prior attempts. |
| `contact` | tripId, message | Enforce 1-500 trimmed characters; store snapshot and visible receipt; no trip changes. |
| `reviewRequest` | requestId | Set reviewed/time; repeat review is a no-op. |
| `reset` / `loadScenario` | named fixture | Explicitly replace synthetic session; adapter increments current revision, never restores an old revision. |

`commit(expectedRevision, command)` serializes updates. `STALE_REVISION` returns a
refresh error and newest state; it does not silently apply a command to data the
editor has not reviewed. Storage/lock availability is exposed as durable shared or
temporary single-tab mode. Input form version is captured when the editor is rendered.

UI: role selector uses buttons with aria-pressed; trip selectors have direction and
window labels; all inputs have visible labels. The communication list shows event
kind, trip, ETA snapshot, channel, sent/delivery/ack status and attempt history.
The contact form has a length hint, associated error and a persistent success region.
Updates preserve active control and unsent form fields. No action performs a real send.
