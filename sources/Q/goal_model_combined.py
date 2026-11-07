"""
Combined goal model: Janelle Brooks-Ward (rider), Frank Moretti (dispatcher) and
Diane Fowler (budget manager).
17-626 Assignment 2: Requirements Analysis. Qingyuan Yao (qingyuay).

Built from goal_model_Janelle.py (G-1 to G-32), goal_model_Frank.py (G-33 to G-68) and
goal_model_Diane.py (G-69 to G-105). Every goal keeps its original ID. Comments cite the
source as Name Tn (stakeholder and transcript turn). New goals start at G-106.

Merged duplicates (kept ID <- absorbed IDs). The kept goal was rewritten to include the
information in the absorbed goal.
- G-2  <- G-97   trip booked or changed when the rider asks (Janelle T8, T10; Diane T22)
- G-7  <- G-99   self-service for routine requests, now "routine and eligible" (Diane T22)
- G-8  <- G-100  staff handle problems and exceptions, with Diane's queue and escalation codes
- G-9  <- G-103  the phone-only alternative (Janelle T8; Diane T10)
- DP-1 <- DP-4   every request is routine and eligible, or needs staff review
- G-12 <- G-104  accessible rider-facing booking (Janelle T30; Diane T10, T26)
- G-10 <- G-68   hold time (Janelle T8, T10; Frank T17)
- G-4  <- G-65   rider sees trip status (Janelle T8, T24; Frank T17)
- G-27 <- G-50   riders told about changed or moved pickups (Janelle T24, T32)
- G-42 <- G-32   pickup inside the 30-minute window, return trips included (Frank T31; Janelle T12, T30)
- G-55 <- G-16, G-31  profile details carried into the reservation, manifest and MDT (Frank T25; Janelle T20, T22, T34)
- G-17 <- G-59   rider reviews and updates the profile (Janelle T34)
- G-45 <- G-79   reason or exception code on every change and cancellation (Frank T13; Diane T12, T14)
- G-47 <- G-80   dispatcher accepts or rejects a same-day change (Frank T9; Diane T26)
- G-35 <- G-78   same-day changes controlled (Frank T9, T17, T33; Diane T24, T26)
- G-72 <- G-57   one immutable audit trail for trip and profile changes (Diane T14, T18; Frank T25)
- G-39 <- G-29   drivers trained in securement and familiar with riders (Janelle T26; Frank T7, T17, T31)
- G-89 <- G-49   changes propagate to the manifest, driver MDT and financial reports (Diane T14; Frank T11, T29)

Conflicts (ConflictLink)
- C1 G-7 vs G-44. Janelle wants to change trips herself (T8, T10). Frank wants no change
  applied to a built manifest without dispatcher approval (T17, T33).
  Resolution: G-107. A self-service change made after the manifest is built goes to the
  dispatcher's impact view instead of applying at once.
- C2 G-10 vs G-58. Shorter holds (Janelle T8, T10; Frank T17) vs not rushing the booking
  (Frank T17). Resolution: verify only the profile fields flagged as stale (G-60, G-61).
- C3 G-76 vs G-105. Cost control vs notice and due process (Diane T26).
  Resolution: a sanction applies only after notice and any appeal (G-87).
- C4 G-55 vs G-94. Frank wants profile fields carried into the driver's MDT (T25). Diane
  wants eligibility information hidden from roles that do not need it (T26).
  Resolution: G-108. The MDT shows only the fields a driver needs at pickup.

New goals (NOT IN TRANSCRIPT): G-106 (shared root), G-107 (resolves C1), G-108 (resolves C4).
The full list of goals not in the transcripts is in missing.json.
"""
from goalmodeling.schema import *


def by(agent_name, software=False):
    """Assign a leaf goal to exactly one agent. Each leaf gets its own agent node, which keeps the graph legible."""
    agent_type = AgentType.SOFTWARE_AGENT if software else AgentType.ENVIRONMENT_AGENT
    return [PerformanceLink(Agent(agent_name, agent_type), None)]


def sw(agent_name):
    return by(agent_name, software=True)


# =======================================================================================
# Shared leaves and subtrees (used by more than one stakeholder branch)
# =======================================================================================

