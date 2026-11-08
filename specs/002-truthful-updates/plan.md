# V2 implementation plan

Input: revised spec.md, Step4 findings and goal-model-v2.md. Uses the existing Spec Kit document structure; this is an explicit technical revision of the already initialized Spec Kit project, not a claim of a new CLI generation run.

1. Commit revised spec/model/plan/tasks before changing app behavior. Preserve V1 files/tag and record parent SHA.
2. Add domain derivation for elapsed estimates and strict delivery-deadline evidence; retain immutable records. Adapt recovery event precedence. Unit-test actual newly required boundaries and existing invariants.
3. Use derived values in both views; label all notification times and display manual follow-up. Retain a stable focusable acknowledged control with guarded reactivation. Keep branding/layout and existing journeys.
4. Add named elapsed and late-delivery fixtures to reproduce Step4 comparisons. Separate V2 storage/identity. No backend/dependencies or real data.
5. Run existing/new domain/store tests, build only public application assets, then browser-check repeated V1 finding sequences and same-origin drafts. Do not fabricate zoom/assistive-tech checks.
6. Publish a separate Site, preserve public-demo/private-repository preference, record source/deployment SHA and URL. Retain GitHub history, v1/v2 references, update README/RTM with actual results and unresolved questions.

Architecture remains pure ES modules + DOM + localStorage/Web Locks, Node24 tests/static build. No new runtime packages. `tripCondition(trip, now)` derives usability; `noticeTiming(notice, now)` derives deadline evidence across recorded attempts. Commands do not invent delivery, arrival or clock-triggered notices. Original state schema fields are sufficient; V2 uses separate local keys. No migration of V1 browser state.

Risks/limits: future-but-stale ETA policy remains unresolved; recorded delivery is not comprehension; mock outcomes are manually advanced. Existing contrast/screen-reader/200% zoom targets require explicit evidence, not an inference from tests. Bounded changes address RQ-01, RQ-02 and ID-01.
