"""
Goal model extracted from the interview with Diane Fowler (transit agency budget manager).
17-626 Assignment 2: Requirements Analysis. Qingyuan Yao (qingyuay).

Source: transcripts/Diane.txt, turns T1 to T29. The comment above each goal cites the
turn(s) it comes from. Goals tagged NOT IN TRANSCRIPT came from a refinement pattern or
heuristic, or from my own interpretation, and are listed in missing.json.

Conventions
- Goal IDs G-69 to G-105 belong to this model. IDs are unique across all three models.
- Refinement annotations carry only the heuristic or pattern code (Appendix A).
- Each leaf goal is assigned to exactly one agent.

Vague terms resolved
- "compliant" (T10): Diane defines it in T18. "Compliant means we pass the audit, not merely
  that we can produce a spreadsheet afterward" (G-70).
- "timely reports on denials and late pickups" (T26): reports produced from the trip data at
  the end of each reporting period (G-75).
- "clear controls over same-day changes" (T26): every change carries an exception code, and
  a dispatcher reviews each same-day change (G-79, G-80).
- "appropriate safeguards around repeated no-shows" (T26): notice and an appeal before any
  sanction (G-85, G-86, G-87).
- "reliable projections" and "dependable budget forecasting" (T10, T26): projections produced
  at the start of each budget cycle from the recorded trip data (G-92).

Conflicts
- G-76 Reduce[AvoidableTripCost] vs G-105 Avoid[RiderSanctionedWithoutNoticeOrAppeal]:
  T26 "cost control has to be balanced with notice and due process." Sanctions for repeated
  no-shows save cost, and notice plus appeal delays them. Resolution (H8): a sanction applies
  only after notice is given and any appeal is resolved (G-87).
"""
from goalmodeling.schema import *


def by(agent_name, software=False):
    """Assign a leaf goal to exactly one agent. Each leaf gets its own agent node, which keeps the graph legible."""
    agent_type = AgentType.SOFTWARE_AGENT if software else AgentType.ENVIRONMENT_AGENT
    return [PerformanceLink(Agent(agent_name, agent_type), None)]


# ---------------------------------------------------------------------------------------
# G-70: federal compliance review
# ---------------------------------------------------------------------------------------

# T14 "an immutable audit trail"; T18 "The system needs an immutable audit trail"; T12 "an auditable change history";
# T16 "event-level auditability for no-shows, cancellations, route reassignment, and late pickups"
g72 = MaintainGoal("<b>G-72</b> ImmutableAuditTrailOfTripEvents",
                   performs=by("TripRecordSystem", software=True), leaf=True)

# T18 "traceability from eligibility determination through trip authorization, dispatch events, and final reconciliation"
g73 = MaintainGoal("<b>G-73</b> TripRecordLinksEligibilityAuthorizationDispatchAndReconciliation",
                   performs=by("TripRecordSystem", software=True), leaf=True)

# T18 "Federal compliance reviews require traceability from eligibility determination ... final reconciliation"
g71 = MaintainGoal("<b>G-71</b> TripTraceableFromEligibilityToReconciliation",
                   refinements=[Refinement(complete=False, children=[g72, g73], annotation="P5")])

# T18 "standardized denial and late-pickup reason codes"
g74 = AchieveGoal("<b>G-74</b> StandardReasonCodeRecorded <b>If</b> DenialOrLatePickupOccurs",
                  performs=by("TripRecordSystem", software=True), leaf=True)

# T26 "timely reports on denials and late pickups for federal review"; T18 "reproducible reporting so an
# auditor can validate service decisions against the underlying trip data" (the condition is my reading of "timely")
g75 = AchieveGoal("<b>G-75</b> DenialAndLatePickupReportProducedFromTripData <b>If</b> ReportingPeriodEnds",
                  performs=by("ReportingSystem", software=True), leaf=True)