# MERGED G-55 <- G-16, G-31. Frank T25 "Those fields should carry forward automatically into the trip record,
# manifest, and driver MDT"; Frank T21, T23; Janelle T34 "apply my wheelchair and attendant details automatically";
# Janelle T20, T22 (attendant visible to the driver)
g55 = AchieveGoal("<b>G-55</b> WheelchairAttendantAssistanceAndAccessNotesCarriedIntoReservationManifestAndMDT <b>If</b> TripBooked",
                  performs=sw("CADSystem"), leaf=True)

# MERGED G-17 <- G-59. Janelle T34 "let me review or update them when needed"
g17 = AchieveGoal("<b>G-17</b> ProfileReviewedAndUpdatedByRider <b>If</b> DetailsOrEquipmentChange",
                  performs=by("Rider"), leaf=True)

# MERGED G-89 <- G-49. Diane T14 "a change in one stage propagates correctly to the manifest and financial reporting";
# Frank T11 "dispatch has to radio the change"; Frank T29 "get the right information to the driver"
g89 = AchieveGoal("<b>G-89</b> ChangePropagatedToManifestDriverMDTAndFinancialReports <b>If</b> TripRecordChanged",
                  performs=sw("TripRecordSystem"), leaf=True)

# MERGED G-72 <- G-57. Diane T14, T18 "an immutable audit trail"; Diane T12, T16; Frank T25 "an audit trail when somebody changes them"
g72 = MaintainGoal("<b>G-72</b> ImmutableAuditTrailOfTripAndProfileChanges",
                   performs=sw("TripRecordSystem"), leaf=True)

# MERGED G-45 <- G-79. Frank T13 "require a clear reason for a change"; Diane T12 "clear exception coding"; Diane T14
g45 = AchieveGoal("<b>G-45</b> ChangeReasonCodeRecorded <b>If</b> TripChangedOrCancelled",
                  performs=sw("TripRecordSystem"), leaf=True)

# Frank T13 "I'd want the system to record those patterns"
g67 = AchieveGoal("<b>G-67</b> NoShowAndLateCancelPatternsRecorded <b>If</b> NoShowOrLateCancelOccurs",
                  performs=sw("DispatchSystem"), leaf=True)

# Diane T26 "notice"
g85 = AchieveGoal("<b>G-85</b> RiderNotifiedBeforeSanction <b>If</b> SanctionProposed",
                  performs=by("AgencyStaff"), leaf=True)

# Diane T26 "due process"
g86 = AchieveGoal("<b>G-86</b> AppealHeardBeforeSanction <b>If</b> RiderAppeals",
                  performs=by("AgencyStaff"), leaf=True)

# Janelle T30 "timely notice if the vehicle is delayed"; the 30-minute window is Frank's definition of late (Frank T31)
g26 = AchieveGoal("<b>G-26</b> DelayNoticeSent <b>If</b> PredictedPickupLaterThan30MinuteWindow",
                  performs=sw("TripTracker"), leaf=True)

# MERGED G-27 <- G-50. Janelle T24 "confirm that the update went through"; Janelle T32 "tell me clearly what happened
# and confirm what's now scheduled"
g27 = AchieveGoal("<b>G-27</b> ChangeExplainedAndNewScheduleConfirmed <b>If</b> TripChangedDelayedOrPickupMoved",
                  performs=sw("TripTracker"), leaf=True)

# MERGED G-42 <- G-32. Frank T31 "pickups are expected within a 30-minute window"; Janelle T12 "a late pickup can make
# me miss her evening visit"; Janelle T30
g42 = AchieveGoal("<b>G-42</b> OutboundAndReturnPickupWithin30MinuteWindow <b>If</b> RunOnSchedule",
                  performs=by("Driver"), leaf=True)

# Frank T29 "Regular rides and returns are generally paired up in the schedule"; Frank T31 "protect the scheduled return"
g41 = MaintainGoal("<b>G-41</b> RegularRidesPairedWithReturnTrips",
                   performs=sw("Scheduler"), leaf=True)

