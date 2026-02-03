# Documentation Style Guide for holm

This guide documents the documentation structure, writing style, and conventions used in the `holm` project to help maintain consistency when adding new documentation.

## Documentation Structure

### Location

- All documentation lives in the `docs/` directory
- Example applications live in `examples/` with corresponding README files
- Main project documentation is in `README.md` at the repository root

## Writing Style

### Tone and Voice

- **Relaxed and friendly**
- **Direct and concise**, get to the point quickly, avoid unnecessary preamble
- **Conversational but professional**, use "we" and "you" when appropriate
- **Practical focus**, emphasize what users can do and how to do it
- **Assume intelligence**, don't over-explain basic programming concepts
- **Avoid marketing bullshit and slop**

### Formatting Conventions

#### Headers

- Use sentence case for headers (e.g., "Quick start guide" not "Quick Start Guide")
- Use H1 (`#`) for document titles only
- Use H2 (`##`) for main sections
- Use H3 (`###`) for subsections
- Use H4 (`####`) for detailed subsections (sparingly)

#### Inline Code

- Use backticks for:
  - File names (e.g., `page.py`, `layout.py`)
  - Variable names (e.g., `metadata`, `handle_submit`)
  - Function names (e.g., `holm.App()`)
  - Package names (e.g., `htmy`, `FastAPI`)
  - Code snippets (e.g., `def page():`)

#### Lists

**Do not overuse lists.**

- Use bullet points for unordered lists
- Use numbered lists for sequential steps
- Keep list items concise
- Use nested lists for related sub-points

#### Links

- Use descriptive link text (avoid "click here")
- Link to other documentation files using relative paths
- Link to external resources with full URLs
- For GitHub repository links, use the full URL:
  `https://github.com/volfpeter/holm/tree/main/examples/...`

### Special Conventions

#### Referencing Code

- When referencing URL paths, don't use backticks: `/users/{id}`

#### Emphasis

- Use **bold** for:
  - Key terms being defined
  - Important concepts
  - Feature names (e.g., **file-system based routing**)
- Use _italics_ for:
  - Emphasis within sentences
  - Introducing terms (e.g., "_Layouts_ are defined...")

#### Code Examples

- Provide complete, runnable examples where necessary
- Include necessary imports
- Use realistic variable names
- Add comments for non-obvious parts
- Follow the project's code style

## Document Types

### 1. Conceptual Documentation

**Purpose**: Explain concepts, architecture, and design decisions

**Examples**:

- `application-components.md`
- `file-system-based-routing.md`

**Structure**:

1. Brief introduction explaining what the concept is
2. Core concepts section with clear definitions
3. Rules or guidelines (using bullet points)
4. Examples illustrating the concepts
5. Cross-references to related documentation

**Style Notes**:

- Use "Rules for _X_:" format for listing constraints (if applicable)
- Use italicized terms when first introducing concepts
- Include practical examples after explaining rules

### 2. Step-by-Step Guides

**Purpose**: Walk users through building something specific

**Examples**:

- `guides/quick-start-guide.md`
- `guides/forms.md`
- `guides/actions-with-htmx.md`

**Structure**:

1. Introduction stating what will be built
2. List of topics that will be covered
3. Link to the corresponding example application
4. Prerequisites (installation requirements)
5. Step-by-step instructions with code examples (corresponding example must be in `examples/`)
6. Explanation of key concepts as they appear
7. How to run the application
8. What to expect when running it, if it makes sense

**Style Notes**:

- Use directory tree diagrams to show file structure, if applicable
- Highlight important code with `hl_lines`
- Highlight new/changed lines with `hl_lines` if the guide builds on another one (continual learning)
- Explain the "why" after showing the "what"
- Include complete file contents, not just snippets
- End with encouragement and next steps

### 3. Quick Reference ("In a Hurry")

**Purpose**: Fast overview for users who want to understand the basics quickly

**Example**:

- `in-a-hurry.md`

**Structure**:

1. One-paragraph overview
2. Core technology stack
3. Key concept (file-system based routing)
4. Component summaries with brief examples
5. No step-by-step instructions

**Style Notes**:

- Extremely concise
- Focus on "what" not "how"
- Use bold for key concepts
- Include minimal code examples

### 4. Example READMEs

**Purpose**: Brief description of example applications

**Location**: `examples/<example-name>/README.md`

**Structure**:

- Single sentence or short paragraph describing the example
- Extremely brief (1-3 lines typically)

**Examples**:

- "The quick start guide example."
- "The simplest possible application."
- "The quick start guide example with actions and HTMX."

## Cross-Referencing

### Internal Links

- Use relative paths for links within docs:
  - `[Application components](application-components.md)`
  - `[Quick start guide](guides/quick-start-guide.md)`
- For links to the index page from other docs:
  - `[holm in a hurry](../in-a-hurry.md)` (when in a subdirectory)

### External Links

- Always use full URLs
- Include protocol (https://)
- Use descriptive text:
  - Good: `[FastAPI documentation](https://fastapi.tiangolo.com/tutorial/)`
  - Bad: `[click here](https://...)`

### Referencing Examples

Always include a link to the corresponding example application:

```markdown
The entire source code of this application can be found in the
[examples/quick-start-guide](https://github.com/volfpeter/holm/tree/main/examples/quick-start-guide)
directory of the repository.
```

## Code Example Standards

### Python Code Style

See [AGENTS.md](/AGENTS.md) for the project's code style.

### Example Applications

Each guide should have a corresponding example in `examples/`:

1. Example directory name matches the guide filename (without `.md`)
2. Example should be complete and runnable
3. Example should follow the exact steps in the guide
4. Example README should be minimal (1-2 sentences)

The code in the guide must exactly match the corresponding example.

### Highlighting Code

Always specify the language for syntax highlighting code blocks.

Use `hl_lines` after the code block language specifier to draw attention to important lines, eg. `hl_lines="6-7 9 15"`.

## Navigation and mkdocs.yml

When adding new documentation:

1. Add the file to the appropriate location in `docs/`
2. Update `mkdocs.yml` in the `nav:` section
3. Follow the existing structure:
   - Main docs at top level
   - Guides under `Guides:`
   - API reference under `API reference:`

## Common Phrases and Patterns

These are **just examples**, you don't need to stick to them.

### Introductions

- "Let's create..."
- "This guide demonstrates..."
- "We'll cover:"
- "Before you continue..."

### Explanations

- "The key difference is..."
- "This is particularly useful when..."
- "In other words..."
- "This means that..."

### Transitions

- "Next, we..."
- "With that said..."
- "That's it!"
- "From here, you can..."

### Code Explanations

- "There are three interesting parts..."
- "The most important thing to note..."
- "The changes are trivial, we simply..."
- "Important details:"

## Checklist for New Documentation

Before submitting new documentation:

- [ ] Follows the appropriate document type structure
- [ ] Uses correct header hierarchy
- [ ] All code blocks have language specified
- [ ] Important code block lines are highlighted with `hl_lines`

- [ ] mkdocs.yml is updated with new navigation entry
- [ ] Cross-references to related docs are included
- [ ] Prerequisites are listed
- [ ] Running instructions are provided
- [ ] No unnecessary preamble or postamble
