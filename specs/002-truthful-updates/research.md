# V2 technical decisions and open questions

RQ-01: use an elapsed-time warning rather than rejecting all past input, so last-known data remains inspectable and no actual arrival is fabricated. This is a new explicit requirement derived from observed goal insufficiency. It resolves the deterministic past-ETA case while leaving future-estimate age SLA U02/U03 open.

RQ-02: derive separate delivery evidence from existing attempt timestamps instead of reusing earlyNoticeMiss or adding an invented success flag. Use strict-before boundary and label missing records. Delivery is a minimum technical observation; channel-specific informed/understood success and escalation ownership remain open. No automatic hold/cancel action is introduced.

ID-01: retain the native acknowledgement button, mark it aria-disabled after success and guard activation; this keeps keyboard location without enabling duplicate actions. UI/UX skill search supplied general native-control/keyboard guidance; the actual disappearance defect and V1 contract are the governing evidence.

Use existing runtime and visual design. No real integrations, new packages, broad redesign or independent student reflection is needed for these changes.