# MERGED G-39 <- G-29. Janelle T26 "trained drivers who understand securement"; Frank T7 "drivers who know how to handle
# people properly"; Frank T17 "drivers who know their riders"; Frank T31
g39 = MaintainGoal("<b>G-39</b> DriversTrainedInSecurementAndFamiliarWithRiders",
                   performs=by("Agency"), leaf=True)

# Janelle T26 "treat me like a passenger, not a problem"
g30 = SoftGoal("Improve[<b>G-30</b> RespectfulTreatmentOfRider]",
               performs=by("Driver"), leaf=True)

# Diane T26 "while still allowing staff to handle exceptions fairly"; Diane T22
g102 = AchieveGoal("<b>G-102</b> ExceptionResolvedFairlyByStaff <b>If</b> ExceptionQueued",
                   performs=by("AgencyStaff"), leaf=True)

# =======================================================================================
# Janelle branch: G-1 rider independence
# =======================================================================================

# Janelle T8, T10 "book or change it myself"
g11 = AchieveGoal("<b>G-11</b> BookingOrChangeSubmittedOnline <b>If</b> RiderNeedsRoutineTrip",
                  performs=by("Rider"), leaf=True)

# Janelle T12 "work with voice control and switch access"
g13 = MaintainGoal("<b>G-13</b> AllControlsOperableByVoiceControlAndSwitchAccess",
                   performs=sw("BookingSystem"), leaf=True)

# Janelle T12 "tiny buttons and drag-and-drop controls aren't usable for me"
g14 = AvoidGoal("<b>G-14</b> TinyButtonsAndDragAndDropControls",
                performs=sw("BookingSystem"), leaf=True)

# MERGED G-12 <- G-104. Janelle T30 "accessible means I can complete the booking and changes independently";
# Diane T10 "an accessible self-service process"; Diane T26 "The rider-facing portion must be accessible"
g12 = MaintainGoal("<b>G-12</b> RiderFacingBookingAccessibleAndCompletableWithoutHelp",
                   refinements=[Refinement(complete=False, children=[g13, g14], annotation="H4")])

# Janelle T32 "remove the need to repeat information that's already on my rider profile"; Janelle T20, T34;
# Frank T23 "otherwise the rider ends up repeating the same information"
g15 = AvoidGoal("<b>G-15</b> RiderReentersProfileInformation",
                refinements=[Refinement(complete=False, children=[g55, g17], annotation="H11")])

# Janelle T24 "view my recurring work trips without calling"; Janelle T26
g18 = MaintainGoal("<b>G-18</b> RecurringWorkTripsVisibleAndSchedulable",
                   performs=sw("BookingSystem"), leaf=True)

# NOT IN TRANSCRIPT: resolves conflict C1 (Janelle T8, T10 vs Frank T17, T33)
g107 = AchieveGoal("<b>G-107</b> SelfServiceChangeSentToDispatcherImpactView <b>If</b> ManifestBuilt",
                   performs=sw("BookingSystem"), leaf=True)

# MERGED G-7 <- G-99. Janelle T10 "an accessible automated system for routine bookings and changes";
# Diane T22 "routine eligible trips can follow a self-service workflow"
g7 = AchieveGoal("<b>G-7</b> TripBookedOrChangedViaSelfService <b>If</b> RequestRoutineAndEligible",
                 refinements=[Refinement(complete=False, children=[g11, g12, g15, g18, g107], annotation="H5")])

# Diane T22 "exceptions should be routed to a staffed assistance queue"; "escalation codes"
g101 = AchieveGoal("<b>G-101</b> ExceptionQueuedWithEscalationCode <b>If</b> NotRoutineOrNeedsReview",
                   performs=sw("BookingSystem"), leaf=True)

# MERGED G-8 <- G-100. Janelle T10 "I still want a real person available when something goes wrong";
# Diane T22 "staff time is reserved for eligibility questions, complex modifications, and cases requiring human review"
g8 = AchieveGoal("<b>G-8</b> RequestHandledByStaff <b>If</b> ProblemNonRoutineOrNeedsReview",
                 refinements=[Refinement(complete=False, children=[g101, g102], annotation="H5")])

# Diane T22 "The system should use structured triage, validation rules, and escalation codes"
g98 = AchieveGoal("<b>G-98</b> RequestTriagedByValidationRules <b>If</b> RequestSubmitted",
                  performs=sw("BookingSystem"), leaf=True)

