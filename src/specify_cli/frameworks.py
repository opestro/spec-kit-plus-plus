"""
Framework Registry for Spec Kit

Manages framework-specific rules injection into AI agent context files.
Supports multi-framework selection (e.g. Vue frontend + FastAPI backend).

Usage:
    from specify_cli.frameworks import (
        FRAMEWORK_REGISTRY,
        select_frameworks_interactive,
        inject_framework_rules,
        install_framework_skills,
        get_available_frameworks,
    )
"""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import List, Optional

# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

FRAMEWORK_REGISTRY: dict[str, dict] = {
    "vue": {
        "name": "Vue.js",
        "description": "Vue 3 + TypeScript + TailwindCSS v4 + Pinia + Vue Router",
        "type": "frontend",
        "rules_file": "vue/rules.md",
        "skills": ["vue/skills/pages"],
    },
    # Coming-soon stubs (no rules_file yet — skipped gracefully at runtime)
    "nuxt": {
        "name": "Nuxt",
        "description": "Nuxt 3 full-stack framework built on Vue 3",
        "type": "frontend",
        "rules_file": "nuxt/rules.md",
        "skills": [],
        "status": "coming-soon",
    },
    "react": {
        "name": "React",
        "description": "React + TypeScript + TailwindCSS best practices",
        "type": "frontend",
        "rules_file": "react/rules.md",
        "skills": [],
        "status": "coming-soon",
    },
    "fastapi": {
        "name": "FastAPI",
        "description": "Python FastAPI backend best practices",
        "type": "backend",
        "rules_file": "fastapi/rules.md",
        "skills": [],
        "status": "coming-soon",
    },
    "express": {
        "name": "Express / Node.js",
        "description": "Node.js + Express or Fastify backend best practices",
        "type": "backend",
        "rules_file": "express/rules.md",
        "skills": [],
        "status": "coming-soon",
    },
    "django": {
        "name": "Django",
        "description": "Python Django backend best practices",
        "type": "backend",
        "rules_file": "django/rules.md",
        "skills": [],
        "status": "coming-soon",
    },
}

# Marker used to delimit the injected block inside agent context files.
FRAMEWORK_SECTION_START = "<!-- spec-kit:framework-rules:start -->"
FRAMEWORK_SECTION_END = "<!-- spec-kit:framework-rules:end -->"

# ---------------------------------------------------------------------------
# Availability helpers
# ---------------------------------------------------------------------------


def get_available_frameworks(frameworks_dir: Path) -> list[str]:
    """Return framework IDs that have a resolved rules_file on disk."""
    available = []
    for fid, meta in FRAMEWORK_REGISTRY.items():
        if meta.get("status") == "coming-soon":
            continue
        rules_path = frameworks_dir / meta["rules_file"]
        if rules_path.exists():
            available.append(fid)
    return available


def _locate_frameworks_dir() -> Optional[Path]:
    """Locate the bundled frameworks/ directory (wheel or source checkout)."""
    # 1. Next to this file inside a wheel: specify_cli/core_pack/frameworks/
    pkg_dir = Path(__file__).parent
    wheel_path = pkg_dir / "core_pack" / "frameworks"
    if wheel_path.is_dir():
        return wheel_path

    # 2. Source-checkout: repo_root/frameworks/
    repo_root = pkg_dir.parent.parent
    src_path = repo_root / "frameworks"
    if src_path.is_dir():
        return src_path

    return None


# ---------------------------------------------------------------------------
# Rules loading
# ---------------------------------------------------------------------------


def get_framework_rules(framework_id: str, frameworks_dir: Optional[Path] = None) -> str:
    """Return the rules.md content for a framework.

    Args:
        framework_id: Key from FRAMEWORK_REGISTRY (e.g. 'vue')
        frameworks_dir: Override path to the frameworks/ directory.
                        Auto-detected when None.

    Returns:
        Rules content as a string, or empty string if not found.
    """
    if frameworks_dir is None:
        frameworks_dir = _locate_frameworks_dir()
    if frameworks_dir is None:
        return ""

    meta = FRAMEWORK_REGISTRY.get(framework_id)
    if not meta:
        return ""

    rules_path = frameworks_dir / meta["rules_file"]
    if not rules_path.exists():
        return ""

    return rules_path.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# Injection into agent context files
# ---------------------------------------------------------------------------


