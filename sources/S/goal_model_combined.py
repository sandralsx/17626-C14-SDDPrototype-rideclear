"""Combined goal model grounded in all three CSV transcripts.

G-16 is merged into G-4. G-34..39 and G-41 are analyst-derived parents.
G-40 was removed because contacting dispatch does not guarantee a status update.
Refinements remain incomplete unless sufficiency has been established.
"""
from goalmodeling.schema import AchieveGoal, MaintainGoal, SoftGoal, Refinement, generate_graph, generate_pako_link

def build_model():
    goals = {}
    goals["G-1"] = AchieveGoal(name="G-1 Ride reservations recorded with pickup, drop-off, date and time details", leaf=True)
    goals["G-2"] = AchieveGoal(name="G-2 Return ride included if [rider requests a return trip]", leaf=True)
    goals["G-3"] = MaintainGoal(name="G-3 Rider information retained for repeat booking", leaf=True)
    goals["G-4"] = MaintainGoal(name="G-4 Assigned vehicle accommodates rider wheelchair, lift and securement requirements", leaf=True)
    goals["G-5"] = AchieveGoal(name="G-5 Rider can book a ride online independently", leaf=True)
    goals["G-6"] = AchieveGoal(name="G-6 Rider can modify an existing booking online independently", leaf=True)
    goals["G-7"] = AchieveGoal(name="G-7 Rider can view scheduled pickup window", leaf=True)
    goals["G-8"] = AchieveGoal(name="G-8 Rider can view live vehicle status and updated arrival estimate", leaf=True)
    goals["G-9"] = AchieveGoal(name="G-9 Rider notified before pickup window expires if [vehicle is running late]", leaf=True)
    goals["G-10"] = AchieveGoal(name="G-10 Rider can contact dispatch if [significant delay makes the revised ETA unsuitable]", leaf=True)
    goals["G-11"] = SoftGoal(name="G-11 Minimize time on hold during booking and trip changes", leaf=True)
    goals["G-12"] = MaintainGoal(name="G-12 Independent use of online booking and changes remains accessible", leaf=True)
    goals["G-13"] = MaintainGoal(name="G-13 Personal care attendant rides free if [a qualifying attendant accompanies the rider]", leaf=True)
    goals["G-14"] = SoftGoal(name="G-14 Improve accuracy and reliability of return-trip arrival information", leaf=True)
    goals["G-15"] = AchieveGoal(name="G-15 Group ride requests by time, location and accessibility requirements", leaf=True)
    goals["G-17"] = AchieveGoal(name="G-17 Shared rides arranged if [capacity and time windows permit]", leaf=True)
    goals["G-18"] = MaintainGoal(name="G-18 Assignments respect driver region and training constraints", leaf=True)
    goals["G-19"] = SoftGoal(name="G-19 Minimize empty vehicle travel and route inefficiency", leaf=True)
    goals["G-20"] = MaintainGoal(name="G-20 Requested pickup windows remain feasible when trips are assigned", leaf=True)
    goals["G-21"] = AchieveGoal(name="G-21 Dispatcher can evaluate capacity, proximity, lift, deadhead and window impacts if [vehicle becomes unavailable]", leaf=True)
    goals["G-22"] = AchieveGoal(name="G-22 Affected riders receive preferred-channel updates if [driver accepts replacement assignment]", leaf=True)
    goals["G-23"] = MaintainGoal(name="G-23 Scheduling and dispatch status stays synchronized across operational users", leaf=True)
    goals["G-24"] = AchieveGoal(name="G-24 Dispatch records delivery, acknowledgement and unreachable riders for changed trips", leaf=True)
    goals["G-25"] = AchieveGoal(name="G-25 Track spending by vehicles, contractors and personnel", leaf=True)
    goals["G-26"] = AchieveGoal(name="G-26 Measure trip volume and cost per trip against budget", leaf=True)
    goals["G-27"] = AchieveGoal(name="G-27 Track productivity and scheduled hours against completed trips", leaf=True)
    goals["G-28"] = AchieveGoal(name="G-28 Report on-time performance, no-shows and trip denials", leaf=True)
    goals["G-29"] = MaintainGoal(name="G-29 Cost and service reports use consistently reconciled trip records", leaf=True)
    goals["G-30"] = AchieveGoal(name="G-30 Reconcile statuses, cancellations, empty travel and invoice units across sources", leaf=True)
    goals["G-31"] = MaintainGoal(name="G-31 Customer-facing service conforms to WCAG 2.1 AA", leaf=True)
    goals["G-32"] = SoftGoal(name="G-32 Reduce manual reconciliation effort in periodic reporting", leaf=True)
    goals["G-33"] = MaintainGoal(name="G-33 Operational efficiency does not compromise required service access", leaf=True)
    goals["G-34"] = AchieveGoal(name="G-34 Riders can arrange accessible paratransit trips independently [INFERRED]", refinements=[
        Refinement(complete=False, children=[goals["G-1"], goals["G-2"], goals["G-3"], goals["G-4"], goals["G-5"], goals["G-6"], goals["G-12"], goals["G-13"]], annotation="H4")])
    goals["G-35"] = AchieveGoal(name="G-35 Riders can anticipate and respond to pickup disruptions [INFERRED]", refinements=[
        Refinement(complete=False, children=[goals["G-7"], goals["G-8"], goals["G-9"], goals["G-10"]], annotation="P1")])
    goals["G-36"] = MaintainGoal(name="G-36 Dispatch provides feasible and coordinated trip service [INFERRED]", refinements=[
        Refinement(complete=False, children=[goals["G-15"], goals["G-4"], goals["G-17"], goals["G-18"], goals["G-20"], goals["G-23"]], annotation="H5")])
    goals["G-37"] = AchieveGoal(name="G-37 Dispatch restores service if [vehicle becomes unavailable] [INFERRED]", refinements=[
        Refinement(complete=False, children=[goals["G-21"], goals["G-22"], goals["G-24"]], annotation="P4")])
    goals["G-38"] = AchieveGoal(name="G-38 Finance can evaluate service cost and compliance from aligned data [INFERRED]", refinements=[
        Refinement(complete=False, children=[goals["G-25"], goals["G-26"], goals["G-27"], goals["G-28"], goals["G-29"], goals["G-30"], goals["G-31"]], annotation="P5")])
    goals["G-39"] = SoftGoal(name="G-39 Minimize service administration burden without reducing access [INFERRED]", refinements=[
        Refinement(complete=False, children=[goals["G-11"], goals["G-19"], goals["G-32"], goals["G-33"]], annotation="H6")])
    # Either display answers the narrow question of pickup timing (Janelle rows 30, 33).
    # The scheduled window alone does not promise a current status or live ETA.
    # G-35 still requires BOTH G-7 and G-8; this OR does not weaken those requirements.
    goals["G-41"] = AchieveGoal(name="G-41 Rider can view pickup timing information [INFERRED]", refinements=[
        Refinement(complete=False, children=[goals["G-7"]], annotation="H4"),
        Refinement(complete=False, children=[goals["G-8"]], annotation="H4")])
    # G-14 is a separate quality goal and must not disappear from the rendered model.
    roots = [goals[x] for x in ("G-34", "G-35", "G-36", "G-37", "G-38", "G-39", "G-41", "G-14")]
    return goals, roots


def generate_diagram(goals, roots):
    # Frank rows 9,13 and Diane rows 14,24 describe an efficiency/access trade-off,
    # not evidence that the goals cannot hold together. No strong conflict is asserted.
    diagram = generate_graph(roots, [])
    inferred = ','.join(g.get_node_id() for g in goals.values() if '[INFERRED]' in g.name)
    return diagram + f'\nclassDef inferred fill:#fff59d,color:#000;\nclass {inferred} inferred;\n'


if __name__ == "__main__":
    goals, roots = build_model()
    diagram = generate_diagram(goals, roots)
    print(diagram)
    print(generate_pako_link(diagram,"edit"))