# T10 "our records have to support federal compliance reviews"; T18 "Compliant means we pass the audit"
g70 = AchieveGoal("<b>G-70</b> FederalComplianceReviewPassed",
                  refinements=[Refinement(complete=False, children=[g71, g74, g75], annotation="H4")])

# ---------------------------------------------------------------------------------------
# G-76: avoidable cost
# ---------------------------------------------------------------------------------------

# T10 "better visibility into cancellations, no-shows, vehicle utilization, and how far in advance riders book";
# T24 "better visibility into demand patterns"
g77 = MaintainGoal("<b>G-77</b> CostDriverMetricsReported",
                   performs=by("ReportingSystem", software=True), leaf=True)

# T12 "clear exception coding"; T14 "structured exception codes"
g79 = AchieveGoal("<b>G-79</b> ExceptionCodeRecorded <b>If</b> TripChangedOrCancelled",
                  performs=by("TripRecordSystem", software=True), leaf=True)

# NOT IN TRANSCRIPT: my reading of "clear controls over same-day changes" (T26)
g80 = AchieveGoal("<b>G-80</b> SameDayChangeReviewedByDispatcher <b>If</b> ChangeRequested",
                  performs=by("Dispatcher"), leaf=True)

# T26 "clear controls over same-day changes"; T24 "more disciplined handling of changes";
# T10 "same-day changes are driving costs faster than our budget can absorb"
g78 = MaintainGoal("<b>G-78</b> SameDayChangesControlled",
                   refinements=[Refinement(complete=False, children=[g79, g80], annotation="H5")])

# T16 "distinguish rider-caused loss from agency service failure" (no-shows, cancellations)
g82 = AchieveGoal("<b>G-82</b> LossCodedAsRiderCaused <b>If</b> NoShowOrLateCancel",
                  performs=by("TripRecordSystem", software=True), leaf=True)

# T16 "distinguish rider-caused loss from agency service failure" (route reassignment, late pickups)
g83 = AchieveGoal("<b>G-83</b> LossCodedAsAgencyServiceFailure <b>If</b> LatePickupOrRouteReassignment",
                  performs=by("TripRecordSystem", software=True), leaf=True)

# T16 (the two causes Diane distinguishes cover every loss event)
dp3 = DomainProperty("DP-3 EachLossEvent IsRiderCaused Or AgencyCaused", leaf=True)

# T16 "standardized reason codes so we can distinguish rider-caused loss from agency service failure.
# Those records are necessary for cost attribution"
g81 = AchieveGoal("<b>G-81</b> LossAttributedToCause <b>If</b> ServiceLossEventOccurs",
                  refinements=[Refinement(complete=True, children=[g82, g83, dp3], annotation="P3")])

# T26 "notice"
g85 = AchieveGoal("<b>G-85</b> RiderNotifiedBeforeSanction <b>If</b> SanctionProposed",
                  performs=by("AgencyStaff"), leaf=True)

# T26 "due process"
g86 = AchieveGoal("<b>G-86</b> AppealHeardBeforeSanction <b>If</b> RiderAppeals",
                  performs=by("AgencyStaff"), leaf=True)

# T26 "appropriate safeguards around repeated no-shows, because cost control has to be balanced with notice and due process"
g87 = AchieveGoal("<b>G-87</b> SanctionApplied <b>If</b> NoShowsRepeated And NoticeGiven And AppealResolved",
                  performs=by("AgencyStaff"), leaf=True)

# T26 "We also need appropriate safeguards around repeated no-shows"
g84 = AchieveGoal("<b>G-84</b> RepeatedNoShowsAddressed <b>If</b> NoShowPatternDetected",
                  refinements=[Refinement(complete=False, children=[g85, g86, g87], annotation="H8")])

