"""
Combined goal model merging goal_model_Janelle.py (rider), goal_model_Frank.py
(dispatcher) and goal_model_Diane.py (budget manager).
17-626 HW2, Step 2.

Goal IDs are kept from the individual models so every goal traces back to its
source model and transcript (see the Source/Derived comments there). Goals removed
by a merge keep their ID retired; new goals created while merging continue at G-85.
Origin tags in the comments below: [J] Janelle, [F] Frank, [D] Diane, [C] new in
the combined model.

Redundancies (duplicate goals merged; retained goal rewritten to include both):
    G-44 [F] RiderNotified If PickupWindowAdjusted
    G-68 [D] StatusNotificationSent If TripStatusChanges
        -> merged into G-17 [J] RiderNotified If PickupDelayedOrTripStatusChanges
    G-67 [D] TripBookedThroughSelfService
        -> merged into G-7 [J] RoundTripBookedThroughSelfService
    G-53 [F] ChangeRequiresDispatcherApproval If ChangeInsideCutoff
        -> merged into G-82 [D] LateChangeDecidedByDispatcher If ChangeInsideCutoff
    G-63 [D] BookingsSyncedToDispatchAndDriverManifests
        -> merged into G-32 [F] ManifestBlockAndAssignmentSyncedWithDispatchRecordInRealTime

Inconsistencies (resolved by rewriting goals):
    I-1 G-81 [D] said changes outside the cutoff are "applied automatically", but
        Frank needs every change rechecked against the run first (G-30, G-39).
        Fix: G-81 now only waives dispatcher approval outside the cutoff, and G-59
        sits under G-36, so every change still passes the run recheck and conflict
        flagging before it is committed (G-37).
    I-2 G-27 [F] split role-based views into a complete case decomposition over
        dispatcher / driver / rider only. Diane adds two more roles: the budget
        manager (dashboards) and call-center staff (22:18:00). Fix: G-78 is
        conditioned on UserIsBudgetManager and added as a case of G-27, and new goal
        G-86 covers call-center staff, so the case split is complete again.

Conflicts (shown with conflict links):
    C-1 G-3 [J] TripChanged If RiderRequestsChange ("change them when needed")
        vs G-28 [F] Reduce[LastMinuteTripChanges] ("I want fewer last-minute changes").
        Resolution: Diane's change-control window (G-59). Outside the cutoff the
        rider's change is accepted without approval (G-81); inside the cutoff it
        goes to the exception queue for a dispatcher decision (G-82), and the rider
        is told the reason and alternatives if it is rejected (G-14).
    C-2 G-60 [D] Minimize[BookingSystemImplementationCost]
        vs G-62 [D] Reduce[CallCenterVolume], which needs self-service booking and
        notifications to be built (Diane 22:20:03).

Refinement annotation codes: see Appendix A of the assignment.
"""
import os
import re

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

# Goals not stated in any transcript (refinement heuristics/patterns, interpretation
# of vague terms, or added while merging); highlighted in yellow in the diagram.
DERIVED_GOALS = {
    "G-8", "G-12", "G-14", "G-18", "G-19", "G-22", "G-23", "G-36", "G-38", "G-43",
    "G-49", "G-52", "G-54", "G-64", "G-65", "G-66", "G-71", "G-81", "G-85", "G-86",
}


def highlight_derived(diagram: str) -> str:
    """Append Mermaid style statements that fill the derived goals in yellow."""
    styles = ""
    for node_id, goal_id in dict.fromkeys(re.findall(r'^(node\d+)\[/"\w+\[(G-\d+):', diagram, re.M)):
        if goal_id in DERIVED_GOALS:
            styles += f"style {node_id} fill:#ffff00\n"
    return diagram.rstrip() + "\n" + styles


