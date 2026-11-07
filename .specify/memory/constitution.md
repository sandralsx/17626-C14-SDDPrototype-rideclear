# RideClear Constitution

## Core Principles

### I. Traceable stakeholder needs
Every selected behavior MUST map to A3-G01..08 and checked interview evidence.
Source-model details, analyst interpretations and prototype assumptions MUST retain
their labels. Window lengths and ETA refresh frequencies MUST NOT be invented as
stakeholder testimony. Unresolved source conflicts MUST remain visible in the model.

### II. Specify before implementation
The specification, acceptance scenarios, plan and tasks MUST exist before application
implementation. Intended behavior changes MUST first amend the specification. V1
artifacts and history MUST be preserved before any V2 work begins.

### III. Accessible, truthful rider communication
Scheduled windows and estimates MUST remain distinct. Unknown or delayed estimates
MUST NOT be labeled on time. Sent, delivered and acknowledged MUST remain distinct.
All rider actions MUST support keyboard operation, labeled controls, visible focus,
non-color status cues and understandable feedback. WCAG 2.1 AA is a scoped target,
not a preemptive conformance claim.

### IV. Bounded and explicit simulation
The prototype MUST use fictional trips and explicit simulated time, ETA, channels and
delivery outcomes. It MUST NOT send real messages, allocate vehicles, cancel trips,
decide sanctions or claim real-world ETA accuracy. Contacting dispatch MUST NOT
implicitly approve a schedule change. Browser-scoped sharing MUST be disclosed.

### V. Evidence-based verification
Tests MUST exercise timing boundaries, notification lifecycle and shared-state
invariants. Implementation checks MUST be recorded accurately and kept separate from
student-authored evaluation and reflection. No Learning Log or Step 6 answers may be
authored by this agent. Failed checks MUST be fixed or reported before preservation.

## Prototype Constraints

The sprint includes trip status, ETA, delay communication, contact, accessibility,
return-trip information and mock communication outcomes. Booking, route optimization,
production authentication, external GPS/SMS, finance and sanctions remain deferred.
The initial prototype is English-language, usable on desktop and narrow screens, with
no required external font or image service. The implementation MUST stay small enough
to review and reproduce from the preserved source.

## Development Workflow and Quality Gates

Follow Spec Kit constitution, specify, plan, tasks and implement phases in order.
Validate the built-in requirements checklist before implementation. Run deterministic
behavior tests and browser checks appropriate to the eight selected goals. Preserve
actual tool version and workflow receipts. Keep source repository private; deploy only
synthetic application assets. A deployment URL is not proof of grader access.

## Governance

This constitution is version 1.0.0, adopted for A3 V1 on the date below. Changes MUST
name the reason and affected requirements and use semantic versioning: major for
incompatible principle changes, minor for added obligations, patch for clarification.
A constitution change is not stakeholder confirmation. Review every phase for scope,
traceability, simulation honesty and learning-log authorship boundaries.

**Version**: 1.0.0 | **Ratified**: 2026-11-07 | **Last Amended**: 2026-11-07
