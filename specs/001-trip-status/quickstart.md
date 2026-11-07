# Quickstart and Validation Guide

Prerequisite: Node.js 24+ (22+ supports the used standard APIs). No npm installation
or external service credential is needed for the app.

```powershell
node --test
node scripts/build.mjs
node scripts/serve.mjs
```

Open the server's printed localhost URL. Do not open index.html through `file:`.
If this host's default Node is older, use the bundled Codex Node executable shown
in `docs/workflow-receipt.md`.

1. Rider view: select outbound and return; inspect separate original window and ETA.
2. Dispatch view: select return, set demo clock 16:50 and ETA 17:45, status en route.
   Save. Window remains 17:00-17:30, a delay notice appears, with sent outcome only.
3. Mark that notice delivered, switch to Rider, acknowledge explicitly. Dispatch
   then shows acknowledged. Viewing without acknowledgement does not change outcome.
4. Load the Late discovery fixture. Confirm the notice is marked as an early-notice
   miss and has no fabricated early send. Load Unknown ETA for the unknown state.
5. Submit a rider request. Inspect the dispatch queue and mark reviewed. Trip/window
   remain unchanged. Blank input produces an associated error and no record.
6. Mark a sent notice unreachable, retry it and inspect both attempts. No trip is
   canceled or rescheduled. Try a change notice without driver acceptance: rejected.
7. In a second same-origin tab and same browser profile, open the other role. Save
   a state change and verify both match. A stale editor must refresh before writing.
8. Use keyboard only for leg selection, notification acknowledgement and contact.
   Inspect at 375 px and 200% zoom. Check live feedback without background focus theft.

These are engineering validation instructions, not prewritten student evaluation
findings or Learning Log answers. Actual run evidence belongs in
`docs/engineering-verification.md`; student observations/reflection remain independent.
