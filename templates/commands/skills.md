---
description: Find and install agent skills for the current project. Skills extend your AI agent with domain-specific best practices for frameworks, tools, and workflows.
---

## User Input

```text
$ARGUMENTS
```

Use the arguments as a search query. If no arguments provided, enter interactive discovery mode.

## Skill Manager

Add reusable agent skills to this project so that every subsequent Spec Kit command automatically benefits from those best practices.

### Step 1 — Discover Available Skills

Run the search in the terminal:

```bash
# If the user provided a search term, use it
npx skills find $ARGUMENTS

# If no arguments, list interactively
npx skills find
```

Read the output and present the user with a numbered list of matched skills, showing:
- Skill name
- Short description
- Source repository

### Step 2 — Confirm Selection

Ask the user:
> "Which skill(s) would you like to install? Enter number(s) from the list above, or type a name directly."

### Step 3 — Install Selected Skill(s)

For each skill chosen, run the install command. Use the correct source from the search results:

```bash
# Install from a GitHub repo
npx skills add <owner/repo> --skill <skill-name>

# Install all skills from a repo
npx skills add <owner/repo> --all

# Add --yes to skip confirmation prompts
npx skills add <owner/repo> --skill <skill-name> --yes
```

**Important installation notes:**
- Default scope is **project** (committed with your team). Pass `-g` only if the user explicitly wants a global (user-wide) installation.
- If the target agent isn't auto-detected, add `-a <agent>` matching the current project's AI agent.
- After install, report the path where the `SKILL.md` was written.

### Step 4 — Read and Apply Skill

After installation, **immediately** read the installed `SKILL.md` content to incorporate the new rules into this session:

```bash
cat ./<agent-dir>/skills/<skill-name>/SKILL.md
```

Then confirm to the user:
> "✓ Skill **[name]** installed. I've loaded its rules and will follow them for the rest of this session and all future Spec Kit commands."

### Step 5 — Report

Output a summary:
- Skill(s) installed and their install path(s)
- Key rules or best practices the skill adds
- How this skill improves upcoming Spec Kit commands (e.g., `/speckit.specify` will now respect Django patterns)
- Tip: skills are committed to the repo so team members benefit automatically
