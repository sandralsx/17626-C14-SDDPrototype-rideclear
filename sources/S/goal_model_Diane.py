"""Stakeholder-specific goal extraction grounded in the supplied CSV. Source row IDs appear on each goal; analyst interpretations should be reviewed."""
from goalmodeling.schema import AchieveGoal, MaintainGoal, SoftGoal, Refinement, generate_graph, generate_pako_link

def build_goals():
    goals = {}
    goals['G-25'] = AchieveGoal(name='G-25 Track spending by vehicles, contractors and personnel', leaf=True) 
    goals['G-26'] = AchieveGoal(name='G-26 Measure trip volume and cost per trip against budget', leaf=True)  # CSV stakeholder rows: 8,11,17
    goals['G-27'] = AchieveGoal(name='G-27 Track productivity and scheduled hours against completed trips', leaf=True)  # 11,17
    goals['G-28'] = AchieveGoal(name='G-28 Report on-time performance, no-shows and trip denials', leaf=True)  # 11,17,24
    goals['G-29'] = MaintainGoal(name='G-29 Cost and service reports use consistently reconciled trip records', leaf=True)  # 19,22,26
    goals['G-30'] = AchieveGoal(name='G-30 Reconcile statuses, cancellations, empty travel and invoice units across sources', leaf=True) 
    goals['G-31'] = MaintainGoal(name='G-31 Customer-facing service conforms to WCAG 2.1 AA', leaf=True)  
    goals['G-32'] = SoftGoal(name='G-32 Reduce manual reconciliation effort in periodic reporting', leaf=True) 
    goals['G-33'] = MaintainGoal(name='G-33 Operational efficiency does not compromise required service access', leaf=True)  # 14,24,32
    goals['G-38'] = AchieveGoal(
        name='G-38 Finance can evaluate service cost and compliance from aligned data [INFERRED]',
        refinements=[Refinement(complete=False, children=[
            goals['G-25'], goals['G-26'], goals['G-27'], goals['G-28'],
            goals['G-29'], goals['G-30'], goals['G-31']
        ], annotation='P5')])
    return goals


def build_roots(goals):
    # Effort reduction and access protection remain separate stakeholder concerns.
    return [goals[x] for x in ('G-38', 'G-32', 'G-33')]


def generate_diagram(goals, roots):
    diagram = generate_graph(roots, [])
    inferred = ','.join(g.get_node_id() for g in goals.values() if '[INFERRED]' in g.name)
    return diagram + f'\nclassDef inferred fill:#fff59d,color:#000;\nclass {inferred} inferred;\n'

if __name__ == "__main__":
    goals = build_goals()
    diagram = generate_diagram(goals, build_roots(goals))
    print(diagram)
    print(generate_pako_link(diagram, "edit"))
