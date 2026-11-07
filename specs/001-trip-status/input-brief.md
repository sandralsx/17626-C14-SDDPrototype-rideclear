# Input for Spec Kit: RideClear V1

Use the completed A3 Step 1/2 model in outputs/a3-step1-step2/docs/goal-model.md as the requirement source. Build an English-language paratransit rider and dispatcher prototype for Trip Status, ETA and Delay Communication. Preserve A3-G01..08 and R-01..08 mappings.

Rider sees two seeded trip legs, their separate scheduled pickup windows, current vehicle status, latest available ETA with as-of time, a distinct delay notification, and a way to report an unsuitable revised ETA. Dispatcher can update mock trip status/ETA, inspect communication outcomes, and view contact requests. A change notice requires the simulated driver-accepted condition; a predicted delay notice does not wait for it. Preferred SMS/phone/email channels are simulated only. Distinguish sent, delivered, acknowledged and unreachable. An acknowledgement requires an explicit user/simulator action.

Apply scoped WCAG 2.1 AA goals to rider interactions. Include a return-trip scenario without pretending to prove real-world ETA accuracy. Preserve all source-model conflicts/context and distinguish evidence from prototype assumptions. No booking, reassignment solver, actual GPS, payment, real SMS, sanctions, or production authentication.

Adopt the following explicit prototype assumptions to resolve U01..05 for V1, without claiming stakeholder confirmation:

1. A valid ETA > that leg's saved window end predicts delay; equality does not. Immediately create a separate delay event. If discovered at/after window end, record an early-notice miss. Do not fabricate an earlier notice. Unknown ETA never appears as on time. A value earlier than window start is labeled ahead of window; it does not change the schedule.
2. The demo uses a fixed service date, local service time, explicit simulated clock and sequential commands. Display every as-of time. No numeric freshness SLA or GPS computation is claimed. Terminal arrived/completed trip states do not generate a new predicted-delay notice.
3. One unchanged ETA/status update is a no-op. Each materially changed delayed ETA generates a new update notice; recovery to within the window generates a recovery notice; losing a previously known ETA generates an estimate-unavailable update. Initial unknown ETA has no fabricated delay ETA. Prior notices remain as history.
4. Accepted change and predicted delay use the same communication mechanism but keep separate event types/triggers. Mock delivery is explicit. Pending messages do not silently advance. Mark unreachable without canceling, holding a run, rescheduling or sanctioning a rider. Allow an explicit simulated retry to a new sent state while keeping attempt history.
5. Contact requests preserve the trip ID and ETA snapshot. Display a clear mock receipt. They never change the scheduled window or ETA. The dispatcher can mark the request reviewed; this does not imply a revised schedule was accepted.
6. Shared state is per browser profile and Site origin, persisted locally, and synchronized across same-origin tabs. It is not a server-backed multi-user system. Use only fictional demo data. Reset explicitly restores fixtures. A stale revision cannot overwrite a newer state; reject and refresh it.

Deliver constitution, feature spec/acceptance scenarios, plan/design artifacts, dependency-ordered tasks, source, tests, build output, and V1 preservation/deployment records. Do not write learning-log.md or create fabricated Step 4 evaluation findings. Document actual engineering verification separately from student evaluation/reflection.