# T10 "trip volume and same-day changes are driving costs faster than our budget can absorb";
# T16 "manifest instability has a direct budget impact through deadhead mileage, missed vehicle utilization,
# overtime, and disputed trip reconciliation"
g76 = SoftGoal("Reduce[<b>G-76</b> AvoidableTripCost]",
               refinements=[Refinement(complete=False, children=[g77, g78, g81, g84], annotation="H4")])

# ---------------------------------------------------------------------------------------
# G-88: one trip record for finance and operations
# ---------------------------------------------------------------------------------------

# T14 "so a change in one stage propagates correctly to the manifest and financial reporting";
# T12 "manifest integrity across booking, modification, cancellation, and dispatch status"
g89 = AchieveGoal("<b>G-89</b> ChangePropagatedToManifestAndFinancialReports <b>If</b> TripRecordChanged",
                  performs=by("TripRecordSystem", software=True), leaf=True)

# T12 "standardized eligibility and service-type fields rather than relying on free-text notes";
# T14 "separate processes with inconsistent data fields"
g90 = MaintainGoal("<b>G-90</b> EligibilityAndServiceTypeStoredAsStructuredFields",
                   performs=by("TripRecordSystem", software=True), leaf=True)

# T8 "documenting trips and tracking spending. That financial visibility needs to continue."
g91 = MaintainGoal("<b>G-91</b> TripsAndSpendingDocumented",
                   performs=by("ReportingSystem", software=True), leaf=True)

# T12 "so finance and operations are reviewing the same trip record"; T14 "We need a canonical trip record"
g88 = MaintainGoal("<b>G-88</b> FinanceAndOperationsShareOneTripRecord",
                   refinements=[Refinement(complete=False, children=[g89, g90, g91], annotation="P5")])

# ---------------------------------------------------------------------------------------
# G-92 and G-93
# ---------------------------------------------------------------------------------------

# T10 "reliable projections for contracts, staffing, and vehicle demand"; T26 "dependable budget forecasting"
# (the condition is my reading of "reliable" and "dependable")
g92 = AchieveGoal("<b>G-92</b> ProjectionsForContractsStaffingAndVehicleDemandProduced <b>If</b> BudgetCycleStarts",
                  performs=by("ReportingSystem", software=True), leaf=True)

# T26 "financial and eligibility information should not be visible to everyone who uses the system"
g94 = AvoidGoal("<b>G-94</b> FinancialOrEligibilityDataShownToUnauthorizedRole",
                performs=by("TripRecordSystem", software=True), leaf=True)

# NOT IN TRANSCRIPT: heuristic H3 (security goal category: keep sensitive-data access accountable)
g95 = AchieveGoal("<b>G-95</b> AccessToSensitiveDataLogged <b>If</b> DataViewed",
                  performs=by("TripRecordSystem", software=True), leaf=True)

# T26 "security and role-based access matter"; T14 "role-based controls"
g93 = MaintainGoal("<b>G-93</b> FinancialAndEligibilityDataVisibleOnlyByRole",
                   refinements=[Refinement(complete=False, children=[g94, g95], annotation="H3")])

# ---------------------------------------------------------------------------------------
# G-96: routine calls
# ---------------------------------------------------------------------------------------

# T22 "The system should use structured triage, validation rules, and escalation codes"
g98 = AchieveGoal("<b>G-98</b> RequestTriagedByValidationRules <b>If</b> RequestSubmitted",
                  performs=by("BookingSystem", software=True), leaf=True)

# T22 "routine eligible trips can follow a self-service workflow"
g99 = AchieveGoal("<b>G-99</b> TripBookedViaSelfService <b>If</b> RoutineAndEligible",
                  performs=by("BookingSystem", software=True), leaf=True)

# T22 "exceptions should be routed to a staffed assistance queue"; "escalation codes"
g101 = AchieveGoal("<b>G-101</b> ExceptionQueuedWithEscalationCode <b>If</b> NotRoutineOrNeedsReview",
                   performs=by("BookingSystem", software=True), leaf=True)

