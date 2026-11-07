"""
Goal model extracted from the interview with Janelle Brooks-Ward (rider).
17-626 Assignment 2: Requirements Analysis. Qingyuan Yao (qingyuay).

Source: transcripts/Janelle.txt, turns T1 to T36. The comment above each goal cites the
turn(s) it comes from. Goals tagged NOT IN TRANSCRIPT came from a refinement pattern or
heuristic, or from my own interpretation, and are listed in missing.json.

Conventions
- Goal IDs G-1 to G-32 belong to this model. IDs are unique across all three models.
- Refinement annotations carry only the heuristic or pattern code (Appendix A).
- Each leaf goal is assigned to exactly one agent.
- Domain properties are labeled DP-n. They are not goals, so they carry no G-n ID.

Vague terms resolved
- "accessible" (T8, T10): Janelle defines it in T30 as completing the booking and changes
  without relying on someone else (G-12). From T12, that needs voice control and switch
  access, and no tiny buttons or drag-and-drop (G-13, G-14).
- "realistic arrival update" and "live estimate" (T8, T24, T30): an estimate computed from
  the vehicle's reported location (G-23, G-24, G-25).
- "timely notice if the vehicle is delayed" (T30): a notice as soon as the predicted pickup
  falls later than the pickup window (G-26).
- "reliable return trip" (T30, T36): a pickup inside the window, plus a notice when that
  cannot hold (G-6, G-26, G-32).

Conflicts: none inside this interview. Conflicts between stakeholders are documented in
goal_model_combined.py.
"""
from goalmodeling.schema import *


def by(agent_name, software=False):
    """Assign a leaf goal to exactly one agent. Each leaf gets its own agent node, which keeps the graph legible."""
    agent_type = AgentType.SOFTWARE_AGENT if software else AgentType.ENVIRONMENT_AGENT
    return [PerformanceLink(Agent(agent_name, agent_type), None)]


# ---------------------------------------------------------------------------------------
# G-2: booking and changing trips
# ---------------------------------------------------------------------------------------

# T8 "an accessible online option where I can book or change it myself"; T10 "routine bookings and changes"
g11 = AchieveGoal("<b>G-11</b> BookingOrChangeSubmittedOnline <b>If</b> RiderNeedsRoutineTrip",
                  performs=by("Rider"), leaf=True)

# T12 "The booking process needs to work with voice control and switch access"
g13 = MaintainGoal("<b>G-13</b> AllControlsOperableByVoiceControlAndSwitchAccess",
                   performs=by("BookingSystem", software=True), leaf=True)

# T12 "tiny buttons and drag-and-drop controls aren't usable for me"
g14 = AvoidGoal("<b>G-14</b> TinyButtonsAndDragAndDropControls",
                performs=by("BookingSystem", software=True), leaf=True)

# T30 "accessible means I can complete the booking and changes independently, without relying on someone else"
g12 = MaintainGoal("<b>G-12</b> BookingAndChangesCompletableWithoutHelp",
                   refinements=[Refinement(complete=False, children=[g13, g14], annotation="H4")])

# T34 "The system should apply my wheelchair and attendant details automatically"; T20, T32
g16 = AchieveGoal("<b>G-16</b> WheelchairAndAttendantDetailsAppliedFromProfile <b>If</b> ReservationCreated",
                  performs=by("BookingSystem", software=True), leaf=True)

# T34 "let me review or update them when needed"
g17 = AchieveGoal("<b>G-17</b> ProfileReviewedAndUpdated <b>If</b> RiderDetailsChange",
                  performs=by("Rider"), leaf=True)

# T32 "remove the need to repeat information that's already on my rider profile";
# T20 "I shouldn't have to explain that again every time"; T34 "I shouldn't have to re-enter or re-explain"
g15 = AvoidGoal("<b>G-15</b> RiderReentersProfileInformation",
                refinements=[Refinement(complete=False, children=[g16, g17], annotation="H11")])

# T24 "view my recurring work trips without calling"; T26 "the ability to schedule regular work trips"
g18 = MaintainGoal("<b>G-18</b> RecurringWorkTripsVisibleAndSchedulable",
                   performs=by("BookingSystem", software=True), leaf=True)