def build():
    """Return (root goals, links) for the combined goal model."""

    # ================================================================ shared goals
    # Goals reached from more than one parent after merging are built first.

    # G-17 [J] merged with G-44 [F] and G-68 [D]
    #      Janelle 21:58:11 "notify me if the pickup is delayed or changed"
    #      Diane 22:16:44 "status notifications would reduce call-center volume"
    #      Frank G-44 (derived): a rider whose pickup window is adjusted must be told
    g17 = AchieveGoal(
        "G-17: RiderNotified <b>If</b> PickupDelayedOrTripStatusChanges",
        performs=performed_by("BookingSystem", SYSTEM, "Push delay, change or status notification"),
        leaf=True)

    # G-7  [J] merged with G-67 [D]
    #      Janelle 21:56:06 "I'd want to book both trips online"
    #      Diane 22:18:00 "Riders would have greater self-service capability"
    g9 = AchieveGoal(
        "G-9: OutboundAndReturnTripDetailsSubmitted",
        performs=performed_by("Rider", ENV, "Enter outbound and return trip details in app"),
        leaf=True,
        annotation="expectation")
    g10 = AchieveGoal(
        "G-10: BookingConfirmed <b>If</b> TripDetailsSubmitted",
        performs=performed_by("BookingSystem", SYSTEM, "Send confirmation with pickup window for each trip"),
        leaf=True)
    g7 = AchieveGoal(
        "G-7: RoundTripBookedThroughSelfService",
        refinements=[Refinement(False, [g9, g10], annotation="P1")])

    # G-32 [F] merged with G-63 [D]
    #      Frank 22:09:51 "the manifest and run should update together"
    #      Diane 22:18:00 "scheduling data synchronization" ... "drivers could receive
    #      current manifests"; Diane 22:19:24 "real-time dispatch synchronization"
    g33 = MaintainGoal(
        "G-33: ManifestSyncedWithDispatchRecord",
        performs=performed_by("BookingSystem", SYSTEM, "Regenerate manifest on record change"),
        leaf=True)
    g34 = MaintainGoal(
        "G-34: VehicleBlockSyncedWithDispatchRecord",
        performs=performed_by("BookingSystem", SYSTEM, "Update vehicle block on record change"),
        leaf=True)
    g35 = MaintainGoal(
        "G-35: DriverAssignmentSyncedWithDispatchRecord",
        performs=performed_by("BookingSystem", SYSTEM, "Update driver assignment on record change"),
        leaf=True)
    g32 = MaintainGoal(
        "G-32: ManifestBlockAndAssignmentSyncedWithDispatchRecordInRealTime",
        refinements=[Refinement(True, [g33, g34, g35], annotation="P5")])

    # G-59 [D] change control, shared by Frank's change handling (G-36) and
    #      Diane's root (G-55); resolves conflict C-1 and inconsistency I-1
    # G-81 [D] rewritten (I-1): outside the cutoff only the approval step is waived
    g81 = AchieveGoal(
        "G-81: ChangeAcceptedWithoutDispatcherApproval <b>If</b> ChangeOutsideCutoff",
        performs=performed_by("BookingSystem", SYSTEM, "Accept change and pass it to run recheck"),
        leaf=True)
    g83 = AchieveGoal(
        "G-83: ChangeQueuedWithTimestamp <b>If</b> ChangeInsideCutoff",
        performs=performed_by("BookingSystem", SYSTEM, "Add change to exception queue with timestamp"),
        leaf=True)
    g84 = AchieveGoal(
        "G-84: QueuedChangeApprovedOrRejected <b>If</b> ChangeQueued",
        performs=performed_by("Dispatcher", ENV, "Assess capacity impact and approve or reject"),
        leaf=True,
        annotation="expectation")
    # G-82 [D] merged with G-53 [F]
    #      Diane 22:19:24 "role-based approval for late modifications"
    #      Frank 22:10:28 "I want fewer last-minute changes"
    g82 = AchieveGoal(
        "G-82: LateChangeDecidedByDispatcher <b>If</b> ChangeInsideCutoff",
        refinements=[Refinement(False, [g83, g84], annotation="P1")])
    g59 = MaintainGoal(
        "G-59: TripChangesControlledByCutoffWindow",
        refinements=[Refinement(True, [g81, g82], annotation="P3")])

    # G-78 [D] rewritten (I-2): now also the budget-manager case of G-27
    #      Diane 22:17:19 "It would provide operational dashboards"
    g78 = MaintainGoal(
        "G-78: OperationalDashboardComputedFromAuditTrail <b>If</b> UserIsBudgetManager",
        performs=performed_by("BookingSystem", SYSTEM, "Compute cost per trip, utilization, on-time, denial and complaint metrics"),
        leaf=True)

    # ================================================================ Janelle (rider)
    # G-8  [J] derived (H6)
    g8 = AchieveGoal(
        "G-8: RecurringTripsBooked <b>If</b> RiderHasStandingWorkSchedule",
        performs=performed_by("BookingSystem", SYSTEM, "Generate recurring trips from saved work schedule"),
        leaf=True)
    # G-2  [J]
    g2 = SoftGoal(
        "Reduce[G-2: TimeSpentBookingRoutineTrips]",
        refinements=[
            Refinement(False, [g7], annotation="H6"),
            Refinement(False, [g8], annotation="H6")])

    # G-11..G-14 [J]
    g11 = AchieveGoal(
        "G-11: ChangeRequestSubmittedInApp",
        performs=performed_by("Rider", ENV, "Edit trip in app"),
        leaf=True,
        annotation="expectation")
    g13 = AchieveGoal(
        "G-13: UpdatedConfirmationSent <b>If</b> ChangeAccepted",
        performs=performed_by("BookingSystem", SYSTEM, "Send updated trip confirmation"),
        leaf=True)
    g14 = AchieveGoal(
        "G-14: ReasonAndAlternativesShown <b>If</b> ChangeRejected",
        performs=performed_by("BookingSystem", SYSTEM, "Show rejection reason and alternative times"),
        leaf=True)
    g12 = AchieveGoal(
        "G-12: ChangeOutcomeCommunicated <b>If</b> ChangeRequestSubmitted",
        refinements=[Refinement(True, [g13, g14], annotation="P3")])

    # G-15..G-22 [J]
    g18 = MaintainGoal(
        "G-18: ReportedVehicleLocation <b>Equals</b> ActualVehicleLocation",
        performs=performed_by("VehicleGPS", ENV, "Report vehicle position"),
        leaf=True,
        annotation="expectation")
    g19 = MaintainGoal(
        "G-19: ETARecomputedFromReportedLocationEveryMinute",
        performs=performed_by("BookingSystem", SYSTEM, "Recompute ETA from GPS position and traffic"),
        leaf=True)
    g20 = AchieveGoal(
        "G-20: ETAShown <b>If</b> RiderViewsUpcomingTrip",
        performs=performed_by("BookingSystem", SYSTEM, "Display ETA on trip screen"),
        leaf=True)
    g15 = MaintainGoal(
        "G-15: RealisticETADisplayed",
        refinements=[Refinement(True, [g18, g19, g20], annotation="P6")])
    g21 = AchieveGoal(
        "G-21: OnTimeStatusShown <b>If</b> ETAWithinPickupWindow",
        performs=performed_by("BookingSystem", SYSTEM, "Label trip as on time"),
        leaf=True)
    g22 = AvoidGoal(
        "G-22: OnTimeStatusShown <b>If</b> ETAOutsidePickupWindow",
        performs=performed_by("BookingSystem", SYSTEM, "Label trip as delayed with new ETA"),
        leaf=True)
    g16 = MaintainGoal(
        "G-16: TripStatusTruthful",
        refinements=[Refinement(True, [g21, g22], annotation="H10")])
    g4 = MaintainGoal(
        "G-4: RiderInformedOfAccurateTripStatus",
        refinements=[Refinement(False, [g15, g16, g17], annotation="H3")])

    # G-5, G-6, G-23, G-24 [J] non-functional
    g23 = MaintainGoal(
        "G-23: AppConformsToWCAG2.1AA",
        performs=performed_by("BookingSystem", SYSTEM, "Support screen reader, scalable text, high contrast"),
        leaf=True)
    g24 = MaintainGoal(
        "G-24: UpcomingTripDetailsShownOnHomeScreen",
        performs=performed_by("BookingSystem", SYSTEM, "List each upcoming trip on home screen"),
        leaf=True)
    g5 = SoftGoal(
        "Improve[G-5: BookingAppAccessibility]",
        refinements=[Refinement(False, [g23, g24], annotation="H4")])
    g6 = SoftGoal(
        "Maximize[G-6: BookingAppAvailabilityDuringServiceHours]",
        performs=performed_by("BookingSystem", SYSTEM, "Serve booking requests during service hours"),
        leaf=True)

    # ================================================================ Frank (dispatcher)
    # G-29, G-31 [F]
    g31 = AvoidGoal(
        "G-31: TripDetailsEnteredMoreThanOnce",
        performs=performed_by("BookingSystem", SYSTEM, "Accept trip edits only through shared dispatch record"),
        leaf=True)
    g29 = MaintainGoal(
        "G-29: SingleSharedDispatchRecord",
        refinements=[Refinement(False, [g31, g32], annotation="H4")])

    # G-30, G-36..G-43 [F]
    g39 = AchieveGoal(
        "G-39: RunImpactRechecked <b>If</b> TripChangeRequested",
        performs=performed_by("BookingSystem", SYSTEM, "Recheck capacity, pickup windows and downstream connections"),
        leaf=True)
    g40 = AchieveGoal(
        "G-40: ConflictFlaggedOnBoard <b>If</b> CapacityOrSequenceConflict",
        performs=performed_by("BookingSystem", SYSTEM, "Raise conflict alert on live board"),
        leaf=True)
    g42 = AchieveGoal(
        "G-42: TripMovedToVehicleWithCapacity",
        performs=performed_by("Dispatcher", ENV, "Reassign trip to another vehicle block"),
        leaf=True,
        annotation="expectation")
    g43 = AchieveGoal(
        "G-43: PickupWindowAdjusted",
        performs=performed_by("Dispatcher", ENV, "Adjust pickup window and resequence run"),
        leaf=True,
        annotation="expectation")
    # G-41 [F]: second alternative now uses the merged G-17 in place of G-44
    g41 = AchieveGoal(
        "G-41: ConflictResolved <b>If</b> ConflictFlaggedOnBoard",
        refinements=[
            Refinement(False, [g42], annotation="H4"),
            Refinement(False, [g43, g17], annotation="H4")])
    # G-36 [F]: now also requires Diane's cutoff control G-59 (I-1, C-1)
    g36 = AchieveGoal(
        "G-36: ChangeClearedForRun <b>If</b> TripChangeRequested",
        refinements=[Refinement(False, [g39, g40, g41, g59], annotation="H5")])
    g37 = AchieveGoal(
        "G-37: ChangeCommittedToRun <b>If</b> ChangeClearedForRun",
        performs=performed_by("BookingSystem", SYSTEM, "Update manifest, run and vehicle block together"),
        leaf=True)
    g38 = MaintainGoal(
        "G-38: ChangeRequestPending <b>Unless</b> ChangeCommitted",
        performs=performed_by("BookingSystem", SYSTEM, "Hold request in pending change queue"),
        leaf=True)
    g30 = AchieveGoal(
        "G-30: TripChangeReflectedInRun <b>If</b> TripChangeRequested",
        refinements=[Refinement(False, [g36, g37, g38], annotation="P4")])

    # G-3  [J]: the rider's change is realized through Frank's run update G-30
    g3 = AchieveGoal(
        "G-3: TripChanged <b>If</b> RiderRequestsChange",
        refinements=[Refinement(False, [g11, g30, g12], annotation="H4")])

    # G-1  [J] root of the rider's model
    g1 = SoftGoal(
        "Improve[G-1: RiderBookingAndTrackingExperience]",
        refinements=[Refinement(False, [g2, g3, g4, g5, g6], annotation="H7")])

    # G-26 [F]
    g26 = SoftGoal(
        "Reduce[G-26: ManualReentryAndRechecking]",
        refinements=[Refinement(False, [g29, g30], annotation="H4")])

    # G-27 role cases [F], completed with G-78 [D] and G-86 [C] (I-2)
    g45 = MaintainGoal(
        "G-45: LiveBoardShowsCapacityWindowsAndAssignments <b>If</b> UserIsDispatcher",
        performs=performed_by("BookingSystem", SYSTEM, "Render live dispatch board"),
        leaf=True)
    g50 = AchieveGoal(
        "G-50: UpdatedManifestPushedToDriver <b>If</b> DispatchRecordChanges",
        performs=performed_by("BookingSystem", SYSTEM, "Push updated manifest to driver tablet"),
        leaf=True)
    g51 = AvoidGoal(
        "G-51: SupersededNotesShownOnManifest",
        performs=performed_by("BookingSystem", SYSTEM, "Drop superseded rider notes from manifest"),
        leaf=True)
    g52 = AchieveGoal(
        "G-52: ManifestUpdateAcknowledged <b>If</b> UpdatedManifestReceived",
        performs=performed_by("Driver", ENV, "Acknowledge updated manifest"),
        leaf=True,
        annotation="expectation")
    g48 = MaintainGoal(
        "G-48: ManifestCurrentAndClean",
        refinements=[Refinement(False, [g50, g51, g52], annotation="H11")])
    g49 = AvoidGoal(
        "G-49: DriverMustReadManifest <b>If</b> VehicleMoving",
        performs=performed_by("BookingSystem", SYSTEM, "Announce updates by audio and defer acknowledgement until stopped"),
        leaf=True)
    g46 = MaintainGoal(
        "G-46: DriverHasClearCurrentManifest <b>If</b> UserIsDriver",
        refinements=[Refinement(False, [g48, g49], annotation="H3")])
    g47 = MaintainGoal(
        "G-47: RiderSeesOnlyOwnTripStatusAndChanges <b>If</b> UserIsRider",
        performs=performed_by("BookingSystem", SYSTEM, "Filter trip view to rider's own trips"),
        leaf=True)
    # G-86 [C] derived (P3 completeness): Diane 22:18:00 "riders, drivers, dispatchers,
    #      and call-center staff" ... "staff would have centralized operational dashboards
    #      rather than reconciling separate records"
    g86 = MaintainGoal(
        "G-86: RiderTripsShownFromSharedRecord <b>If</b> UserIsCallCenterStaff",
        performs=performed_by("BookingSystem", SYSTEM, "Show caller's trips from shared dispatch record"),
        leaf=True)
    g27 = MaintainGoal(
        "G-27: RoleAppropriateTripInformationShown",
        refinements=[Refinement(True, [g45, g46, g47, g78, g86], annotation="P3")])

    # G-28 [F]: G-53 replaced by the merged G-82
    g54 = AchieveGoal(
        "G-54: ChangeSubmittedBeforeCutoff <b>If</b> RiderPlansChange",
        performs=performed_by("Rider", ENV, "Submit change before cutoff"),
        leaf=True,
        annotation="expectation")
    g28 = SoftGoal(
        "Reduce[G-28: LastMinuteTripChanges]",
        refinements=[Refinement(False, [g82, g54], annotation="P7")])

    # G-25 [F] root of the dispatcher's model
    g25 = SoftGoal(
        "Improve[G-25: RunEfficiencyAndReliability]",
        refinements=[Refinement(False, [g26, g27, g28], annotation="H4")])

    # ================================================================ Diane (budget manager)
    # G-56, G-61..G-66 [D]: G-63 replaced by the merged G-32
    g65 = AchieveGoal(
        "G-65: SeatCapacityReserved <b>If</b> TripBooked",
        performs=performed_by("BookingSystem", SYSTEM, "Reserve seat on vehicle block"),
        leaf=True)
    g66 = AchieveGoal(
        "G-66: SeatCapacityReleased <b>If</b> TripCancelledOrNoShow",
        performs=performed_by("BookingSystem", SYSTEM, "Release seat on vehicle block"),
        leaf=True)
    g64 = MaintainGoal(
        "G-64: VehicleCapacityAccurate",
        refinements=[Refinement(True, [g65, g66], annotation="H9")])
    g61 = SoftGoal(
        "Maximize[G-61: VehicleUtilization]",
        refinements=[Refinement(False, [g32, g64], annotation="H4")])
    # G-62 [D]: G-67 and G-68 replaced by the merged G-7 and G-17
    g62 = SoftGoal(
        "Reduce[G-62: CallCenterVolume]",
        refinements=[Refinement(False, [g7, g17], annotation="H4")])
    g56 = SoftGoal(
        "Reduce[G-56: CostPerPassengerTrip]",
        refinements=[
            Refinement(False, [g61], annotation="H6"),
            Refinement(False, [g62], annotation="H6")])

    # G-57, G-69..G-77 [D]
    g72 = AchieveGoal(
        "G-72: ReportDraftGeneratedFromAuditTrail <b>If</b> ReportingPeriodEnds",
        performs=performed_by("BookingSystem", SYSTEM, "Generate denial and late-pickup report draft"),
        leaf=True)
    g73 = AchieveGoal(
        "G-73: ReportReviewedAndSubmitted <b>If</b> ReportDraftGenerated",
        performs=performed_by("BudgetManager", ENV, "Review and submit federal report"),
        leaf=True,
        annotation="expectation")
    g69 = AchieveGoal(
        "G-69: FederalDenialAndLatePickupReportFiled <b>If</b> ReportingPeriodEnds",
        refinements=[Refinement(False, [g72, g73], annotation="P1")])
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
    g70 = MaintainGoal(
        "G-70: CompleteTripAuditTrail",
        refinements=[Refinement(False, [g74, g75, g76, g77], annotation="P5")])
    g71 = AvoidGoal(
        "G-71: AuditRecordAlteredAfterCapture",
        performs=performed_by("BookingSystem", SYSTEM, "Store audit records append-only"),
        leaf=True)
    g57 = MaintainGoal(
        "G-57: ComplianceSubstantiatedDuringAudit",
        refinements=[Refinement(False, [g69, g70, g71], annotation="H3")])

    # G-58, G-79, G-80 [D]
    g79 = AchieveGoal(
        "G-79: VarianceFlagged <b>If</b> MetricDeviatesFromServicePlan",
        performs=performed_by("BookingSystem", SYSTEM, "Flag metric outside service plan tolerance"),
        leaf=True)
    g80 = AchieveGoal(
        "G-80: MonthlyReviewCompleted <b>If</b> DashboardAndVariancesAvailable",
        performs=performed_by("BudgetManager", ENV, "Review metrics against approved service plan"),
        leaf=True,
        annotation="expectation")
    g58 = AchieveGoal(
        "G-58: MonthlyMetricsReviewedAgainstServicePlan <b>If</b> MonthEnds",
        refinements=[Refinement(False, [g78, g79, g80], annotation="H11")])

    # G-60 [D]
    g60 = SoftGoal(
        "Minimize[G-60: BookingSystemImplementationCost]",
        performs=performed_by("BudgetManager", ENV, "Weigh technology spending against expected savings"),
        leaf=True)

    # G-55 [D] root of the budget manager's model
    g55 = SoftGoal(
        "Improve[G-55: CostEffectiveAndCompliantParatransitService]",
        refinements=[Refinement(False, [g56, g57, g58, g59, g60], annotation="H12")])

    # ================================================================ combined root
    # G-85 [C] derived (H12): abstracts the three stakeholders' root goals up to the
    #      boundary of the paratransit service as a whole
    g85 = SoftGoal(
        "Improve[G-85: ParatransitServiceForRidersDispatchAndAgency]",
        refinements=[Refinement(False, [g1, g25, g55], annotation="H12")])

    # ================================================================ obstacles and conflicts
    divergent_records = Obstacle("TripDetailsDivergeAcrossRunSheetsAndNotes", annotation="H8")
    ripple_delay = Obstacle("DelayRipplesToDownstreamPickups", annotation="H8")

    links = [
        ObstructionLink(g29, divergent_records),
        ResolutionLink(g31, divergent_records),
        ObstructionLink(g30, ripple_delay),
        ResolutionLink(g39, ripple_delay),
        ConflictLink(g3, g28),   # C-1
        ConflictLink(g60, g62),  # C-2
    ]

    return [g85], links


if __name__ == "__main__":
    roots, links = build()
    output = highlight_derived(generate_graph(roots, links))
    print(output)

    config = {"theme": "default", "themeVariables": {"fontFamily": "Helvetica"}}
    link = generate_pako_link(output, "view", config=config)
    print(link)

    mermaid_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mermaid.txt")
    with open(mermaid_path, "w", encoding="utf-8") as f:
        f.write(link + "\n")
