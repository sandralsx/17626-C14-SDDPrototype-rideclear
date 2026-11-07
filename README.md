# RideClear - 17-626 Assignment 3

**Current stage: V1 technical evaluation / Step 4.** Trip Status, ETA and Delay Communication,
based on three team members' HW2 models and checked Shuxin HW1 evidence.

## Deliverable links

| Component | Current state |
| --- | --- |
| GitHub Version 1 | [v1 preserved version](https://github.com/sandralsx/17626-a3-rideclear/tree/v1). |
| GitHub Version 2 | Not created; V1 evaluation is recorded, and specification revision awaits Step 5. |
| Prototype V1 URL | [Open Prototype V1](https://rideclear-a3-v1-shuxin-20261107.tomato-star.chatgpt.site) · deployed and public for grading. |
| Prototype V2 URL | Not deployed. V1 will remain separate. |
| Requirements Analysis and Learning Log | [Goal model and decisions](docs/goal-model.md), [V1 spec](specs/001-trip-status/spec.md), [V1 RTM](docs/traceability-v1.md), [Step 4 technical evaluation](docs/evaluation-v1/README.md). Student-authored learning-log.md remains to be written independently. |

The demo was deployed successfully and opened in the browser. After the user explicitly
authorized public demo access, its access policy was changed to public on 2026-11-07.
The source repository remains private. The immutable v1 tag records the initial
preservation state before that later access-only change; application code is unchanged.

The final assignment requires all five actual links when V2 and the independent
Learning Log exist. This stage does not invent missing final-deliverable URLs.

## Step 4 evaluation

[RTM](docs/traceability-v1.md) traces all eight selected requirements from checked interviews through goals, spec IDs and immutable V1 code to actual evidence and satisfaction. [Findings](docs/evaluation-v1/findings.md): one implementation defect (acknowledgement focus loss), two requirements issues (elapsed/stale ETA semantics and early discovery versus timely delivery). [Execution record](docs/evaluation-v1/test-execution.md) states observed passes and unverified checks. Existing tests:17 passed. These are AI-authored technical records, not the independent student Learning Log. V1 remains frozen; no V2 changes have been made.

## Prototype

Rider view: inspect outbound/return windows, updated ETA/status, distinct delay
notices, explicit acknowledgement and a contact request. Dispatch view: update
mock information, inspect communication attempt history and review contact requests.

Use **Demo controls & sample scenarios** for normal trips, early delay, late discovery
and unknown ETA. All data/channels are fictional. No real message or ride change is
performed. State is shared only within the same browser profile and site origin;
different devices are independent demo sessions. Open two tabs to compare views.

The view selector is for demonstration and does not implement production access
control. If storage or Web Locks is unavailable, the app labels current-tab temporary
mode instead of promising saved cross-tab state.

## Run locally

Requires Node 22+; no package installation is needed.

```text
node --test
node scripts/build.mjs
node scripts/serve.mjs
```

Open the printed localhost URL. The host's default Node 14 is too old; use a modern
Node or the bundled executable listed in [workflow receipt](docs/workflow-receipt.md).

## Review the engineering chain

- [Assignment requirements](docs/assignment-requirements.md)
- [Goal model, source ID mapping and Step 1/2 decisions](docs/goal-model.md)
- [Constitution](.specify/memory/constitution.md)
- [Specification and acceptance scenarios](specs/001-trip-status/spec.md)
- [Plan](specs/001-trip-status/plan.md), [research](specs/001-trip-status/research.md), [data model](specs/001-trip-status/data-model.md), [contract](specs/001-trip-status/contracts/ui-and-state.md), [tasks](specs/001-trip-status/tasks.md)
- [Implementation map](docs/implementation-map.md), [engineering verification](docs/engineering-verification.md), [actual Spec Kit workflow receipt](docs/workflow-receipt.md)

Original model/evidence copies remain in sources/ in this **private repository**.
The deployment serves only assets built from frontend/, not those source documents.
Unconfirmed prototype assumptions remain labeled in the spec. Return-trip information
behavior is demonstrated; physical pickup punctuality and prediction accuracy are not.

Learning Log authorship and all Step 6 examples/answers must be completed by the
student without AI assistance under the assignment. No such log is generated here.