# MERGED DP-1 <- DP-4. Diane T22 (routine eligible trips vs exceptions)
dp1 = DomainProperty("DP-1 EachRequest IsRoutineAndEligible Or NeedsStaffReview", leaf=True)

# MERGED G-9 <- G-103. Janelle T6, T8 "call the day before and sit on hold"; Diane T10 "the phone center carrying
# too much routine booking work" (the current process, kept as the alternative refinement of G-2)
g9 = AchieveGoal("<b>G-9</b> EveryRequestBookedThroughPhoneCenter",
                 performs=by("ReservationAgent"), leaf=True)

# MERGED G-2 <- G-97. Janelle T4, T8, T10; Diane T22 "rather than forcing every request through the phone center"
g2 = AchieveGoal("<b>G-2</b> TripBookedOrChanged <b>If</b> RiderRequests",
                 refinements=[
                     # Alternative 1: triage into self-service and staff
                     Refinement(complete=True, children=[g98, g7, g8, dp1], annotation="P2"),
                     # Alternative 2: every request by phone (the current process)
                     Refinement(complete=False, children=[g9], annotation="H6"),
                 ])

# Janelle T18 "I need the system to know which ones can accommodate my chair before assigning a trip"
g19 = AchieveGoal("<b>G-19</b> CompatibleVehiclesIdentified <b>If</b> TripRequested",
                  performs=sw("Scheduler"), leaf=True)

# Janelle T16 "use my rider mobility profile for vehicle assignment"; Janelle T12
g20 = AchieveGoal("<b>G-20</b> TripAssignedToVehicle <b>If</b> VehicleFitsMobilityProfile",
                  performs=sw("Scheduler"), leaf=True)

# Janelle T16 "prevent a trip from being scheduled on a vehicle that can't accommodate my chair"
g21 = AvoidGoal("<b>G-21</b> TripScheduledOnIncompatibleVehicle",
                performs=sw("Scheduler"), leaf=True)

# Janelle T16 "Different vehicles have different lift platforms, clearances, securement configurations, and
# wheelchair capacity limits"; Frank T7 "matching riders, windows, equipment"
dp2 = DomainProperty("DP-2 VehiclesDifferInLift, Clearance, Securement And WheelchairCapacity", leaf=True)

# Janelle T12, T14, T16, T18
g3 = MaintainGoal("<b>G-3</b> RiderCarriedOnlyByCompatibleVehicle",
                  refinements=[Refinement(complete=False, children=[g19, g20, g21, dp2], annotation="P4")])

# Janelle T24 "I'd want to see the actual pickup window"
g22 = AchieveGoal("<b>G-22</b> PickupWindowShown <b>If</b> TripScheduled",
                  performs=sw("BookingSystem"), leaf=True)

# NOT IN TRANSCRIPT: pattern P6, because the system cannot observe where the vehicle is
g24 = AchieveGoal("<b>G-24</b> VehicleLocationReported <b>If</b> VehicleInService",
                  performs=by("VehicleGPS"), leaf=True)

# NOT IN TRANSCRIPT: pattern P6, and my reading of "realistic" (Janelle T8, T30)
g25 = AchieveGoal("<b>G-25</b> ArrivalEstimateComputedFromReportedLocation",
                  performs=sw("TripTracker"), leaf=True)

# Janelle T24 "a live estimate of when the van will arrive"; Janelle T8; Frank T17 "riders asking where their van is"
g23 = AchieveGoal("<b>G-23</b> LiveArrivalEstimateShown <b>If</b> VehicleEnRoute",
                  refinements=[Refinement(complete=False, children=[g24, g25], annotation="P6")])

# MERGED G-4 <- G-65. Janelle T8 "instead of waiting without knowing what's happening"; Janelle T24;
# Frank T17 "Janelle's right that customers need clearer status information"
g4 = AchieveGoal("<b>G-4</b> RiderInformedOfTripStatus <b>If</b> TripBooked",
                 refinements=[Refinement(complete=False, children=[g22, g23, g26, g27], annotation="H3")])

