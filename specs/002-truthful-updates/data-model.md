# V2 data model revision

Retain V1 Trip/Notice/Attempt/Request fields and source snapshots. Add notice kind `elapsed` for an updated but already elapsed non-delayed estimate. No age/SLA field or guessed arrival is added.

Derived, not stored: elapsed estimate usability from nonterminal status and now>eta; discovery-before-end from createdAt<windowEnd; delivery timing from recorded deliveredAt and windowEnd; pending/deadline-without-evidence from now and missing delivery. Acknowledgement remains a separate fact. Original timestamps are immutable except their explicit allowed outcome transition from null to the current simulated time.

New fixture names `elapsed-eta` and `late-delivery` are deterministic fictional sequences. V2 keeps schemaVersion1 because its new origin/key starts a separate demo document; it never reads/writes the V1 key.
