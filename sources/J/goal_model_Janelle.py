"""
Goal model extracted from the interview with Janelle (paratransit rider).
17-626 HW2, Step 1.

Goal IDs: G-1 .. G-24 (IDs continue in goal_model_Frank.py and goal_model_Diane.py
so that every goal across the three models has a unique ID).

Trace convention (comment above each goal):
    Source  -> timestamp (UTC, from Janelle.csv) + quote from the stakeholder turn
    Derived -> goal not stated in the transcript; added by the refinement
               heuristic / pattern named, or by interpretation of a vague term

Vague / ambiguous terms resolved:
    "realistic arrival time"   -> ETA recomputed at least every minute from the
                                  vehicle's GPS position and traffic (G-15, G-19)
    "honest about delays"      -> "on time" shown only while the ETA is inside the
                                  pickup window (G-16, G-21, G-22)
    "delayed"                  -> ETA later than the end of the pickup window (G-17)
    "clear confirmation"       -> confirmation lists the pickup window for every
                                  booked trip (G-10)
    "genuinely accessible"     -> WCAG 2.1 AA conformance (G-23)
    "without hunting through
     screens"                  -> each upcoming trip's details on the home screen (G-24)
    "reliable"                 -> booking app available during all service hours (G-6)

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
    """Return (root goals, links) for the Janelle goal model."""

    # ---------------------------------------------------------------- G-2 booking time
    # G-9  Source 21:56:06 "I'd want to book both trips online"
    #      Source 21:55:36 "I usually book both the morning and return trips in the same phone call"
    g9 = AchieveGoal(
        "G-9: OutboundAndReturnTripDetailsSubmitted",
        performs=performed_by("Rider", ENV, "Enter outbound and return trip details in app"),
        leaf=True,
        annotation="expectation")
    # G-10 Source 21:58:11 "It should give me clear confirmation"
    g10 = AchieveGoal(
        "G-10: BookingConfirmed <b>If</b> TripDetailsSubmitted",
        performs=performed_by("BookingSystem", SYSTEM, "Send confirmation with pickup window for each trip"),
        leaf=True)
    # G-7  Source 21:58:11 "one accessible place where I can book both trips"
    #      Refined with P1 (milestone: details submitted -> booking confirmed)
    g7 = AchieveGoal(
        "G-7: RoundTripBookedOnline",
        refinements=[Refinement(False, [g9, g10], annotation="P1")])
    # G-8  Derived (H6): alternative to online booking for a routine commute.
    #      Grounded in 21:54:58 "give them my work schedule" and 21:56:06 "a routine booking"
    g8 = AchieveGoal(
        "G-8: RecurringTripsBooked <b>If</b> RiderHasStandingWorkSchedule",
        performs=performed_by("BookingSystem", SYSTEM, "Generate recurring trips from saved work schedule"),
        leaf=True)
    # G-2  Source 21:56:06 "I'm not satisfied with spending twenty minutes on hold just to make a routine booking"
    #      Source 21:54:58 "it takes too long"
    #      OR-refinement (H6): self-service online booking vs. standing (subscription) trips
    g2 = SoftGoal(
        "Reduce[G-2: TimeSpentBookingRoutineTrips]",
        refinements=[
            Refinement(False, [g7], annotation="H6"),
            Refinement(False, [g8], annotation="H6")])

    # ---------------------------------------------------------------- G-3 trip changes
    # G-11 Source 21:58:11 "change a ride without calling"
    g11 = AchieveGoal(
        "G-11: ChangeRequestSubmittedInApp",
        performs=performed_by("Rider", ENV, "Edit trip in app"),
        leaf=True,
        annotation="expectation")
    # G-13 Source 21:58:11 "give me clear confirmation"
    g13 = AchieveGoal(
        "G-13: UpdatedConfirmationSent <b>If</b> ChangeAccepted",
        performs=performed_by("BookingSystem", SYSTEM, "Send updated trip confirmation"),
        leaf=True)
    # G-14 Derived (P3): the case where the change cannot be accepted is not covered in the transcript
    g14 = AchieveGoal(
        "G-14: ReasonAndAlternativesShown <b>If</b> ChangeRejected",
        performs=performed_by("BookingSystem", SYSTEM, "Show rejection reason and alternative times"),
        leaf=True)
    # G-12 Derived (H4): how does the rider learn the result of a change request?
    #      Decomposed by case (P3): accepted / rejected covers all outcomes -> complete
    g12 = AchieveGoal(
        "G-12: ChangeOutcomeCommunicated <b>If</b> ChangeRequestSubmitted",
        refinements=[Refinement(True, [g13, g14], annotation="P3")])
    # G-3  Source 21:56:06 "change them when needed"
    #      Source 21:58:11 "change a ride without calling"
    g3 = AchieveGoal(
        "G-3: TripChanged <b>If</b> RiderRequestsChange",
        refinements=[Refinement(False, [g11, g12], annotation="H4")])

    # ---------------------------------------------------------------- G-4 trip status
    # G-18 Derived (P6): the actual vehicle position is not monitorable by the system;
    #      the GPS-reported position is used as a monitorable proxy
    g18 = MaintainGoal(
        "G-18: ReportedVehicleLocation <b>Equals</b> ActualVehicleLocation",
        performs=performed_by("VehicleGPS", ENV, "Report vehicle position"),
        leaf=True,
        annotation="expectation")
    # G-19 Interpretation of "realistic" (see module docstring)
    g19 = MaintainGoal(
        "G-19: ETARecomputedFromReportedLocationEveryMinute",
        performs=performed_by("BookingSystem", SYSTEM, "Recompute ETA from GPS position and traffic"),
        leaf=True)
    # G-20 Source 21:57:45 "I want the app to show a realistic estimated arrival time for the vehicle"
    g20 = AchieveGoal(
        "G-20: ETAShown <b>If</b> RiderViewsUpcomingTrip",
        performs=performed_by("BookingSystem", SYSTEM, "Display ETA on trip screen"),
        leaf=True)
    # G-15 Source 21:56:06 "see a realistic arrival time"
    #      Source 21:54:58 "I don't always know exactly when the van will arrive"
    g15 = MaintainGoal(
        "G-15: RealisticETADisplayed",
        refinements=[Refinement(True, [g18, g19, g20], annotation="P6")])
    # G-21 Source 21:58:11 "be honest about delays instead of calling a ride on time
    #      when the van is still nowhere nearby"
    g21 = AchieveGoal(
        "G-21: OnTimeStatusShown <b>If</b> ETAWithinPickupWindow",
        performs=performed_by("BookingSystem", SYSTEM, "Label trip as on time"),
        leaf=True)
    # G-22 Derived (H10): converse of G-21 -- "on time" only if the ETA is in the window
    g22 = AvoidGoal(
        "G-22: OnTimeStatusShown <b>If</b> ETAOutsidePickupWindow",
        performs=performed_by("BookingSystem", SYSTEM, "Label trip as delayed with new ETA"),
        leaf=True)
    # G-16 Source 21:58:11 "be honest about delays"
    g16 = MaintainGoal(
        "G-16: TripStatusTruthful",
        refinements=[Refinement(True, [g21, g22], annotation="H10")])
    # G-17 Source 21:58:11 "notify me if the pickup is delayed or changed"
    #      Source 21:59:07 "clear about any changes or delays"
    g17 = AchieveGoal(
        "G-17: RiderNotified <b>If</b> PickupDelayedOrChanged",
        performs=performed_by("BookingSystem", SYSTEM, "Push delay or change notification"),
        leaf=True)
    # G-4  Source 21:59:29 "gives riders accurate information"
    #      Instantiated into accuracy (G-15), accuracy/truthfulness (G-16) and
    #      stimulus-response (G-17) goal categories (H3)
    g4 = MaintainGoal(
        "G-4: RiderInformedOfAccurateTripStatus",
        refinements=[Refinement(False, [g15, g16, g17], annotation="H3")])

    # ---------------------------------------------------------------- G-5 accessibility (non-functional)
    # G-23 Interpretation of "genuinely accessible" (see module docstring)
    g23 = MaintainGoal(
        "G-23: AppConformsToWCAG2.1AA",
        performs=performed_by("BookingSystem", SYSTEM, "Support screen reader, scalable text, high contrast"),
        leaf=True)
    # G-24 Source 21:58:11 "show the details for each trip without making me hunt through screens"
    g24 = MaintainGoal(
        "G-24: UpcomingTripDetailsShownOnHomeScreen",
        performs=performed_by("BookingSystem", SYSTEM, "List each upcoming trip on home screen"),
        leaf=True)
    # G-5  Source 21:59:07 "I need it to be genuinely accessible"
    #      Source 21:58:11 "I want one accessible place"
    g5 = SoftGoal(
        "Improve[G-5: BookingAppAccessibility]",
        refinements=[Refinement(False, [g23, g24], annotation="H4")])

    # ---------------------------------------------------------------- G-6 reliability (non-functional)
    # G-6  Source 21:59:07 "I need it to be genuinely accessible, reliable"
    g6 = SoftGoal(
        "Maximize[G-6: BookingAppAvailabilityDuringServiceHours]",
        performs=performed_by("BookingSystem", SYSTEM, "Serve booking requests during service hours"),
        leaf=True)

    # ---------------------------------------------------------------- G-1 root
    # G-1  Source 21:56:43 "it would save time and make booking and tracking my rides much easier"
    #      Source 21:59:29 "I hope the system makes booking genuinely accessible and gives
    #      riders accurate information"
    #      Children are the rider's wishes (H7)
    g1 = SoftGoal(
        "Improve[G-1: RiderBookingAndTrackingExperience]",
        refinements=[Refinement(False, [g2, g3, g4, g5, g6], annotation="H7")])

    return [g1], []


if __name__ == "__main__":
    roots, links = build()
    output = generate_graph(roots, links)
    print(output)

    config = {"theme": "default", "themeVariables": {"fontFamily": "Helvetica"}}
    print(generate_pako_link(output, "edit", config=config))
