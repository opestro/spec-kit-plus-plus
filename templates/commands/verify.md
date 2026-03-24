---
description: Verify the implementation — review generated code quality, run tests, and validate endpoints (backend) or UI flows (frontend, if e2e tooling exists).
---

## User Input

```text
$ARGUMENTS
```

Use arguments to target a specific task or feature (e.g., a task ID, feature branch, or file path). If empty, verify the most recently implemented feature.

## Verify Implementation

Run this flow in order after `/speckit.implement`:

---

### Step 1 — Locate the Implementation

1. Check `.specify/` for the most recent tasks file or the feature specified in arguments.
2. Identify the files and modules changed during the last implementation.
3. List the changed paths for the user to confirm scope.

---

### Step 2 — Code Quality Review

For each changed file, perform a static review:

- **Correctness**: Does the code match the spec and plan requirements?
- **Framework rules**: Does it follow the framework rules configured in this project (check agent context file for `## Framework Rules` and `## Standards` sections)?
- **No regressions**: Are existing contracts, interfaces, and APIs preserved?
- **Security**: No hardcoded secrets, no obvious injection vectors, no missing auth checks.
- **Dead code / unused imports**: Flag anything that should be cleaned up.

Report findings as a checklist:
```
✓ Correctness
✓ Framework compliance
⚠ Minor: unused import in src/api/users.ts:3
✓ No regressions
✓ Security
```

---

### Step 3 — Ask About Tests

Ask the user:

> "Should I run the test suite now? Options:
> 1. **Yes** — run existing tests and report results
> 2. **Write + run** — write missing unit tests then run them
> 3. **Skip** — skip automated tests for now"

Handle each choice:

#### Option 1 — Run Existing Tests

Detect and run the project's test runner:

```bash
# Detect runner (check package.json scripts, pyproject.toml, etc.)
pnpm run test       # or: npm test, pytest, cargo test, go test ./...
```

Report: number passed / failed / skipped, and any error messages.

#### Option 2 — Write + Run Tests

For each changed module:
- Write unit tests targeting the new logic (NOT integration/e2e)
- Place test files alongside source files (e.g., `MyComponent.spec.ts` next to `MyComponent.vue`)
- Run the test suite and confirm all pass

---

### Step 4 — Detect Project Type and Run Integration Tests

**Detect the project type** by checking:
- `package.json` scripts for `"dev"`, `"start"`, `"server"` → likely has a backend/API
- Framework files: `server.ts`, `app.py`, `main.go`, `routes/` → backend
- Presence of `openapi.json`, `swagger.yaml` → API with documented endpoints

#### Backend Projects — Test Endpoints

If a running server is detected (check if dev server is up, or start one):

```bash
# Test discovered endpoints — adapt to detected framework
curl -s -o /dev/null -w "%{http_code}" http://localhost:<port>/api/health
```

For each endpoint modified or created in this implementation:
1. Send a realistic test request (GET, POST, etc.) with valid sample data
2. Assert the response status code is as expected (200, 201, etc.)
3. Validate the response shape matches the spec's API contract
4. Test at least one error case (e.g., missing required field → 422)

Report results in a table:
```
Endpoint                  Method  Status  Result
/api/users                GET     200     ✓
/api/users                POST    201     ✓
/api/users (missing name) POST    422     ✓
```

#### Frontend Projects — Skip by Default

Do NOT run e2e or browser tests unless:
- The user explicitly requested them (check arguments), OR
- An e2e tool is detected in the project (`playwright`, `cypress`, `vitest/browser`, `puppeteer`)

If an e2e tool is detected, ask:
> "I found **[tool]** in this project. Do you want me to run e2e tests for the affected UI flows?"

Only run e2e if the user confirms.

---

### Step 5 — Final Report

Output a summary panel:

```
╭─ Verification Summary ─────────────────────────────────╮
│                                                        │
│  Code Review      ✓ (1 warning — see above)            │
│  Unit Tests       ✓ 34 passed, 0 failed                │
│  Endpoints        ✓ 3/3 passed                         │
│  E2E Tests        — skipped (not requested)            │
│                                                        │
│  Status: READY ✓  (or: ISSUES FOUND ⚠)                │
│                                                        │
╰────────────────────────────────────────────────────────╯
```

If any step fails, stop and fix issues before marking the feature complete.

If all steps pass:
> "✓ Implementation verified. You can now merge this feature or continue with the next task via `/speckit.tasks`."
