---
description: Build or audit the UI component kit for this project — discover the design system and scaffold base components.
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## UI Kit Builder

Build or refine the project's UI component library by following this exact flow:

### Step 1 — Discover Existing UI

Before doing anything, scan the project for existing UI context:

1. Check `src/components/ui/` (or `components/ui/`) for existing base components.
2. Check for a UI library declaration in `package.json` (shadcn, radix-vue, headlessui, etc.).
3. Check `tailwind.config.*` for a configured design token system (colors, fonts, spacing).
4. Check `src/assets/` or `index.css` for CSS custom properties (design tokens).

**If existing UI found**: Respect it — extend without breaking existing patterns. Skip to Step 3.
**If no UI found**: Continue to Step 2.

---

### Step 2 — Context Discovery (New Projects Only)

**Core principle: "Pick a reference → AI infers 80% → asks only about the missing 20%."**

Ask the user ONE focused question first:

> "Share a reference — a URL, screenshot, or existing design you like — and I'll infer the design system from it. Or tell me what you're building and I'll suggest styles."

Once you have a reference (or they describe the project), infer:
- **Color palette**: Primary, accent, neutral, success/error
- **Typography**: Font family, scale, weights
- **Border style**: Rounded vs sharp, border width
- **Spacing system**: Tight, balanced, or spacious
- **Vibe/aesthetic**: Minimal, glassmorphic, bold, corporate, playful

Then ask ONLY about what you couldn't infer. Maximum 3 follow-up questions, covering:
1. Target platform (web, mobile web, desktop-focused)?
2. Pre-made library (shadcn-vue, PrimeVue, Headless UI) or pure TailwindCSS custom?
3. Any brand constraint (must match existing brand colors or logo)?

**If they choose a pre-made library**: Run `npx skills find <library>` to find its agent skill, install it with `npx skills add ...`, and read the installed `SKILL.md` before generating any components.

---

### Step 3 — Scaffold / Audit Components

Based on what was discovered or defined, scaffold or audit these base components:

#### Tier 1 — Always Required
- `Button.vue` (variants: primary, secondary, ghost, destructive; sizes: sm, md, lg)
- `Input.vue` (with label, helper text, error state)
- `Badge.vue` (variants: default, success, warning, error)
- `Card.vue` (with header, body, footer slots)

#### Tier 2 — Include When Relevant
- `Modal.vue` / `Dialog.vue`
- `Dropdown.vue` / `Select.vue`
- `Toast.vue` / `Alert.vue`
- `Skeleton.vue` (loading state)
- `Avatar.vue`

For each component:
1. Implement using established design tokens (CSS vars or Tailwind config values, never hardcoded colors)
2. Write a `*.spec.ts` test alongside it
3. Export from `src/components/ui/index.ts`

---

### Step 4 — Document Design Tokens

Create or update `src/assets/design-tokens.css` (or equivalent) documenting the full token system:

```css
:root {
  --color-primary: ...;
  --color-surface: ...;
  --radius-base: ...;
  /* etc */
}
```

---

### Step 5 — Report

Output a summary:
- Design system decisions made (tokens, library used)
- Components created / audited
- Any unresolved questions or [NEEDS REVIEW] items
- Suggested next command: `/speckit.specify` to start specifying features using the new UI kit