# T26 "while still allowing staff to handle exceptions fairly"; T22 "staff time is reserved for eligibility
# questions, complex modifications, and cases requiring human review"
g102 = AchieveGoal("<b>G-102</b> ExceptionResolvedFairlyByStaff <b>If</b> ExceptionQueued",
                   performs=by("AgencyStaff"), leaf=True)

# T22 "exceptions should be routed to a staffed assistance queue rather than forcing every request through the phone center"
g100 = AchieveGoal("<b>G-100</b> ExceptionHandledByStaff <b>If</b> NotRoutineOrNeedsReview",
                   refinements=[Refinement(complete=False, children=[g101, g102], annotation="H5")])

# T22 (routine eligible trips vs exceptions cover every request)
dp4 = DomainProperty("DP-4 EachRequest IsRoutineAndEligible Or NeedsReview", leaf=True)

# T10 "the phone center carrying too much routine booking work" (the current way, kept as the alternative)
g103 = AchieveGoal("<b>G-103</b> EveryRequestHandledByPhoneCenter",
                   performs=by("ReservationAgent"), leaf=True)

# T22 "routine eligible trips can follow a self-service workflow, while exceptions should be routed to a staffed
# assistance queue rather than forcing every request through the phone center"
g97 = AchieveGoal("<b>G-97</b> TripRequestHandled <b>If</b> RequestSubmitted",
                  refinements=[
                      # Alternative 1: triage into self-service and a staffed queue
                      Refinement(complete=True, children=[g98, g99, g100, dp4], annotation="P2"),
                      # Alternative 2: every request through the phone center (the current process)
                      Refinement(complete=False, children=[g103], annotation="H6"),
                  ])

# T10 "riders could complete it through an accessible self-service process"; T26 "The rider-facing portion must be accessible"
g104 = MaintainGoal("<b>G-104</b> RiderFacingBookingAccessible",
                    performs=by("BookingSystem", software=True), leaf=True)

# T10 "the phone center carrying too much routine booking work"; T26 "reduce routine calls"
g96 = SoftGoal("Reduce[<b>G-96</b> RoutineCallsToPhoneCenter]",
               refinements=[Refinement(complete=False, children=[g97, g104], annotation="H4")])

# ---------------------------------------------------------------------------------------
# Roots
# ---------------------------------------------------------------------------------------

# T2 "manage paratransit costs responsibly"; T6 "how service levels and trip volume affect what we can afford";
# T10 "careful distinctions between necessary service and trips that could be handled more cost-effectively";
# T24 "the operational data and the service obligations involved"
g69 = MaintainGoal("<b>G-69</b> ServiceObligationsMetWithinBudget",
                   refinements=[Refinement(complete=False, children=[g70, g76, g88, g92, g93, g96], annotation="H12")])

# T26 "cost control has to be balanced with notice and due process"
# (the converse of G-87: no sanction unless notice was given and any appeal was heard)
g105 = AvoidGoal("<b>G-105</b> RiderSanctionedWithoutNoticeOrAppeal",
                 refinements=[Refinement(complete=False, children=[g85, g86], annotation="H9")])

ROOTS = [g69, g105]
CONFLICTS = [ConflictLink(g76, g105)]  # T26: cost control vs notice and due process
# Goals not in the transcript. They are highlighted yellow in the diagram.
NOT_IN_TRANSCRIPT = {"G-80": g80, "G-95": g95}


def highlight(graph, goals):
    """Color the goals that are not in the transcript yellow."""
    return graph + "".join(f"style {g.get_node_id()} fill:#fff59d,stroke:#b59f00\n" for g in goals)


if __name__ == "__main__":
    graph = highlight(generate_graph(ROOTS, CONFLICTS), NOT_IN_TRANSCRIPT.values())
    print(graph)
    print(generate_pako_link(graph, "view",
                             config={"theme": "default", "themeVariables": {"fontFamily": "Tahoma"}}))
