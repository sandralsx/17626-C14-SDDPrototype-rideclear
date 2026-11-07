"""
Goal model extracted from the interview with Frank Moretti (paratransit dispatcher).
17-626 HW2, Step 1.

Goal IDs: G-25 .. G-54 (continuing from goal_model_Janelle.py, G-1 .. G-24).

Trace convention (comment above each goal):
    Source  -> timestamp (UTC, from Frank.csv) + quote from the stakeholder turn
    Derived -> goal not stated in the transcript; added by the refinement
               heuristic / pattern named, or by interpretation of a vague term

Vague / ambiguous terms resolved:
    "one shared dispatch record" -> trip details are entered once and the manifest,
                                    vehicle block and driver assignment are kept in
                                    sync with that record (G-29, G-31, G-32)
    "out of sequence"            -> a change violates vehicle capacity, a pickup
                                    window, or a downstream connection on the run (G-39, G-40)
    "clean manifests"            -> only current trips and current rider notes;
                                    superseded notes are removed (G-48, G-51)
    "clear enough to keep them
     moving safely"              -> the driver never has to read or tap the manifest
                                    while the vehicle is moving (G-49)
    "last-minute changes"        -> changes requested inside a configurable cutoff
                                    before the pickup window (G-28, G-53)
    "the right information for
     that person"                -> information shown is decided by the user's role (G-27)

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
    """Return (root goals, links) for the Frank goal model."""

    # ---------------------------------------------------------------- G-29 shared record
    # G-31 Source 22:07:33 "The same trip details get entered and cross-checked in several
    #      places, and that's where mistakes creep into the run sheet"
    #      Source 22:09:09 "so updates don't get entered three different ways"
    g31 = AvoidGoal(
        "G-31: TripDetailsEnteredMoreThanOnce",
        performs=performed_by("BookingSystem", SYSTEM, "Accept trip edits only through shared dispatch record"),
        leaf=True)
    # G-33..G-35 Source 22:09:51 "when a rider, vehicle, or driver changes, the manifest
    #      and run should update together"
    #      Source 22:07:33 "updating manifests ... reconciling vehicle blocks, and reassigning drivers"
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
    # G-32 Source 22:09:51 "the manifest and run should update together"
    #      Divide-and-conquer (P5) over the conjunction manifest AND block AND assignment
    g32 = MaintainGoal(
        "G-32: ManifestBlockAndAssignmentSyncedWithDispatchRecord",
        refinements=[Refinement(True, [g33, g34, g35], annotation="P5")])
    # G-29 Source 22:09:09 "Give us one shared dispatch record"
    #      Source 22:09:51 "one dispatch record would help"
    g29 = MaintainGoal(
        "G-29: SingleSharedDispatchRecord",
        refinements=[Refinement(False, [g31, g32], annotation="H4")])

    # ---------------------------------------------------------------- G-30 trip changes
    # G-39 Source 22:06:48 "When one trip changes, I have to recheck the run, the window,
    #      and the downstream connections"
    g39 = AchieveGoal(
        "G-39: RunImpactRechecked <b>If</b> TripChangeRequested",
        performs=performed_by("BookingSystem", SYSTEM, "Recheck capacity, pickup windows and downstream connections"),
        leaf=True)
    # G-40 Source 22:09:51 "alerts when a change puts the route out of sequence"
    #      Source 22:10:28 "The board should flag vehicle capacity and route conflicts"
    g40 = AchieveGoal(
        "G-40: ConflictFlaggedOnBoard <b>If</b> CapacityOrSequenceConflict",
        performs=performed_by("BookingSystem", SYSTEM, "Raise conflict alert on live board"),
        leaf=True)
    # G-42 Source 22:07:33 "reassigning drivers when a trip changes"
    g42 = AchieveGoal(
        "G-42: TripMovedToVehicleWithCapacity",
        performs=performed_by("Dispatcher", ENV, "Reassign trip to another vehicle block"),
        leaf=True,
        annotation="expectation")
    # G-43 Derived (H4): alternative way to resolve a conflict when no vehicle has capacity
    g43 = AchieveGoal(
        "G-43: PickupWindowAdjusted",
        performs=performed_by("Dispatcher", ENV, "Adjust pickup window and resequence run"),
        leaf=True,
        annotation="expectation")
    # G-44 Derived (H4): a rider whose window moves must be told
    #      (cf. 22:10:28 "If riders can see accurate status and changes themselves")
    g44 = AchieveGoal(
        "G-44: RiderNotified <b>If</b> PickupWindowAdjusted",
        performs=performed_by("BookingSystem", SYSTEM, "Notify rider of new pickup window"),
        leaf=True)
    # G-41 Source 22:06:48 "so I don't throw the whole route out of sequence"
    #      OR-refinement (H4): move the trip, or adjust the window and tell the rider
    g41 = AchieveGoal(
        "G-41: ConflictResolved <b>If</b> ConflictFlaggedOnBoard",
        refinements=[
            Refinement(False, [g42], annotation="H4"),
            Refinement(False, [g43, g44], annotation="H4")])
    # G-36 Derived (P4): guard -- a change is cleared once its run impact is checked
    #      and any conflict is resolved. Responsibilities split (H5) between the
    #      system (recheck, flag) and the dispatcher (resolve)
    g36 = AchieveGoal(
        "G-36: ChangeClearedForRun <b>If</b> TripChangeRequested",
        refinements=[Refinement(False, [g39, g40, g41], annotation="H5")])
    # G-37 Source 22:09:51 "the manifest and run should update together"
    g37 = AchieveGoal(
        "G-37: ChangeCommittedToRun <b>If</b> ChangeClearedForRun",
        performs=performed_by("BookingSystem", SYSTEM, "Update manifest, run and vehicle block together"),
        leaf=True)
    # G-38 Derived (P4): the request must not be lost before it is committed
    g38 = MaintainGoal(
        "G-38: ChangeRequestPending <b>Unless</b> ChangeCommitted",
        performs=performed_by("BookingSystem", SYSTEM, "Hold request in pending change queue"),
        leaf=True)
    # G-30 Source 22:06:15 "changing trip details all have to line up"
    #      Source 22:06:48 "When one trip changes, I have to recheck the run"
    #      Guard-introduction (P4)
    g30 = AchieveGoal(
        "G-30: TripChangeReflectedInRun <b>If</b> TripChangeRequested",
        refinements=[Refinement(False, [g36, g37, g38], annotation="P4")])

    # G-26 Source 22:07:33 "there's a lot of repetitive work"
    #      Source 22:09:51 "That'd cut down the phone calls and the rechecking"
    g26 = SoftGoal(
        "Reduce[G-26: ManualReentryAndRechecking]",
        refinements=[Refinement(False, [g29, g30], annotation="H4")])

    # ---------------------------------------------------------------- G-27 role-based information
    # G-45 Source 22:09:51 "a live board showing vehicle capacity, windows, driver assignments"
    g45 = MaintainGoal(
        "G-45: LiveBoardShowsCapacityWindowsAndAssignments <b>If</b> UserIsDispatcher",
        performs=performed_by("BookingSystem", SYSTEM, "Render live dispatch board"),
        leaf=True)
    # G-50 Source 22:09:09 "Drivers need the live manifest"
    g50 = AchieveGoal(
        "G-50: UpdatedManifestPushedToDriver <b>If</b> DispatchRecordChanges",
        performs=performed_by("BookingSystem", SYSTEM, "Push updated manifest to driver tablet"),
        leaf=True)
    # G-51 Source 22:10:28 "drivers need clean manifests without digging through old notes"
    g51 = AvoidGoal(
        "G-51: SupersededNotesShownOnManifest",
        performs=performed_by("BookingSystem", SYSTEM, "Drop superseded rider notes from manifest"),
        leaf=True)
    # G-52 Derived (H11): the system cannot ensure the driver read the update; the
    #      driver is the single agent responsible for acknowledging it
    g52 = AchieveGoal(
        "G-52: ManifestUpdateAcknowledged <b>If</b> UpdatedManifestReceived",
        performs=performed_by("Driver", ENV, "Acknowledge updated manifest"),
        leaf=True,
        annotation="expectation")
    # G-48 Source 22:09:09 "Drivers need the live manifest, pickup window, vehicle
    #      assignment, and clear rider notes"
    #      Refined until each goal has a single responsible agent (H11)
    g48 = MaintainGoal(
        "G-48: ManifestCurrentAndClean",
        refinements=[Refinement(False, [g50, g51, g52], annotation="H11")])
    # G-49 Source 22:10:28 "my drivers deserve information that's clear enough to keep
    #      them moving safely" -- safety category instantiated (H3)
    g49 = AvoidGoal(
        "G-49: DriverMustReadManifest <b>If</b> VehicleMoving",
        performs=performed_by("BookingSystem", SYSTEM, "Announce updates by audio and defer acknowledgement until stopped"),
        leaf=True)
    # G-46 Source 22:08:37 "Drivers get their assigned manifest, vehicle block, pickup
    #      windows, and rider notes"
    g46 = MaintainGoal(
        "G-46: DriverHasClearCurrentManifest <b>If</b> UserIsDriver",
        refinements=[Refinement(False, [g48, g49], annotation="H3")])
    # G-47 Source 22:08:37 "riders only get their own trip details, not the shared run
    #      or other passengers' information"
    #      Source 22:09:09 "riders need their own trip status and changes, not everybody else's details"
    g47 = MaintainGoal(
        "G-47: RiderSeesOnlyOwnTripStatusAndChanges <b>If</b> UserIsRider",
        performs=performed_by("BookingSystem", SYSTEM, "Filter trip view to rider's own trips"),
        leaf=True)
    # G-27 Source 22:09:09 "more information only helps if it's the right information
    #      for that person"
    #      Decomposition by case on user role (P3); dispatcher/driver/rider covers all roles
    g27 = MaintainGoal(
        "G-27: RoleAppropriateTripInformationShown",
        refinements=[Refinement(True, [g45, g46, g47], annotation="P3")])

    # ---------------------------------------------------------------- G-28 last-minute changes
    # G-53 Interpretation of "last-minute" (see module docstring)
    g53 = MaintainGoal(
        "G-53: ChangeRequiresDispatcherApproval <b>If</b> ChangeInsideCutoff",
        performs=performed_by("BookingSystem", SYSTEM, "Route late change requests to dispatcher approval"),
        leaf=True)
    # G-54 Derived (P7): when riders change trips is not controllable by the system;
    #      it is an expectation on the rider
    g54 = AchieveGoal(
        "G-54: ChangeSubmittedBeforeCutoff <b>If</b> RiderPlansChange",
        performs=performed_by("Rider", ENV, "Submit change before cutoff"),
        leaf=True,
        annotation="expectation")
    # G-28 Source 22:10:28 "I want fewer last-minute changes, because one adjustment can
    #      upset an entire run"
    g28 = SoftGoal(
        "Reduce[G-28: LastMinuteTripChanges]",
        refinements=[Refinement(False, [g53, g54], annotation="P7")])

    # ---------------------------------------------------------------- G-25 root
    # G-25 Source 22:11:06 "makes the runs cleaner for the riders and my drivers"
    #      Source 22:05:51 "I keep things moving"
    g25 = SoftGoal(
        "Improve[G-25: RunEfficiencyAndReliability]",
        refinements=[Refinement(False, [g26, g27, g28], annotation="H4")])

    # ---------------------------------------------------------------- obstacles (H8)
    # Source 22:07:33 "that's where mistakes creep into the run sheet"
    divergent_records = Obstacle("TripDetailsDivergeAcrossRunSheetsAndNotes", annotation="H8")
    # Source 22:06:15 "One small delay can ripple through the rest of the day"
    ripple_delay = Obstacle("DelayRipplesToDownstreamPickups", annotation="H8")

    links = [
        ObstructionLink(g29, divergent_records),
        ResolutionLink(g31, divergent_records),
        ObstructionLink(g30, ripple_delay),
        ResolutionLink(g39, ripple_delay),
    ]

    return [g25], links


if __name__ == "__main__":
    roots, links = build()
    output = generate_graph(roots, links)
    print(output)

    config = {"theme": "default", "themeVariables": {"fontFamily": "Helvetica"}}
    print(generate_pako_link(output, "edit", config=config))
