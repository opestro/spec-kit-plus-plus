# AGENTS.md

## About Spec Kit and Specify

**GitHub Spec Kit** is a comprehensive toolkit for implementing Spec-Driven Development (SDD) - a methodology that emphasizes creating clear specifications before implementation. The toolkit includes templates, scripts, and workflows that guide development teams through a structured approach to building software.

**Specify CLI** is the command-line interface that bootstraps projects with the Spec Kit framework. It sets up the necessary directory structures, templates, and AI agent integrations to support the Spec-Driven Development workflow.

The toolkit supports multiple AI coding assistants, allowing teams to use their preferred tools while maintaining consistent project structure and development practices.

---

## Adding New Agent Support

This section explains how to add support for new AI agents/assistants to the Specify CLI. Use this guide as a reference when integrating new AI tools into the Spec-Driven Development workflow.

### Overview

Specify supports multiple AI agents by generating agent-specific command files and directory structures when initializing projects. Each agent has its own conventions for:

- **Command file formats** (Markdown, TOML, etc.)
- **Directory structures** (`.claude/commands/`, `.windsurf/workflows/`, etc.)
- **Command invocation patterns** (slash commands, CLI tools, etc.)
- **Argument passing conventions** (`$ARGUMENTS`, `{{args}}`, etc.)

### Current Supported Agents

| Agent                      | Directory              | Format   | CLI Tool        | Description                 |
| -------------------------- | ---------------------- | -------- | --------------- | --------------------------- |
| **Claude Code**            | `.claude/commands/`    | Markdown | `claude`        | Anthropic's Claude Code CLI |
| **Gemini CLI**             | `.gemini/commands/`    | TOML     | `gemini`        | Google's Gemini CLI         |
| **GitHub Copilot**         | `.github/agents/`      | Markdown | N/A (IDE-based) | GitHub Copilot in VS Code   |
| **Cursor**                 | `.cursor/commands/`    | Markdown | `cursor-agent`  | Cursor CLI                  |
| **Qwen Code**              | `.qwen/commands/`      | Markdown | `qwen`          | Alibaba's Qwen Code CLI     |
| **opencode**               | `.opencode/command/`   | Markdown | `opencode`      | opencode CLI                |
| **Codex CLI**              | `.agents/skills/`      | Markdown | `codex`         | Codex CLI (skills)          |
| **Windsurf**               | `.windsurf/workflows/` | Markdown | N/A (IDE-based) | Windsurf IDE workflows      |
| **Junie**                  | `.junie/commands/`     | Markdown | `junie`         | Junie by JetBrains          |
| **Kilo Code**              | `.kilocode/workflows/` | Markdown | N/A (IDE-based) | Kilo Code IDE               |
| **Auggie CLI**             | `.augment/commands/`   | Markdown | `auggie`        | Auggie CLI                  |
| **Roo Code**               | `.roo/commands/`       | Markdown | N/A (IDE-based) | Roo Code IDE                |
| **CodeBuddy CLI**          | `.codebuddy/commands/` | Markdown | `codebuddy`     | CodeBuddy CLI               |
| **Qoder CLI**              | `.qoder/commands/`     | Markdown | `qodercli`      | Qoder CLI                   |
| **Kiro CLI**               | `.kiro/prompts/`       | Markdown | `kiro-cli`      | Kiro CLI                    |
| **Amp**                    | `.agents/commands/`    | Markdown | `amp`           | Amp CLI                     |
| **SHAI**                   | `.shai/commands/`      | Markdown | `shai`          | SHAI CLI                    |
| **Tabnine CLI**            | `.tabnine/agent/commands/` | TOML | `tabnine`       | Tabnine CLI                 |
| **Kimi Code**              | `.kimi/skills/`        | Markdown | `kimi`          | Kimi Code CLI (Moonshot AI) |
| **Pi Coding Agent**        | `.pi/prompts/`         | Markdown | `pi`            | Pi terminal coding agent    |
| **iFlow CLI**              | `.iflow/commands/`     | Markdown | `iflow`         | iFlow CLI (iflow-ai)        |
| **IBM Bob**                | `.bob/commands/`       | Markdown | N/A (IDE-based) | IBM Bob IDE                 |
| **Trae**                   | `.trae/rules/`         | Markdown | N/A (IDE-based) | Trae IDE                    |
| **Generic**                | User-specified via `--ai-commands-dir` | Markdown | N/A | Bring your own agent        |