# T10 "I prefer an accessible automated system for routine bookings and changes"; T8
g7 = AchieveGoal("<b>G-7</b> TripBookedOrChangedViaSelfService <b>If</b> RequestRoutine",
                 refinements=[Refinement(complete=False, children=[g11, g12, g15, g18], annotation="H5")])

# T10 "I still want a real person available when something goes wrong"
g8 = AchieveGoal("<b>G-8</b> RequestHandledByStaff <b>If</b> ProblemOrNonRoutineRequest",
                 performs=by("ReservationStaff"), leaf=True)

# NOT IN TRANSCRIPT: domain property that makes the case split of G-2 complete (pattern P3)
dp1 = DomainProperty("DP-1 EachRequest IsRoutine Or NeedsStaff", leaf=True)

# T6 "booking by phone and waiting on hold"; T8 "call the day before and sit on hold"
# (the current way of booking, kept as the alternative refinement of G-2)
g9 = AchieveGoal("<b>G-9</b> TripBookedByPhoneCall",
                 performs=by("ReservationStaff"), leaf=True)

# T4 "I use paratransit five days a week to get to and from work"; T8; T10
g2 = AchieveGoal("<b>G-2</b> TripBookedOrChanged <b>If</b> RiderRequests",
                 refinements=[
                     # Alternative 1: self-service for routine requests, staff for problems
                     Refinement(complete=True, children=[g7, g8, dp1], annotation="P3"),
                     # Alternative 2: every request by phone (the current process)
                     Refinement(complete=False, children=[g9], annotation="H6"),
                 ])

# ---------------------------------------------------------------------------------------
# G-3: compatible vehicle
# ---------------------------------------------------------------------------------------

# T18 "I need the system to know which ones can accommodate my chair before assigning a trip"
# and "I'm asking for that information during booking"
g19 = AchieveGoal("<b>G-19</b> CompatibleVehiclesIdentified <b>If</b> TripRequested",
                  performs=by("Scheduler", software=True), leaf=True)

# T16 "use my rider mobility profile for vehicle assignment"; T12 "match me with a vehicle that has the right lift"
g20 = AchieveGoal("<b>G-20</b> TripAssignedToVehicle <b>If</b> VehicleFitsMobilityProfile",
                  performs=by("Scheduler", software=True), leaf=True)

# T16 "prevent a trip from being scheduled on a vehicle that can't accommodate my chair"
g21 = AvoidGoal("<b>G-21</b> TripScheduledOnIncompatibleVehicle",
                performs=by("Scheduler", software=True), leaf=True)

# T16 "Different vehicles have different lift platforms, clearances, securement configurations,
# and wheelchair capacity limits"
dp2 = DomainProperty("DP-2 VehiclesDifferInLift, Clearance, Securement And WheelchairCapacity", leaf=True)

# T12 "My wheelchair is larger than standard"; T14 "the system needs to accommodate my wheelchair"; T16; T18
g3 = MaintainGoal("<b>G-3</b> RiderCarriedOnlyByCompatibleVehicle",
                  refinements=[Refinement(complete=False, children=[g19, g20, g21, dp2], annotation="P4")])

# ---------------------------------------------------------------------------------------
# G-4: trip status information
# ---------------------------------------------------------------------------------------

# T24 "I'd want to see the actual pickup window"
g22 = AchieveGoal("<b>G-22</b> PickupWindowShown <b>If</b> TripScheduled",
                  performs=by("BookingSystem", software=True), leaf=True)

# NOT IN TRANSCRIPT: pattern P6, because the system cannot observe where the vehicle is
g24 = AchieveGoal("<b>G-24</b> VehicleLocationReported <b>If</b> VehicleInService",
                  performs=by("VehicleGPS"), leaf=True)

# NOT IN TRANSCRIPT: pattern P6, and my reading of "realistic" in T8 and T30
g25 = AchieveGoal("<b>G-25</b> ArrivalEstimateComputedFromReportedLocation",
                  performs=by("TripTracker", software=True), leaf=True)

# T24 "a live estimate of when the van will arrive, especially for the trip home"; T8 "a realistic arrival update"
g23 = AchieveGoal("<b>G-23</b> LiveArrivalEstimateShown <b>If</b> VehicleEnRoute",
                  refinements=[Refinement(complete=False, children=[g24, g25], annotation="P6")])