def inject_framework_rules(
    agent_rules_file: Path,
    framework_ids: List[str],
    frameworks_dir: Optional[Path] = None,
) -> bool:
    """Append (or replace) a framework-rules block in the agent context file.

    The block is delimited by HTML comments so it can be updated idempotently
    without duplicating content:

        <!-- spec-kit:framework-rules:start -->
        ...
        <!-- spec-kit:framework-rules:end -->

    Args:
        agent_rules_file: Path to the AGENTS.md / CLAUDE.md / etc. file.
        framework_ids: List of framework IDs to inject rules for.
        frameworks_dir: Override path to frameworks/ directory.

    Returns:
        True if at least one framework's rules were injected.
    """
    if not framework_ids:
        return False

    if frameworks_dir is None:
        frameworks_dir = _locate_frameworks_dir()

    sections: list[str] = []
    for fid in framework_ids:
        rules = get_framework_rules(fid, frameworks_dir)
        if rules.strip():
            sections.append(rules.strip())

    if not sections:
        return False

    combined = "\n\n---\n\n".join(sections)
    block = f"{FRAMEWORK_SECTION_START}\n\n{combined}\n\n{FRAMEWORK_SECTION_END}"

    if agent_rules_file.exists():
        existing = agent_rules_file.read_text(encoding="utf-8")
        # Replace existing block if present
        if FRAMEWORK_SECTION_START in existing:
            start = existing.index(FRAMEWORK_SECTION_START)
            end = existing.index(FRAMEWORK_SECTION_END) + len(FRAMEWORK_SECTION_END)
            updated = existing[:start] + block + existing[end:]
        else:
            # Append with a separator
            updated = existing.rstrip("\n") + "\n\n" + block + "\n"
    else:
        # Create the file with just the block
        agent_rules_file.parent.mkdir(parents=True, exist_ok=True)
        updated = block + "\n"

    agent_rules_file.write_text(updated, encoding="utf-8")
    return True


def remove_framework_rules(agent_rules_file: Path) -> bool:
    """Remove the injected framework-rules block from an agent context file.

    Returns True if a block was found and removed.
    """
    if not agent_rules_file.exists():
        return False

    existing = agent_rules_file.read_text(encoding="utf-8")
    if FRAMEWORK_SECTION_START not in existing:
        return False

    start = existing.index(FRAMEWORK_SECTION_START)
    end = existing.index(FRAMEWORK_SECTION_END) + len(FRAMEWORK_SECTION_END)
    # Remove the block and any leading blank lines before it
    updated = existing[:start].rstrip("\n") + "\n" + existing[end:].lstrip("\n")
    agent_rules_file.write_text(updated, encoding="utf-8")
    return True


# ---------------------------------------------------------------------------
# Skill installation
# ---------------------------------------------------------------------------

# Agents that use SKILL.md-based layouts
_SKILL_AGENTS = {
    "codex": "speckit-",   # .agents/skills/speckit-<name>/SKILL.md
    "kimi": "speckit.",    # .kimi/skills/speckit.<name>/SKILL.md
}

# Agent skill directory mapping  (matches AGENT_SKILLS_DIR_OVERRIDES in __init__.py)
_AGENT_SKILLS_DIRS: dict[str, str] = {
    "codex": ".agents/skills",
    "kimi": ".kimi/skills",
    "amp": ".agents/commands",
}


def _get_agent_skills_dir(agent_name: str, project_root: Path) -> Optional[Path]:
    """Return the skills directory for *agent_name*, or None if not a skill agent."""
    if agent_name in _AGENT_SKILLS_DIRS:
        return project_root / _AGENT_SKILLS_DIRS[agent_name]
    return None


