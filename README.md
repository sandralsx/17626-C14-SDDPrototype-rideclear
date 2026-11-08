# RideClear — 17-626 Assignment3

**Current stage: Step5 technical work complete — Prototype V2.** Scope: Trip Status, ETA and Delay Communication, based on the three team HW2 models and checked Shuxin HW1 interview evidence. The GitHub repository remains private; both fictional demo pages are public.

## Required deliverable navigation

| Component | Link / actual state |
| --- | --- |
| GitHub Version1 | [Preserved v1](https://github.com/sandralsx/17626-a3-rideclear/tree/v1) |
| GitHub Version2 | [Preserved v2](https://github.com/sandralsx/17626-a3-rideclear/tree/v2), descendant in the same repository |
| Prototype V1 URL | [Open V1](https://rideclear-a3-v1-shuxin-20261107.tomato-star.chatgpt.site) |
| Prototype V2 URL | [Open V2](https://rideclear-a3-v2-shuxin-20261107.tomato-star.chatgpt.site) |
| Requirements Analysis and Learning Log | [V1 goal analysis](docs/goal-model.md), [V2 model revision](docs/goal-model-v2.md), [V1 RTM](docs/traceability-v1.md), [V2 RTM](docs/traceability-v2.md), [technical change register](docs/v2-requirements-change-register.md). **learning-log.md must still be independently authored by the student.** |

The assignment submits one repository URL. The technical components are preserved and linked here; no missing student Learning Log or Step6 response is fabricated. This README does not claim the whole assignment is finished.

## Compare V1 and V2

V2 adds explicit elapsed-estimate usability requirements and separates discovery, sent, delivered and acknowledged times/deadline evidence. It also corrects the existing keyboard-focus defect after acknowledgement. [Revised spec](specs/002-truthful-updates/spec.md), [requirements change register](docs/v2-requirements-change-register.md), [verified results](docs/verification-v2/README.md), [release/source provenance](docs/release-v2.md).

In V2 open **Demo controls & sample scenarios**:

1. **Load elapsed ETA**: at17:35, Return's last17:15 ETA is shown as needing an update, with original08:40 as-of and no invented arrival.
2. **Load late delivery**: notice identified/sent16:50 but delivered17:35 after17:30 end; timing and follow-up are shown separately. Tab to Acknowledge, press Return; focus remains on Update acknowledged.

Normal, early-delay, late-discovery and unknown fixtures remain available. Reset replaces fictional records only. No real messages, trip changes, GPS, production accounts or financial integration are performed. Shared state is limited to one browser profile/origin. Separate devices have independent demo sessions. The role selector is a demo control, not an access-control boundary.

## Engineering chain

- [Assignment requirements](docs/assignment-requirements.md), [original model/source crosswalk](docs/source-crosswalk.csv), [V1 model](docs/goal-model.md), [V2 model](docs/goal-model-v2.md)
- [Spec Kit constitution](.specify/memory/constitution.md), [original workflow receipt](docs/workflow-receipt.md)
- [V1 spec/plan/tasks](specs/001-trip-status/spec.md), [V1 evaluation/findings](docs/evaluation-v1/README.md)
- [V2 spec](specs/002-truthful-updates/spec.md), [plan](specs/002-truthful-updates/plan.md), [tasks](specs/002-truthful-updates/tasks.md), [data model](specs/002-truthful-updates/data-model.md), [contract](specs/002-truthful-updates/contracts/ui-and-state.md)
- [V2 RTM](docs/traceability-v2.md) · [CSV](docs/traceability-v2.csv), [verification/evidence](docs/verification-v2/README.md), [release](docs/release-v2.md)

V2 spec/model/planning commit624261a precedes implementation commit89d4904.25 tests pass. Actual deployed browser checks confirm the three change paths. Numeric freshness SLA and informed/understood receipt success remain unconfirmed; field ETA accuracy, full WCAG certification, exact375px and200% zoom are not claimed.

## Run locally

Node22+; no dependency installation needed. Use the bundled Node24.22.1 when the host default is older.

```text
node --test
node scripts/build.mjs
node scripts/serve.mjs
```

Only five files built from frontend/ are public assets. Original interviews, assignment PDF, models and technical documents remain in the private repository and local academic deliverable package.

AI assistance was used for technical artifacts. Per the assignment PDF p5, the student must independently write learning-log.md and all Step6 examples/answers without AI assistance. No such log or answers were generated.
