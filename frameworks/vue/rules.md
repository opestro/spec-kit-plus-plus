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