# Janelle T26 "I don't want to lose the door-to-door assistance"
g28 = MaintainGoal("<b>G-28</b> DoorToDoorAssistanceProvided",
                   performs=by("Driver"), leaf=True)

# Janelle T26; Janelle T20, T22 (attendant)
g5 = MaintainGoal("<b>G-5</b> RiderAssistedSafelyFromDoorToDoor",
                  refinements=[Refinement(complete=False, children=[g28, g39, g30, g55], annotation="H7")])

# Janelle T30 "reliability for the return trip"; Janelle T36; Frank T31 "Evenings are our tightest window"
g6 = SoftGoal("Improve[<b>G-6</b> ReturnTripReliability]",
              refinements=[Refinement(complete=False, children=[g42, g26, g41], annotation="P7")])

# Janelle T6 "Now I have independence and can keep my job"; Janelle T26, T28
g1 = SoftGoal("Increase[<b>G-1</b> RiderIndependence]",
              refinements=[Refinement(complete=False, children=[g2, g3, g4, g5, g6], annotation="H12")])

# =======================================================================================
# Frank branch: G-33 shared route runs clean
# =======================================================================================

# Frank T31 "accounting for vehicle capacity, driver hours, traffic"
g40 = AchieveGoal("<b>G-40</b> RunPlannedWithinCapacityAndDriverHours <b>If</b> ManifestBuilt",
                  performs=sw("Scheduler"), leaf=True)

# Frank T31 "pickups are expected within a 30-minute window, and anything beyond that is late"
g34 = MaintainGoal("<b>G-34</b> PickupsWithin30MinuteWindow",
                   refinements=[Refinement(complete=False, children=[g40, g41, g42], annotation="H5")])

# Frank T9 "flags conflicts with vehicle capacity and existing pickups"
g51 = AchieveGoal("<b>G-51</b> CapacityAndPickupConflictsFlagged <b>If</b> ChangeProposed",
                  performs=sw("DispatchSystem"), leaf=True)

# Frank T9 "lets dispatchers see which riders and drivers will be affected"
g52 = AchieveGoal("<b>G-52</b> AffectedRidersAndDriversShown <b>If</b> ChangeProposed",
                  performs=sw("DispatchSystem"), leaf=True)

# Frank T13 "show dispatch the cost to the rest of the route before we accept it"
g53 = AchieveGoal("<b>G-53</b> CostToRestOfRouteShown <b>If</b> ChangeProposed",
                  performs=sw("DispatchSystem"), leaf=True)

# Frank T9 "shows the impact before we approve a change"; Frank T33 "a clear impact view before any change is accepted"
g46 = AchieveGoal("<b>G-46</b> RouteImpactShownToDispatcher <b>If</b> ChangeReasonRecorded",
                  refinements=[Refinement(complete=False, children=[g51, g52, g53], annotation="P5")])

# MERGED G-47 <- G-80. Frank T9 "make the call with the whole route in front of us"; Frank T11;
# Diane T26 "clear controls over same-day changes"
g47 = AchieveGoal("<b>G-47</b> ChangeAcceptedOrRejectedByDispatcher <b>If</b> RouteImpactShown",
                  performs=by("Dispatcher"), leaf=True)

# Frank T11 "re-sequence the run, check the window, and protect the other scheduled pickups"; Frank T19
g48 = AchieveGoal("<b>G-48</b> RunResequencedWithinWindows <b>If</b> ChangeAccepted",
                  performs=sw("DispatchSystem"), leaf=True)

# Frank T9, T11 "the ugly ones come after the manifest is built"
g43 = AchieveGoal("<b>G-43</b> ChangeAppliedSafely <b>If</b> ChangeRequestedAfterManifestBuilt",
                  refinements=[Refinement(complete=False, children=[g45, g46, g47, g48, g89, g27], annotation="P1")])

# Frank T17 "dispatch still needs enough control to protect the shared routes"; Frank T33
g44 = AvoidGoal("<b>G-44</b> ChangeAppliedWithoutDispatcherApproval",
                performs=sw("DispatchSystem"), leaf=True)

