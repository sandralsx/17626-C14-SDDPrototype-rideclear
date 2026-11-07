# Spec Kit and V1 Workflow Receipt

This is an engineering provenance record, not the Learning Log or a Step 6 answer.

## Actual tooling

- Official PyPI package `specify-cli==1.3.2`, installed into the task-local
  `work/specify-packages` directory. No global Python environment was intentionally
  changed. Version sanity check reported Specify CLI 1.3.2, Python 3.12.14, Windows.
- Project initialization succeeded with:

```text
specify init --here --force --non-interactive --integration codex --script ps --ignore-agent-tools
```

The executable was invoked through a task-local Python launcher calling the actual
`specify_cli:main` entry point. `--force` merged only the newly created project's
existing .git and hosting manifest. The first attempted `--no-git` flag was rejected
by 1.3.2 before initialization; the successful invocation above omits it.

Original installed metadata is retained in `.specify/init-options.json`,
`.specify/integrations/speckit.manifest.json` and `codex.manifest.json`, including
installer version/timestamps and source-file hashes.

## Agentic workflow actually followed

Spec Kit's specify/plan/tasks commands are agent workflows, not shell commands that
call an LLM. The coding agent read and executed the installed command instructions:

1. `speckit-constitution`: resolved constitution-template with the shipped
   `resolve-template.ps1`, then authored project constitution 1.0.0.
2. `speckit-specify`: resolved spec-template through the shipped resolver, wrote its
   initial contents to `specs/001-trip-status/spec.md`, persisted
   `.specify/feature.json`, then filled the specification and built-in quality
   checklist. Result: 16 checked, 0 unchecked.
3. `speckit-plan`: executed shipped `setup-plan.ps1 -Json` and populated the plan,
   research, data model, UI/state contract and quickstart. Bounded research used
   official MDN/W3C material; project assumptions remained explicitly unconfirmed.
4. `speckit-tasks`: executed shipped `setup-tasks.ps1 -Json`, used its resolved task
   template and generated 20 dependency-ordered tasks across four user stories.
5. `speckit-implement`: executed shipped
   `check-prerequisites.ps1 -Json -RequireTasks -IncludeTasks`, checked the existing
   requirements checklist without modifying its markers in the implementation
   phase, then implemented the planned source and tests.

No `.specify/extensions.yml` existed, so there were no registered pre/post hooks.
No optional analyze/converge command is claimed as executed. Engineering checks are
listed separately in `engineering-verification.md`.

## Reproduction environment

Application commands require Node 22+; this host used Node 24.22.1 at:

```text
C:/Program Files/WindowsApps/OpenAI.CodexPrimaryRuntime.v26-1105-1297-0_26.1105.1297.0_x64__3k8sg7r9htsxt/dependencies/node/bin/node.exe
```

The host's default PATH points to Node 14, so invoke the bundled path or install/use
a modern Node when reproducing. App build/test has zero npm dependencies. The public
build contains five application assets; it does not include original transcripts,
assignment PDF, source goal models or Spec Kit authoring material.

GitHub private repository was created through the user's existing browser login,
and existing Git authentication was confirmed by a successful private `ls-remote`.
No new GitHub token or account credential was created or written into the project.

V1 release/deployment facts are recorded in `release-v1.md`. Later V2 work must start
from this preserved version and follow actual student-led V1 evaluation findings.
