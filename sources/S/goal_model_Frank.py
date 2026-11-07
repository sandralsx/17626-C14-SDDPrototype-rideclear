"""Stakeholder-specific goal extraction grounded in the supplied CSV. Source row IDs appear on each goal; analyst interpretations should be reviewed."""
from goalmodeling.schema import AchieveGoal, MaintainGoal, SoftGoal, Refinement, generate_graph, generate_pako_link

def build_goals():
    goals = {}
    goals['G-15'] = AchieveGoal(name='G-15 Group ride requests by time, location and accessibility requirements', leaf=True)  
    goals['G-16'] = MaintainGoal(name='G-16 Vehicle assignment fits lift and wheelchair securement needs', leaf=True) 
    goals['G-17'] = AchieveGoal(name='G-17 Shared rides arranged if [capacity and time windows permit]', leaf=True)
    goals['G-18'] = MaintainGoal(name='G-18 Assignments respect driver region and training constraints', leaf=True) 
    goals['G-19'] = SoftGoal(name='G-19 Minimize empty vehicle travel and route inefficiency', leaf=True)  
    goals['G-20'] = MaintainGoal(name='G-20 Requested pickup windows remain feasible when trips are assigned', leaf=True)  # CSV stakeholder rows: 9,13
    goals['G-21'] = AchieveGoal(name='G-21 Dispatcher can assess replacement assignment effects if [a vehicle becomes unavailable]', leaf=True)  # CSV stakeholder rows: 20,32
    goals['G-22'] = AchieveGoal(name='G-22 Affected riders receive notice if [a replacement assignment is accepted]', leaf=True)  # CSV stakeholder rows: 20,24
    goals['G-23'] = MaintainGoal(name='G-23 Scheduling and dispatch status stays synchronized across operational users', leaf=True)  # CSV stakeholder rows: 26,30,32
    goals['G-24'] = AchieveGoal(name='G-24 Dispatch can record delivery and acknowledgement of change notices', leaf=True)  # CSV stakeholder rows: 24,35
    goals['G-36'] = MaintainGoal(
        name='G-36 Dispatch provides feasible and coordinated trip service [INFERRED]',
        refinements=[Refinement(complete=False, children=[
            goals['G-15'], goals['G-16'], goals['G-17'], goals['G-18'],
            goals['G-20'], goals['G-23']
        ], annotation='H5')])
    goals['G-37'] = AchieveGoal(
        name='G-37 Dispatch restores service if [vehicle becomes unavailable] [INFERRED]',
        refinements=[Refinement(complete=False, children=[
            goals['G-21'], goals['G-22'], goals['G-24']
        ], annotation='P4')])
    return goals


def build_roots(goals):
    # G-19 is an optimization preference, not a mandatory feasibility condition.
    return [goals[x] for x in ('G-36', 'G-37', 'G-19')]


def generate_diagram(goals, roots):
    diagram = generate_graph(roots, [])
    inferred = ','.join(g.get_node_id() for g in goals.values() if '[INFERRED]' in g.name)
    return diagram + f'\nclassDef inferred fill:#fff59d,color:#000;\nclass {inferred} inferred;\n'

if __name__ == "__main__":
    goals = build_goals()
    diagram = generate_diagram(goals, build_roots(goals))
    print(diagram)
    print(generate_pako_link(diagram, "edit"))