# MERGED G-35 <- G-78. Frank T9 "ripple through the whole board and can wreck a shared route"; Frank T13, T17, T33;
# Diane T26 "clear controls over same-day changes"; Diane T24 "more disciplined handling of changes"
g35 = MaintainGoal("<b>G-35</b> SameDayChangesControlledToProtectSharedRoute",
                   refinements=[Refinement(complete=False, children=[g43, g44], annotation="H10")])

# Frank T25 "a single source of truth for the rider profile, with structured fields"
g56 = MaintainGoal("<b>G-56</b> SingleProfileRecordWithStructuredFields",
                   performs=sw("CADSystem"), leaf=True)

# Frank T25 "a prompt to verify stale information during booking"
g60 = AchieveGoal("<b>G-60</b> StaleProfileFieldsFlagged <b>If</b> BookingMade",
                  performs=sw("CADSystem"), leaf=True)

# Frank T23 "We verify the equipment, passenger-assistance needs, and curb-to-door access notes during booking"
g61 = AchieveGoal("<b>G-61</b> FlaggedFieldsConfirmedOrCorrected <b>If</b> FieldsFlagged",
                  performs=by("ReservationAgent"), leaf=True)

# Frank T17 "rushing a booking is how you get the wrong address, bad equipment information"
g58 = AvoidGoal("<b>G-58</b> BookingConfirmedWithUnverifiedDetails",
                refinements=[Refinement(complete=False, children=[g60, g61], annotation="H8")])

# Frank T23 "it isn't always complete or current"; Frank T25
g54 = MaintainGoal("<b>G-54</b> RiderProfileCompleteAndCurrent",
                   refinements=[Refinement(complete=False, children=[g56, g72, g58, g17], annotation="P6")])

# Frank T23 "the driver gets surprised at pickup"; Frank T21, T27, T31
g36 = AvoidGoal("<b>G-36</b> DriverSurprisedAtCurb",
                refinements=[Refinement(complete=False, children=[g54, g55, g89], annotation="H4")])

# Frank T19 "ordered stops, pickup and drop-off windows, rider names, mobility equipment, addresses"
g62 = MaintainGoal("<b>G-62</b> ManifestListsOrderedStopsWindowsAndAddresses",
                   performs=sw("DispatchSystem"), leaf=True)

# Frank T19 "trip status, and any no-show or late-cancel indicators"
g63 = MaintainGoal("<b>G-63</b> ManifestShowsTripStatusAndNoShowOrLateCancelFlags",
                   performs=sw("DispatchSystem"), leaf=True)

# Frank T19 "plus the vehicle assignment"
g64 = MaintainGoal("<b>G-64</b> ManifestShowsVehicleAssignment",
                   performs=sw("DispatchSystem"), leaf=True)

# Frank T19 "A clear manifest is the operational run sheet"; Frank T17; Diane T12 "manifest integrity"
g37 = MaintainGoal("<b>G-37</b> ManifestCompleteForDriverAndDispatch",
                   refinements=[Refinement(complete=False, children=[g62, g55, g63, g64], annotation="P5")])

# Frank T7 "without a complaint call"; Frank T17 "riders asking where their van is"
g38 = SoftGoal("Reduce[<b>G-38</b> ComplaintAndStatusCalls]",
               refinements=[Refinement(complete=False, children=[g4], annotation="H4")])

# Frank T7 "I'm proud when a shared route runs clean"; Frank T17
g33 = MaintainGoal("<b>G-33</b> SharedRouteRunsClean",
                   refinements=[Refinement(complete=False, children=[g34, g35, g36, g37, g38, g39], annotation="H12")])

# =======================================================================================
# Diane branch: G-69 service obligations met within budget
# =======================================================================================

# Diane T18 "traceability from eligibility determination through trip authorization, dispatch events, and final reconciliation"
g73 = MaintainGoal("<b>G-73</b> TripRecordLinksEligibilityAuthorizationDispatchAndReconciliation",
                   performs=sw("TripRecordSystem"), leaf=True)

# Diane T18
g71 = MaintainGoal("<b>G-71</b> TripTraceableFromEligibilityToReconciliation",
                   refinements=[Refinement(complete=False, children=[g72, g73], annotation="P5")])

