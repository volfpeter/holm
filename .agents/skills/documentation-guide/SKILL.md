---
name: documentation-guide
description: >
  Use when writing or modifying documentation, guides, or example READMEs. Covers documentation
  structure, writing style, formatting conventions, cross-referencing, and code example standards.
---

# Documentation Style Guide for holm

Conventions for `holm` project documentation. When in doubt, follow existing patterns in `docs/`.

## Structure

- All documentation lives in `docs/`
- Example applications live in `examples/` with corresponding README files
- `README.md` content is synced with `docs/index.md`

## Writing Style

### Tone

- Relaxed, friendly, direct and concise — no unnecessary preamble
- Conversational but professional; use "we" and "you"
- Practical: emphasize what users can do and how
- Assume intelligence; don't over-explain basics
- No marketing bullshit or slop

### Formatting

#### Headers

- Sentence case (e.g., "Quick start guide" not "Quick Start Guide")
- H1 for titles only, H2 for sections, H3 for subsections, H4 sparingly

#### Inline Code

- Backticks for file names (`page.py`), variable/function/package names (`metadata`, `holm.App()`, `htmy` — not FastAPI or Starlette), and code snippets (`def page():`)
- No backticks for URL paths: `/users/{id}`

#### Lists

- Don't overuse lists
- Bullet points for unordered, numbered for sequential
- Keep items concise; nest for sub-points

#### Emphasis

- **Bold** for key terms being defined, important concepts, feature names (**file-system based routing**)
- _Italics_ for emphasis and when introducing terms ("_Layouts_ are defined...")

## Document Types

### 1. Conceptual Documentation

Explain concepts, architecture, and design decisions.

**Examples**: `application-components.md`, `file-system-based-routing.md`

**Structure**:

1. Brief introduction
2. Core concepts with clear definitions
3. Rules or guidelines (bullet points)
4. Examples
5. Cross-references

**Notes**:

- Use "Rules for _X_:" format for constraints (if applicable)
- Include practical examples after explaining rules

### 2. Step-by-Step Guides

Walk users through building something specific.

**Examples**: `guides/quick-start-guide.md`, `guides/forms.md`, `guides/actions-with-htmx.md`

**Structure**:

1. Introduction stating what will be built
2. Topics covered
3. Link to the corresponding example application
4. Prerequisites
5. Step-by-step instructions with code examples (corresponding example must be in `examples/`)
6. Explanation of key concepts as they appear
7. How to run the application
8. What to expect when running it, if it makes sense

**Notes**:

- Use directory tree diagrams for file structure, if applicable
- Use `hl_lines` to highlight important code, or new/changed lines when a guide builds on another
- Explain the "why" after the "what"
- Include complete file contents, not just snippets
- End with next steps

### 3. Quick Reference ("In a Hurry")

Fast overview; focus on "what" not "how". Example: `in-a-hurry.md`

**Structure**:

1. One-paragraph overview
2. Core technology stack
3. Key concept (file-system based routing)
4. Component summaries with brief examples
5. No step-by-step instructions

**Notes**: Extremely concise; bold key concepts; minimal code.

### 4. Example READMEs

`examples/<example-name>/README.md` — a single sentence or short paragraph (1-3 lines) describing the example.

**Examples**:

- "The quick start guide example."
- "The simplest possible application."
- "The quick start guide example with actions and HTMX."

## Cross-Referencing

### Internal Links

- Relative paths within docs:
  - `[Application components](application-components.md)`
  - `[Quick start guide](guides/quick-start-guide.md)`
  - `[holm in a hurry](../in-a-hurry.md)` (from a subdirectory)

### External Links

- Full URLs with protocol (`https://`)
- Descriptive link text, never "click here"
- GitHub links use the full URL: `https://github.com/volfpeter/holm/tree/main/...`

### Referencing Examples

Always link to the corresponding example application:

```markdown
The entire source code of this application can be found in the
[examples/quick-start-guide](https://github.com/volfpeter/holm/tree/main/examples/quick-start-guide)
directory of the repository.
```

## Code Examples

### Example Applications

Each guide has a corresponding, complete, runnable example in `examples/`:

- Directory name matches the guide filename (without `.md`)
- The example follows the exact steps in the guide
- Code in the guide must exactly match the example
- Example README is minimal (1-2 sentences)

### Code Style

- Follow the project's code style — see `AGENTS.md`
- Complete, runnable examples with necessary imports
- Realistic variable names; comments only for non-obvious parts

### Highlighting

- Always specify the language for code blocks
- Use `hl_lines` after the language specifier for important lines, e.g. `hl_lines="6-7 9 15"`

## Navigation (mkdocs.yml)

When adding documentation:

1. Add the file under `docs/`
2. Update `nav:` in `mkdocs.yml`, following existing structure:
   - Main docs at top level
   - Guides under `Guides:`
   - API reference under `API reference:`

## Checklist

- [ ] Follows the appropriate document type structure
- [ ] Correct header hierarchy
- [ ] Code blocks have a language; important lines highlighted with `hl_lines`
- [ ] `mkdocs.yml` updated with a nav entry
- [ ] Cross-references included
- [ ] Prerequisites listed
- [ ] Running instructions provided
- [ ] No unnecessary preamble or postamble