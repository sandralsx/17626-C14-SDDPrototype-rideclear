"""
Goal model extracted from the interview with Frank Moretti (paratransit dispatcher).
17-626 Assignment 2: Requirements Analysis. Qingyuan Yao (qingyuay).

Source: transcripts/Frank.txt, turns T1 to T35. The comment above each goal cites the
turn(s) it comes from. Goals tagged NOT IN TRANSCRIPT came from a refinement pattern or
heuristic, or from my own interpretation, and are listed in missing.json.

Conventions
- Goal IDs G-33 to G-68 belong to this model. IDs are unique across all three models.
- Refinement annotations carry only the heuristic or pattern code (Appendix A).
- Each leaf goal is assigned to exactly one agent.

Vague terms resolved
- "a shared route runs clean" (T7, T17): every pickup inside its window, no change applied
  without a dispatcher seeing its impact, and no surprise for the driver at the curb (G-33).
- "late" (T31): Frank defines it. Pickups are expected within a 30-minute window, and
  anything beyond that is late (G-34).
- "last-minute change" (T9, T11, T13): any change that arrives after the manifest is
  built, including pickup changes, address corrections and cancellations (G-43).
- "enough control to protect the shared routes" (T17): no change reaches a built manifest
  until a dispatcher has seen its impact and accepted it (G-44, G-47).

Conflicts
- G-68 Reduce[RiderHoldTime] vs G-58 Avoid[BookingConfirmedWithUnverifiedDetails]:
  T17 "Holding time frustrates riders, but rushing a booking is how you get the wrong
  address, bad equipment information, or a trip that doesn't fit the route." At peak call
  volume, verifying every booking makes the hold longer. Resolution (H8): verify only the
  profile fields that are flagged as stale (G-60, G-61).
"""
from goalmodeling.schema import *


def by(agent_name, software=False):
    """Assign a leaf goal to exactly one agent. Each leaf gets its own agent node, which keeps the graph legible."""
    agent_type = AgentType.SOFTWARE_AGENT if software else AgentType.ENVIRONMENT_AGENT
    return [PerformanceLink(Agent(agent_name, agent_type), None)]


# ---------------------------------------------------------------------------------------
# G-34: pickups inside the window
# ---------------------------------------------------------------------------------------

# T31 "We have to protect the scheduled return while accounting for vehicle capacity, driver hours, traffic"
g40 = AchieveGoal("<b>G-40</b> RunPlannedWithinCapacityAndDriverHours <b>If</b> ManifestBuilt",
                  performs=by("Scheduler", software=True), leaf=True)

# T29 "Regular rides and returns are generally paired up in the schedule"; T31 "protect the scheduled return"
g41 = MaintainGoal("<b>G-41</b> RegularRidesPairedWithReturnTrips",
                   performs=by("Scheduler", software=True), leaf=True)

# T31 "pickups are expected within a 30-minute window, and anything beyond that is late"
g42 = AchieveGoal("<b>G-42</b> RiderPickedUpWithinWindow <b>If</b> RunOnSchedule",
                  performs=by("Driver"), leaf=True)

# T31 "Evenings are our tightest window ... one late pickup can push the whole shared route behind"
g34 = MaintainGoal("<b>G-34</b> PickupsWithin30MinuteWindow",
                   refinements=[Refinement(complete=False, children=[g40, g41, g42], annotation="H5")])

# ---------------------------------------------------------------------------------------
# G-35: protecting the shared route from last-minute changes
# ---------------------------------------------------------------------------------------

# T13 "require a clear reason for a change"
g45 = AchieveGoal("<b>G-45</b> ChangeReasonRecorded <b>If</b> ChangeRequested",
                  performs=by("DispatchSystem", software=True), leaf=True)

# T9 "flags conflicts with vehicle capacity and existing pickups"
g51 = AchieveGoal("<b>G-51</b> CapacityAndPickupConflictsFlagged <b>If</b> ChangeProposed",
                  performs=by("DispatchSystem", software=True), leaf=True)

# T9 "lets dispatchers see which riders and drivers will be affected"
g52 = AchieveGoal("<b>G-52</b> AffectedRidersAndDriversShown <b>If</b> ChangeProposed",
                  performs=by("DispatchSystem", software=True), leaf=True)

# T13 "show dispatch the cost to the rest of the route before we accept it"
g53 = AchieveGoal("<b>G-53</b> CostToRestOfRouteShown <b>If</b> ChangeProposed",
                  performs=by("DispatchSystem", software=True), leaf=True)

# T9 "a system that shows the impact before we approve a change"; T33 "a clear impact view before any change is accepted"
g46 = AchieveGoal("<b>G-46</b> RouteImpactShownToDispatcher <b>If</b> ChangeReasonRecorded",
                  refinements=[Refinement(complete=False, children=[g51, g52, g53], annotation="P5")])