# Diane T18 "standardized denial and late-pickup reason codes"
g74 = AchieveGoal("<b>G-74</b> StandardReasonCodeRecorded <b>If</b> DenialOrLatePickupOccurs",
                  performs=sw("TripRecordSystem"), leaf=True)

# Diane T26 "timely reports on denials and late pickups for federal review"; Diane T18 "reproducible reporting"
g75 = AchieveGoal("<b>G-75</b> DenialAndLatePickupReportProducedFromTripData <b>If</b> ReportingPeriodEnds",
                  performs=sw("ReportingSystem"), leaf=True)

# Diane T10; Diane T18 "Compliant means we pass the audit"
g70 = AchieveGoal("<b>G-70</b> FederalComplianceReviewPassed",
                  refinements=[Refinement(complete=False, children=[g71, g74, g75], annotation="H4")])

# Diane T10 "visibility into cancellations, no-shows, vehicle utilization, and how far in advance riders book"; Diane T24
g77 = MaintainGoal("<b>G-77</b> CostDriverMetricsReported",
                   performs=sw("ReportingSystem"), leaf=True)

# Diane T16 (no-shows, cancellations)
g82 = AchieveGoal("<b>G-82</b> LossCodedAsRiderCaused <b>If</b> NoShowOrLateCancel",
                  performs=sw("TripRecordSystem"), leaf=True)

# Diane T16 (route reassignment, late pickups)
g83 = AchieveGoal("<b>G-83</b> LossCodedAsAgencyServiceFailure <b>If</b> LatePickupOrRouteReassignment",
                  performs=sw("TripRecordSystem"), leaf=True)

# Diane T16
dp3 = DomainProperty("DP-3 EachLossEvent IsRiderCaused Or AgencyCaused", leaf=True)

# Diane T16 "distinguish rider-caused loss from agency service failure ... cost attribution"
g81 = AchieveGoal("<b>G-81</b> LossAttributedToCause <b>If</b> ServiceLossEventOccurs",
                  refinements=[Refinement(complete=True, children=[g82, g83, dp3], annotation="P3")])

# Diane T26 "cost control has to be balanced with notice and due process"
g87 = AchieveGoal("<b>G-87</b> SanctionApplied <b>If</b> NoShowsRepeated And NoticeGiven And AppealResolved",
                  performs=by("AgencyStaff"), leaf=True)

# Diane T26 "appropriate safeguards around repeated no-shows"; Frank T13 "record those patterns"
g84 = AchieveGoal("<b>G-84</b> RepeatedNoShowsAddressed <b>If</b> NoShowPatternDetected",
                  refinements=[Refinement(complete=False, children=[g67, g85, g86, g87], annotation="H8")])

# Diane T10 "same-day changes are driving costs faster than our budget can absorb"; Diane T16
g76 = SoftGoal("Reduce[<b>G-76</b> AvoidableTripCost]",
               refinements=[Refinement(complete=False, children=[g77, g35, g81, g84], annotation="H4")])

# Diane T12 "standardized eligibility and service-type fields rather than relying on free-text notes"; Diane T14
g90 = MaintainGoal("<b>G-90</b> EligibilityAndServiceTypeStoredAsStructuredFields",
                   performs=sw("TripRecordSystem"), leaf=True)

# Diane T8 "documenting trips and tracking spending. That financial visibility needs to continue."
g91 = MaintainGoal("<b>G-91</b> TripsAndSpendingDocumented",
                   performs=sw("ReportingSystem"), leaf=True)

# Diane T12 "so finance and operations are reviewing the same trip record"; Diane T14 "a canonical trip record"
g88 = MaintainGoal("<b>G-88</b> FinanceAndOperationsShareOneTripRecord",
                   refinements=[Refinement(complete=False, children=[g89, g90, g91], annotation="P5")])

# Diane T10 "reliable projections for contracts, staffing, and vehicle demand"; Diane T26 "dependable budget forecasting"
g92 = AchieveGoal("<b>G-92</b> ProjectionsForContractsStaffingAndVehicleDemandProduced <b>If</b> BudgetCycleStarts",
                  performs=sw("ReportingSystem"), leaf=True)

