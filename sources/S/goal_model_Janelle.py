"""Stakeholder-specific goal extraction grounded in the supplied CSV. Source row IDs appear on each goal; analyst interpretations should be reviewed."""
from goalmodeling.schema import AchieveGoal, MaintainGoal, SoftGoal, Refinement, generate_graph, generate_pako_link

def build_goals():
    goals = {}
    goals['G-1'] = AchieveGoal(name='G-1 Ride reservations recorded with pickup, drop-off, date and time details', leaf=True)  #8, 10
    goals['G-2'] = AchieveGoal(name='G-2 Return ride included if [rider requests a return trip]', leaf=True)
    goals['G-3'] = MaintainGoal(name='G-3 Rider information retained for repeat booking', leaf=True) 
    goals['G-4'] = MaintainGoal(name='G-4 Assigned vehicle accommodates rider power wheelchair', leaf=True) 
    goals['G-5'] = AchieveGoal(name='G-5 Rider can book a ride online independently', leaf=True) 
    goals['G-6'] = AchieveGoal(name='G-6 Rider can modify an existing booking online independently', leaf=True)  
    goals['G-7'] = AchieveGoal(name='G-7 Rider can view scheduled pickup window', leaf=True) 
    goals['G-8'] = AchieveGoal(name='G-8 Rider can view live vehicle status and updated arrival estimate', leaf=True)  # 20, 30, 33
    goals['G-9'] = AchieveGoal(name='G-9 Rider notified of delay before pickup window expires if [the vehicle is running late]', leaf=True)
    goals['G-10'] = AchieveGoal(name='G-10 Rider can contact dispatch if [a significant delay makes the revised arrival time unsuitable]', leaf=True)
    goals['G-11'] = SoftGoal(name='G-11 Minimize time on hold during booking and trip changes', leaf=True)  # 8, 22, 30
    goals['G-12'] = MaintainGoal(name='G-12 Independent use of online booking and changes remains accessible', leaf=True)
    goals['G-13'] = MaintainGoal(name='G-13 Personal care attendant rides free if [the program permits a qualifying accompanying attendant]', leaf=True)
    goals['G-14'] = SoftGoal(name='G-14 Improve accuracy and reliability of return-trip arrival information', leaf=True) 
    # Analyst-derived parents retain the same IDs and meanings in the combined model.
    goals['G-34'] = AchieveGoal(
        name='G-34 Riders can arrange accessible paratransit trips independently [INFERRED]',
        refinements=[Refinement(complete=False, children=[
            goals['G-1'], goals['G-2'], goals['G-3'], goals['G-4'],
            goals['G-5'], goals['G-6'], goals['G-12'], goals['G-13']
        ], annotation='H4')])
    goals['G-35'] = AchieveGoal(
        name='G-35 Riders can anticipate and respond to pickup disruptions [INFERRED]',
        refinements=[Refinement(complete=False, children=[
            goals['G-7'], goals['G-8'], goals['G-9'], goals['G-10']
        ], annotation='P1')])
    # Either display provides timing information (Janelle rows 30, 33).
    # This narrow OR does not replace the requirement for BOTH displays in G-35.
    goals['G-41'] = AchieveGoal(
        name='G-41 Rider can view pickup timing information [INFERRED]',
        refinements=[
            Refinement(complete=False, children=[goals['G-7']], annotation='H4'),
            Refinement(complete=False, children=[goals['G-8']], annotation='H4')])
    return goals


def build_roots(goals):
    return [goals[x] for x in ('G-34', 'G-35', 'G-41', 'G-11', 'G-14')]


def generate_diagram(goals, roots):
    diagram = generate_graph(roots, [])
    inferred = ','.join(g.get_node_id() for g in goals.values() if '[INFERRED]' in g.name)
    return diagram + f'\nclassDef inferred fill:#fff59d,color:#000;\nclass {inferred} inferred;\n'

if __name__ == "__main__":
    goals = build_goals()
    diagram = generate_diagram(goals, build_roots(goals))
    print(diagram)
    print(generate_pako_link(diagram, "edit"))
