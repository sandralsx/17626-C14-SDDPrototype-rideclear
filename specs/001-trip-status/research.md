# Phase 0 Research and Decisions

No technical unknown blocks the bounded V1. Stakeholder U01..06 remain explicitly
unconfirmed and are operationalized by spec PA-01..07, not resolved by research.

## Decision: One local demo state with lock/revision writes

Use localStorage for reload persistence and the storage event for other tabs.
The writing tab renders directly because the event is not fired on that window.
Use a named Web Lock around re-read, expected-revision check and write. A normal
revision check without serialization is not an atomic concurrency guarantee.

Rationale: a shared same-browser demo is the declared scope. Alternative: a server
database supports different devices/users but expands the sprint. Memory only is
simple but loses reload/cross-tab behavior. If storage or locks are absent, switch
to clearly labeled current-tab temporary mode, not a falsely durable shared mode.

Sources: [MDN storage event](https://developer.mozilla.org/en-US/docs/Web/API/Window/storage_event),
[MDN Web Locks](https://developer.mozilla.org/en-US/docs/Web/API/Web_Locks_API),
[MDN localStorage](https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage),
[MDN setItem](https://developer.mozilla.org/en-US/docs/Web/API/Storage/setItem).

## Decision: Native controls and a persistent polite status region

Use native buttons/selects/forms, visible associated labels, an error associated
with invalid input, and a persistent role=status region for succinct feedback.
Do not move focus on background state changes. Store role and current leg per tab,
so another tab does not change a user's view selection.

Rationale: predictable keyboard operation matters for independent use. Alternative:
custom div controls and page replacement would add accessibility/focus work without
benefit. An assertive live region is inappropriate for routine updates. These choices
support scoped WCAG goals; they do not prove full assistive-technology conformance.

Sources: [W3C semantic HTML](https://www.w3.org/WAI/ARIA/apg/practices/read-me-first/),
[W3C form labels](https://www.w3.org/WAI/tutorials/forms/labels/),
[W3C status messages](https://www.w3.org/WAI/WCAG21/Understanding/status-messages.html),
[W3C focus order](https://www.w3.org/WAI/WCAG21/Understanding/focus-order.html).

## Decision: Static modules and service-day minute values

Represent demo times as integers 0..1439 in America/New_York on 2026-11-07.
Convert only at input/output; use explicit simulated now rather than host timezone.
Use no real provider service, credentials or runtime dependency. Node 24 runs tests
and copies exact assets for deployment. No new timing SLA is inferred.

Alternative: absolute timestamps and a real-time feed are appropriate for production
cross-day service but unnecessary for this single-service-day mock. Plain static
deployment also permits keeping V1 and later V2 at separate URLs.

## Visual direction

The local design-system search returned transit-blue flat UI guidance, but its
marketing-page pattern and loud display typography do not fit a rider utility.
Apply subject-specific judgment: transport sign typography, clear large time values,
an original-window/current-estimate split and a quiet route line. Avoid marketing
sections and decorative maps that imply real tracking.

Tokens: ink #123C54, action teal #00685D, canvas #F2F6F8, white #FFFFFF,
warning ink #854900 on #FFF1D6, muted ink #526674. Bahnschrift/Trebuchet for
headings, Segoe UI/system sans for body, Consolas/monospace for utility times.
Use spacious touch controls, obvious focus, non-color statuses and reduced motion.

Layout: trip/leg selector and primary pickup panel alongside a compact notification
and contact column. Dispatch uses an editor plus readable communication queue.
The signature is the paired saved window and live estimate, joined to the leg's
route line; it directly encodes the central requirement distinction.
