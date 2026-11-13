# RideClear — 17-626 Assignment3

**Submission snapshot: Prototype V1 and V2, requirements analysis, traceability, Spec Kit artifacts, and the student-revised English Learning Log.** Scope: Trip Status, ETA and Delay Communication, based on the three team HW2 models and checked Shuxin HW1 interview evidence. The GitHub repository remains private; both fictional demo pages are public.

## Required deliverable navigation

| Component | Link / actual state |
| --- | --- |
| GitHub Version1 | [Preserved v1](https://github.com/sandralsx/17626-a3-rideclear/tree/v1) |
| GitHub Version2 | [Current V2 submission](https://github.com/sandralsx/17626-a3-rideclear/tree/main) · [Preserved v2 prototype release](https://github.com/sandralsx/17626-a3-rideclear/tree/v2), descendant of V1 in the same repository |
| Prototype V1 URL | [Open V1](https://rideclear-a3-v1-shuxin-20261107.tomato-star.chatgpt.site) |
| Prototype V2 URL | [Open V2](https://rideclear-a3-v2-shuxin-20261107.tomato-star.chatgpt.site) |
| Requirements Analysis and Learning Log | [Learning Log — student-revised English version](docs/learning-log.md), [V1 goal analysis](docs/goal-model.md), [V2 model revision](docs/goal-model-v2.md), [V1 RTM](docs/traceability-v1.md), [V2 RTM](docs/traceability-v2.md), [technical change register](docs/v2-requirements-change-register.md). **Student revision of the Learning Log is complete; teammates can review the current materials.** |

The assignment submits one repository URL. The technical components are preserved and linked here. The current English Learning Log includes the student's revisions, confirmed on 2026-11-12, under the student-reported instructor update allowing AI drafting followed by personal revision. The student confirmed that they and their teammates operated V1 and V2. AI-assisted technical checks remain distinguished from procedures personally repeated by the team. This default-branch submission includes the current log and subsequent documentation updates. The preserved v1/v2 tags retain the original prototype releases; current submission documents are linked from this README. Unresolved verification and stakeholder questions remain explicitly recorded.

## Team GitHub accounts

- [Shuxin Liu / sandralsx](https://github.com/sandralsx) — repository owner.
- [JasonYao-QY](https://github.com/JasonYao-QY) — teammate.
- [ALT-JS](https://github.com/ALT-JS) — teammate.

The repository remains private. Teammates must accept their GitHub collaboration invitations to access it. Grading staff also need appropriate repository access; the public prototype URLs are separate from repository access.

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
- Active Spec Kit feature: `specs/002-truthful-updates` ([selection](.specify/feature.json)).
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

AI assistance was used for technical artifacts and the initial Learning Log draft. On2026-11-08 the student supplied a subsequent instructor email update: “Learning Log can be written by AI, but revised by person.” The student has confirmed completing their revision of the current log, following that updated drafting/revision arrangement. Earlier versioned documents retain the original PDF authorship rule as historical records; they have not been rewritten retrospectively. The preserved v1/v2 tags and prototype code/deployments are unchanged by these local documentation updates.
