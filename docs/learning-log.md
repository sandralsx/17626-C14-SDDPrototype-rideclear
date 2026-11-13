# Learning Log

## 1. Sprint Planning and Requirements Selection

For this part, we focused sprint on pickup information and delay communication. Our project, RideClear, lets riders check their pickup window, trip status, and ETA, receive delay notices, and contact dispatch when a revised time does not work.

We chose this scope because during the interview, Janelle described a return ride that was over forty minutes late and said she only learned about the delay after the pickup window ended, Frank wanted consistent information and a way to check updates, and Diane needed accessibility requirement throughout her journey. These requirements directly affect users and tell us uncertainties worth exploring through the prototype.

Three members in our group contributed our models from HW2. Shuxin Liu gathered the files, coordinated the AI-assisted workflow, and checked progress against the assignment. Qingyuan Yao and Jiashen Du contributed their modeling perspectives and participated in prototype use and discussion. The merged model retained the S, J, and Q prefixes and original IDs. We selected eight related goals first, and deferred others like full booking, vehicle reassignment, route optimization, and financial reconciliation. The selected goals were supported by available interviews.

Our discussions clarified some distinctions: an updated ETA must not overwrite the original pickup window; viewing information is different from receiving a notice; and sending, delivery, and acknowledgement are separate events. Contacting dispatch records a request rather than approving a new schedule. Shared state supports consistency between views, while accessibility constrains the entire flow. The model and RTM preserved these decisions, trade-offs, and unresolved conflicts.

## 2. Prototype Evaluation

We developed and used both V1 and V2, and discussed whether the information made sense to riders. Some detailed technical findings also drew on saved AI-assisted checks. We did not independently repeat every procedure. V1 RTM rated four requirements fully satisfied and four partially satisfied in the prototype’s scope.

The first major issue was elapsed ETAs. With a pickup window of 17:00–17:30 and an ETA of 17:15, V1 still displayed “Within pickup window” at simulated time 17:35. Changing a delayed ETA to an already elapsed time could also trigger a recovery notice. We classified this as requirements issue RQ-01: the original specification allowed past ETAs but did not define how they should appear after they elapsed. The code followed the rules, but they did not adequately support reliable information.

The second issue concerned notification timestamps. A notice sent at 16:50 but delivered at 17:35 appeared with “Delivered” beside 16:50, which could mislead riders. Requirements issue RQ-02 called for distinguishing discovery, sending, delivery, and acknowledgement, and defining follow-up when delivery was late. In contrast, removing the acknowledgement button and losing keyboard focus violated an existing requirement, making it implementation defect ID-01.

All of the 17 existing automated tests passed despite the focus defect, showing why interaction checks were also necessary. Mock data can not establish real ETA accuracy, and our testing use doesn't mean stakeholder acceptance. But screen-reader, 200% zoom, and other accessibility checks remained incomplete.

## 3. Revisions and Learning

For V2, we revised the specification, model relationships, and plan before changing the code. FR-017 requires an unfinished trip with an elapsed ETA to display “Estimate needs updating,” preserve the original timing information, and state that arrival is unconfirmed. An elapsed ETA cannot trigger recovery. FR-018 labels notification event times separately and counts delivery as early only when it occurs strictly before the window ends. Late or unrecorded delivery prompts manual follow-up. To correct ID-01, V2 retains the acknowledgement control and focus while preventing repeated acknowledgement. This fixes an existing requirement rather than introducing a new one.

V2 passed all 25 tests, supported by browser checks. There are still unresolved questions about when a future ETA becomes stale, and who owns escalation. We did not present these assumptions as confirmed facts.

Shuxin Liu gathered the HW2 models, coordinated the AI-assisted workflow, and checked the work against the assignment requirements. She learned that displaying a valid ETA does not necessarily provide reliable information, and that human judgment is needed to assess AI-generated requirements and evidence. Jiashen Du contributed his HW2 model and participated in using and discussing both prototypes. He learned why sending, delivery, and acknowledgement must be defined separately, and how precise acceptance criteria help prevent misleading interpretations. Qingyuan Yao contributed his HW2 model and joined the prototype comparison and team discussions. He learned to distinguish requirements problems from implementation defects, and how traceability connects interview needs to specifications, code, and evaluation results.

Spec-driven development made the connections between goals, acceptance scenarios, the RTM, and code clearer. We would explain our scope decisions, issue classifications, and reasons for the V2 changes to management, alongside the division of work between the team and AI. In future collaboration, we should assign responsibility for reviewing each acceptance scenario before implementation, rather than focus only on files and development speed.