### Step-by-Step Integration Guide

Follow these steps to add a new agent (using a hypothetical new agent as an example):

#### 1. Add to AGENT_CONFIG

**IMPORTANT**: Use the actual CLI tool name as the key, not a shortened version.

Add the new agent to the `AGENT_CONFIG` dictionary in `src/specify_cli/__init__.py`. This is the **single source of truth** for all agent metadata:

```python
AGENT_CONFIG = {
    # ... existing agents ...
    "new-agent-cli": {  # Use the ACTUAL CLI tool name (what users type in terminal)
        "name": "New Agent Display Name",
        "folder": ".newagent/",  # Directory for agent files
        "commands_subdir": "commands",  # Subdirectory name for command files (default: "commands")
        "install_url": "https://example.com/install",  # URL for installation docs (or None if IDE-based)
        "requires_cli": True,  # True if CLI tool required, False for IDE-based agents
    },
}
```

**Key Design Principle**: The dictionary key should match the actual executable name that users install. For example:

- ✅ Use `"cursor-agent"` because the CLI tool is literally called `cursor-agent`
- ❌ Don't use `"cursor"` as a shortcut if the tool is `cursor-agent`

This eliminates the need for special-case mappings throughout the codebase.

**Field Explanations**:

- `name`: Human-readable display name shown to users
- `folder`: Directory where agent-specific files are stored (relative to project root)
- `commands_subdir`: Subdirectory name within the agent folder where command/prompt files are stored (default: `"commands"`)
  - Most agents use `"commands"` (e.g., `.claude/commands/`)
  - Some agents use alternative names: `"agents"` (copilot), `"workflows"` (windsurf, kilocode), `"prompts"` (codex, kiro-cli, pi), `"command"` (opencode - singular)
  - This field enables `--ai-skills` to locate command templates correctly for skill generation
- `install_url`: Installation documentation URL (set to `None` for IDE-based agents)
- `requires_cli`: Whether the agent requires a CLI tool check during initialization

#### 2. Update CLI Help Text

Update the `--ai` parameter help text in the `init()` command to include the new agent:

```python
ai_assistant: str = typer.Option(None, "--ai", help="AI assistant to use: claude, gemini, copilot, cursor-agent, qwen, opencode, codex, windsurf, kilocode, auggie, codebuddy, new-agent-cli, or kiro-cli"),
```

Also update any function docstrings, examples, and error messages that list available agents.

#### 3. Update README Documentation

Update the **Supported AI Agents** section in `README.md` to include the new agent:

- Add the new agent to the table with appropriate support level (Full/Partial)
- Include the agent's official website link
- Add any relevant notes about the agent's implementation
- Ensure the table formatting remains aligned and consistent

#### 4. Update Release Package Script

Modify `.github/workflows/scripts/create-release-packages.sh`:

##### Add to ALL_AGENTS array

```bash
ALL_AGENTS=(claude gemini copilot cursor-agent qwen opencode windsurf kiro-cli)
```

##### Add case statement for directory structure

```bash
case $agent in
  # ... existing cases ...
  windsurf)
    mkdir -p "$base_dir/.windsurf/workflows"
    generate_commands windsurf md "\$ARGUMENTS" "$base_dir/.windsurf/workflows" "$script" ;;
esac
```

#### 4. Update GitHub Release Script

Modify `.github/workflows/scripts/create-github-release.sh` to include the new agent's packages:

```bash
gh release create "$VERSION" \
  # ... existing packages ...
  .genreleases/spec-kit-template-windsurf-sh-"$VERSION".zip \
  .genreleases/spec-kit-template-windsurf-ps-"$VERSION".zip \
  # Add new agent packages here
```

#### 5. Update Agent Context Scripts

##### Bash script (`scripts/bash/update-agent-context.sh`)

Add file variable:

```bash
WINDSURF_FILE="$REPO_ROOT/.windsurf/rules/specify-rules.md"
```

Add to case statement:

```bash
case "$AGENT_TYPE" in
  # ... existing cases ...
  windsurf) update_agent_file "$WINDSURF_FILE" "Windsurf" ;;
  "")
    # ... existing checks ...
    [ -f "$WINDSURF_FILE" ] && update_agent_file "$WINDSURF_FILE" "Windsurf";
    # Update default creation condition
    ;;
esac
```

##### PowerShell script (`scripts/powershell/update-agent-context.ps1`)

Add file variable:

```powershell
$windsurfFile = Join-Path $repoRoot '.windsurf/rules/specify-rules.md'
```

Add to switch statement:

```powershell
switch ($AgentType) {
    # ... existing cases ...
    'windsurf' { Update-AgentFile $windsurfFile 'Windsurf' }
    '' {
        foreach ($pair in @(
            # ... existing pairs ...
            @{file=$windsurfFile; name='Windsurf'}
        )) {
            if (Test-Path $pair.file) { Update-AgentFile $pair.file $pair.name }
        }
        # Update default creation condition
    }
}
```

#### 6. Update CLI Tool Checks (Optional)

For agents that require CLI tools, add checks in the `check()` command and agent validation:

```python
# In check() command
tracker.add("windsurf", "Windsurf IDE (optional)")
windsurf_ok = check_tool_for_tracker("windsurf", "https://windsurf.com/", tracker)

# In init validation (only if CLI tool required)
elif selected_ai == "windsurf":
    if not check_tool("windsurf", "Install from: https://windsurf.com/"):
        console.print("[red]Error:[/red] Windsurf CLI is required for Windsurf projects")
        agent_tool_missing = True
```

**Note**: CLI tool checks are now handled automatically based on the `requires_cli` field in AGENT_CONFIG. No additional code changes needed in the `check()` or `init()` commands - they automatically loop through AGENT_CONFIG and check tools as needed.

## Important Design Decisions

### Using Actual CLI Tool Names as Keys

**CRITICAL**: When adding a new agent to AGENT_CONFIG, always use the **actual executable name** as the dictionary key, not a shortened or convenient version.

**Why this matters:**

- The `check_tool()` function uses `shutil.which(tool)` to find executables in the system PATH
- If the key doesn't match the actual CLI tool name, you'll need special-case mappings throughout the codebase
- This creates unnecessary complexity and maintenance burden

**Example - The Cursor Lesson:**

❌ **Wrong approach** (requires special-case mapping):

```python
AGENT_CONFIG = {
    "cursor": {  # Shorthand that doesn't match the actual tool
        "name": "Cursor",
        # ...
    }
}

# Then you need special cases everywhere:
cli_tool = agent_key
if agent_key == "cursor":
    cli_tool = "cursor-agent"  # Map to the real tool name
```

✅ **Correct approach** (no mapping needed):

```python
AGENT_CONFIG = {
    "cursor-agent": {  # Matches the actual executable name
        "name": "Cursor",
        # ...
    }
}

# No special cases needed - just use agent_key directly!
```

**Benefits of this approach:**

- Eliminates special-case logic scattered throughout the codebase
- Makes the code more maintainable and easier to understand
- Reduces the chance of bugs when adding new agents
- Tool checking "just works" without additional mappings

#### 7. Update Devcontainer files (Optional)

For agents that have VS Code extensions or require CLI installation, update the devcontainer configuration files:

##### VS Code Extension-based Agents

For agents available as VS Code extensions, add them to `.devcontainer/devcontainer.json`:

