# forge-init — Scaffold a New Forge

Create a new Eidos AGI forge — a skills-and-templates repo with visionlog, guardrails, and GitHub presence. The forge pattern is how we package reusable agent knowledge.

## Trigger

User says `/forge-init` or asks to create a new forge.

### Arguments

- `<forge-name>` — required. The name of the forge (e.g., `demo-forge`, `test-forge`).
- `"<description>"` — optional one-liner. If not provided, ask for it.

## What a Forge Is

A forge is a repo that contains:
- **Claude Code skills** (`.claude/skills/`) — the agent knowledge
- **Templates** (`templates/`) — parameterized files the skills generate from
- **Visionlog** (`.visionlog/`) — vision, goals, guardrails
- **Community health** — CLAUDE.md, README, LICENSE
- **No software** — no pyproject.toml, no CLI, no package

Forges are how Eidos AGI packages reusable agent capabilities. Each forge owns a domain: foss-forge owns open-source standards, demo-forge owns demo creation, test-forge owns testing, etc.

## Instructions

### Step 1: Create the Repo Structure

```
~/repos-eidos-agi/<forge-name>/
├── .claude/
│   └── skills/          ← agent skills go here
├── .visionlog/          ← initialized by visionlog project_init
├── templates/           ← parameterized file templates
├── CLAUDE.md            ← project instructions for Claude Code
├── README.md            ← public-facing docs
└── LICENSE              ← MIT (from foss-forge template)
```

Create the directories and files:

1. `mkdir -p ~/repos-eidos-agi/<forge-name>/.claude/skills ~/repos-eidos-agi/<forge-name>/templates`
2. `cd ~/repos-eidos-agi/<forge-name> && git init && git branch -m main`

### Step 2: Initialize Visionlog

Call visionlog tools:
1. `project_init` with path and project_name
2. `project_set` with the path
3. `vision_set` — ask the user what this forge does and write the vision

### Step 3: Set Standard Guardrails

Every forge gets these guardrails (create via `guardrail_create`):

1. **No software — skills and templates only**
   - Rule: This repo must never become a Python package or installable tool.
   - Why: Skills evolve with the agent. Software requires maintenance. Consistency across forges.

2. One or more **domain-specific guardrails** — ask the user what constraints apply to this forge's domain.

### Step 4: Write Community Health Files

Generate from foss-forge templates at `~/repos-eidos-agi/foss-forge/templates/`:

- **LICENSE** — read `LICENSE.tmpl`, substitute `{{YEAR}}` and `{{AUTHOR_NAME}}` (Eidos AGI)
- **CLAUDE.md** — write a project-specific CLAUDE.md with:
  - One-line description
  - What this forge contains (skills list, templates list)
  - Guardrails summary
  - Related forges
- **README.md** — write a public README with:
  - Hero line
  - What it is / why it exists
  - Skills table
  - Usage instructions (clone + symlink/copy skills)
  - License

### Step 5: Create GitHub Repo

Use `mcp__github__create_repository`:
- `name`: `<forge-name>`
- `organization`: `eidos-agi`
- `description`: the one-liner
- `private`: false
- `autoInit`: false

### Step 6: Initial Commit + Push

```bash
git add -A
git commit -m "feat: initialize <forge-name> — <one-liner>"
git remote add origin https://github.com/eidos-agi/<forge-name>.git
git push -u origin main
```

### Step 7: Register the Forge

Update the forge registry at `~/repos-eidos-agi/forge-forge/registry.yaml` — add the new forge with its name, description, repo, and skills list.

### Step 8: Cross-Link

- If the new forge has a relationship with other forges (like demo-forge → foss-forge), note it in both READMEs

## Rules

- **Always initialize visionlog.** A forge without a vision is just a folder.
- **Always set the "no software" guardrail.** This is the defining constraint of the forge pattern.
- **Always create the GitHub repo and push.** Forges are public by default.
- **Ask the user for the vision.** Don't invent what the forge should do — the user knows.
- **Keep the initial commit lean.** CLAUDE.md, README, LICENSE, visionlog, empty skills/ and templates/. The skills come later.
- **Always register the forge** in forge-forge's registry.yaml after creation.