# Diane T26 "financial and eligibility information should not be visible to everyone who uses the system"
g94 = AvoidGoal("<b>G-94</b> FinancialOrEligibilityDataShownToUnauthorizedRole",
                performs=sw("TripRecordSystem"), leaf=True)

# NOT IN TRANSCRIPT: heuristic H3 (security goal category)
g95 = AchieveGoal("<b>G-95</b> AccessToSensitiveDataLogged <b>If</b> DataViewed",
                  performs=sw("TripRecordSystem"), leaf=True)

# NOT IN TRANSCRIPT: resolves conflict C4 (Frank T25 vs Diane T26)
g108 = MaintainGoal("<b>G-108</b> DriverMDTShowsOnlyFieldsNeededAtPickup",
                    performs=sw("CADSystem"), leaf=True)

# Diane T26 "security and role-based access matter"; Diane T14 "role-based controls"
g93 = MaintainGoal("<b>G-93</b> FinancialAndEligibilityDataVisibleOnlyByRole",
                   refinements=[Refinement(complete=False, children=[g94, g95, g108], annotation="H3")])

# Diane T10 "the phone center carrying too much routine booking work"; Diane T26 "reduce routine calls"
g96 = SoftGoal("Reduce[<b>G-96</b> RoutineCallsToPhoneCenter]",
               refinements=[Refinement(complete=False, children=[g2, g12], annotation="H4")])

# Diane T2 "manage paratransit costs responsibly"; Diane T6, T10, T24
g69 = MaintainGoal("<b>G-69</b> ServiceObligationsMetWithinBudget",
                   refinements=[Refinement(complete=False, children=[g70, g76, g88, g92, g93, g96], annotation="H12")])

# =======================================================================================
# Cross-stakeholder soft goals and the shared root
# =======================================================================================

# MERGED G-10 <- G-68. Janelle T8 "sit on hold for around 20 minutes"; Janelle T10; Frank T17 "Holding time frustrates riders"
g10 = SoftGoal("Reduce[<b>G-10</b> BookingHoldTime]",
               refinements=[Refinement(complete=False, children=[g7], annotation="H6")])

# Diane T26 "cost control has to be balanced with notice and due process"
g105 = AvoidGoal("<b>G-105</b> RiderSanctionedWithoutNoticeOrAppeal",
                 refinements=[Refinement(complete=False, children=[g85, g86], annotation="H9")])

# Frank T13 "a fair way to protect the shared run without treating every rider like a problem";
# Janelle T26 "treat me like a passenger, not a problem"; Diane T26 "handle exceptions fairly"
g66 = SoftGoal("Improve[<b>G-66</b> FairTreatmentOfRiders]",
               refinements=[Refinement(complete=False, children=[g30, g45, g67, g102, g105], annotation="H6")])

# NOT IN TRANSCRIPT: shared root, found by abstracting the three stakeholder roots (H12)
g106 = MaintainGoal("<b>G-106</b> ParatransitServesRidersRunsCleanAndStaysWithinBudget",
                    refinements=[Refinement(complete=False, children=[g1, g33, g69, g10, g66], annotation="H12")])

ROOTS = [g106]
CONFLICTS = [
    ConflictLink(g7, g44),    # C1: rider self-service changes vs dispatcher approval
    ConflictLink(g10, g58),   # C2: shorter holds vs not rushing the booking
    ConflictLink(g76, g105),  # C3: cost control vs notice and due process
    ConflictLink(g55, g94),   # C4: profile fields on the driver's MDT vs role-based visibility
]
# Goals in this model that are not in any transcript. They are highlighted yellow in the diagram.
NOT_IN_TRANSCRIPT = {"G-24": g24, "G-25": g25, "G-95": g95, "G-106": g106, "G-107": g107, "G-108": g108}


def highlight(graph, goals):
    """Color the goals that are not in any transcript yellow."""
    return graph + "".join(f"style {g.get_node_id()} fill:#fff59d,stroke:#b59f00\n" for g in goals)


if __name__ == "__main__":
    graph = highlight(generate_graph(ROOTS, CONFLICTS), NOT_IN_TRANSCRIPT.values())
    print(graph)
    print(generate_pako_link(graph, "view",
                             config={"theme": "default", "themeVariables": {"fontFamily": "Tahoma"}}))