# T9 "we can make the call with the whole route in front of us"; T11 "decide whether it creates a late pickup or a no-show"
g47 = AchieveGoal("<b>G-47</b> ChangeAcceptedOrRejectedByDispatcher <b>If</b> RouteImpactShown",
                  performs=by("Dispatcher"), leaf=True)

# T11 "re-sequence the run, check the window, and protect the other scheduled pickups";
# T19 "enough route detail to re-sequence safely"
g48 = AchieveGoal("<b>G-48</b> RunResequencedWithinWindows <b>If</b> ChangeAccepted",
                  performs=by("DispatchSystem", software=True), leaf=True)

# T11 "If the driver's already rolling, dispatch has to radio the change";
# T29 "get the right information to the driver before it becomes a curbside problem"; T25 "driver MDT"
g49 = AchieveGoal("<b>G-49</b> DriverRunSheetUpdated <b>If</b> TripChangedAfterManifestReleased",
                  performs=by("DispatchSystem", software=True), leaf=True)

# NOT IN TRANSCRIPT: pattern P1 adds this last milestone, because re-sequencing a shared run
# moves the pickup times of the other riders on it
g50 = AchieveGoal("<b>G-50</b> AffectedRidersNotified <b>If</b> PickupTimeMoved",
                  performs=by("TripTracker", software=True), leaf=True)

# T9 "last-minute changes ... ripple through the whole board"; T11 "the ugly ones come after the manifest is built"
g43 = AchieveGoal("<b>G-43</b> ChangeAppliedSafely <b>If</b> ChangeRequestedAfterManifestBuilt",
                  refinements=[Refinement(complete=False, children=[g45, g46, g47, g48, g49, g50], annotation="P1")])

# T17 "dispatch still needs enough control to protect the shared routes"; T33 "before any change is accepted"
# (the converse of G-43: a change reaches a built manifest only through dispatcher approval)
g44 = AvoidGoal("<b>G-44</b> ChangeAppliedWithoutDispatcherApproval",
                performs=by("DispatchSystem", software=True), leaf=True)

# T9 "they ripple through the whole board and can wreck a shared route"; T13; T17; T33
g35 = MaintainGoal("<b>G-35</b> SharedRouteProtectedFromLastMinuteChanges",
                   refinements=[Refinement(complete=False, children=[g43, g44], annotation="H10")])

# ---------------------------------------------------------------------------------------
# G-36: no surprises for the driver at the curb
# ---------------------------------------------------------------------------------------

# T25 "a single source of truth for the rider profile, with structured fields for mobility device
# dimensions, securement type, attendant status, and curb-to-door access instructions"
g56 = MaintainGoal("<b>G-56</b> SingleProfileRecordWithStructuredFields",
                   performs=by("CADSystem", software=True), leaf=True)

# T25 "with an audit trail when somebody changes them"
g57 = AchieveGoal("<b>G-57</b> ProfileChangeLoggedInAuditTrail <b>If</b> ProfileEdited",
                  performs=by("CADSystem", software=True), leaf=True)

# T25 "a prompt to verify stale information during booking"
g60 = AchieveGoal("<b>G-60</b> StaleProfileFieldsFlagged <b>If</b> BookingMade",
                  performs=by("CADSystem", software=True), leaf=True)

# T23 "We verify the equipment, passenger-assistance needs, and curb-to-door access notes during booking"
g61 = AchieveGoal("<b>G-61</b> FlaggedFieldsConfirmedOrCorrected <b>If</b> FieldsFlagged",
                  performs=by("ReservationAgent"), leaf=True)

# T17 "rushing a booking is how you get the wrong address, bad equipment information, or a trip that doesn't fit the route"
g58 = AvoidGoal("<b>G-58</b> BookingConfirmedWithUnverifiedDetails",
                refinements=[Refinement(complete=False, children=[g60, g61], annotation="H8")])

# NOT IN TRANSCRIPT: pattern P6, because the system cannot observe the rider's actual equipment;
# only the rider can report a change to it
g59 = AchieveGoal("<b>G-59</b> EquipmentChangeReportedByRider <b>If</b> EquipmentChanges",
                  performs=by("Rider"), leaf=True)

# T23 "Usually the mobility profile is in the CAD record, but it isn't always complete or current"
g54 = MaintainGoal("<b>G-54</b> RiderProfileCompleteAndCurrent",
                   refinements=[Refinement(complete=False, children=[g56, g57, g58, g59], annotation="P6")])

