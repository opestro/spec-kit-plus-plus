---
description: Fast-path command to specify, plan, break into tasks, and implement a small feature in a single workflow — no manual handoffs needed.
handoffs:
  - label: Verify Implementation
    agent: speckit.verify
    prompt: Verify the implementation produced by quick mode
    send: true
scripts:
  sh: scripts/bash/create-new-feature.sh "{ARGS}"
  ps: scripts/powershell/create-new-feature.ps1 "{ARGS}"
agent_scripts:
  sh: scripts/bash/update-agent-context.sh __AGENT__
  ps: scripts/powershell/update-agent-context.ps1 -AgentType __AGENT__
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

---

## ⚡ Quick Mode — Full Pipeline in One Command

This command runs the **entire spec-driven workflow** in sequence without requiring manual handoffs between `/speckit.specify`, `/speckit.plan`, `/speckit.tasks`, and `/speckit.implement`. It is designed for **small, well-understood features** that don't need deep upfront clarification.

> **Note**: For complex features with many unknowns, prefer the individual commands so you can review artifacts at each stage.

---

## Outline

### Step 1 — Feature Setup

1. Run `{SCRIPT}` from the repo root to create the feature branch and directory.
2. Read the user's input as the feature description.
3. Read `.specify/memory/constitution.md` if it exists — enforce all architectural rules throughout.
4. Update agent context by running `{AGENT_SCRIPT}`.

### Step 2 — Quick Specification

Write a concise `spec.md` for the feature. Keep it tight — this is quick mode:

- **What**: A 1–2 sentence summary of what we are building.
- **Why**: The user-facing benefit or business reason.
- **Acceptance Criteria**: A bullet list of 3–7 clear, testable outcomes.
- **Out of Scope**: Explicitly list anything that is NOT part of this quick task.

> Do NOT ask clarifying questions unless a fundamental ambiguity would block implementation entirely. Make a reasonable assumption and note it in the spec.

### Step 3 — Lightweight Technical Plan

Write a compact `plan.md` directly (skip full research phase for quick tasks):

- **Tech Stack**: Infer from existing project files (package.json, pyproject.toml, go.mod, etc.) — do not ask.
- **Files to Create/Modify**: List every file that will be touched with a one-line purpose.
- **Key Decisions**: Note any important choices made (e.g. "Using existing auth middleware").
- **Constitution Check**: Confirm no constitution rules are violated. If any would be violated, stop and report to the user before continuing.

### Step 4 — Task Breakdown

Write `tasks.md` with a minimal, flat task list. Use this format:

```text
# Tasks — [Feature Name]

## Phase 1: Implementation
- [ ] [T01] Description of task 1 — `path/to/file.ext`
- [ ] [T02] Description of task 2 — `path/to/file.ext`
...

## Phase 2: Validation
- [ ] [T0N] Run existing tests to confirm no regressions
```

Rules:
- Keep tasks atomic (one file change per task where possible).
- Mark parallel-safe tasks with `[P]` after the ID.
- Only add a tests phase if the project has an existing test suite.

### Step 5 — Implementation

Execute each task in `tasks.md` sequentially:

1. For each `- [ ] [T##]` task:
   - Implement the change.
   - Mark as `- [x] [T##]` when complete.
   - Report progress briefly.
2. Follow the project's existing code style, file structure, and naming conventions.
3. Do NOT add new dependencies unless strictly required. If you must, note it clearly.
4. Do NOT refactor unrelated code. Stay focused on the feature scope.

### Step 6 — Completion Report

After all tasks are complete, output a short summary:

```
✅ Quick Feature Complete: [Feature Name]

Branch:        [branch name]
Spec:          [path to spec.md]
Plan:          [path to plan.md]
Tasks:         [N/N completed]

Files Changed:
  • path/to/file1.ext — what was done
  • path/to/file2.ext — what was done

Next step: Run /speckit.verify to validate the implementation.
```

---

## Guard Rails

- **Scope creep**: If the feature description implies more than ~2 hours of work, stop and tell the user to use the full pipeline (`/speckit.specify` → `/speckit.plan` → `/speckit.tasks` → `/speckit.implement`).
- **Constitution violations**: Hard stop — do not implement anything that violates the constitution. Report violations to the user.
- **Ambiguity**: Make one reasonable assumption per ambiguity, state it clearly in the spec, and continue. Only ask if there is no safe default.