# T30 "timely notice if the vehicle is delayed"; T32 "if a ride is changed or delayed, the system should tell me"
# (the condition is my reading of "delayed" and "timely")
g26 = AchieveGoal("<b>G-26</b> DelayNoticeSent <b>If</b> PredictedPickupLaterThanWindow",
                  performs=by("TripTracker", software=True), leaf=True)

# T24 "confirm that the update went through"; T32 "tell me clearly what happened and confirm what's now scheduled"
g27 = AchieveGoal("<b>G-27</b> ChangeExplainedAndNewScheduleConfirmed <b>If</b> TripChangedOrDelayed",
                  performs=by("TripTracker", software=True), leaf=True)

# T8 "instead of waiting without knowing what's happening"; T24
g4 = AchieveGoal("<b>G-4</b> RiderInformedOfTripStatus <b>If</b> TripBooked",
                 refinements=[Refinement(complete=False, children=[g22, g23, g26, g27], annotation="H3")])

# ---------------------------------------------------------------------------------------
# G-5: assisted ride
# ---------------------------------------------------------------------------------------

# T26 "I don't want to lose the door-to-door assistance"
g28 = MaintainGoal("<b>G-28</b> DoorToDoorAssistanceProvided",
                   performs=by("Driver"), leaf=True)

# T26 "trained drivers who understand securement"
g29 = MaintainGoal("<b>G-29</b> DriversTrainedInWheelchairSecurement",
                   performs=by("Agency"), leaf=True)

# T26 "treat me like a passenger, not a problem"
g30 = SoftGoal("Improve[<b>G-30</b> RespectfulTreatmentOfRider]",
               performs=by("Driver"), leaf=True)

# T20 "so the driver and agency know she's traveling with me"; T22 "a new driver doesn't see the attendant listed"
g31 = AchieveGoal("<b>G-31</b> AttendantVisibleToDriver <b>If</b> AttendantOnReservation",
                  performs=by("BookingSystem", software=True), leaf=True)

# T26 (door-to-door assistance, securement, treatment); T20 and T22 (attendant)
g5 = MaintainGoal("<b>G-5</b> RiderAssistedSafelyFromDoorToDoor",
                  refinements=[Refinement(complete=False, children=[g28, g29, g30, g31], annotation="H7")])

# ---------------------------------------------------------------------------------------
# G-6: return trip reliability
# ---------------------------------------------------------------------------------------

# T12 "a late pickup can make me miss her evening visit"; T30 "getting home late can affect my evening care arrangements"
g32 = AchieveGoal("<b>G-32</b> ReturnPickupWithinWindow <b>If</b> ReturnTripScheduled",
                  performs=by("Driver"), leaf=True)

# T30 "one important thing is reliability for the return trip"; T36 "reliable, especially for return trips"
g6 = SoftGoal("Improve[<b>G-6</b> ReturnTripReliability]",
              refinements=[Refinement(complete=False, children=[g32, g26], annotation="P7")])

# ---------------------------------------------------------------------------------------
# Roots
# ---------------------------------------------------------------------------------------

# T6 "Now I have independence and can keep my job"; T26 "The service gives me independence";
# T28 "that puts my transportation back in someone else's hands, which is exactly what paratransit should help me avoid"
g1 = SoftGoal("Increase[<b>G-1</b> RiderIndependence]",
              refinements=[Refinement(complete=False, children=[g2, g3, g4, g5, g6], annotation="H12")])

# T8 "sit on hold for around 20 minutes just to book a routine ride"; T10 "I shouldn't have to wait 20 minutes"
g10 = SoftGoal("Reduce[<b>G-10</b> BookingHoldTime]",
               refinements=[Refinement(complete=False, children=[g7], annotation="H6")])

ROOTS = [g1, g10]
CONFLICTS = []  # no conflict inside Janelle's interview
# Goals not in the transcript. They are highlighted yellow in the diagram.
NOT_IN_TRANSCRIPT = {"G-24": g24, "G-25": g25}


def highlight(graph, goals):
    """Color the goals that are not in the transcript yellow."""
    return graph + "".join(f"style {g.get_node_id()} fill:#fff59d,stroke:#b59f00\n" for g in goals)


if __name__ == "__main__":
    graph = highlight(generate_graph(ROOTS, CONFLICTS), NOT_IN_TRANSCRIPT.values())
    print(graph)
    print(generate_pako_link(graph, "view",
                             config={"theme": "default", "themeVariables": {"fontFamily": "Helvetica"}}))
