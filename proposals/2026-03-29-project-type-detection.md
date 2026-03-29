# Proposal: improve-forge project type detection is validated — refine it

## Learning
Knowledge forges and software projects need fundamentally different evaluation. Trying to "run tests" on a knowledge forge wastes time. Trying to "check skill coherence" on a Python CLI is nonsensical. Project type detection makes every improve-forge step smarter.

## Source
improve-forge runs on itself (knowledge forge) and eidos-assistant (software). Without type detection, the agent tried to run builds on a forge and check skill pipelines on software. With it, each run was appropriate to the project type.

## Proposed Change
- **Target forge:** improve-forge
- **Target file:** `.claude/skills/improve.md` Step 1
- **Change:** The current type detection (knowledge forge / software / mixed) is good. Propose extending it: add "infrastructure" type (Dockerfiles, CI configs, Terraform) and "data pipeline" type (ETL, SQL, dbt). Each type gets different applicable dimensions and different Step 2/6 behaviors.

## Why This Matters
The eidos ecosystem has all of these: knowledge forges, Mac apps, Python MCP servers, ETL pipelines, Supabase schemas. A one-size-fits-all rubric misses type-specific issues.

## Evidence
improve-forge on itself: skipped performance and security (N/A for knowledge forge). improve-forge on eidos-assistant: checked all 9 dimensions. The type detection made both runs appropriate.