def install_framework_skills(
    agent_name: str,
    framework_ids: List[str],
    project_root: Path,
    frameworks_dir: Optional[Path] = None,
) -> list[str]:
    """Copy framework SKILL.md files into the agent skill directory.

    Only installs for agents that support SKILL.md-based layouts (codex, kimi).
    For other agents the framework rules are injected into the context file instead.

    Args:
        agent_name: The agent key from AGENT_CONFIG (e.g. 'codex', 'gemini').
        framework_ids: List of framework IDs to install skills for.
        project_root: Root directory of the target project.
        frameworks_dir: Override path to frameworks/ directory.

    Returns:
        List of installed skill directory names.
    """
    prefix = _SKILL_AGENTS.get(agent_name)
    skills_dir = _get_agent_skills_dir(agent_name, project_root)

    if prefix is None or skills_dir is None:
        # Not a skill-based agent — rules injected into context file instead
        return []

    if frameworks_dir is None:
        frameworks_dir = _locate_frameworks_dir()
    if frameworks_dir is None:
        return []

    installed: list[str] = []

    for fid in framework_ids:
        meta = FRAMEWORK_REGISTRY.get(fid)
        if not meta:
            continue
        for skill_rel in meta.get("skills", []):
            skill_src_dir = frameworks_dir / skill_rel
            skill_md = skill_src_dir / "SKILL.md"
            if not skill_md.exists():
                continue

            # skill_rel is like "vue/skills/pages" — we want the last segment
            skill_name = f"{prefix}fw-{fid}-{Path(skill_rel).name}"
            dest_dir = skills_dir / skill_name
            dest_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(skill_md, dest_dir / "SKILL.md")
            installed.append(skill_name)

    return installed


# ---------------------------------------------------------------------------
# Interactive multi-select (used by specify init)
# ---------------------------------------------------------------------------


def select_frameworks_interactive(available_ids: list[str]) -> list[str]:
    """Display an interactive checkbox-style selector for frameworks.

    Uses readchar for keyboard input. Supports:
        ↑ / ↓   — move cursor
        SPACE   — toggle selection
        ENTER   — confirm
        ESC / q — skip (no frameworks selected)

    Args:
        available_ids: List of selectable framework IDs.

    Returns:
        List of selected framework IDs (may be empty).
    """
    import readchar
    from rich.console import Console
    from rich.live import Live
    from rich.panel import Panel
    from rich.table import Table

    console = Console()

    # Group by type for display
    type_order = ["frontend", "backend"]
    grouped: dict[str, list[str]] = {t: [] for t in type_order}
    for fid in available_ids:
        meta = FRAMEWORK_REGISTRY.get(fid, {})
        ftype = meta.get("type", "frontend")
        grouped.setdefault(ftype, []).append(fid)

    # Flat ordered list for navigation
    ordered: list[str] = []
    for ftype in type_order:
        ordered.extend(grouped.get(ftype, []))

    if not ordered:
        return []

    selected: set[str] = set()
    cursor = 0

    def _make_panel() -> Panel:
        table = Table.grid(padding=(0, 2))
        table.add_column(width=3)   # checkbox
        table.add_column(width=20)  # name
        table.add_column()          # description

        current_type: str | None = None
        for fid in ordered:
            meta = FRAMEWORK_REGISTRY.get(fid, {})
            ftype = meta.get("type", "frontend")
            idx = ordered.index(fid)

            if ftype != current_type:
                current_type = ftype
                table.add_row("", f"[bold dim]{ftype.upper()}[/bold dim]", "")

            checkbox = "[green]●[/green]" if fid in selected else "○"
            name = meta.get("name", fid)
            desc = meta.get("description", "")

            if idx == cursor:
                table.add_row(
                    f"[cyan]▶[/cyan] {checkbox}",
                    f"[cyan bold]{name}[/cyan bold]",
                    f"[dim]{desc}[/dim]",
                )
            else:
                table.add_row(
                    f"  {checkbox}",
                    f"[white]{name}[/white]",
                    f"[bright_black]{desc}[/bright_black]",
                )

        table.add_row("", "", "")
        table.add_row("", "[dim]↑/↓ move  ·  SPACE select  ·  ENTER confirm  ·  ESC skip[/dim]", "")
        return Panel(table, title="[bold]Choose frameworks (optional)[/bold]", border_style="cyan", padding=(1, 2))

    console.print()
    result: list[str] = []

    try:
        with Live(_make_panel(), console=console, transient=True, auto_refresh=False) as live:
            while True:
                key = readchar.readkey()

                if key in (readchar.key.UP, readchar.key.CTRL_P):
                    cursor = (cursor - 1) % len(ordered)
                elif key in (readchar.key.DOWN, readchar.key.CTRL_N):
                    cursor = (cursor + 1) % len(ordered)
                elif key == " ":
                    fid = ordered[cursor]
                    if fid in selected:
                        selected.discard(fid)
                    else:
                        selected.add(fid)
                elif key == readchar.key.ENTER:
                    result = [fid for fid in ordered if fid in selected]
                    break
                elif key in (readchar.key.ESC, "q", readchar.key.CTRL_C):
                    break

                live.update(_make_panel(), refresh=True)
    except KeyboardInterrupt:
        pass

    return result