```json
{
  "customizations": {
    "vscode": {
      "extensions": [
        // ... existing extensions ...
        // [New Agent Name]
        "[New Agent Extension ID]"
      ]
    }
  }
}
```

##### CLI-based Agents

For agents that require CLI tools, add installation commands to `.devcontainer/post-create.sh`:

```bash
#!/bin/bash

# Existing installations...

echo -e "\n🤖 Installing [New Agent Name] CLI..."
# run_command "npm install -g [agent-cli-package]@latest" # Example for node-based CLI
# or other installation instructions (must be non-interactive and compatible with Linux Debian "Trixie" or later)...
echo "✅ Done"

```

**Quick Tips:**

- **Extension-based agents**: Add to the `extensions` array in `devcontainer.json`
- **CLI-based agents**: Add installation scripts to `post-create.sh`
- **Hybrid agents**: May require both extension and CLI installation
- **Test thoroughly**: Ensure installations work in the devcontainer environment

## Agent Categories

### CLI-Based Agents

Require a command-line tool to be installed:

- **Claude Code**: `claude` CLI
- **Gemini CLI**: `gemini` CLI
- **Cursor**: `cursor-agent` CLI
- **Qwen Code**: `qwen` CLI
- **opencode**: `opencode` CLI
- **Junie**: `junie` CLI
- **Kiro CLI**: `kiro-cli` CLI
- **CodeBuddy CLI**: `codebuddy` CLI
- **Qoder CLI**: `qodercli` CLI
- **Amp**: `amp` CLI
- **SHAI**: `shai` CLI
- **Tabnine CLI**: `tabnine` CLI
- **Kimi Code**: `kimi` CLI
- **Pi Coding Agent**: `pi` CLI

### IDE-Based Agents

Work within integrated development environments:

- **GitHub Copilot**: Built into VS Code/compatible editors
- **Windsurf**: Built into Windsurf IDE
- **IBM Bob**: Built into IBM Bob IDE

## Command File Formats

### Markdown Format

Used by: Claude, Cursor, opencode, Windsurf, Junie, Kiro CLI, Amp, SHAI, IBM Bob, Kimi Code, Qwen, Pi

**Standard format:**

```markdown
---
description: "Command description"
---

Command content with {SCRIPT} and $ARGUMENTS placeholders.
```

**GitHub Copilot Chat Mode format:**

```markdown
---
description: "Command description"
mode: speckit.command-name
---

Command content with {SCRIPT} and $ARGUMENTS placeholders.
```

### TOML Format

Used by: Gemini, Tabnine

```toml
description = "Command description"

prompt = """
Command content with {SCRIPT} and {{args}} placeholders.
"""
```

## Directory Conventions

- **CLI agents**: Usually `.<agent-name>/commands/`
- **Skills-based exceptions**:
  - Codex: `.agents/skills/` (skills, invoked as `$speckit-<command>`)
- **Prompt-based exceptions**:
  - Kiro CLI: `.kiro/prompts/`
  - Pi: `.pi/prompts/`
- **IDE agents**: Follow IDE-specific patterns:
  - Copilot: `.github/agents/`
  - Cursor: `.cursor/commands/`
  - Windsurf: `.windsurf/workflows/`

## Argument Patterns

Different agents use different argument placeholders:

- **Markdown/prompt-based**: `$ARGUMENTS`
- **TOML-based**: `{{args}}`
- **Script placeholders**: `{SCRIPT}` (replaced with actual script path)
- **Agent placeholders**: `__AGENT__` (replaced with agent name)

## Testing New Agent Integration

1. **Build test**: Run package creation script locally
2. **CLI test**: Test `specify init --ai <agent>` command
3. **File generation**: Verify correct directory structure and files
4. **Command validation**: Ensure generated commands work with the agent
5. **Context update**: Test agent context update scripts

## Common Pitfalls

