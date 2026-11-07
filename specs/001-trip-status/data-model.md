# Phase 1 Data Model

All values are fictional, single-service-day fixtures. The saved schema version is 1.

## DemoState

- `schemaVersion`: exactly 1.
- `revision`: nonnegative integer, incremented only for material mutations.
- `now`: integer minutes 0..1439; monotonic within one loaded scenario.
- `serviceDate`: `2026-11-07`; `timezone`: `America/New_York`.
- `channel`: enum `sms | phone | email`; used for future notice/retry attempts.
- `trips`: two TripLeg records; `notices`: Notice list; `requests`: ContactRequest list.
- `nextId`: increasing integer used for deterministic notice/request IDs.
- `scenario`: name of loaded fixture. Reset replaces the demo but preserves monotonic
  revision at the adapter boundary so old editors remain stale.

## TripLeg

`id` is `outbound` or `return`; `direction`, `origin`, `destination`, `vehicle`,
`windowStart`, `windowEnd` are fixture identity/schedule fields. Window start must be
less than end. `status` is `scheduled | en-route | arrived | completed`.
`eta` is null or integer minutes 0..1439. `updatedAt` is simulated now when a
material ETA/status update occurs. The update command cannot edit the saved window.

Derived display status: terminal operational status takes precedence; otherwise
unknown ETA → estimate unavailable; ETA > end → delayed; ETA < start → ahead of
window; remaining values → within pickup window. Never infer an actual arrival.

## Notice and Attempt

Notice: `id`, `tripId`, `kind` (`delay | recovery | unavailable | change`), `eta`,
`windowStart`, `windowEnd`, `createdAt`, `earlyNoticeMiss` (boolean for delay),
`attempts`. Snapshots never track later edits. One material command creates at most
one notice: delay/recovery/unavailable takes precedence over an accepted change.

Attempt: `channel`, `sentAt`, `outcome` (`sent | delivered | acknowledged | unreachable`),
`deliveredAt`, `acknowledgedAt`, `unreachableAt`. Only applicable timestamps are set.
`sent` transitions to delivered or unreachable. Delivered can become acknowledged.
Only unreachable can retry, appending a new sent attempt on current channel.
History is append-preserved; existing attempts are never removed by retry.

## ContactRequest

`id`, `tripId`, `eta` snapshot, `message`, `createdAt`, `reviewed` and `reviewedAt`.
Message validation: **1-500 trimmed characters**. Render as text, never HTML.
Review changes only the request. No trip field is modified.

## Persistence/consistency

The adapter owns serialization and expected revision. Re-read current storage under
a Web Lock, reject a stale revision before invoking the pure command, then persist
the complete new state or leave durable state unchanged on failure. Other tabs use
storage events. On storage failure use the latest known state in a clearly labeled
temporary in-memory session. No storage/locks → no cross-tab consistency claim.

Role, leg selection and unsent form text are per-tab UI state, not shared business data.
