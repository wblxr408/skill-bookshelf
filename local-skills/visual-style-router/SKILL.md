---
name: visual-style-router
description: Route visual prompt writing toward the right presentation style for any project. Use when Codex needs to write image-generation prompts, poster prompts, hero-scene prompts, system-diagram prompts, explainer art prompts, or product-visual prompts and should decide whether the project needs a structured process poster or a cinematic narrative hero illustration. Especially useful when the user provides a system, workflow, architecture, product, research platform, or brand concept but does not know which visual style will communicate it best.
---

# Visual Style Router

Choose between two reusable visual directions before writing prompts:
- `structural-poster`: information-first, diagrammatic, modular, auditable
- `narrative-hero`: mood-first, cinematic, story-driven, emotionally branded

Read the decision rules below first. Then read only the one matching reference file:
- For structure-first outputs, read `references/structural-poster.md`
- For scene-first outputs, read `references/narrative-hero.md`

If the user already names a style explicitly, honor that unless it directly conflicts with the communication goal.

## Decision Workflow

Follow this order:

1. Identify the communication job.
2. Infer whether the image must primarily explain or primarily evoke.
3. Choose one primary style.
4. Write the prompt in that style.
5. If helpful, mention one secondary influence from the other style without blending them evenly.

## Style Selection Rules

Choose `structural-poster` when most of these are true:
- The user wants to explain a workflow, system, pipeline, methodology, lifecycle, framework, or architecture.
- The image needs labeled modules, arrows, stages, feedback loops, gates, legends, or layered process bands.
- The image is meant for documentation, technical communication, internal design review, keynote system slide, or audited product explanation.
- Correct sequencing and clarity matter more than atmosphere.
- The user asks for a process-map feel, architecture-poster feel, infographic, or "one image explains the whole system".

Choose `narrative-hero` when most of these are true:
- The user wants a landing-page hero, campaign visual, brand poster, story scene, or emotional flagship image.
- The image should make the system feel alive, memorable, premium, cozy, intense, magical, or aspirational.
- The system is better conveyed through environment, props, characters, holograms, and cinematic lighting than through explicit arrows and boxes.
- The goal is persuasion, mood, identity, or product aura before detailed explanation.
- The user asks for a hero visual, website hero image, cinematic feel, narrative feel, late-night studio scene, or poster feel.

## Tie-Breakers

If both styles seem plausible, decide with these tie-breakers in order:

1. If the image must teach the viewer how the system works, choose `structural-poster`.
2. If the image must make the viewer feel what the system is like, choose `narrative-hero`.
3. If the output will contain many labels or named modules, choose `structural-poster`.
4. If the output will likely fail when overloaded with text, choose `narrative-hero`.
5. If the user asks for something like a website banner or hero image, choose `narrative-hero`.
6. If the user asks for something like a product architecture overview or process overview, choose `structural-poster`.

## Output Contract

After choosing a style, produce:
- a one-line style decision
- a short rationale with 2-4 bullets
- one complete prompt
- one negative prompt if the target model benefits from it
- optional model-specific variants only if the user asks

Keep the rationale short. Most of the effort should go into the final prompt.

## Prompt Construction Rules

For both styles:
- Preserve the project's real concepts; do not invent core modules casually.
- Prefer concise labels over paragraphs inside the image.
- Do not copy a reference image composition verbatim.
- Do not use copyrighted characters or branded mascots unless the user explicitly owns them.
- Convert vague requests into production-ready visual language.
- Keep one dominant communication mode; do not average the two styles into a muddy hybrid.

For project extraction:
- Identify the system name, domain, actors, main stages, critical artifacts, control points, and emotional tone.
- If the project has explicit principles like "human in control" or "auditable", make them visible in the prompt.
- If the project is complex, compress to the few concepts that drive composition.

## Safe Assumptions

Make reasonable assumptions instead of blocking unless a missing detail would radically change the image:
- If no aspect ratio is given, default to `16:9`.
- If no output use is given, infer from wording:
  - workflow/system/architecture -> `structural-poster`
  - hero/website/poster -> `narrative-hero`
- If no palette is given:
  - `structural-poster`: white or light editorial background with blue/green governance accents
  - `narrative-hero`: dark warm environment with cool holographic contrast

## Examples

Use `structural-poster`:
- "Turn this multi-agent workflow into one complete system poster"
- "Create a one-image process overview for my research platform"
- "Apply this infographic style to my system design"

Use `narrative-hero`:
- "Write a website hero prompt for this AI product"
- "I want a late-night research studio hero visual showing the system working with me"
- "Turn this platform into a story-driven brand poster"

## Failure Modes To Avoid

Avoid these common mistakes:
- choosing `narrative-hero` for a request that clearly needs readable process communication
- choosing `structural-poster` for a request that clearly needs emotional brand impact
- overfilling a poster with paragraph text
- writing a scene prompt that quietly turns into a dashboard screenshot
- blending both styles equally and losing both clarity and mood

## References

Read exactly one of these after making the routing decision:
- `references/structural-poster.md`
- `references/narrative-hero.md`