1. **Using shorthand keys instead of actual CLI tool names**: Always use the actual executable name as the AGENT_CONFIG key (e.g., `"cursor-agent"` not `"cursor"`). This prevents the need for special-case mappings throughout the codebase.
2. **Forgetting update scripts**: Both bash and PowerShell scripts must be updated when adding new agents.
3. **Incorrect `requires_cli` value**: Set to `True` only for agents that actually have CLI tools to check; set to `False` for IDE-based agents.
4. **Wrong argument format**: Use correct placeholder format for each agent type (`$ARGUMENTS` for Markdown, `{{args}}` for TOML).
5. **Directory naming**: Follow agent-specific conventions exactly (check existing agents for patterns).
6. **Help text inconsistency**: Update all user-facing text consistently (help strings, docstrings, README, error messages).

## Future Considerations

When adding new agents:

- Consider the agent's native command/workflow patterns
- Ensure compatibility with the Spec-Driven Development process
- Document any special requirements or limitations
- Update this guide with lessons learned
- Verify the actual CLI tool name before adding to AGENT_CONFIG

---

*This documentation should be updated whenever new agents are added to maintain accuracy and completeness.*

<!-- spec-kit:framework-rules:start -->

# Vue.js Framework Rules

> These rules are automatically injected by Spec Kit based on your selected frameworks.
> Source: [vue-rulekit](https://github.com/posva/vue-rulekit) by Eduardo San Martín Morote.

## Standards

MUST FOLLOW THESE RULES, NO EXCEPTIONS

- **Stack**: Vue 3, TypeScript, TailwindCSS v4, Vue Router, Pinia, Pinia Colada
- **Patterns**: ALWAYS use Composition API + `<script setup>`, NEVER use Options API
- ALWAYS keep types alongside your code; prefer `interface` over `type` for defining types
- Keep unit and integration tests alongside the file they test: `src/ui/Button.vue` + `src/ui/Button.spec.ts`
- ALWAYS use TailwindCSS classes rather than manual CSS
- DO NOT hard code colors — use Tailwind's color system
- ONLY add meaningful comments that explain **why** something is done, not **what** it does
- Dev server is already running on `http://localhost:5173` with HMR enabled. NEVER launch it yourself
- ALWAYS use named functions when declaring methods; use arrow functions only for callbacks
- ALWAYS prefer named exports over default exports

## Project Structure

```
public/           # Public static files (favicon, robots.txt, static images)
src/
├── api/          # MUST export individual functions that fetch data
├── components/   # Reusable Vue components
│   ├── ui/       # Base UI components (buttons, inputs, etc.)
│   ├── layout/   # Layout components (header, footer, sidebar)
│   └── features/ # Feature-specific components grouped by domain
├── composables/  # Composition functions
├── stores/       # Pinia stores for global state (NOT data fetching)
├── queries/      # Pinia Colada queries for data fetching
├── pages/        # Page components (Vue Router + Unplugin Vue Router)
│   ├── (home).vue       # index page using a route group
│   ├── users.vue        # renders at /users
│   └── users.[userId].vue  # renders at /users/:userId
├── plugins/      # Vue plugins
├── utils/        # Global utility pure functions
├── assets/       # Static assets processed by Vite (CSS, fonts, etc.)
├── main.ts       # Entry point — add/configure plugins, mount app
├── App.vue       # Root Vue component
└── router/
    └── index.ts  # Router setup
```

**Handling Existing Structures**: If the project already has an established structure that differs from the best practices above, you MUST ask the user whether to keep their existing structure or migrate to the best practice one. Do not force the best practice structure without permission.

## UI Design & Project Context

- **Respect Existing UI**: If the project already has its own unique UI design or component library, you MUST follow and respect those UI design elements.
- **Starting from Scratch**: If no UI design exists, ALWAYS ask the user before building components: "Do you want to use pre-made elements (e.g., shadcn-vue) or build custom components based on TailwindCSS?". If they choose a pre-made UI library, **install its agent skill** using `npx skills find <library-name>` and `npx skills add ...` to learn the exact component implementation rules before you start generating code. (Suggest using `/speckit.ui` if applicable to build a UI kit).
- **New Project Context**: If the project is new and lacks high-level context, ask:
  - What are you building? (dashboard, landing page, SaaS, mobile app, etc.)
  - What is the main goal of this component?
  - Who is the target user?
  - What are your brand preferences? (colors, border styles, typography) - *Provide visual references when possible.*

**Core Discovery Shift (CRITICAL)**:
Instead of asking 20 detailed questions upfront, use this approach: **"Pick a reference → AI infers 80% → asks only what's missing"**. 
Ask the user for a reference (a URL, an image, or an existing component). Infer the design system (colors, spacing, typography) from that reference, and only ask questions about the missing 20%.

## Vue Component Best Practices

- Name files consistently using PascalCase (`UserProfile.vue`) OR kebab-case (`user-profile.vue`)
- ALWAYS use PascalCase for component names in source code
- Compose names from most general to most specific: `SearchButtonClear.vue` not `ClearSearchButton.vue`
- ALWAYS define props with `defineProps<{ propOne: number }>()` and TypeScript types, WITHOUT `const props =`
- Use `const props =` ONLY if props are used in the script block
- Destructure props to declare default values
- ALWAYS define emits with `const emit = defineEmits<{ eventName: [argOne: type]; otherEvent: [] }>()` for type safety
- ALWAYS use camelCase in JS for props and emits, even if they are kebab-case in templates
- ALWAYS use kebab-case in templates for props and emits
- ALWAYS use the prop shorthand if possible: `<MyComponent :count />` instead of `<MyComponent :count="count" />`
- ALWAYS use the shorthand for slots: `<template #default>` instead of `<template v-slot:default>`
- ALWAYS use `defineModel<type>({ required, get, set, default })` to define v-model bindings

### defineModel() Examples

```vue
<script setup lang="ts">
// Simple two-way binding
const title = defineModel<string>()

// With options and modifiers
const [title, modifiers] = defineModel<string>({
  default: 'default value',
  required: true,
  get: (value) => value.trim(),
  set: (value) => {
    if (modifiers.capitalize) {
      return value.charAt(0).toUpperCase() + value.slice(1)
    }
    return value
  },
})

// Multiple v-model bindings
const firstName = defineModel<string>('firstName')
const age = defineModel<number>('age')
</script>
```

## File-Based Routing (Vue Router / Unplugin Vue Router)

- AVOID files named `index.vue` — use a route group with a meaningful name: `pages/(home).vue`
- ALWAYS use explicit param names: prefer `userId` over `id`, `postSlug` over `slug`
- Use `[[paramName]]` for optional route parameters
- Use `]+` for repeatable params: `/posts.[[slug]]+.vue`
- Use `[...path]` to match anything including slashes
- Use `definePage()` inside page components to customize `meta`, `name`, `path`, `alias`
- ALWAYS refer to `typed-router.d.ts` for route names and parameters
- Prefer named route locations: `router.push({ name: '/users/[userId]', params: { userId } })`

## Development Workflow

1. Plan tasks, review with user. Include tests when possible
2. Write code following the project structure and standards above
3. **ALWAYS test implementations work**:
   - Write unit and integration tests for logic and components
   - Use the agent-browser to test like a real user
4. Stage changes with `git add` once a feature works
5. Review and analyze the need for refactoring

## Testing Workflow

- Test critical logic first; split code if needed to make it testable
- **Browser Testing**: Navigate → Wait for load → Test primary interactions → Test edge cases → Check JS console for errors → Fix immediately

## Project Commands

- `pnpm run build` — bundle for production
- `pnpm run test` — run all tests
- `pnpm vitest run <test-files>` — run specific test files (add `--coverage` for coverage)

## Research & Documentation

- **NEVER hallucinate or guess URLs**
- ALWAYS try accessing the `llms.txt` file first: e.g. `https://pinia-colada.esm.dev/llms.txt`
- ALWAYS follow existing links in documentation indices
- Verify examples and patterns from documentation before using

<!-- spec-kit:framework-rules:end -->
