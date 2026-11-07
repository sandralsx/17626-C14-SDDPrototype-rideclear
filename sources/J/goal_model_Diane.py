"""
Goal model extracted from the interview with Diane Fowler (paratransit budget manager).
17-626 HW2, Step 1.

Goal IDs: G-55 .. G-84 (continuing from goal_model_Janelle.py, G-1 .. G-24,
and goal_model_Frank.py, G-25 .. G-54).

Trace convention (comment above each goal):
    Source  -> timestamp (UTC, from Diane.csv) + quote from the stakeholder turn
    Derived -> goal not stated in the transcript; added by the refinement
               heuristic / pattern named, or by interpretation of a vague term

Vague / ambiguous terms resolved:
    "compliant"                -> the stakeholder's own definition: the reported
                                  numbers can be substantiated during an audit (G-57)
    "auditable"                -> audit records are append-only and cannot be
                                  altered after capture (G-71)
    "cost-effective"           -> cost per passenger trip is reduced against the
                                  approved service plan (G-56)
    "variance"                 -> a monthly metric deviates from its target in the
                                  approved service plan beyond a set tolerance (G-79)
    "without manual
     reconciliation"           -> dashboard metrics are computed directly from the
                                  audit trail (G-78)
    "operational cutoff"       -> a configurable change-control window before the
                                  pickup time (G-59, G-81, G-82)

Refinement annotation codes: see Appendix A of the assignment.
"""
from goalmodeling.schema import *


def performed_by(agent_name: str, agent_type: AgentType, operation_name: str):
    """Build a one-element performance list for a leaf goal."""
    if agent_type == AgentType.SOFTWARE_AGENT:
        category = OperationCategory.SOFTWARE_TO_BE_OPERATION
    else:
        category = OperationCategory.ENVIRONMENT_OPERATION
    return [PerformanceLink(Agent(agent_name, agent_type), Operation(operation_name, category))]


SYSTEM = AgentType.SOFTWARE_AGENT
ENV = AgentType.ENVIRONMENT_AGENT


