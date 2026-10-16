---
name: project-index-router
description: Route implementation work to the smallest required project docs first. Use when a task needs fast lookup of the correct truth sources, scope docs, UI constraints, API contracts, schemas, design indexes, or task-specific reading order before coding, reviewing, or prompting. Also use when you want to minimize token use by reading only the minimum necessary documents for a given project task.
---

# Project Index Router

## What This Skill Does

Use this skill to decide **which project documents to read first** and **which ones to avoid**.
It turns a vague task like "build the login page" into a short, ordered reading path.

## Core Rule

Do not start from raw implementation unless the docs are already fully known.
Always route through the smallest set of truth sources first.

## Workflow

1. Classify the task.
2. Read the minimum route for that task.
3. Read the truth sources in the required order.
4. Extract only the constraints needed for implementation.
5. Proceed with coding or analysis.

## Routing Logic

### 1. Always check these first

- project scope / freeze docs
- implementation index docs
- API or schema contracts when data is involved
- UI hard constraints when visuals are involved

### 2. Use the task type to narrow the route

- Frontend work -> frontend stack + UI constraints + API/schema
- Backend/API work -> API contract + schema + backend stack
- Database work -> persistence + transaction boundaries
- Workflow/SSE work -> async/workflow docs + API contract
- Agent/RAG work -> agent index + module design + CIM/boundary docs
- UI prompt work -> UI hard constraints + relevant reference figures

### 3. Prefer project-specific indexes over broad folders

If a project has a curated index file, read that before opening many standalone docs.
If there is a JSON or machine-readable index, use it when you need faster lookup.

## Output Style

When using this skill, provide:

- the task category
- the minimum docs to read
- the ordered reading sequence
- the reason for any skipped docs

Keep it short.

## Good Defaults

- If unsure, start with the project index and scope docs.
- If the task touches APIs, always verify against the contract docs.
- If the task touches UI, always verify against the visual constraints and reference figures.
- If the task touches data structures, always verify against schema definitions.

## Anti-Patterns

- Reading the whole docs tree
- Starting implementation before reading the project index
- Using generic patterns when a project-specific constraint exists
- Rechecking the same broad docs repeatedly instead of using a curated route

## References

Read the project-specific route file when available.
Use it as the canonical place to store task routing rules for that project.
