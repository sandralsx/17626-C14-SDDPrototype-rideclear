# Goal model V2 — technical revision after V1 evaluation

Read with retained [full V1 model and conflicts](goal-model.md) and [V2 JSON](goal-model-v2.json). All eight selected goals, 210 original combined goal definitions, individual aliases, provenance and deferred goals remain preserved in the original JSON/sources. This overlay changes interpretation/relations without claiming new stakeholder evidence.

| Original goal / relation | V1 observation | V2 refinement / relation | Status / assumption |
| --- | --- | --- | --- |
| A3-G02 current status/ETA → G07 reliable Return info; D10 | RQ-01 / EV12,26: elapsed ETA called within-window/recovered | G02-U usable interpretation requires last recorded value+as-of+explicit elapsed warning; display alone supports, but does not establish, G07 reliability | FR-017; elapsed now>eta is V2-PA-01, not stakeholder-confirmed age SLA. U02/U03 remain unresolved. |
| A3-G03 early notice depends on G08 communication evidence; D03/D05 | RQ-02 / EV06,17: early discovery with late delivery | Split discovery-before-end from recorded delivery-before-end; G03-D and G03-R are distinct evaluation subgoals. A sent event alone cannot establish receipt. G08 supports delivery/ack evidence, not guaranteed comprehension | FR-018; V2-PA-02 minimum delivery evidence only. U01/U04 receipt success/escalation remain open. |
| A3-G06 accessible journey constrains G03/G08; D08 | ID-01 / EV20: keyboard focus falls to BODY | Stable acknowledged control/focus continuation realizes the existing constraint; no new independent stakeholder goal | FR-019 clarification; implementation defect correction. |

D01 window versus ETA, D04 passive status versus distinct notification, D05 acceptance trigger versus predicted delay, D07 contact response and D12 no automatic approval remain separate. Shared data G05 continues to support both timestamp/presentation views. D03 late discovery cannot be made early. D10 now explicitly separates availability of an input from usability of its interpretation.

No original conflict is removed: cost/call volume versus broader operational scope, J:G-60↔G-62, external system boundaries and unconfirmed source-model numeric details remain as in the full model. D09 still limits G07 to information quality; physical punctuality/accurate prediction cannot be established by a mock. No general one-minute refresh SLA or proof-of-comprehension requirement is fabricated. No stakeholder clarification has occurred.
