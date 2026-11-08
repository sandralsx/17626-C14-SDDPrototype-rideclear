# V2 UI and state contract

Inherits V1 commands/revision/storage contract. No external HTTP/notification API.

- tripCondition(trip, now): terminal first, unknown next, elapsed known ETA if now>eta, then valid window relation. Last ETA and updatedAt are never replaced with actual arrival.
- noticeTiming(notice, now): delay-only deadline evaluation; strict-before discovery; earliest recorded delivery across attempts determines before/late. Without delivery, now<windowEnd is pending and now>=windowEnd is no delivery recorded before deadline. An unreachable latest attempt also demands human follow-up. No timestamp mutation.
- updateTrip priority follows revised FR-010; an elapsed non-delayed ETA generates `elapsed` instead of `recovery`. setClock derives display only.
- Every notice exposes labeled creation/identification and complete per-attempt sent/delivered/acknowledged/unreachable time history. Missing values explicitly say not recorded. Common presentation function keeps both views consistent.
- A rider acknowledgement keeps the same ack-noticeID button, changes its label/state to Update acknowledged / aria-disabled=true and rejects further activation without a write. The stable status region announces the result.
- V2 storage/lock/session keys are distinct from V1. Separate deployment origin further isolates state. Existing stale editor, drafts, receipts and temporary-storage rules remain applicable.