def build():
    """Return (root goals, links) for the Diane goal model."""

    # ---------------------------------------------------------------- G-56 cost per trip
    # G-63 Source 22:18:00 "scheduling data synchronization" ... "drivers could receive
    #      current manifests and pickup information"
    g63 = MaintainGoal(
        "G-63: BookingsSyncedToDispatchAndDriverManifests",
        performs=performed_by("BookingSystem", SYSTEM, "Synchronize bookings to dispatch schedule and manifests"),
        leaf=True)
    # G-65 Derived (H9): implied by "vehicle utilization analysis" (22:17:19); a booked
    #      trip must hold a seat on the vehicle
    g65 = AchieveGoal(
        "G-65: SeatCapacityReserved <b>If</b> TripBooked",
        performs=performed_by("BookingSystem", SYSTEM, "Reserve seat on vehicle block"),
        leaf=True)
    # G-66 Derived (H9): converse of G-65; cancellations and no-shows (22:16:44) must
    #      free the seat again
    g66 = AchieveGoal(
        "G-66: SeatCapacityReleased <b>If</b> TripCancelledOrNoShow",
        performs=performed_by("BookingSystem", SYSTEM, "Release seat on vehicle block"),
        leaf=True)
    # G-64 Derived (H4): how is utilization measured and improved? capacity must be accurate
    g64 = MaintainGoal(
        "G-64: VehicleCapacityAccurate",
        refinements=[Refinement(True, [g65, g66], annotation="H9")])
    # G-61 Source 22:20:03 "better vehicle utilization"
    #      Source 22:16:00 "vehicle utilization"
    g61 = SoftGoal(
        "Maximize[G-61: VehicleUtilization]",
        refinements=[Refinement(False, [g63, g64], annotation="H4")])
    # G-67 Source 22:18:00 "Riders would have greater self-service capability"
    g67 = AchieveGoal(
        "G-67: TripBookedThroughSelfService",
        performs=performed_by("Rider", ENV, "Book trip in app"),
        leaf=True,
        annotation="expectation")
    # G-68 Source 22:16:44 "self-service booking and status notifications would reduce
    #      call-center volume"
    #      Source 22:18:00 "automated trip status updates"
    g68 = AchieveGoal(
        "G-68: StatusNotificationSent <b>If</b> TripStatusChanges",
        performs=performed_by("BookingSystem", SYSTEM, "Send trip status notification"),
        leaf=True)
    # G-62 Source 22:16:44 "would reduce call-center volume"
    #      Source 22:20:03 "Reduced call-center demand"
    g62 = SoftGoal(
        "Reduce[G-62: CallCenterVolume]",
        refinements=[Refinement(False, [g67, g68], annotation="H4")])
    # G-56 Source 22:15:35 "The trips themselves are the largest cost"
    #      Source 22:16:00 "cost per passenger trip"
    #      OR-refinement (H6): each alternative lowers cost per trip on its own, with
    #      different pros/cons (G-61 needs dispatch changes, G-62 needs rider adoption)
    g56 = SoftGoal(
        "Reduce[G-56: CostPerPassengerTrip]",
        refinements=[
            Refinement(False, [g61], annotation="H6"),
            Refinement(False, [g62], annotation="H6")])

    # ---------------------------------------------------------------- G-57 compliance
    # G-72 Source 22:17:19 "federally compliant reporting without relying on manual reconciliation"
    g72 = AchieveGoal(
        "G-72: ReportDraftGeneratedFromAuditTrail <b>If</b> ReportingPeriodEnds",
        performs=performed_by("BookingSystem", SYSTEM, "Generate denial and late-pickup report draft"),
        leaf=True)
    # G-73 Source 22:16:00 "produce federal reports on denials and late pickups"
    g73 = AchieveGoal(
        "G-73: ReportReviewedAndSubmitted <b>If</b> ReportDraftGenerated",
        performs=performed_by("BudgetManager", ENV, "Review and submit federal report"),
        leaf=True,
        annotation="expectation")
    # G-69 Source 22:16:00 "produce federal reports on denials and late pickups"
    #      Milestone-driven (P1): draft generated -> reviewed and submitted
    g69 = AchieveGoal(
        "G-69: FederalDenialAndLatePickupReportFiled <b>If</b> ReportingPeriodEnds",
        refinements=[Refinement(False, [g72, g73], annotation="P1")])
    # G-74..G-77 Source 22:16:44 "capture booking transactions, trip denials,
    #      cancellations, no-shows, and pickup timestamps in a centralized audit trail"
    g74 = AchieveGoal(
        "G-74: BookingLogged <b>If</b> TripBooked",
        performs=performed_by("BookingSystem", SYSTEM, "Write booking event to audit trail"),
        leaf=True)
    g75 = AchieveGoal(
        "G-75: DenialLogged <b>If</b> TripRequestDenied",
        performs=performed_by("BookingSystem", SYSTEM, "Write denial event to audit trail"),
        leaf=True)
    g76 = AchieveGoal(
        "G-76: CancellationOrNoShowLogged <b>If</b> TripCancelledOrNoShow",
        performs=performed_by("BookingSystem", SYSTEM, "Write cancellation or no-show event to audit trail"),
        leaf=True)
    g77 = AchieveGoal(
        "G-77: PickupTimestampLogged <b>If</b> RiderPickedUp",
        performs=performed_by("BookingSystem", SYSTEM, "Write pickup timestamp to audit trail"),
        leaf=True)
    # G-70 Source 22:17:19 "an auditable data lineage from booking through completed trip"
    #      Divide-and-conquer (P5) over the event types to be recorded
    g70 = MaintainGoal(
        "G-70: CompleteTripAuditTrail",
        refinements=[Refinement(False, [g74, g75, g76, g77], annotation="P5")])
    # G-71 Derived (H3): security-integrity category instantiated from "auditable record"
    #      (22:16:00)
    g71 = AvoidGoal(
        "G-71: AuditRecordAlteredAfterCapture",
        performs=performed_by("BookingSystem", SYSTEM, "Store audit records append-only"),
        leaf=True)
    # G-57 Source 22:16:00 "compliant means we can substantiate the numbers during an audit"
    #      Instantiated into information (G-69), completeness (G-70) and integrity (G-71)
    #      goal categories (H3)
    g57 = MaintainGoal(
        "G-57: ComplianceSubstantiatedDuringAudit",
        refinements=[Refinement(False, [g69, g70, g71], annotation="H3")])

    # ---------------------------------------------------------------- G-58 monthly review
    # G-78 Source 22:17:19 "It would provide operational dashboards"
    #      Source 22:16:00 "cost per passenger trip, vehicle utilization, on-time pickup
    #      performance, trip denials, and complaint trends"
    g78 = MaintainGoal(
        "G-78: OperationalDashboardComputedFromAuditTrail",
        performs=performed_by("BookingSystem", SYSTEM, "Compute cost per trip, utilization, on-time, denial and complaint metrics"),
        leaf=True)
    # G-79 Source 22:17:19 "automated variance analysis"
    g79 = AchieveGoal(
        "G-79: VarianceFlagged <b>If</b> MetricDeviatesFromServicePlan",
        performs=performed_by("BookingSystem", SYSTEM, "Flag metric outside service plan tolerance"),
        leaf=True)
    # G-80 Source 22:16:00 "I review monthly operating metrics"
    g80 = AchieveGoal(
        "G-80: MonthlyReviewCompleted <b>If</b> DashboardAndVariancesAvailable",
        performs=performed_by("BudgetManager", ENV, "Review metrics against approved service plan"),
        leaf=True,
        annotation="expectation")
    # G-58 Source 22:16:00 "I review monthly operating metrics ... against the approved service plan"
    #      Source 22:14:34 "I also review spending against our service commitments"
    #      Refined until each goal has a single responsible agent (H11)
    g58 = AchieveGoal(
        "G-58: MonthlyMetricsReviewedAgainstServicePlan <b>If</b> MonthEnds",
        refinements=[Refinement(False, [g78, g79, g80], annotation="H11")])

    # ---------------------------------------------------------------- G-59 change control
    # G-81 Derived (P3): the case outside the cutoff is not covered in the transcript
    g81 = AchieveGoal(
        "G-81: ChangeAppliedAutomatically <b>If</b> ChangeOutsideCutoff",
        performs=performed_by("BookingSystem", SYSTEM, "Apply change and sync dispatch"),
        leaf=True)
    # G-83 Source 22:19:24 "Changes inside the operational cutoff would need to enter an
    #      exception queue with an auditable timestamp"
    g83 = AchieveGoal(
        "G-83: ChangeQueuedWithTimestamp <b>If</b> ChangeInsideCutoff",
        performs=performed_by("BookingSystem", SYSTEM, "Add change to exception queue with timestamp"),
        leaf=True)
    # G-84 Source 22:19:24 "role-based approval for late modifications" ... "so dispatch
    #      can assess vehicle capacity and service impact before committing them"
    g84 = AchieveGoal(
        "G-84: QueuedChangeApprovedOrRejected <b>If</b> ChangeQueued",
        performs=performed_by("Dispatcher", ENV, "Assess capacity impact and approve or reject"),
        leaf=True,
        annotation="expectation")
    # G-82 Source 22:19:24 "role-based approval for late modifications"
    #      Milestone-driven (P1): queued -> decided
    g82 = AchieveGoal(
        "G-82: LateChangeDecided <b>If</b> ChangeInsideCutoff",
        refinements=[Refinement(False, [g83, g84], annotation="P1")])
    # G-59 Source 22:19:24 "configurable change-control windows, real-time dispatch
    #      synchronization, and role-based approval for late modifications"
    #      Decomposition by case (P3): outside / inside the cutoff covers all changes
    g59 = MaintainGoal(
        "G-59: TripChangesControlledByCutoffWindow",
        refinements=[Refinement(True, [g81, g82], annotation="P3")])

    # ---------------------------------------------------------------- G-60 implementation cost
    # G-60 Source 22:20:03 "could justify the expense if the implementation remains
    #      controlled and cost-effective"
    g60 = SoftGoal(
        "Minimize[G-60: BookingSystemImplementationCost]",
        performs=performed_by("BudgetManager", ENV, "Weigh technology spending against expected savings"),
        leaf=True)

    # ---------------------------------------------------------------- G-55 root
    # G-55 Source 22:14:34 "review spending against our service commitments so we remain
    #      cost-effective and compliant"
    #      Abstracted from the goals below up to the agency's service boundary (H12)
    g55 = SoftGoal(
        "Improve[G-55: CostEffectiveAndCompliantParatransitService]",
        refinements=[Refinement(False, [g56, g57, g58, g59, g60], annotation="H12")])

    # ---------------------------------------------------------------- conflicts
    # Source 22:20:03: call-center savings (G-62) require building self-service booking
    # and notifications, which competes with keeping implementation cost down (G-60);
    # Diane says the savings "could" justify the expense only "if the implementation
    # remains controlled and cost-effective".
    links = [ConflictLink(g60, g62)]

    return [g55], links


if __name__ == "__main__":
    roots, links = build()
    output = generate_graph(roots, links)
    print(output)

    config = {"theme": "default", "themeVariables": {"fontFamily": "Helvetica"}}
    print(generate_pako_link(output, "edit", config=config))