# T25 "Those fields should carry forward automatically into the trip record, manifest, and driver MDT";
# T21 "the mobility profile doesn't carry the right equipment and access notes into the driver's run sheet";
# T23 "then carry them into the manifest"
g55 = AchieveGoal("<b>G-55</b> EquipmentAssistanceAndAccessNotesCarriedIntoManifestAndMDT <b>If</b> TripBooked",
                  performs=by("CADSystem", software=True), leaf=True)

# T23 "the driver gets surprised at pickup"; T21 "we find out at the curb"; T27 "they call dispatch from the curb";
# T31 "dispatch gets pulled into a curbside problem"
g36 = AvoidGoal("<b>G-36</b> DriverSurprisedAtCurb",
                refinements=[Refinement(complete=False, children=[g54, g55, g49], annotation="H4")])

# ---------------------------------------------------------------------------------------
# G-37: complete manifest
# ---------------------------------------------------------------------------------------

# T19 "ordered stops, pickup and drop-off windows, rider names, mobility equipment, addresses"
g62 = MaintainGoal("<b>G-62</b> ManifestListsOrderedStopsWindowsAndAddresses",
                   performs=by("DispatchSystem", software=True), leaf=True)

# T19 "trip status, and any no-show or late-cancel indicators"
g63 = MaintainGoal("<b>G-63</b> ManifestShowsTripStatusAndNoShowOrLateCancelFlags",
                   performs=by("DispatchSystem", software=True), leaf=True)

# T19 "plus the vehicle assignment"
g64 = MaintainGoal("<b>G-64</b> ManifestShowsVehicleAssignment",
                   performs=by("DispatchSystem", software=True), leaf=True)

# T19 "A clear manifest is the operational run sheet"; T17 "A clean manifest ... keep the day from coming apart"
g37 = MaintainGoal("<b>G-37</b> ManifestCompleteForDriverAndDispatch",
                   refinements=[Refinement(complete=False, children=[g62, g55, g63, g64], annotation="P5")])

# ---------------------------------------------------------------------------------------
# G-38 and G-39
# ---------------------------------------------------------------------------------------

# T17 "Janelle's right that customers need clearer status information"
g65 = AchieveGoal("<b>G-65</b> TripStatusVisibleToRider <b>If</b> TripScheduled",
                  performs=by("TripTracker", software=True), leaf=True)

# T7 "everybody gets where they're going without a complaint call"; T17 "riders asking where their van is"
g38 = SoftGoal("Reduce[<b>G-38</b> ComplaintAndStatusCalls]",
               refinements=[Refinement(complete=False, children=[g65], annotation="H4")])

# T7 "drivers who know how to handle people properly"; T17 "drivers who know their riders"; T31 "The driver usually knows the rider best"
g39 = MaintainGoal("<b>G-39</b> DriversSkilledAndFamiliarWithRiders",
                   performs=by("Agency"), leaf=True)

# ---------------------------------------------------------------------------------------
# Roots
# ---------------------------------------------------------------------------------------

# T7 "I'm proud when a shared route runs clean and everybody gets where they're going";
# T17 "A clean manifest and drivers who know their riders are what keep the day from coming apart"
g33 = MaintainGoal("<b>G-33</b> SharedRouteRunsClean",
                   refinements=[Refinement(complete=False, children=[g34, g35, g36, g37, g38, g39], annotation="H12")])

# T13 "I'd want the system to record those patterns"; T13 "no-shows, late cancels"
g67 = AchieveGoal("<b>G-67</b> NoShowAndLateCancelPatternsRecorded <b>If</b> NoShowOrLateCancelOccurs",
                  performs=by("DispatchSystem", software=True), leaf=True)

# T13 "That gives us a fair way to protect the shared run without treating every rider like a problem"
g66 = SoftGoal("Improve[<b>G-66</b> FairTreatmentOfRiders]",
               refinements=[Refinement(complete=False, children=[g67, g45], annotation="H6")])

# T17 "Holding time frustrates riders"
g68 = SoftGoal("Reduce[<b>G-68</b> RiderHoldTime]",
               performs=by("ReservationAgent"), leaf=True)

ROOTS = [g33, g66, g68]
CONFLICTS = [ConflictLink(g68, g58)]  # T17: shorter holds vs not rushing the booking
# Goals not in the transcript. They are highlighted yellow in the diagram.
NOT_IN_TRANSCRIPT = {"G-50": g50, "G-59": g59}


def highlight(graph, goals):
    """Color the goals that are not in the transcript yellow."""
    return graph + "".join(f"style {g.get_node_id()} fill:#fff59d,stroke:#b59f00\n" for g in goals)


if __name__ == "__main__":
    graph = highlight(generate_graph(ROOTS, CONFLICTS), NOT_IN_TRANSCRIPT.values())
    print(graph)
    print(generate_pako_link(graph, "view",
                             config={"theme": "default", "themeVariables": {"fontFamily": "Tahoma"}}))
